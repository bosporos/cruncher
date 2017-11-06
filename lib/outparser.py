import csv
import os.path

class outparser:
    def __init__(self, path):
        self.path = path
        self.fd = open(path, 'wb')
        self.writer = csv.writer(self.fd, delimiter=',', quotechar='|', quoting = csv.QUOTE_MINIMAL)
    
    def write(self, data):
        for row in data:
            self.writer.writerow(row.values())
