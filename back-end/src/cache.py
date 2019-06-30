import csv

class Cache:
    def __init__(self, data):
        self.data = data
    
    def get_by_id(self, id):
        return self.data[id]

def FromCsvFilePath(filePath):
    with open(filePath) as file:
        entries = [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]
    data = {row['id']: row for row in entries}
    return Cache(data)