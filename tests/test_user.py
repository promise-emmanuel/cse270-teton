import requests
import pytest

BASE_URL = "http://example.com/users"


@pytest.fixture(autouse=True)
def mock_requests(monkeypatch):
    """
    Monkey-patch requests.get so all tests hit this fake server.
    """
    class FakeResponse:
        def __init__(self, status, text):
            self.status_code = status
            self.text = text

    def fake_get(url, params=None, **kwargs):
        user = params.get("username")
        pwd = params.get("password")
        if user == "admin" and pwd == "admin":
            return FakeResponse(401, "")
        elif user == "admin" and pwd == "qwerty":
            return FakeResponse(200, "Welcome, admin!")
        else:
            return FakeResponse(400, "Bad Request")

    monkeypatch.setattr(requests, "get", fake_get)
    yield


def test_auth_fail():
    """Mocked wrong password → 401 & empty"""
    resp = requests.get(BASE_URL, params={"username": "admin", "password": "admin"})
    assert resp.status_code == 401
    assert resp.text == ""


def test_auth_success():
    """Mocked correct password → 200 & welcome text"""
    resp = requests.get(BASE_URL, params={"username": "admin", "password": "qwerty"})
    assert resp.status_code == 200
    assert "Welcome, admin" in resp.text
