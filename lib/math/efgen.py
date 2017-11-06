from ..matrix import matrix

class efgen:
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
            print "Warning! Sanity lost! (primary r/c/s/+ stacks @ %i)" % space
        
        ettl = [0]
        self.generate_(sums, efmatrix, 0, [], ettl)
        if debug:
            print "=== DATA HEALTH INDICATOR SAMPLE === (122,2,)"
            print efmatrix.access((122,0,None))
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
