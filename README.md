# Class Blog

A blog built by our class in the GIZ-FMLE Nigeria Python training. Authors publish articles with photos, and readers comment and like.

**Live site:** https://roundedoj.pythonanywhere.com

## Features
- Articles with a cover image, photo gallery, search and pagination
- Author-only writing pages (authors are added by the admin)
- Reader sign-up to like and comment
- Admin can hide comments
- Share links for WhatsApp, X, Facebook, LinkedIn and email
- Responsive design with a consistent colour palette and free fonts (Outfit and Inter)

## Built with
Python, Django, SQLite, Bootstrap, Git/GitHub, PythonAnywhere

## Run it locally
```bash
git clone https://github.com/roundedoj/classblog.git
cd classblog
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Then open http://127.0.0.1:8000/

## Limitations
- SQLite and local photo storage suit a small audience, not heavy traffic
- No password reset by email yet
- Four extra photo slots per save
- Free hosting must be renewed monthly

## Next steps
PostgreSQL and cloud storage, custom domain, email features, categories and tags, automated tests.

## What I learned
Building, deploying and fixing a live Django site, and using Git to move changes from laptop to server.