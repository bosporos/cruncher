import mpmath as mm

from lib.matrix import matrix
from ..math.efgen import efgen
from ..math.chisquaredtest import ChiSquaredTest

def gl_perform(data, vparser, latex_dump_tables = False):
    rp = gl_rp(data, vparser)
    m_actual = rp.matrix
    
    efgenner = efgen(m_actual)
    ef_data = efgenner.generate(debug=True)
    m_expected = ef_data['eftable']
    
    row_totals = ef_data['row_totals']
    col_totals = ef_data['col_totals']
    total = ef_data['total']
    
    #        A B C D Totals
    # Male   3 2 1 0 4
    # Female 2 1 0-1 4
    # Other  1 0-1-2 4
    # Totals 6 3 2 3 12
    
    # === DUMP TABLE === #
    
    getlang = lambda name: list(vparser.pvalues['WantWorkLanguage']['possibilities'])[name]
    rezgender = lambda g: g if g in ['Male','Female'] else 'Other'
    getgender = lambda name: rezgender(list(vparser.pvalues['Gender']['possibilities'])[name])
    NL = "\\\\"
    
    # Ok, this should work (I hope!)
    
#    for gend_idx in range(m_actual.dimensions[0]):
#        print "& %s" % getgender(gend_idx),
#    print "& Totals", NL
#    
#    for lang_idx in range(m_actual.dimensions[1]):
#        print getlang(lang_idx),
#        for gend_idx in range(m_actual.dimensions[0]):
#            print "& %i" % m_actual.access((gend_idx, lang_idx)),
#        print "& %i" % col_totals[lang_idx], NL
#    
#    print "Totals",
#    for gend_idx in range(m_actual.dimensions[0]):
#        print "& %i" % row_totals[gend_idx],
#    print "& %i" % total, NL
    
#    for gend_idx in range(m_actual.dimensions[0]):
#        print "& %s" % getgender(gend_idx),
#    print "& Totals", NL
#    
#    for lang_idx in range(m_actual.dimensions[1]):
#        print getlang(lang_idx),
#        for gend_idx in range(m_actual.dimensions[0]):
#            # THIS IS DIFFERENT: m_expected.access(...) v. m_actual.access(...)
#            # Also, "& %f" v. "& %i", b/c expecteds can be non-intish
#            print "& %f" % m_expected.access((gend_idx, lang_idx)),
#        print "& %i" % col_totals[lang_idx], NL
#    
#    print "Totals",
#    for gend_idx in range(m_actual.dimensions[0]):
#        print "& %i" % row_totals[gend_idx],
#    print "& %i" % total, NL

    
    # === CHI SQUARED CALC === #
    
    O = m_actual.data # observed
    E = m_expected.data # expected
    
    O_E = {}
    for coord in O:
        O_E[coord] = mm.fsub(O[coord], E[coord])
    
    O_E_squared = {}
    for coord in O_E:
        O_E_squared[coord] = mm.power(O_E[coord], 2)
    
    O_E_squared_over_E = {}
    for coord in O_E:
        O_E_squared_over_E[coord] = mm.fdiv(O_E_squared[coord], E[coord])
    
    lines = ["","","","","","","","","","",""]
    for a in range(m_actual.dimensions[0]): # Gender
        gendement = dict()
        for b in range(m_actual.dimensions[1]): # Language
            # dimensions[1] = ( ... , HERE )
            # dimensions[0] = ( HERE , ... )
            coord = (a, b)
            gendement[b] = O[coord]
#            print "%s & %i & %f & %f & %f & %f \\\\" % (gl_coord_stringify(coord, vparser, debug = False), O[coord], E[coord], O_E[coord], O_E_squared[coord], O_E_squared_over_E[coord])
        lines[0] += "\\textbf{%s} & \\textbf{Frequency} & " % getgender(a)
        taken = set()
        for counter in range(10):
            highest = 0
            which_highest = 0
            for lang_idx in gendement:
                if gendement[lang_idx] >= highest and lang_idx not in taken:
                    which_highest = lang_idx
                    highest = gendement[lang_idx]
            lines[counter + 1] += "%s & %i &" % (getlang(which_highest), highest)
            taken.add(which_highest)
    for line in lines:
        print "%s \\\\" % line

    chi_squared_val = mm.fsum(O_E_squared_over_E.values())
    df = m_actual.degreesOfFreedom()

    print "Degrees of Freedom:", df
    print "Chi Squared Value:", chi_squared_val
    
    p_value = ChiSquaredTest(df=df, chisquaredcalc = chi_squared_val, heavy = 1000)
    print p_value


def gl_coord_stringify(coord, vparser, debug = False):
    gender = list(vparser.pvalues['Gender']['possibilities'])[coord[0]]
    if gender not in ['Male', 'Female']:
        # This is necessary because of the way I grouped gender into M/F/Other
        # The lookup performed here will come back with something? that's not M/F
        # but not necessarily 'Other'
        gender = 'Other'
    
    lang = list(vparser.pvalues['WantWorkLanguage']['possibilities'])[coord[1]]
    if debug:
        return "%s: %s, %s" % (coord, gender, lang)
    else:
        return "%s, %s" % (gender, lang)
    

class gl_rp:
    def __init__(self, data, vp):
        # Need to turn the data into a matrix (lit. a scatterplot. Kinda)
        X = 'Gender' # Independent Var
        Y = 'WantWorkLanguage' # Not an independent Var/ Not sure about dependent, tho...
        
        # SX = Set of all possible X (Gender)
        # SY = Set of all possible Y (Gender)
        (SX, SY) = [list(vp.pvalues[n]['possibilities']) for n in (X, Y)]
        print "Squaring data... (%s | %s)" % (X, Y)
        size = (LX, LY) = [len(n) for n in (SX, SY)]
        m = matrix(size)
        for datum in data:
            x = SX.index(vp.resolvePartialSplinter(datum[X].split('; '), 'm/f/o'))
            # Generate a point for each language
            for lang in datum[Y].split('; '):
                tuple = (x, SY.index(lang))
                delta = self.calcDelta(lang, datum[Y].split('; '))
                m.set(tuple, mm.mpf(m.access_pt(tuple) + delta))
        self.matrix = m
    
    def calcDelta(self, lang, langs):
        method = 1
        if method == 0:
            # Method 1:
            return 1.0 / float(len(langs))
        elif method == 1:
            # Method 2:
            return 1.0
