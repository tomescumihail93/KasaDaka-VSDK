# KasaDaka-Voice Service Development Kit


## Project setup

1. Create a virtual env
2. Navigate with terminal while in the virtual env to the folder with manage.py
3. run pip install -r requirements.txt
4. Run: python manage.py makemigrations
5. Run: python manage.py migrate
6. Run: python manage.py createsuperuser
7. Not mandatory to initialize test vxml app: python manage.py loaddata initial_data.json
8. Run: python manage.py runserver
9. You can access your projects admin panel by typing the url generated by the server


# CAREFUL!
If deploying to heroku check ‘vsdk/settings.py’ DEBUG variable to FALSE