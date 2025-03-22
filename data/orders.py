import requests
from data.urls import order_url
import allure

@allure.step("Создание нового заказа с данными")
def create_order(payload):
    response = requests.post(order_url, json=payload)
    return response