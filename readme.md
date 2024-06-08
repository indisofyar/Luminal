# Luminal

## Overview
Luminal is an analytics API which helps users make sense of data from XRPL. 

## Who's it for?



**Local development**
    
    source ./env/bin/activate
    cd luminal
     ./manage.py makemigrations --settings=luminal.settings.local
     ./manage.py migrate --settings=luminal.settings.local
     ./manage.py runserver --settings=luminal.settings.local

    
**Setup** 

    pip install virtualenv
    source ./env/bin/activate
    pip install -r ./luminal/requirements.txt
    