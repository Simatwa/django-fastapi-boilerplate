.PHONY: install setup developmentsuperuser test runserver runserver-prod default

default: install setup developmentsuperuser runserver-api

install:
	pip install -r requirements.txt

setup:
	python manage.py makemigrations users finance external management

	python manage.py migrate

	python manage.py collectstatic --no-input


developmentsuperuser:
	python manage.py createsuperuser --username developer \
	 --email developer@localhost.domain --noinput

test:
	python -m unittest discover -s api/tests -p 'test_*.py' -f -v

pytest:
	pytest api/tests/* -xv

runserver:
	python manage.py runserver

runserver-uwsgi:
	uwsgi --http=0.0.0.0:8080 -w wsgi:application --static-map /static=files/static --static-map=/media=files/media

runserver-api:
	python -m api run api

dumpdata:
	python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 4 \
    --exclude auth.permission \
    --exclude contenttypes \
    --exclude sessions \
    --exclude admin.logentry \
	> db.json


loaddata:
	python manage.py loaddata db.json
