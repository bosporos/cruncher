import mpmath

def productMomentCorrelation(data, heavy = 53):
    # r = sum[(x-X)(y-Y)]/sqrt(sum[(x-X)^2] * sum[(y-Y)^2])
    
    mpmath.mp.dps = heavy
    
    # x
    xdat = [p[0] for p in data]
    # y
    ydat = [p[1] for p in data]

    xbar = mpmath.fdiv(mpmath.mpf(mpmath.fsum(xdat)), mpmath.mpf(len(data)))
    ybar = mpmath.fdiv(mpmath.mpf(mpmath.fsum(ydat)), mpmath.mpf(len(data)))
    
    # x-xbar
    x_zt_line = [mpmath.fsub(x, xbar) for x in xdat]
    # y-ybar
    y_zt_line = [mpmath.fsub(y, ybar) for y in ydat]
    # (x-xbar)(y-ybar)
    head_qe_line = [mpmath.fmul(x_zt_line[n], y_zt_line[n]) for n in range(len(data))]
    summa_head = mpmath.fsum(head_qe_line)
    
    # (x-xbar)^2
    dubs_lefpi_line = [mpmath.power(xzt, 2) for xzt in x_zt_line]
    # (y-ybar)^2
    dubs_ragpi_line = [mpmath.power(yzt, 2) for yzt in y_zt_line]
    
    print "x & y & x - \\bar{x} & y - \\bar{y} & (x-\\bar{x})(y-\\bar{y}) & (x-\\bar{x})^2 & (y-\\bar{y})^2 \\\\"
    for i in range(len(xdat)):
        print "%i & %f & %f & %f & %f & %f & %f \\\\" % (xdat[i],ydat[i],x_zt_line[i],y_zt_line[i],head_qe_line[i],dubs_lefpi_line[i],dubs_ragpi_line[i])
    
    summa_dubleft = mpmath.fsum(dubs_lefpi_line)
    summa_dubright = mpmath.fsum(dubs_ragpi_line)
    prod_dubs_summa = mpmath.fmul(summa_dubleft, summa_dubright)
    prod_daps = mpmath.sqrt(prod_dubs_summa)
    
    print "& & & & %f & %f & %f \\\\" % (summa_head, summa_dubleft, summa_dubright)
    
    finn = mpmath.fdiv(summa_head, prod_daps)
    return finn

CHUNDJIK_JAMAK_DJAH = """
from lib.math.statistika import statistikon as s
ds = [0,1,2,3,4,4,5]
a = s(ds, True)
a.c_median()

from lib.math.statistika import statistikon
ds = {1:9, 2:1, 3:3, 5:3, 6:8, 7:1, 8:3}
a = statistikon(ds)
"""
