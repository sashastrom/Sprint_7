import allure
import requests
from data.urls import *


@allure.title("Проверяем что в тело ответа возвращается список заказов.")
class TestGetOrdersList:

    def test_check_get_list_of_orders(self):
        params = {
            "limit": 10,
            "page": 0,
        }
        response = requests.get(order_url, params=params)
        assert response.status_code == 200
        response_json = response.json()
        orders = response_json.get("orders")
        assert orders is not None, "Ответ не содержит список заказов"
        assert isinstance(orders, list), "Поле 'orders' должно быть списком"
        assert len(orders) > 0, "Список заказов пуст"