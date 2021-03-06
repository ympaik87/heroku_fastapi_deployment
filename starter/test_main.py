from fastapi.testclient import TestClient
import logging
import pytest
from main import app


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


@pytest.fixture
def client():
    with TestClient(app) as clt:
        yield clt


def test_welcome(client):
    req = client.get('/')
    assert req.status_code == 200, "Status code is not 200"
    assert req.json() == "Welcome, this API returns predictions on Salary", "Wrong json output"


def test_post(client):
    sample_dict = {
        "age": 49,
        "workclass": "State-gov",
    }
    response = client.post('/items', json=sample_dict)
    assert response.status_code == 200, "Status code is not 200"
    assert response.json() == sample_dict


def test_get_prediction_negative(client):
    input_dict = {
        "age": 49,
        "workclass": "State-gov",
        "fnlgt": 77516,
        "education": "Bachelors",
        "education-num": 13,
        "marital-status": "Married-civ-spouse",
        "occupation": "Adm-clerical",
        "relationship": "Not-in-family",
        "race": "White",
        "sex": "Male",
        "capital-gain": 2174,
        "capital-loss": 0,
        "hours-per-week": 40,
        "native-country": "United-States"
    }
    response = client.post('/predict', json=input_dict)
    assert response.status_code == 200, "Status code is not 200"
    assert response.json() == {"Predicted salary": "<=50K"}, \
        "Wrong json output"


def test_get_prediction_positive(client):
    input_dict = {
        "age": 41,
        "workclass": "Private",
        "fnlgt": 45781,
        "education": "Masters",
        "education-num": 14,
        "marital-status": "Married-civ-spouse",
        "occupation": "Prof-specialty",
        "relationship": "Not-in-family",
        "race": "White",
        "sex": "Male",
        "capital-gain": 2020,
        "capital-loss": 0,
        "hours-per-week": 50,
        "native-country": "United-States"
    }
    response = client.post("/predict", json=input_dict)
    assert response.status_code == 200, "Status code is not 200"
    assert response.json() == {"Predicted salary": ">50K"}, "Wrong json output"
