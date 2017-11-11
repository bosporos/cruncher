import constants

class vparser:
    def __init__(self, data, splinterOn='; ', cannotSplinter=set(), splinterPartial={}):
        # enforce this
        # NO CAN DO
        # RELY CALLER
#        splinterPartial = splinterPartial - cannotSplinter
        self.pvalues = {}
        self.constructBaseFromTemplate(data[0])
        self.constructValuesLists(data, splinterOn, cannotSplinter, splinterPartial)
        if constants.DEBUG['DEBUG_MAKE_VALUES_SCHEMA']:
            self.debugDump()
        self.constructValuesFrequencyLists(data, splinterOn, cannotSplinter, splinterPartial)
    
    def debugDump(self):
        for field in self.pvalues.keys():
            if self.pvalues[field]['type'] == 'nominal':
                print "%s: Nominal" % field
                print "\tPossibilities: |%s|" % '|,|'.join(self.pvalues[field]['possibilities'])
            elif self.pvalues[field]['type'] == 'interval':
                print "%s: Interval" % field
                print "\tRange: |%i| to |%i|" % (self.pvalues[field]['range']['min'], self.pvalues[field]['range']['max'])
    
    def constructValuesLists(self, data, splinterOn, cannotSplinter, splinterPartial): 
        for datum in data:
            for field in datum.keys():
                value = datum[field]
                if self.pvalues[field]['type'] == 'nominal':
                    if (field in cannotSplinter):
                        self.attemptAddPValue(field, value)
                    else:
                        values = value.split(splinterOn)
                        if field in splinterPartial:
                            # Ok, this will do a partial splinter
                            mode = splinterPartial[field]
                            tmp_value = self.resolvePartialSplinter(values, mode)
                            self.attemptAddPValue(field, tmp_value)
                        else:
                            # Ok, complete splinter
                            for tmp_value in values:
                                self.attemptAddPValue(field, tmp_value)
                elif self.pvalues[field]['type'] == 'interval':
                    num_value = constants.numerify(value)
                    if num_value < self.pvalues[field]['range']['min']:
                        self.pvalues[field]['range']['min'] = num_value
                    if num_value > self.pvalues[field]['range']['max']:
                        self.pvalues[field]['range']['max'] = num_value
    
    def constructValuesFrequencyLists(self, data, splinterOn, cannotSplinter, splinterPartial):
        frequencies = {}
        for field in self.pvalues.keys():
            if self.pvalues[field]['type'] == 'interval':
                # DO NOT COLLECT FREQUENCIES
                field_occurrences = False
            elif self.pvalues[field]['type'] == 'nominal':
                field_occurrences = {key: 0 for key in self.pvalues[field]['possibilities']}
            frequencies[field] = field_occurrences
        for datum in data:
            for field in datum:
                if frequencies[field] != False:
                    value = datum[field]
                    if (field in cannotSplinter):
                        frequencies[field][value] += 1
                    else:
                        values = value.split(splinterOn)
                        if field in splinterPartial:
                            # Ok, this will do a partial splinter
                            mode = splinterPartial[field]
                            tmp_value = self.resolvePartialSplinter(values, mode)
                            frequencies[field][tmp_value] += 1
                        else:
                            for tmp_value in values:
                                if not constants.DISTRIBUTE_SPLIT_FIELDS:
                                    frequencies[field][tmp_value] += 1
                                else:
                                    # Note: maybe add some balancing here
                                    frequencies[field][tmp_value] += (1.0 / len(values))
        if constants.DEBUG['DEBUG_MAKE_VALUES_FREQUENCIES']:
            print frequencies
        for key in frequencies.keys():
            self.pvalues[key]['frequencies'] = frequencies[key]
    
    def resolvePartialSplinter(self, values, mode):
        if mode == 'first':
            return values[0]
        elif mode == 'last':
            return values[-1]
        elif mode == 'm/f/o':
            vtmp = self.resolvePartialSplinter(values, 'last')
            if vtmp == 'Male' or vtmp == 'Female':
                return vtmp
            else:
                return 'Other'
    
    def constructBaseFromTemplate(self, template):
        for field in template.keys():
            self.pvalues[field] = {}
            if constants.isNumeric(template[field]):
                self.pvalues[field]['type'] = 'interval'
                self.pvalues[field]['range'] = {'min': 0, 'max': 0}
            else:
                self.pvalues[field]['type'] = 'nominal'
                self.pvalues[field]['possibilities'] = set()
    
    def attemptAddPValue(self, field, value):
        if value not in self.pvalues[field]:
            self.pvalues[field]['possibilities'].add(value)
