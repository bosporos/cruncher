import csv
import os.path

class reader:
    def __init__(self, path):
        if not os.path.isfile(path):
            raise Exception("File does not exist: %s" % path)
        
        self.path = path
        self.fd = open(path, 'r')
    
    def read(self):
        self.fd.seek(0)
        reader = csv.reader(self.fd, delimiter=',', quotechar='"')
        return reader
