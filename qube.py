class matrix:
    def __init__(self, dimensions):
        self.dimensions = list(dimensions)
        self.space = len(dimensions)
        self.data = self.constructNDimensionalObject(dimensions)
    
    def constructNDimensionalObject(self, dimensions):
        return self.construct_(dimensions, [])
        
    def access_pt(self, coordinates):
        return self.data[coordinates]
    
    def access(self, coordinates):
        cl = len(coordinates)
        if cl != self.space:
            print "Sanity lost: N-Ary Space Dimensionality Not Equal To Arity Of Coordinate"
            quit()
    
    def construct_(self, dimensions, elements):
        dimensions = list(dimensions) 
        dict = {}
        dim = dimensions.pop()
        if len(dimensions) == 0:
            for element in range(dim):
                dict[tuple(elements + [element])] = 0
        else:
            for element in range(dim):
                tmp = self.construct_(dimensions, elements + [element])
                dict.update(tmp)
        return dict
    
    def degreesOfFreedom(self):
        df = 1
        for dim in self.dimensions:
            df = df * (dim - 1)
        return df
    
    
