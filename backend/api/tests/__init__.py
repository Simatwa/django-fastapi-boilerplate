from fastapi.testclient import TestClient
from api import app

client = TestClient(app, "http://testserver/api")
