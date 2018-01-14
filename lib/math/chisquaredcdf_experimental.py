import mpmath

# From: @DSM
# From: https://stackoverflow.com/questions/6298105/precision-of-cdf-in-scipy-stats

def pdf(x,k):
    x,k = mpmath.mpf(x), mpmath.mpf(k)
    if x < 0: return 0
    return 1/(2**(k/2) * mpmath.gamma(k/2)) * (x**(k/2-1)) * mpmath.exp(-x/2)

def cdf(x,k): 
    x,k = mpmath.mpf(x), mpmath.mpf(k)
    return mpmath.gammainc(k/2, 0, x/2, regularized=True)

def cdf_via_quad(s,k):
    return mpmath.quad(lambda x: pdf(x,k), [0, s])
