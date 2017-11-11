import math
from decimal import *
import mpmath as mp

# F(k, a) = g(k/2, a/2) / G(k/2)
def F(k, x):
    upper = g(k/2, x/2)
    lower = G1(k/2)
    print "lower gamma: %f" % upper
    print "upper gamma: %f" % lower
    return upper / lower

# WORKING
def G1(s):
    return math.factorial(s - 1)

# WORKING
def G(s, x):
    if int(s) != s:
        print "Not yet possible: Cannot do upper incomplete gamma function for s where not positive integer"
        quit()
    if s <= 0:
        print "Not yet possible: Cannot do upper incomplete gamma function for s<=0"
        quit()
    base = G1(s - 1)
    epow = math.e ** -x
    summus = sum([(x ** k)/math.factorial(k) for k in range(s)])
    return base * epow * summus

# WORKING
def g(s, x):
    return G1(s) - G(s, x)

###
### Using MPMATH
###

# F(k, a) = g(k/2, a/2) / G(k/2)
def F_(k, x):
#    upper = g_(mp.fdiv(k,2), mp.fdiv(x,2))
#    lower = G1_(mp.fdiv(k,2))
    upper = mp.gammainc(mp.fdiv(k,2),0,mp.fdiv(x,2))
    lower = mp.gamma(mp.fdiv(k,2))
    print "lower gamma: %f" % upper
    print "upper gamma: %f" % lower
    return mp.fdiv(upper, lower)

# WORKING
def G1_(s):
    return mp.factorial(mp.fsub(s,1))

# WORKING
def G_(s, x):
    if int(s) != s:
        print "Not yet possible: Cannot do upper incomplete gamma function for s where not positive integer"
        quit()
    if s <= 0:
        print "Not yet possible: Cannot do upper incomplete gamma function for s<=0"
        quit()
    base = G1_(mp.fsub(s, 1))
    epow = mp.power(mp.e, mp.fneg(x))
    summus = mp.fsum([mp.power(x,k)/mp.factorial(k) for k in range(s)])
    return mp.fprod([base, epow, summus])

# WORKING
def g_(s, x):
    return mp.fsub(G1_(s), G_(s, x))


####
#### HEAVY DUTY FUNCTIONS
####

def HeavyF(k, x, sigfigs = 64000):
    with localcontext() as ctx:
        ctx.prec = sigfigs
        k = Decimal(k)
        x = Decimal(x)
        upper = Heavyg(k/2, x/2, sigfigs)
        lower = HeavyG1(k/2, sigfigs)
        return Decimal(upper / lower)

# WORKING
def HeavyG1(s, sigfigs = 64000):
    with localcontext() as ctx:
        s = Decimal(s)
        ctx.prec = sigfigs
        return Decimal(math.factorial(s - 1))

# WORKING
def HeavyG(s, x, sigfigs = 64000):
    if int(s) != s:
        print "Not yet possible: Cannot do upper incomplete gamma function for s where not positive integer"
        quit()
    if s <= 0:
        print "Not yet possible: Cannot do upper incomplete gamma function for s<=0"
        quit()
    with localcontext() as ctx:
        ctx.prec = sigfigs
        s = Decimal(s)
        x = Decimal(x)
        base = HeavyG1(s - 1, sigfigs)
        epow = Decimal(math.e ** -float(x))
#        summus = sum([(ctx.power(x, k))/math.factorial(k) for k in range(s)])
        summus = 0
        for k in range(s):
            print k
            summus += (ctx.power(x, k))/math.factorial(k)
        return base * epow * summus

# WORKING
def Heavyg(s, x, sigfigs = 64000):
    with localcontext() as ctx:
        ctx.prec = sigfigs
        return HeavyG1(s, sigfigs) - HeavyG(s, x, sigfigs)

###
### P-VALUE STUFF
###

def PValueForF(F):
    return 1 - F

def HeavyPValueForF(F, sigfigs = 64000):
    with localcontext() as ctx:
        ctx.prec = sigfigs
        return 1 - F

def PValueForF_(F):
    return mp.fsub(1, F)
