"""
Urls of allauth :
    path("signup/", views.signup, name="account_signup"),
    path("login/", views.login, name="account_login"),
    path("logout/", views.logout, name="account_logout"),
    path("password/change/", views.password_change,
         name="account_change_password"),
    path("password/set/", views.password_set, name="account_set_password"),
    path("inactive/", views.account_inactive, name="account_inactive"),

    # E-mail
    path("email/", views.email, name="account_email"),
    path("confirm-email/", views.email_verification_sent,
         name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email,
            name="account_confirm_email"),

    # password reset
    path("password/reset/", views.password_reset,
         name="account_reset_password"),
    path("password/reset/done/", views.password_reset_done,
         name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", views.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),

"""

from django.contrib import admin
from django.urls import path, include
from allauth.account import views

import core.views as vC

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url 

urlpatterns = [
    
    path('account', include('allauth.urls')),        # retravailler les urls 
    path('teams', vC.TeamsView.as_view(),name='teams'), # global -> vue team
    path('game', vC.GameView.as_view(),name='game'), #team -> game 
    path('createGame', vC.CreateGameView.as_view(),name='create_game'),
    path('changeTeamName', vC.ChooseTeamName.as_view(),name='change_team_name'),
    path('',vC.HomeView.as_view(), name="home"),

     # Admin
     path('admin/', admin.site.urls),
     path('ad', vC.AdminView.as_view(),name='ad'),
     path(r'^delete_team/(?P<team_id>\d+)/$', vC.DeleteTeamView.as_view(),name='ad_delete_team'),
     path(r'^create_team$', vC.CreateTeamView.as_view(),name='ad_create_team'),
     path(r'^end_game$', vC.EndGameView.as_view(),name='ad_end_game'),

     # Admin : Pause / Start
     path(r'^pause_game$', vC.PauseGameView.as_view(),name='ad_pause_game'),
     path(r'^start_game$', vC.StartGameView.as_view(),name='ad_start_game'),

     # Ajax Requests 
     url(r'^ajax/get_teams/$', vC.get_teams, name='ajax_get_teams'),
     url(r'^ajax/update_progression/$', vC.post_progression, name='ajax_update_progression'),
     url(r'^ajax/get_game_status/$', vC.get_game_status, name='ajax_get_game_status'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
