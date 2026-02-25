import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def post_calc(client, a, b, operation):
    return client.post(
        "/calculate",
        data=json.dumps({"a": a, "b": b, "operation": operation}),
        content_type="application/json",
    )


# Health check
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


# Index page
def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200


# Arithmetic operations
def test_add(client):
    resp = post_calc(client, 3, 4, "add")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 7


def test_subtract(client):
    resp = post_calc(client, 10, 3, "subtract")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 7


def test_multiply(client):
    resp = post_calc(client, 3, 4, "multiply")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 12


def test_divide(client):
    resp = post_calc(client, 10, 4, "divide")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 2.5


# Error cases
def test_divide_by_zero(client):
    resp = post_calc(client, 5, 0, "divide")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_unknown_operation(client):
    resp = post_calc(client, 1, 1, "power")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_invalid_input(client):
    resp = client.post(
        "/calculate",
        data=json.dumps({"a": "abc", "b": 1, "operation": "add"}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()
