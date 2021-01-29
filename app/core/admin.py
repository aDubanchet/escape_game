from django.contrib import admin
from .models import *

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['created_at','status','timer']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name','progression']