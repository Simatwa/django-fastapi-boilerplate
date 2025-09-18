from fastapi.testclient import TestClient
from users.models import CustomUser

from api import app

base_url = "http://testserver/api"

test_credentials = {
    "username": "developer",
    "password": "development",
    "grant_type": "password",
}

client = TestClient(app, base_url)
