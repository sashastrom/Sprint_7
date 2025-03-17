import unittest

import allure
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

@allure.feature("Список заказов")
@allure.story("Проверка списка заказов")
@allure.description("Проверяем что в тело ответа возвращается список заказов.")
class GetListOfOrdersTest(unittest.TestCase):

    def test_check_get_list_of_orders(self):
        params = {
            "limit": 10,
            "page": 0,
        }
        response = requests.get(BASE_URL, params=params)
        self.assertEqual(response.status_code, 200, "Код не соответствует ожидаемому 200")
        response_json = response.json()
        orders = response_json.get("orders")
        self.assertIsNotNone(orders, "Ответ не содержит список заказов")
        self.assertIsInstance(orders, list, "Поле 'orders' должно быть списком")
        self.assertGreater(len(orders), 0, "Список заказов пуст")
if __name__ == "__main__":
    unittest.main()