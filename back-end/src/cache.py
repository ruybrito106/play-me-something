import csv
import random

class Cache:
    def __init__(self, data):
        self.data = data
    
    def get_by_id(self, id):
        return self.data[id]

    def get_sample_values(self, n=1):
        return random.sample(list(self.data.values()), n)

def FromCsvFilePath(filePath, idColumn='id'):
    with open(filePath) as file:
        entries = [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
    data = {row[idColumn]: row for row in entries}
    return Cache(data)