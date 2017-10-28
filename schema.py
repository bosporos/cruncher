from reader import reader
from constants import CRUNCHER_PATHS, DEBUG

class schema:
    def __init__(self):
        print "Attempting to open schema..."
        self.reader = reader(CRUNCHER_PATHS['SCHEMA'])
        self.schema = dict()
        self.index = []
        
        print "Attempting to process schema..."
        for row in self.reader.read():
            field = row[0]
            question = row[1]
            self.schema[field] = '|' + question + '|'
            self.index.append(field)
        print "Schema read!"
        if DEBUG['DEBUG_READ_SCHEMA']:
            for field in self.index:
                question = self.schema[field]
                print "{field}: {question}".format(field=field,question=question)
    
    def getNumberOfFields(self):
        return len(self.index)
    
    def getIndexOfField(self, field):
        return self.index.index(field)
    
    def getQuestionForField(self, field):
        return self.schema[field]
    
    def getFields():
        return self.index
