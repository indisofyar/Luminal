
**Local development**
    
    source ./env/bin/activate
    cd luminal
     ./manage.py migrate --settings=luminal.settings.local

     ./manage.py runserver --settings=luminal.settings.local

    
**Setup** 

    pip install virtualenv
    source ./env/bin/activate
    pip install -r ./luminal/requirements.txt
    