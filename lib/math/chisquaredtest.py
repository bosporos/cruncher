import math
from decimal import *

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
        epow = ctx.power(Decimal(math.e), -x)
        summus = sum([(ctx.power(x, k))/math.factorial(k) for k in range(s)])
        return base * epow * summus

# WORKING
def Heavyg(s, x, sigfigs = 64000):
    with localcontext() as ctx:
        ctx.prec = sigfigs
        return HeavyG1(s, sigfigs) - HeavyG(s, x, sigfigs)

def PValueForF(F):
    return 1 - F

def HeavyPValueForF(F, sigfigs = 64000):
    with localcontext() as ctx:
        ctx.prec = sigfigs
        return 1 - F

# RETURN False = No association
# RETURN True = Association
def ChiSquaredTest(df, chisquaredcalc, significance = 0.05, heavy = False, sigfigs = 64000):
    if heavy:
        f = HeavyF(k=df, x=chisquaredcalc, sigfigs = sigfigs)
        p = HeavyPValueForF(f, sigfigs = sigfigs)
        with localcontext() as ctx:
            ctx.prec = 64000
            if p < significance:
                return True
            else:
                return False
    else:
        f = F(k=df, x=chisquaredcalc)
        p = PValueForF(f)
        if p < significance:
            return True
        else:
            return False

if __name__ == "__main__":
    print ChiSquaredTest(df=4, chisquaredcalc=51.6, significance=0.05, heavy=False)
