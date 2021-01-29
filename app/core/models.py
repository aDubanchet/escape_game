from django.db import models
from django.conf import settings

import uuid

# Game Account
from django.contrib.auth.models import AbstractUser

# Date 
import datetime
from datetime import timezone

class Game(models.Model):
    # Chaque partie possède des équipes 

    created_at = models.DateTimeField(auto_now=True) # Champ s'initialisant auto à partir de la date
    timer = models.FloatField() # Champ minuteur
    status = models.CharField(max_length=20,default='WAITING')

class Team(models.Model):
    # Chaque equipe possède des joueurs 
    """
    Model : Team 
    """
    name = models.CharField(max_length=255,default='')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    progression = models.IntegerField(default=0) # Gerer ce field 

    ## On Crée une relation optionnel avec la partie
    game = models.ForeignKey(Game,on_delete=models.CASCADE,blank=True, null=True) 

    # Enlever ce champ pour un système plus sécurisé /!\
    password = models.CharField(max_length=100,default='')
    team_name_updated_by = models.CharField(max_length=16,default='admin')
    
class Account(AbstractUser):
    team = models.OneToOneField(Team,blank=True,null=True,related_name='team',on_delete=models.CASCADE)

