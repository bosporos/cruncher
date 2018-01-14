from lib.matrix import matrix
from ..math.efgen import efgen
from ..math.chisquaredgen import chisquaredgen
from ..math.chisquaredtest import ChiSquaredTest

__CGL__ = {
    'axes': {
        'X': 'Country',
        'Y': 'Gender',
        'Z': 'WantWorkLanguage'
    },
    'conf': {
        'GENDER_RES': 'm/f/o'
    }
}

def cgl_perform(data, vp):
    rp = cgl_rp(data, vp)
    m_actual = rp.matrix

    efgenner = efgen(m_actual)
    m_expected = efgenner.generate(debug=False)
    
    t_chisqrd = chisquaredgen(m_actual, m_expected)

    global cgl_stat_matrix_df
    global cgl_stat_chi_squared
    # flag debug=True to print DF value
    (cgl_stat_matrix_df, cgl_stat_chi_squared) = t_chisqrd.calculate(debug=True)
    # Should be Degrees Of Freedom: 16864
    # {'phi_coefficient': 0.6871276478410416,
    #  'cramers_v': 0.3435638239205208,
    #  'chi_squared': 18959.90284859763,
    #  'corrected_cramers_v': 0.10216302207164774
    # }
    print "Chi Squared Calculation: [%f]" % cgl_stat_chi_squared
    global cgl_stat_chi_squared_p_value
    cgl_stat_chi_squared_p_value = ChiSquaredTest(df=cgl_stat_matrix_df, chisquaredcalc = cgl_stat_chi_squared, heavy = 10000)
    print "P value:", cgl_stat_chi_squared_p_value

class cgl_rp:
    def __init__(self, data, vp):
        X = __CGL__['axes']['X']
        Y = __CGL__['axes']['Y']
        Z = __CGL__['axes']['Z']
        (SX, SY, SZ) = [list(vp.pvalues[n]['possibilities']) for n in (X,Y,Z)]
        print "Qubing data... (%s | %s | %s)" % (X, Y, Z)
        size = (LX, LY, LZ) = [len(n) for n in (SX, SY, SZ)]
        m = matrix(size)
        for datum in data:
            x = SX.index(datum[X])
            y = SY.index(vp.resolvePartialSplinter(datum[Y].split('; '), __CGL__['conf']['GENDER_RES']))
            if self.isEligible(datum):
                for lang in datum[Z].split('; '):
                    tuple = (x, y, SZ.index(lang))
                    m.set(tuple, m.access_pt(tuple) + 1)
        self.matrix = m
    
    def isEligible(self, datum):
        # add functionality to ignore <5 countries, genders, and langs
        # add functionality for gender-combine
        return True
