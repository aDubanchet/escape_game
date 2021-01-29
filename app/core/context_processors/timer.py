from django.core.exceptions import ObjectDoesNotExist
from core.models import Game
import datetime

def timer(request):
    try:
        game = Game.objects.all()
        if game.exists() :
            game = game.first()
            timer = game.timer
            created_at = game.created_at.timestamp()
            if game.status == 'WAITING': #Si la game n'a pas été crée ou est en pause
                
                return {'created_at': created_at,'timer':timer}
            else :  
                return {'created_at':created_at,'timer':timer} #CHANGE THIS 

    except ObjectDoesNotExist :
        pass
    return {'created_at':False,'timer':False}