# Web App Firewall UI

## Backend
### Access through port 8000
```
deactivate;
cd /home/administrator/EPR402/UserInterface;
source .ui_venv/bin/activate;
cd backend;
python manage.py runserver 0.0.0.0:8000;
```

## Frontend
### Access through port 3000
```
deactivate;
cd /home/administrator/EPR402/UserInterface;
source .ui_venv/bin/activate;
cd frontend;
npm start;
```