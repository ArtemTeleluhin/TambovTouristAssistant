import sqlite3
import csv

DATABASE_NAME = "attractions_base.db"
CSV_NAME = "attractions_list.csv"


def convert_to_csv(database_name, csv_name):
    con = sqlite3.connect(database_name)
    database = con.cursor()
    data = list(database.execute("SELECT * FROM articles_tambov_2").fetchall())
    con.close()
    dict_list = []
    for elem in data:
        dict_list.append({
            'id': elem[0],
            'title': elem[1],
            'url': elem[2],
            'latitude': elem[3],
            'longitude': elem[4],
            'is_correctly': elem[5]
        })
    with open(csv_name, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(dict_list[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in dict_list:
            writer.writerow(d)


def print_from_csv(csv_name):
    with open(csv_name, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in list(reader)[:10]:
            print(dict(row))
