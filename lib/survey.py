from schema import schema
from reader import reader
from constants import CRUNCHER_PATHS, DEBUG, CRUNCHER_FIELDS

class survey:
    def __init__(self):
        self.schema = schema()
        
        print "Attempting to open survey data..."
        self.reader = reader(CRUNCHER_PATHS['PUBLIC'])
        print "Success!"
        
        for name in CRUNCHER_FIELDS:
            print "Extracting Field: [%s], index: [%i]" % (name, self.schema.getIndexOfField(name))
        
        self.performRowLengthSanityCheck()
        self.processData()
    
    def processData(self):
        print "Attempting to process survey data..."
        
        self.data = []
        first_item_has_been_ignored = False
        for row in self.reader.read():
            if not first_item_has_been_ignored:
                first_item_has_been_ignored = True
                continue
            tmp = self.extractFieldsFromRow(row)
            if 'NA' not in tmp.values():
                self.data.append(tmp)
                if DEBUG['DEBUG_READ_PUBLIC']:
                    print "Datum: ",
                    for field in CRUNCHER_FIELDS:
                        print field + '=|' + datum[field] + '| ',
                    print
        print "N=%i" % len(self.data)
        self.n = len(self.data)
    
    def extractFieldsFromRow(self, row):
        datum = {}
        for field in CRUNCHER_FIELDS:
            datum[field] = row[self.schema.getIndexOfField(field) - 1]
        return datum
    
    def performRowLengthSanityCheck(self):
        print "Checking row length sanity..."
        l = self.schema.getNumberOfFields() - 1
        idx = 0
        parity = 0
        for row in self.reader.read():
            if len(row) != l:
                print "Anomalous Row Length: %i @ idx: %i" % (len(row), idx)
                parity = parity + 1
            idx = idx + 1
        if parity > 0:
            print "Row lengths are not sane (n=%i)" % parity
            quit()
        else:
            print "Row lengths are sane"
