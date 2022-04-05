import requests
from bs4 import BeautifulSoup as BS
import sqlite3

URL = "https://ru.wikipedia.org/w/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&limit=1200&offset=0&ns0=1&search=-incategory%3A%22%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D0%B8%D0%B8+%D0%BF%D0%BE+%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83%22+%D1%81.%D1%88.+%D0%B2.%D0%B4.+%D0%A2%D0%B0%D0%BC%D0%B1%D0%BE%D0%B2&advancedSearch-current={%22fields%22:{%22phrase%22:%22%D0%A2%D0%B0%D0%BC%D0%B1%D0%BE%D0%B2%22,%22plain%22:[%22%D1%81.%D1%88.%22,%22%D0%B2.%D0%B4.%22]}}"
DATABASE_NAME = "attractions_base.db"
WIKI = "https://ru.wikipedia.org"
STEP = 100


def convert_cord(text):
    x = int(text[:text.find('°')])
    y = int(text[text.find('°') + 1:text.find('′')])
    z = int(text[text.find('′') + 1:text.find('″')])
    return x + y / 60 + z / 3600


def parse_cords(url):
    r = requests.get(url)
    html = BS(r.content, 'html.parser')
    text = html.select(".mw-kartographer-maplink")
    if text:
        text = text[0].text
    else:
        return None
    text = text.split()
    title = html.select(".firstHeading")[0].text
    return title, url, convert_cord(text[0]), convert_cord(text[3])


def save_in_db(data):
    con = sqlite3.connect(DATABASE_NAME)
    database = con.cursor()
    for elem in data:
        database.execute(
            f"INSERT INTO articles_tambov(title, url, latitude, longitude, is_correctly) VALUES('{elem[0]}', '{elem[1]}', {elem[2]}, {elem[3]}, 1)"
        )
        con.commit()
    con.close()


def save_problem_list(problem_list):
    with open('problem.txt', 'w', encoding='utf-8') as file:
        for elem in problem_list:
            file.write(elem + "\n")


def main():
    r = requests.get(URL)
    html = BS(r.content, 'html.parser')
    blocks = html.select("ul.mw-search-results > li.mw-search-result > div.mw-search-result-heading > a")
    result_list = []
    problem_list = []
    count = 0
    for elem in blocks:
        count += 1
        url = elem['href']
        if not url.startswith(WIKI):
            url = WIKI + url
        try:
            res = parse_cords(url)
            if res:
                result_list.append(res)
        except:
            problem_list.append(url)
        if count % STEP == 0:
            print("Обработано страниц:", count)
    print("Страниц с координатами:", len(result_list))
    print("Страниц, с которыми возникли проблемы:", len(problem_list))
    print("Всего страниц:", count)
    save_in_db(result_list)
    print("Сохранено в базу данных")
    save_problem_list(problem_list)
    print("Ссылки, с которыми возникли проблемы, сохранены")
    print()
    print("Ссылки, с которыми возникли проблемы:")
    print(*problem_list)


main()
