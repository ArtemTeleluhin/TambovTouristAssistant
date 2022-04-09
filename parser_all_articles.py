import requests
from bs4 import BeautifulSoup as BS
import sqlite3

URL_LIST = (
    "https://ru.wikipedia.org/w/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&limit=5000&offset=0&profile=default&search=-incategory%3A%22%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D0%B8%D0%B8+%D0%BF%D0%BE+%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83%22+%D0%A2%D0%B0%D0%BC%D0%B1%D0%BE%D0%B2&advancedSearch-current={%22fields%22:{%22plain%22:[%22%D0%A2%D0%B0%D0%BC%D0%B1%D0%BE%D0%B2%22]}}&ns0=1",
    "https://ru.wikipedia.org/w/index.php?title=%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&limit=5000&offset=5000&profile=default&search=-incategory%3A%22%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D0%B8%D0%B8+%D0%BF%D0%BE+%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83%22+%D0%A2%D0%B0%D0%BC%D0%B1%D0%BE%D0%B2&advancedSearch-current={%22fields%22:{%22plain%22:[%22%D0%A2%D0%B0%D0%BC%D0%B1%D0%BE%D0%B2%22]}}&ns0=1"
)
DATABASE_NAME = "attractions_base.db"
WIKI = "https://ru.wikipedia.org"
STEP = 100
cords_separators_weights = {
    '°': 1,
    '′': 1 / 60,
    '″': 1 / 3600
}


def convert_cord(cord):
    result = 0.0
    start = 0
    for finish in range(len(cord)):
        if not cord[finish].isdigit():
            if start != finish:
                result += float(cord[start:finish]) * cords_separators_weights[cord[finish]]
            start = finish + 1
    return result


def convert_cords(cords):
    cords = cords.replace(' ', '')
    cords = list(cords)
    for i in range(len(cords)):
        if not (cords[i].isdigit() or cords[i] in cords_separators_weights):
            cords[i] = ' '
    cords = ''.join(cords)
    return tuple(convert_cord(cord) for cord in cords.split())


def parse_cords(url):
    r = requests.get(url)
    html = BS(r.content, 'html.parser')
    text = html.select(".mw-kartographer-maplink")
    if text:
        text = text[0].text
    else:
        return None
    title = html.select(".firstHeading")[0].text
    cords = convert_cords(text)
    if len(cords) < 2:
        return None
    return title, url, cords[0], cords[1]


def save_in_db(data):
    con = sqlite3.connect(DATABASE_NAME)
    database = con.cursor()
    for elem in data:
        database.execute(
            f"INSERT INTO articles_tambov_2(title, url, latitude, longitude, is_correctly) VALUES('{elem[0]}', '{elem[1]}', {elem[2]}, {elem[3]}, 1)"
        )
        con.commit()
    con.close()


def save_problem_list(problem_list):
    with open('problem.txt', 'w', encoding='utf-8') as file:
        for elem in problem_list:
            file.write(elem + "\n")


def main():
    result_list = []
    problem_list = []
    sum_count = 0
    for url in URL_LIST:
        print('Обработка списка выдачи')
        r = requests.get(url)
        html = BS(r.content, 'html.parser')
        blocks = html.select("ul.mw-search-results > li.mw-search-result > div.mw-search-result-heading > a")
        for i, elem in enumerate(blocks):
            sum_count += 1
            url = elem['href']
            if not url.startswith(WIKI):
                url = WIKI + url
            try:
                res = parse_cords(url)
                if res:
                    result_list.append(res)
            except:
                problem_list.append(url)
            if i % STEP == 0:
                print("Обработано страниц:", i)
        print('Обработка списка выдачи закончена')
    print("Страниц с координатами:", len(result_list))
    print("Страниц, с которыми возникли проблемы:", len(problem_list))
    print("Всего страниц", sum_count)
    save_in_db(result_list)
    print("Сохранено в базу данных")
    save_problem_list(problem_list)
    print("Ссылки, с которыми возникли проблемы, сохранены")
    print()
    print("Ссылки, с которыми возникли проблемы:")
    print(*problem_list)


main()
