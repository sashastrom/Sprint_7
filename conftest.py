import pytest
import requests
from data.helpers import generate_random_string
from data.urls import *


@pytest.fixture
def register_new_courier():
    login_pass = []
    response = None

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(courier_url, data=payload)

    if response.status_code == 201:
        courier_id = response.json().get('id')
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
        login_pass.append(courier_id)

    yield login_pass, response

    if login_pass:
        courier_id = login_pass[3]
        delete_courier = delete_courier_url.format(id=courier_id)
        delete_response = requests.delete(delete_courier)
        if delete_response.status_code != 200:
            print(f"Ошибка при удалении курьера: {delete_response.status_code} - {delete_response.json()}")