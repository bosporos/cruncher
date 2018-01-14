import mpmath
import math
import matplotlib.pyplot as plt

from lib.matrix import matrix
from ..math.correlaza import productMomentCorrelation
from ..math.statistika import statistikon
from ..dbl.scatter import RG_SCATTER

class RG_rp:
    def __init__(self, data, vp, debug = False):
        # point = number, {m/f/o}
        self.points = {}
        for datum in data:
            _RC = datum['Country']
            if _RC not in self.points:
                self.points[_RC] = {'number':0,'genders':{'Male':0,'Female':0,'Other':0}}
            self.points[_RC]['number'] = self.points[_RC]['number'] + 1
            _G = vp.resolvePartialSplinter(datum['Gender'].split('; '), 'm/f/o')
            self.points[_RC]['genders'][_G] = self.points[_RC]['genders'][_G] + 1
#        print self.points
    
    def scatter(self, g_crosswise, restrictForTotalRespondentsIsGreaterThan = 0):
        # Correlation between total and male/total, female/total, and other/total
        # Thus, x3
        scatter = []
        for country in self.points:
            p_ = self.points[country]
            t_pt_x = p_['number']
            if t_pt_x > restrictForTotalRespondentsIsGreaterThan:
                t_pt_yc_s = sum(p_['genders'].values())
                t_pt_ys_n = p_['genders'][g_crosswise]
                # t_pt_y E [0,1], where t_pt_y is the percent chance that a randomly
                # selected person from that country will be of a given gender
                t_pt_y = mpmath.fdiv(t_pt_ys_n, t_pt_yc_s)
                pt = (t_pt_x, t_pt_y)
                # Addendum Criticus
                scatter.append(pt)
        return scatter

def RG_scatterdump(scatter, g):
    print "Respondent/Gender (Gender=%s)" % g
    correlation = productMomentCorrelation(scatter)
    print "Correlation:", correlation
#    print "Scatterplot:"
#    sp = RG_SCATTER(scatter, c = 'ro', g = g)

def RG_perform_dump_statistikon(rp):
    print "# Of Respondents/Country"
    print "# Of Data Points: %i" % len(rp.points)
    # Dict -> Unweighted list
    dds_g = {}
    for country in rp.points:
        dds_g[country] = rp.points[country]['number']
    stat = statistikon(list(dds_g.values()), unweighted = True)
    RG_statistikon_dump("Respondents/Country", stat)

def RG_statistikon_dump(scriptus, statistik):
    print "Total # Of %s: %f" % (scriptus, statistik.c_sum())
    print "Mean # Of %s: %f" % (scriptus, statistik.c_mean())
    print "Median # Of %s: %f" % (scriptus, statistik.c_median())
    print "Mode # Of %s: %s" % (scriptus, statistik.c_mode())
    print "Min/Max (C-Range) Of %s: (%f,%f)" % (scriptus, statistik.c_range()[0], statistik.c_range()[1])
    print "Standard Deviation Of %s: %f" % (scriptus, statistik.c_stdev())

def RG_perform(data, vp):
    rp = RG_rp(data, vp)
    deg = 0
#    RG_scatterdump(rp.scatter('Male', deg), 'Male')
#    RG_scatterdump(rp.scatter('Other', deg), 'Other')
    RG_scatterdump(rp.scatter('Female', deg), 'Female')
#    RG_correlation_cut_gradient(rp, H=100)
#    RG_perform_dump_statistikon(rp)

def RG_correlation_cut_gradient(rp, H):
    m_correlations = []
    f_correlations = []
    o_correlations = []
    for deg in range(H+1):
        m_correlations.append(productMomentCorrelation(rp.scatter('Male', deg)))
        f_correlations.append(productMomentCorrelation(rp.scatter('Female', deg)))
        o_correlations.append(productMomentCorrelation(rp.scatter('Other', deg)))
    plt.plot(range(H+1), m_correlations, 'r-')
    plt.plot(range(H+1), f_correlations, 'b-')
    plt.plot(range(H+1), o_correlations, 'g-')
    plt.axis([0,H,-1,1])
    plt.xlabel("Number Of Respondents Per Country Below Which Data Has Been Excluded")
    plt.ylabel("Pearson's Product Moment Correlation For Resulting Data Set")
    plt.show()
    C=int(math.ceil(H/2)) + 1
    for deg in range(C):
        print "%i & %f & %f & %f &" % (deg+1, m_correlations[deg], f_correlations[deg], o_correlations[deg]),
        if (deg+C) > H:
            print "& & & \\\\"
        else:
            print "%i & %f & %f & %f \\\\" % (deg+C+1, m_correlations[deg+C], f_correlations[deg+C], o_correlations[deg+C])
