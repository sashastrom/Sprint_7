import allure
from conftest import *
from data.response_codes import *
from data.login_data import *
from data.login_courier import login_courier


class TestCourierLogin:

    @allure.title("Проверяем, что курьер может авторизоваться")
    def test_courier_login_success(self):
        login = LOGIN
        password = PASSWORD
        response = login_courier(login, password)
        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"
        assert 'id' in response.json(), "В ответе нет поля 'id'"


    @allure.title("Проверяем, что курьер не может авторизоваться без обязательных полей (логин или пароль)")
    def test_missing_login_or_password(self):
        payload = {
            "login": "",
            "password": ""
        }
        response = requests.post(login_url, json=payload)
        assert response.status_code == 400
        assert response.json().get("message") == error_message_missing_fields


    @allure.title("Проверяем, что система вернёт ошибку, если неправильно указать логин или пароль")
    def test_wrong_login_or_password(self):
        login = LOGIN
        password = "wrong_password"
        response = login_courier(login, password)
        assert response.status_code == 400
        assert response.json().get("message") == error_message_wrong_credentials


    @allure.title("Проверяем, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_missing_login(self):
        payload = {
            "login": "",
            "password": PASSWORD
        }
        response = requests.post(login_url, json=payload)
        assert response.status_code == 400
        assert response.json().get("message") == error_message_missing_fields


    @allure.title("Проверяем, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_missing_password(self):
        payload = {
            "login": LOGIN,
            "password": ""
        }
        response = requests.post(login_url, json=payload)
        assert response.status_code == 400
        assert response.json().get("message") == error_message_missing_fields


    @allure.title("Проверяем, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_non_existent_user(self):
        login = "nonexistent_user"
        password = "any_password"
        response = login_courier(login, password)
        assert response.status_code == 400
        assert response.json().get("message") == error_message_non_existent_user


    @allure.title("Проверяем, что успешный запрос возвращает id.")
    def test_successful_login_returns_id(self):
        login = "ninja"
        password = "1234"
        response = login_courier(login, password)
        assert response.status_code == 200
        assert 'id' in response.json(), "В ответе нет поля 'id'"