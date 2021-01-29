#!/bin/sh

# exit if errors
set -e 

echo "Start Django EntryPoint.sh"
python manage.py collectstatic --noinput 
python manage.py makemigrations 
python manage.py migrate 
echo "from django.contrib.auth.models import User;from core.models import Account;user = Account.objects.create_user('admin',password='escapeGame81pam');user.is_superuser=True;user.is_staff=True;user.save()" | python manage.py shell
# Command that runs the app using uWSGI 
# --master : master service no background service 
uwsgi --socket :8000 --master --enable-threads --module app.wsgi 