import allure
from conftest import *
from data.response_codes import *


class TestCourierCreation:

    @allure.title("Проверяем успешную регистрацию курьера")
    def test_courier_success_registration(self, register_new_courier):
        login_pass, response = register_new_courier
        assert response.status_code == 201
        assert response.json() == success_response
        print(f"Курьер создан: Логин {login_pass[0]}, Пароль {login_pass[1]}")

    @allure.title("Проверяем что нельзя создать 2 одинаковых курьера с тем же логином.")
    def test_duplicate_courier(self, register_new_courier):
        login_pass, _ = register_new_courier
        payload = {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
        }
        response = requests.post(courier_url, data=payload)
        assert response.status_code == 409
        assert response.json().get("message") == conflict_message
        print(f"Ошибка: {conflict_message}")

    @allure.title("Проверяем, что нельзя создать курьера без ввода обязательных полей")
    def test_missing_fields(self):
        payload = {
            "login": "",
            "password": "",
            "firstName": ""
        }
        response = requests.post(courier_url, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == error_message
        print(f"Ошибка: {error_message}")

    @allure.title("Проверяем, что успешный запрос возвращает код 201")
    def test_success_response(self, register_new_courier):
        login_pass, response = register_new_courier
        assert response.status_code == 201
        print("Код ответа правильный: 201")

    @allure.title("Проверяем, что успешный запрос возвращает '{'ok': true}'")
    def test_success_response_message(self, register_new_courier):
        login_pass, response = register_new_courier
        assert response.status_code == 201
        assert response.json() == success_response
        print(f"Ответ успешный: {success_response}")

    @allure.title("Проверяем, что если нет одного из полей, возвращается ошибка")
    def test_missing_one_field(self):
        payload = {
            "login": "unique_login",
            "password": "",
            "firstName": "Test"
        }
        response = requests.post(courier_url, data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == error_message
        print(f"Ошибка: {error_message}")

    @allure.title("Проверяем, что если есть такой же курьер логин - возвращается ошибка")
    def test_existing_login(self, register_new_courier):
        login_pass, _ = register_new_courier
        payload = {
            "login": login_pass[0],
            "password": "new_password",
            "firstName": "New Name"
        }
        response = requests.post(courier_url, data=payload)
        assert response.status_code == 409
        assert response.json().get("message") == conflict_message
        print(f"Ошибка: {conflict_message}")