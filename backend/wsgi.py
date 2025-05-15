# /usr/bin/python3
"""
Converts fastapi app to wsgi app

uwsgi --http=0.0.0.0:8080 -w wsgi:application

Using make:
    $ make runserver-uwsgi

NOTE: This is not a good approach of running asynchronous application.
Consider using gunicorn or the default uvicorn which are optimized for
production purposes as well.

Pro: Good for 1 second fireup offering quick access of the app.
"""

from api import app
from a2wsgi import ASGIMiddleware

application = ASGIMiddleware(app)
