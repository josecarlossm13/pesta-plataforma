release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn plataforma.wsgi --log-file -