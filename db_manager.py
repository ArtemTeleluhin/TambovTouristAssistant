import sqlite3
from coordinate_math import count_distance


class DBManager:
    def __init__(self, db_name):
        con = sqlite3.connect(db_name)
        database = con.cursor()
        self.data = list(database.execute("SELECT * FROM articles_tambov").fetchall())
        con.close()

    def sort_by_distance(self, latitude, longitude):
        return sorted(map(lambda elem: elem + (count_distance(latitude, longitude, elem[3], elem[4]),), self.data),
                      key=lambda elem: elem[-1])


if __name__ == '__name__':
    db_manager = DBManager('attractions_base.db')
    for elem in db_manager.sort_by_distance(50.0, 50.0):
        if '"' in elem[2]:
            print(elem[2])
    while True:
        latitude, longitude = map(float, input().split())
        print(db_manager.sort_by_distance(latitude, longitude)[0])
