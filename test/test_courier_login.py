import allure
import requests


def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
    return response



@allure.feature("Логин курьера")
@allure.story("Авторизуемся с правильным логином и паролем")
@allure.description("Проверяем что курьер может авторизоваться")
def test_courier_login_success():
    login = "ninja"
    password = "1234"
    response = login_courier(login, password)
    if response.status_code == 200:
        print(f"Авторизация успешна! ID: {response.json()['id']}")
    else:
        print(f"Ошибка при авторизации: {response.status_code} - {response.json()}")



@allure.feature("Логин курьера")
@allure.story("Для авторизации нужно передать все обязательные поля")
@allure.description("Проверяем что курьер не может авторизоваться без обязательных полей (логин или пароль)")
def test_missing_login_or_password():
    payload = {
        "login": "",
        "password": ""
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для входа":
        print("Ошибка: отсутствуют обязательные поля для авторизации.")
    else:
        print(f"Ошибка при авторизации с отсутствующими полями: {response.status_code} - {response.json()}")



@allure.feature("Логин курьера")
@allure.story("Авторизуемся с неверным логином или паролем")
@allure.description("Проверяем что система вернёт ошибку, если неправильно указать логин или пароль")
def test_wrong_login_or_password():
    login = "ninja"
    password = "wrong_password"
    response = login_courier(login, password)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для входа":
        print(f"Ошибка: Неверный логин или пароль.")
    else:
        print(f"Ошибка при авторизации с неправильными данными: {response.status_code} - {response.json()}")



@allure.feature("Логин курьера")
@allure.story("Авторизация без логина")
@allure.description("Проверяем что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
def test_missing_login():
    payload = {
        "login": "",
        "password": "1234"
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для входа":
        print("Ошибка: отсутствует логин для авторизации.")
    else:
        print(f"Ошибка при авторизации без логина: {response.status_code} - {response.json()}")



@allure.feature("Логин курьера")
@allure.story("Авторизация без пароля")
@allure.description("Проверяем что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
def test_missing_password():
    payload = {
        "login": "ninja",
        "password": ""
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для входа":
        print("Ошибка: отсутствует пароль для авторизации.")
    else:
        print(f"Ошибка при авторизации без пароля: {response.status_code} - {response.json()}")



@allure.feature("Логин курьера")
@allure.story("Авторизация с несуществующим логином")
@allure.description("Проверяем что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
def test_non_existent_user():
    login = "nonexistent_user"
    password = "any_password"
    response = login_courier(login, password)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для входа":
        print(f"Ошибка: Курьер с логином '{login}' не существует.")
    else:
        print(f"Ошибка при авторизации с несуществующим пользователем: {response.status_code} - {response.json()}")



@allure.feature("Логин курьера")
@allure.story("Успешный запрос")
@allure.description("Проверяем что успешный запрос возвращает id.")
def test_successful_login_returns_id():
    login = "ninja"
    password = "1234"
    response = login_courier(login, password)
    if response.status_code == 200 and "id" in response.json():
        print(f"Успешная авторизация! Получен ID: {response.json()['id']}")
    else:
        print(f"Ошибка при авторизации: {response.status_code} - {response.json()}")