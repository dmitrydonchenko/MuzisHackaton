###### Класс для получения информации о событиях, связанных с заданным исполнителем, в заданном городе

import vk


# авторизация в vk
session = vk.AuthSession(app_id='5299950', user_login='89889800727', user_password='VkRentProject420')
api = vk.API(session)

# получаем список городов России
cities = api.database.getCities(country_id = 1)


def get_events_from_vk(artist_name, event_city):
    current_city_id = 1
    for city in cities:
        if isinstance(city, dict):
            if city["title"] == event_city:
                current_city_id = city["cid"]
    events = api.groups.search(q = artist_name, type = "event", country_id = 1, city_id = current_city_id)
    for event in events:
        if isinstance(event, dict):
            print(event["name"])


