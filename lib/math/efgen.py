import mpmath as mm
from ..matrix import matrix

# For 3-dimensional ef-tables
class efgen3:
    def __init__(self, m):
        self.m = m
    
    def generate(self, debug = False):
        space = self.m.space
        dim = self.m.dimensions
        
        efmatrix = matrix(dim)
        sums = {'totals': [], 'total': 0}
        for d_idx in range(space):
            tuple = [None for ____n_tmp_idx in range(space)]
            sums[d_idx] = {}
            for p_idx in range(dim[d_idx]):
                tuple[d_idx] = p_idx
                sums[d_idx][p_idx] = sum(self.m.access(tuple).values())
            sums['totals'].append(sum(sums[d_idx].values()))
        print "S-Totals: ", sums['totals']
        sums['total'] = sums['totals'][0]
        if len(set(sums['totals'])) > 1:
            print sums
            print "Warning! Sanity lost! (primary r/c/s/+ stacks @ %i)" % space
        
        ettl = [0]
        self.generate_(sums, efmatrix, 0, [], ettl)
        if debug:
#            print "=== DATA HEALTH INDICATOR SAMPLE === (122,2,)"
#            print efmatrix.access((122,0,None))
            sanity = (float(ettl[0])/float(sums['total']))*100.0
            print "Sanity: %f%%" % sanity 
        return efmatrix
    
    def generate_(self, sums, m, d_idx, build, ettl):
        if d_idx  == self.m.space:
            # Finally. $build is fully fleshed out at this point, so that's
            # ready to go
            fscl = [float(sums[n][build[n]])/sums['total'] for n in range(d_idx)]
            fsc = reduce(lambda x,y:x*y, fscl, 1)
            end = fsc * sums['total']
            ettl[0] += end
            m.set(tuple(build), end)
        else:
            for variation in range(self.m.dimensions[d_idx]):
                self.generate_(sums, m, d_idx + 1, build + [variation], ettl)

class efgen:
    def __init__(self, matrix):
        self.m = matrix
    
    def generate(self, debug = False):
        dim = self.m.dimensions
        if debug:
            print "efgen: diagnostic: 2,0-space dimensions: ",
            print dim
        
        
        col_totals = {}
        row_totals = {}
        
        for row in range(dim[0]):
            # A 2-tuple indexed dict
            tuple_coord_row = self.m.access((row, None))
            row_sum = mm.fsum(tuple_coord_row.values())
            row_totals[row] = row_sum
        for col in range(dim[1]):
            # A 2-tuple indexed dict
            tuple_coord_col = self.m.access((None, col))
            col_sum = mm.fsum(tuple_coord_col.values())
            col_totals[col] = col_sum
        
        total_from_rows = mm.fsum(row_totals.values())
        total_from_cols = mm.fsum(col_totals.values())
        
        if debug:
            print "efgen: diagnostic: Row Total: %f" % total_from_rows
            print "efgen: diagnostic: Column Total: %f" % total_from_cols
        if total_from_rows != total_from_cols:
            print "efgen: warning! Sanity lost! (primary r/c stacks in 2,0-space)"
            3/0
        
        total = total_from_rows
        
        col_probs = {n: col_totals[n]/total for n in range(len(col_totals))}
        row_probs = {n: row_totals[n]/total for n in range(len(row_totals))}
        
        efmatrix = matrix(dim)
        
        for row in range(dim[0]):
            for col in range(dim[1]):
                coord = (row, col)
                prob = mm.fmul(col_probs[col], row_probs[row])
                val = mm.fmul(prob, total)
                efmatrix.set(coord, val)
        
        return {
            'eftable': efmatrix,
            'row_totals': row_totals,
            'col_totals': col_totals,
            'total': total
        }
        
         




