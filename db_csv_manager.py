import csv
from coordinate_math import count_distance
from copy import deepcopy


class DBManager:
    def __init__(self, csv_name):
        self.data = []
        with open(csv_name) as file:
            reader = csv.DictReader(file)
            self.data = [dict(elem) for elem in reader]

    def sort_by_distance(self, latitude, longitude):
        result = deepcopy(self.data)
        for elem in result:
            elem['dict'] = count_distance(latitude, longitude, elem['latitude'], elem['longitude'])
        result.sort(key=lambda elem: elem['dict'])
        return result
