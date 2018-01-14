import math
import mpmath as m

class statistikon:
    def __init__(self, dd, unweighted = False):
        if unweighted == True:
            dds_wc = {}
            for e in dd:
                dds_wc[e] = 0
            for e in dd:
                dds_wc[e] = dds_wc[e] + 1
            dd = dds_wc
        if unweighted == 2:
            dds_wc = {}
            # To turn lists where index=value, value=weight into dicts
            for e in range(len(dd)):
                dds_wc[e] = dd[e]
            dd = dds_wc
        # Nesyetyu numrez ex l'fouerm dictus
        self.dd = dd
        
    def c_median(self, heavy = 53):
        # MPMath par le numrez q'sant largeux
        # MPMath, tayen, par l'divsjon d'numrez deux
        m.mp.dps = heavy
        l = self.c_len(heavy=heavy)
        if m.fmod(l, 2) != 0:
            if m.fmod(l, 2) != 1:
                print "Insanity: # elementnoye ex weighted set n'est intish"
                3/0
            # OK, nous suent salvet
            midx = (math.ceil(l/2.0)) - 1
            return self.c_idx(midx)
        else:
            # OK, nous suent in l'midum ent le numrez midienteux
            midxh = l / 2.0
            midxl = midxh - 1
            mvh = self.c_idx(idx=midxh)
            mvl = self.c_idx(idx=midxl)
            return (mvh + mvl) / 2
    
    def c_mode(self):
        modes = []
        modal_zenith = 0
        for e in self.dd:
            if self.dd[e] == modal_zenith:
                modes.append(e)
            if self.dd[e] > modal_zenith:
                modes = [e]
                modal_zenith = self.dd[e]
        return modes
    
    def c_range(self):
        minv = min(self.dd.keys())
        maxv = max(self.dd.keys())
        return [minv, maxv]
    
    def c_stdev(self):
        mean = self.c_mean()
        
        collate = []
        for e in self.dd:
            inner = m.power(m.fsub(e,mean), 2)
            for ___t in range(self.dd[e]):
                collate.append(inner)
        summa = m.fsum(collate)
        print "Summa:", summa
        N = self.c_len()
        return m.sqrt(m.fdiv(summa, N))
    
    def c_mean(self, heavy = 53):
        # MPMath par le numrez q'sant largeux
        m.mp.dps = heavy
        total = self.c_sum(heavy=heavy)
        mean = m.fdiv(total, self.c_len(heavy=heavy))
        return mean
    
    def c_len(self, heavy = 53):
        m.mp.dps = heavy
        tot_len = m.mpf(0)
        for idx in self.dd:
            tot_len = m.fadd(tot_len, self.dd[idx])
        return tot_len
    
    def c_sum(self, heavy = 53):
        m.mp.dps = heavy
        total = m.mpf(0)
        for idx in self.dd:
            t_wt = m.mpf(self.dd[idx])
            t_vl = m.fmul(t_wt, idx)
            total = m.fadd(t_vl, total)
        return total
    
    def c_idx(self, idx):
        k = None
        totalniy = 0
        for e in self.dd:
            for t___ in range(self.dd[e]):
                if idx == totalniy:
                    return e
                totalniy += 1
        print "Idx not found (statistikon.c_idx(%i))" % idx
        3/0
