import csv
import sys
import re
import math

CRUNCHER_SURVEY_SCHEMA = 'survey_results_schema.csv'
CRUNCHER_SURVEY_DATA = 'survey_results_public.csv'
CRUNCHER_KEYS = {'Gender','WantWorkLanguage','Country','Salary'}

cruncher_schema = {}
cruncher_kindex = []
cruncher_data = []
cruncher_vbase = {}

# A 4-dimensional set, accessed by 3-tuples, consisting of ???s
class qube:
    def __init__(self, tuple):
        self.dimensions = tuple
        self.xl = self.dimensions[0]
        self.yl = self.dimensions[1]
        self.zl = self.dimensions[2]
        self.data = [[[0 for a in range(tuple[2])] for b in range(tuple[1])] for c in range(tuple[0])]
    
    def degreesOfFreedom(self):
        return (self.xl - 1) * (self.yl - 1) * (self.zl - 1)
    
    def access(self, tuple):
        tuple = list(tuple)
        if None in tuple:
            if tuple.count(None) == 1:
                where = tuple.index(None)
                line = [0] * self.dimensions[where]
                for i in range(0, self.dimensions[where]):
                    tuple[where] = i
                    (x, y, z) = tuple
                    line[i] = self.data[x][y][z]
                return line
            elif tuple.count(None) == 2:
                for a in tuple:
                    if a is not None:
                        break
                clear = tuple.index(a)
                where = list({0, 1, 2} - {clear})
                plane = [[0 for j in range(0, self.dimensions[where[1]])] for k in range(0, self.dimensions[where[0]])]
                for a in range(0, self.dimensions[where[0]]):
                    for b in range(0, self.dimensions[where[1]]):
                        tuple[where[0]] = a
                        tuple[where[1]] = b
                        (x, y, z) = tuple
                        plane[a][b] = self.data[x][y][z]
                return plane
            elif tuple.count(None) == 3:
                return self.data;
        return self.data[tuple[0]][tuple[1]][tuple[2]]
    
    def set(self, tuple, value):
        tuple = list(tuple)
        if None in tuple:
            if tuple.count(None) == 1:
                where = tuple.index(None)
                for i in range(self.dimensions[where]):
                    tuple[where] = i
                    (x, y, z) = tuple
                    if hasLength(value):
                        self.data[x][y][z] = value[i % len(value)]
                    else:
                        self.data[x][y][z] = value
            elif tuple.count(None) == 2:
                for a in tuple:
                    if a is not None:
                        break
                clear = tuple.index(a)
                where = list({0, 1, 2} - {clear})
                for a in range(self.dimensions[where[0]]):
                    for b in range(self.dimensions[where[1]]):
                        tuple[where[0]] = a
                        tuple[where[1]] = b
                        (x, y, z) = tuple
                        if hasLength(value):
                            if hasLength(value[a % len(value)]):
                                self.data[x][y][z] = value[a % len(value)][b % len(value[a % len(value)])]
                            else:
                                self.data[x][y][z] = value[b % len(value)]
                        else:
                            self.data[x][y][z] = value
            elif tuple.count(None) == 3:
                self.data = value.copy()
        else:
            self.data[tuple[0]][tuple[1]][tuple[2]] = value

def hasLength(val):
    try:
        len(val)
    except TypeError:
        return False
    return True

def readSchema(debug = False):
    schema_fd = open(CRUNCHER_SURVEY_SCHEMA, 'r')
    schema_reader = csv.reader(schema_fd, delimiter=',')
    for row in schema_reader:
        assess = row[0]
        question = row[1]
        cruncher_schema[assess] = '|' + question + '|'
        cruncher_kindex.append(assess)
    for assess in cruncher_schema.keys():
        question = cruncher_schema[assess]
        if debug:
            print("{assess}: {question}".format(assess=assess,question=question))

def cruncherSurveyCheckRowLengths(data_reader):
    l = len(cruncher_schema) - 1
    idx = 0
    parity = True
    for row in data_reader:
        if(len(row) != l):
            print "Anomalous Row Length: %i @ idx: %i" % ((l-len(row)), idx)
            parity = False
        idx = idx + 1
    return parity

def cruncherRowLengthSanityCheck(data_reader):
    print "Row Length Sanity Check:", 
    rowLengthsAreCorrect = cruncherSurveyCheckRowLengths(data_reader)
    if not rowLengthsAreCorrect:
        print "\tRow Lengths Are All Wrong!"
        quit()
    print "\tRow Lengths are sane!"

def cruncherExtractCruncherKeysFromRow(row):
    datum = {}
    for assess in CRUNCHER_KEYS:
        datum[assess] = row[cruncher_kindex.index(assess) - 1]
    return datum

def cruncherDumpDatumToStdout(datum):
    print "Datum: ",
    for assess in CRUNCHER_KEYS:
        print assess + '=|' + datum[assess] + '| ',
    print

def readSurveyData(debug = False):
    data_fd = open(CRUNCHER_SURVEY_DATA, 'r')
    data_reader = csv.reader(data_fd, delimiter=',')
    for name in CRUNCHER_KEYS:
        print "Extracting Key: [%s], index: [%i]" % (name, cruncher_kindex.index(name))
    
#    cruncherRowLengthSanityCheck(data_reader)
    past_first=False
    for row in data_reader:
        if not past_first:
            past_first = True
            continue
        tmp = cruncherExtractCruncherKeysFromRow(row)
        if 'NA' not in tmp.values():
            cruncher_data.append(tmp)
            if debug:
                cruncherDumpDatumToStdout(tmp)
    print "N=%i" % len(cruncher_data)

numericality = re.compile("[0-9\.e]+")
def isNumeric(str):
    return numericality.match(str)

def cruncherConstructValueLists(debug = False):
    anvil = cruncher_data[0]
    for ding in anvil.keys():
        if isNumeric(anvil[ding]):
            cruncher_vbase[ding] = 'NA'
        else:
            cruncher_vbase[ding] = set()
    for acid in cruncher_data:
        for field in acid.keys():
            if cruncher_vbase[field] != 'NA':
                if field != "WantWorkLanguage" and field != "Gender":
                    if acid[field] not in cruncher_vbase[field]:
                        cruncher_vbase[field].add(acid[field])
                else:
                    values = acid[field].split('; ')
                    if field != "Gender":
                        for value in values:
                            if value not in cruncher_vbase[field]:
                                cruncher_vbase[field].add(value)
                    else:
                        if values[0] not in cruncher_vbase[field]:
                            cruncher_vbase[field].add(values[0])
    if debug:
        for field in cruncher_vbase.keys():
            if cruncher_vbase[field] == 'NA':
                print "%s: Quantitative" % field
            else:
                print "%s: Categorical" % field
                print "\tPossibilities: |%s|" % '|,|'.join(cruncher_vbase[field])

def cruncherParseInformationToValues(debug = False):
    base = {}
    for field in cruncher_vbase.keys():
        if cruncher_vbase[field] == 'NA':
            field_occurrences = False
        else:
            field_occurrences = {key: 0 for key in cruncher_vbase[field]}
        base[field] = field_occurrences
    for datum in cruncher_data:
        for field in datum:
            if base[field] != False:
                if field != "WantWorkLanguage" and field != "Gender":
                    base[field][datum[field]] += 1
                else:
                    values = datum[field].split('; ')
                    if field != "Gender":
                        for value in values:
                            base[field][value] += 1
                    else:
                        base[field][values[0]] += 1
    if debug:
        print base
    global cruncher_base
    cruncher_base = base.copy()

# This creates a 3-matrix of overlapping set items
# Note that each point is not one person, but a language one person uses
# For consideration: divide the value of a person based on number of languages
def cruncherQubifyCGL(debug = False):
    X = "Country"
    Y = "Gender"
    Z = "WantWorkLanguage"
    (SX, SY, SZ) = (cruncher_base[X].keys(), cruncher_base[Y].keys(), cruncher_base[Z].keys())
    print "Qubing data... (%s | %s | %s)" % (X, Y, Z)
    (w, h, d) = (len(SX), len(SY), len(SZ))
    size = (w, h, d)
    q = qube(size)
    for datum in cruncher_data:
        x = SX.index(datum[X])
        y = SY.index(datum[Y].split('; ')[0])
        if cruncherCGLIsEligible(datum):
            for lang in datum[Z].split('; '):
                tuple = (x, y, SZ.index(lang))
                q.set(tuple, q.access(tuple) + 1)
    global q_cgl
    q_cgl = q

def cruncherCGLIsEligible(datum):
# add functionality to ignore <5 countries, genders, and langs
    return True

def planeSum(plane):
    _sum = 0
    for line in plane:
        _sum += sum(line)
    return _sum

# Expected Freq Table for Qubedata
def cruncherQubifyExpected(Q, debug = False):
    q = qube(Q.dimensions)
    (w, h, d) = Q.dimensions
    
    x_sums = [planeSum(Q.access([x, None, None])) for x in range(w)]
    y_sums = [planeSum(Q.access([None, y, None])) for y in range(h)]
    z_sums = [planeSum(Q.access([None, None, z])) for z in range(d)]
    total = float(sum(x_sums))
    if total != sum(y_sums) or total != sum(z_sums):
        print "Warning: Something lost its sanity (primary r/c/s stacks)"
        print "%i %i %i" % (sum(x_sums), sum(y_sums), sum(z_sums))
    
    print x_sums
    print y_sums
    print z_sums
    
    ettl = 0
    for x in range(w):
        x_prob = float(x_sums[x]) / total
        for y in range(h):
            y_prob = float(y_sums[y]) / total
            for z in range(d):
                z_prob = float(z_sums[z]) / total
                end = total * x_prob * y_prob * z_prob
                q.set([x,y,z], end)
                ettl += end
    
    print "Sanity: %f%%" % ((float(ettl)/total)*100.0)
    return q

def cruncherQubePerformDifferentialsAndCalculateChiSquared(quay, qubee):
    dim = (w, h, d) = quay.dimensions
    if dim != qubee.dimensions:
        print "Warning: Qube differntial is not 3-stable! (%i %i %i) (%i %i %i)" % (w, h, d, qubee.dimensions[0], qubee.dimensions[1], qubee.dimensions[2])
        quit()
    
    # assume qubee = Expected
    # assume quay = Observed
    df = quay.degreesOfFreedom()
    print "Degrees Of Freedom: %i" % df
    delta = []
    for x in range(w):
        for y in range(h):
            for z in range(d):
                diff = qubee.access([x,y,z]) - quay.access([x,y,z])
                diff_pow2 = diff ** 2
                if qubee.access([x,y,z]) != 0:
                    chilm = diff_pow2 / qubee.access([x,y,z])
                else:
                    chilm = 0
                delta.append(chilm)
    chi_squared = float(sum(delta))
    
    total = float(sum([planeSum(quay.access([x, None, None])) for x in range(w)]))
    (w, h, d) = (float(w), float(h), float(d))

    phi_coefficient = math.sqrt(chi_squared / total)
    
    phi_coefficient_sqrd = (phi_coefficient ** 2)
    cramersV = math.sqrt(phi_coefficient_sqrd / min(w - 1,h - 1,d - 1))
    
    ccrps = ((w - 1) * (h - 1) * (d - 1)) / (total - 1)
    Nify = lambda n: n - (((n - 1) ** 2) / total)
    ccrk = Nify(w)
    ccrr = Nify(h)
    ccrg = Nify(d)
    ccrphisqrd = max(0, phi_coefficient_sqrd - ccrps)
    correctedCramersV = math.sqrt(ccrphisqrd / min(ccrk, ccrr, ccrg))
    
    return {'chi_squared': chi_squared, 'phi_coefficient': phi_coefficient, 'cramers_v': cramersV, 'corrected_cramers_v': correctedCramersV} 

readSchema()
readSurveyData()
cruncherConstructValueLists(True)
cruncherParseInformationToValues()
cruncherQubifyCGL(True)
q_cgl_x = cruncherQubifyExpected(q_cgl, True)
print cruncherQubePerformDifferentialsAndCalculateChiSquared(q_cgl, q_cgl_x)
#cruncherSquarifyCGS(True)
