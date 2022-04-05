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


class ArticlesQueue:
    def __init__(self, data, user_latitude, user_longitude):
        self.data = data
        self.current_position = 0
        self.user_latitude = user_latitude
        self.user_longitude = user_longitude
        self.flag_is_top_selected = False

    def get_current_element(self):
        return self.data[self.current_position]

    def next_element(self):
        if self.is_last():
            return None
        self.flag_is_top_selected = False
        self.current_position += 1
        return self.data[self.current_position]

    def prev_element(self):
        if self.is_first():
            return None
        self.flag_is_top_selected = False
        self.current_position -= 1
        return self.data[self.current_position]

    def is_last(self):
        if self.current_position == len(self.data) - 1:
            return True
        return False

    def is_first(self):
        if self.current_position == 0:
            return True
        return False

    def get_user_cords(self):
        return self.user_latitude, self.user_longitude

    def get_top_articles(self, count):
        self.flag_is_top_selected = True
        return self.data[:min(count, len(self.data))]

    def is_top_last(self):
        return self.flag_is_top_selected


if __name__ == '__name__':
    db_manager = DBManager('attractions_base.db')
    for elem in db_manager.sort_by_distance(50.0, 50.0):
        if '"' in elem[2]:
            print(elem[2])
    while True:
        latitude, longitude = map(float, input().split())
        print(db_manager.sort_by_distance(latitude, longitude)[0])
