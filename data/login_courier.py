import requests
import allure
from data.urls import login_url


@allure.step("Логин курьера с логином и паролем")
def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(login_url, json=payload)
    return response