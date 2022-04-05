import requests

APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"
MAP_REQUEST = "https://static-maps.yandex.ru/1.x/?l=map&pt={},{},ya_ru"
ARTICLE_MARK = "~{},{},pm2rdm"


def draw_map(user_cords, *articles_cords):
    user_latitude, user_longitude = user_cords
    map_request = MAP_REQUEST.format(str(user_longitude), str(user_latitude))
    for article_latitude, article_longitude in articles_cords:
        map_request += ARTICLE_MARK.format(str(article_longitude), str(article_latitude))
    while True:
        response = requests.get(map_request)
        if response:
            return response.content
