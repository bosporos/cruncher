import mpmath
from chisquaredcdf_experimental import cdf

# RETURN False = No association
# RETURN True = Association
def ChiSquaredTest(df, chisquaredcalc, heavy = 53):
    mpmath.mp.dps = heavy
    cdfv = cdf(k=df, x=chisquaredcalc)
    pval = mpmath.fsub(1, cdfv)
    return pval

if __name__ == "__main__":
    # Works
    print ChiSquaredTest(df=4, chisquaredcalc=51.6, significance=0.05, heavy = 10000)
