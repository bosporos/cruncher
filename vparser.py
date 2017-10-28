import re

numericality = re.compile("[0-9\.e]+")
def isNumeric(str):
    return numericality.match(str)

class vparser:
    def __init__(self, data, splinterOn=';', cannotSplinter=set(), splinterPartial=set()):
        # enforce this
        splinterPartial = splinterPartial - cannotSplinter
        self.pvalues = {}
        
        template = data[0]
        for field in template.keys():
            self.pvalues = {}
            if isNumeric(template[field]):
                self.pvalues[field]['type'] = 'interval'
            else:
                self.pvalues[field]['type'] = 'nominal'
                self.pvalues[field]['possibilities'] = set()
        for datum in data:
            for field in datum.keys():
                value = datum[field]
                if self.pvalues[field]['type'] == 'nominal':
                    if field not in cannotSplinter or splinterOn not in value:
                        if 
                        
