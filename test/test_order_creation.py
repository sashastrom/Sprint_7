import allure
from conftest import *

class TestOrderCreation:

    @pytest.mark.parametrize(
        "first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color, expected_status_code",
        [    # можно указать один из цветов — BLACK или GREY
            ("Naruto", "Uchiha", "Konoha, 142 apt.", 4, "+7 800 355 35 35", 5, "2020-06-06", "Saske, come back to Konoha",
             ["BLACK"], 201),
            ("Naruto", "Uchiha", "Konoha, 142 apt.", 4, "+7 800 355 35 35", 5, "2020-06-06", "Saske, come back to Konoha",
             ["GREY"], 201),
            # можно указать оба цвета
            ("Naruto", "Uchiha", "Konoha, 142 apt.", 4, "+7 800 355 35 35", 5, "2020-06-06", "Saske, come back to Konoha",
             ["BLACK", "GREY"], 201),
            # можно совсем не указывать цвет
            ("Naruto", "Uchiha", "Konoha, 142 apt.", 4, "+7 800 355 35 35", 5, "2020-06-06", "Saske, come back to Konoha",
             [], 201)
        ]
    )
    @allure.title("Проверяем что: можно указать разные параметры цветов, тело ответа содержит track")
    def test_create_order(self, first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color,
                          expected_status_code):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
            "color": color
        }

        response = create_order(payload)

        # Проверяем статус код ответа
        assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

        # Проверяем что есть поле track
        response_json = response.json()
        assert "track" in response_json, f"Expected 'track' field in response, but got {response_json}"
        print(f"Order created successfully with track: {response_json['track']}")
