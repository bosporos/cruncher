from efgen import efgen as efgen
from .. import matrix as matrix

class chisquaredgen:
    def __init__(self, m_actual, m_expected):
        self.m_a = m_actual
        self.m_x = m_expected
    
    def calculate(self, debug = False):
        ma = self.m_a
        mx = self.m_x
        
        dim = ma.dimensions
        if dim != mx.dimensions:
            print "Warning: Matrix differential is not %i-stable" % ma.space
            print "Matrix 1: ", ma.dimensions
            print "Matrix 2: ", mx.dimensions
            quit()
        
        df = ma.degreesOfFreedom()
        if debug:
            print "Degrees Of Freedom: %i" % df
        delta = []
        # n-tuples (b/c data=dict)
        for point in ma.data:
            diff = mx.access_pt(point) - ma.access_pt(point)
            diff_pow2 = diff ** 2
            if mx.access_pt(point) != 0:
                chilm = diff_pow2 / mx.access(point)
            else:
                chilm = 0
            delta.append(chilm)
        chi_squared = float(sum(delta))
        
        return (df, chi_squared)
