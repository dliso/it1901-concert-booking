# IT1901 Prosjekt I
## Festivalbookingsystem
### Hvordan kjøre prosjektet
1. Åpne en terminal med `bash`
  - Mac/Linux: Bare åpne en terminal
  - Windows: ???
2. Lag et såkalt virtual environment: `virtualenv-3 -p $(which python36) venv`
3. Aktiver virtual environment-et du nettopp lagde: `source venv/bin/activate`
4. Installer nødvendige biblioteker: `pip install -r requirements.txt`
5. Start prosjektet: `python3 manage.py runserver`
6. Åpne [localhost:8000](localhost:8000) i nettleseren din.
