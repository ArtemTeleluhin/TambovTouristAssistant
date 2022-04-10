import csv
from coordinate_math import count_distance
from copy import deepcopy


class DBManager:
    def __init__(self, csv_name):
        self.data = []
        with open(csv_name) as file:
            reader = csv.DictReader(file)
            self.data = [dict(elem) for elem in reader]
        for elem in self.data:
            elem['id'] = int(elem['id'])
            elem['latitude'] = float(elem['latitude'])
            elem['longitude'] = float(elem['longitude'])
            elem['is_correctly'] = bool(elem['is_correctly'])

    def sort_by_distance(self, latitude, longitude):
        result = deepcopy(self.data)
        for elem in result:
            elem['dist'] = count_distance(latitude, longitude, elem['latitude'], elem['longitude'])
        result.sort(key=lambda elem: elem['dist'])
        return result
