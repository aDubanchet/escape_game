# Utils
from django.shortcuts import render, redirect

# Class Based Views 
from django.views import View

# tests 
from django.http import HttpResponse

# Login View :
from allauth.account.forms import LoginForm
from allauth.account.views import LoginView

# Decorators pour l'authentification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

# Models 
from .models import Team, Game, Account

# Forms 
from .forms import GameForm

#Import transactions and errors
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# messages
from django.contrib import messages

# password generator
import random, string

# Date 
import datetime
from datetime import timezone

# http and json response for ajax request
from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import get_object_or_404
import json

from django.contrib.auth.mixins import UserPassesTestMixin

# -----------------------
# Decorators  
# -----------------------

def superuser_required():
    # Fonction pour vérifier si l'utilisateur est Admin 
    # Django appelle ça des décorateurs
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper

# -----------------------
# Home View 
# -----------------------

class HomeView(View):
    # Vue principale renvoyant à la page de connexion
    template_name = 'home/home.html'
    def get(self,request):
        return redirect('account_login')

# -----------------------
# Game Views
# -----------------------
@method_decorator(login_required,name='dispatch')
class TeamsView(View):
    """
    Vue affichant des informations sur la partie en cours tel que 
    la liste des équipes et leur classement. 
    """
    template_name = 'game/teams.html'  # Déclaration du template utilisé 

    def get(self,request):  
        # Lorsque la méthode GET est utilisée :
        # On récupère la liste des équipes, des infos sur la partie en cours
        # afin de les envoyer au template ( /templates/game/global.html )
        # Dans certaines parties de ce template, il y a des {{ game }}
        # Ce sont les variables qu'on a crée puis envoyé ci-dessous
        context = {}
        user = request.user 
        game = Game.objects.all().first()
        teams = Team.objects.all().order_by('-progression')

        if user.team :
            if user.team.team_name_updated_by == 'admin':
                return redirect('change_team_name')

            context['team_name'] = user.team.name
            context['team_progression'] = user.team.progression

        context['teams'] = teams
        context['game'] = game
        context['user'] = user
        return render(request,self.template_name,context) 

@method_decorator(login_required,name='dispatch')
class GameView(View):
    template_name = 'game/game.html'
    def get(self,request):
        context = {}
        user = request.user 
        game = Game.objects.all().first()
        teams = Team.objects.all().order_by('-progression') # on tri dans l'ordre décroissant

        # Cette ligne n'est pas utile pour l'instant mais pourrai l'être plus tard
        # Elle vérifie si l'utilisateur possède une équipe, si ce n'est pas le cas
        # Elle n'envoie pas la variable 
        if user.team :
            context['team_name'] = user.team.name
            context['team_progression'] = user.team.progression

        context['teams'] = teams
        context['game'] = game
        context['user'] = user
        return render(request,self.template_name,context)

@method_decorator(login_required,name='dispatch')
class ChooseTeamName(View):
    template_name = 'game/changeTeamName.html'
    def get(self,request):
        user = request.user
        if user.is_superuser :
            redirect('ad')
        return render(request,self.template_name,{})

    def post(self,request):
        user = request.user
        team = user.team
        teams = Team.objects.all()

        #select_related('team').get(username=user.username)
        if 'team_name' in request.POST :

            if teams :
                for t in teams :
                    if request.POST['team_name'] == t.name :
                        messages.error(request, 'Une équipe possède déjà ce nom.')
                        return redirect('change_team_name')

            user.username = request.POST['team_name']
            user.save()
            team.name = request.POST['team_name']
            team.team_name_updated_by = 'player'
            team.save()

            return redirect('game')
            
class IncrementProgressionView(View):
    def post(self,request):
        progression_input = request.POST['progression']


# -----------------------
#   Admin Views 
# -----------------------

# AJOUTER UN Decorateur pour les Permissions ADMIN

@superuser_required()
@method_decorator(login_required,name='dispatch')
class AdminView(View):
    template_name = 'admin/admin.html'
    
    def get(self,request):
        context = {}
        
        # Get the game
        game = Game.objects.all()

        # On recupere les équipes et on enleve l'admin
        teams = Team.objects.all()

        if not game.exists():
            return redirect('create_game')

        game = game.first()
        t = datetime.datetime.now()

        context['game'] = game
        context['teams'] = teams
        return render(request,self.template_name,context)


@superuser_required()
@method_decorator(login_required,name='dispatch')
class CreateGameView(View):
    template_name = 'admin/create_game.html'
    
    def get(self,request):
        context = {}
        # Si une game est en cours redirige vers AdminView
        game = Game.objects.all()
        if game.exists():
            return redirect('ad')
        
        # Formulaire de Creation de Partie
        game_creation_form = GameForm()

        context['game_creation_form'] = game_creation_form
        return render(request,self.template_name,context)

    def post(self,request):
        context = {}
        game = Game.objects.all()
        if game.exists():
            return redirect('ad')       

        # Formulaire de Creation de Partie
        game_creation_form = GameForm(request.POST)
        if game_creation_form.is_valid():
            game_creation_form.save()
        else :
            messages.warning(request, 'Il y a eu une erreur. Merci de ressayer.')
        # Message
        messages.success(request, 'La Partie a bien été créée.')
        return redirect('ad') #Redirige vers AdminView


@superuser_required()       
class DeleteTeamView(View):
    def post(self,request,team_id):
        try:
            with transaction.atomic():
                team = Team.objects.get(id=team_id)
                team.delete()
            messages.info(request, "L'équipe a bien été supprimée.")
        except ObjectDoesNotExist:
            messages.error(request, 'Une erreur est survenue.')
        return redirect('ad')

@superuser_required()
class CreateTeamView(View):
    def post(self,request):
        if request.POST['team_name']:
            team_name = request.POST['team_name']
            teams = Team.objects.all()
            users = Account.objects.all()
            if team_name == '' :
                messages.warning(request, 'Veuillez rentrer un nom d\'équipe correct')
                return redirect('ad')   
            else :
                for team in teams:
                    if team.name == team_name :
                        messages.warning(request, 'Une équipe possède déjà ce nom.')
                        return redirect('ad')
                for user in users:
                    if user.username == team_name:
                        messages.warning(request, 'Une équipe possède déjà ce nom.')
                        return redirect('ad')                                                  
            try:
                with transaction.atomic():
                    password = ''.join(random.choice(string.ascii_uppercase)for _ in range(0,6))
                    team = Team.objects.create(name=team_name,password=password) 
                    user = Account.objects.create_user(username=team_name,email='',password=password,team=team)
                messages.info(request, "L'équipe a bien été créée.")
            except ObjectDoesNotExist:
                messages.warning(request, 'Une erreur est survenue.')
            return redirect('ad')
        else :
            messages.warning(request, 'Une erreur est survenue.')
            return redirect('ad')          

@superuser_required()
class EndGameView(View):
    def get(self,request):
        game = Game.objects.all()
        teams = Team.objects.all()
        try:
            with transaction.atomic():
                if game.exists():
                    game[0].delete()
                for team in teams:
                    team.delete()
            messages.info(request, "La partie a bien été arrêtée.")
        except ObjectDoesNotExist:
            messages.error(request, 'Une erreur est survenue.')
        return redirect('ad')


@superuser_required()
class PauseGameView(View):
    def get(self,request):
        # Met la Game en Pause
        game = Game.objects.all()
        if game.exists():
            game = game.first()
            duree = datetime.datetime.now(timezone.utc) - game.created_at
            game.status = "PAUSED"
            game.timer = game.timer - datetime.timedelta(seconds=duree.total_seconds()).total_seconds()/60
            game.created_at = datetime.datetime.now(timezone.utc) 
            game.save()

        return redirect('ad')

@superuser_required()
class StartGameView(View):

    def get(self,request):
        # Si une game est en cours redirige vers AdminView
        game = Game.objects.all()
        if game.exists():
            game = game.first()
            game.status = "INGAME"
            game.created_at = datetime.datetime.now(timezone.utc)
            game.save()
        return redirect('ad')


# ------------------------------
#   JSON Response Views
# ------------------------------
# Pour les requêtes avec JQuery

def get_teams(request):
    #GET request : pour récupérer les informations des équipes 
    teams = Team.objects.all().order_by('-progression') # on tri dans l'ordre décroissant
    teams_progression = {}
    for team in teams:
        data = {
            str(team.name) : team.progression
        }
        teams_progression.update(data)

    print(teams_progression)
    # convert the data(QuerySet) to JSON type string.
    return JsonResponse(teams_progression)

def post_progression(request):
   #POST request : Quand une équipe envoie sa progression 
   # https://realpython.com/django-and-ajax-form-submissions/ 
   user = request.user
   if request.method == "POST" :
       
        response_data = {}
        post_progression = request.POST.get('post_progression')
        post_team_name = request.POST.get('post_team_name')

        if int(post_progression) == 0 :
            return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json")      
        
        #No need test user security
        team = get_object_or_404(Team,name=str(post_team_name))
        team.progression = post_progression
        team.save()

        response_data['result'] = 'Updated Progression successful'
        return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json")
    #return HttpResponse(json.dumps({}),content_type = "application/json")

def get_game_status(request):
    #GET request : pour que le client sache si la partie a commencé
    game = Game.objects.all().first()
    game_status = game.status

    data = {
        'status' : game_status
    }

    # convert the data(QuerySet) to JSON type string.
    return JsonResponse(data)
