import matplotlib.pyplot as plt

class RG_SCATTER:
    def __init__(self, data, c, g):
        self.xkcd = [p[0] for p in data]
        self.ykcd = [p[1] for p in data]
        plt.plot(self.xkcd, self.ykcd, c)
        plt.axis([-100,max(self.xkcd),0.0,1.0])
        plt.xlabel("Number of respondents in country")
        plt.ylabel("Proportion of respondents who are %s" % g)
        plt.show()
