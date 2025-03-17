import allure
import requests
import random
import string

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass, response



@allure.feature("Регистрация курьера")
@allure.story("Создание нового курьера")
@allure.description("Проверяем успешную регистрацию курьера")
def test_courier_success_registration():
    login_pass, response = register_new_courier_and_return_login_password()
    if response.status_code == 201 and response.json() == {"ok": True}:
        print(f"Курьер создан: Логин {login_pass[0]}, Пароль {login_pass[1]}")
    else:
        print(f"Ошибка при создании курьера: {response.status_code} - {response.json()}")



@allure.feature("Регистрация курьера")
@allure.story("Создание 2-х одинаковых курьеров")
@allure.description("Проверяем что нельзя создать 2 одинаковых курьера с тем же логином.")
def test_duplicate_courier():
    login_pass, _ = register_new_courier_and_return_login_password()
    payload = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для создания учетной записи":
        print("Ошибка: Невозможно создать курьера с таким же логином.")
    else:
        print(f"Ошибка при создании курьера с дублирующимся логином: {response.status_code} - {response.json()}")



@allure.feature("Регистрация курьера")
@allure.story("Ввод обязательных полей")
@allure.description("Проверяем, что нельзя создать курьера без ввода обязательных полей")
def test_missing_fields():
    payload = {
        "login": "",
        "password": "",
        "firstName": ""
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для создания учетной записи":
        print("Ошибка: Не переданы обязательные поля для создания курьера.")
    else:
        print(f"Ошибка при создании курьера с отсутствующими полями: {response.status_code} - {response.json()}")



@allure.feature("Регистрация курьера")
@allure.story("Запрос возвращает правильный код ответа")
@allure.description("Проверяем, что успешный запрос возвращает код 201")
def test_success_response():
    login_pass, response = register_new_courier_and_return_login_password()
    if response.status_code == 201:
        print("Код ответа правильный: 201")
    else:
        print(f"Ошибка с кодом ответа: {response.status_code} - {response.json()}")



@allure.feature("Регистрация курьера")
@allure.story("Запрос возвращает правильный ответ")
@allure.description("Проверяем, что успешный запрос возвращает '{'"'ok'"':true}'")
def test_success_response_message():
    login_pass, response = register_new_courier_and_return_login_password()
    if response.status_code == 201 and response.json() == {"ok": True}:
        print('Ответ успешный: {"ok": true}')
    else:
        print(f"Ошибка в ответе: {response.status_code} - {response.json()}")



@allure.feature("Регистрация курьера")
@allure.story("Нет ввода обязательных полей")
@allure.description("Проверяем, что если нет одного из полей, возвращается ошибка")
def test_missing_one_field():
    payload = {
        "login": "unique_login",
        "password": "",
        "firstName": "Test"
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для создания учетной записи":
        print("Ошибка: отсутствует одно из обязательных полей.")
    else:
        print(f"Ошибка при создании курьера с отсутствующим полем: {response.status_code} - {response.json()}")



@allure.feature("Регистрация курьера")
@allure.story("Путаемся создать курьера который уже есть")
@allure.description("Проверяем, что если есть такой же курьер логин - возвращается ошибка")
def test_existing_login():
    login_pass, _ = register_new_courier_and_return_login_password()
    payload = {
        "login": login_pass[0],
        "password": "new_password",
        "firstName": "New Name"
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    if response.status_code == 400 and response.json().get("message") == "Недостаточно данных для создания учетной записи":
        print("Ошибка: Невозможно создать курьера с таким логином.")
    else:
        print(f"Ошибка при создании курьера с уже существующим логином: {response.status_code} - {response.json()}")