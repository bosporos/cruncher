import mpmath

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
        coordinates = list(coordinates)
        cl = len(coordinates)
        if cl != self.space:
            print "matrix: access: Sanity lost: N-Ary Space Dimensionality Not Equal To Arity Of Coordinate"
            quit()
        
        if None in coordinates:
            df = coordinates.count(None)
            iter = df
            # a list of coordinates
            queue = [coordinates]
            while None in queue[0]:
                tqueue = []
                for queued in queue:
                    nindex = queued.index(None)
                    for variation in range(self.dimensions[nindex]):
                        tmp = queued[:]
                        tmp[nindex] = variation
                        tqueue.append(tmp)
                queue = tqueue
            out = dict()
            for coordinatePoint in queue:
                out[tuple(coordinatePoint)] = self.data[tuple(coordinatePoint)]
            return out
        else:
            return self.data[tuple(coordinates)]
    
    def set(self, coordinates, nv):
        coordinates = list(coordinates)
        cl = len(coordinates)
        if cl != self.space:
            print "matrix: set: Sanity lost: N-Ary Space Dimensionality Not Equal To Arity Of Coordinate"
            quit()
        if None in coordinates:
            print "You can't pass wild coordinates to matrix::set"
            quit()
        self.data[tuple(coordinates)] = nv
    
    def construct_(self, dimensions, elements):
        dimensions = list(dimensions) 
        dict = {}
        dim = dimensions.pop()
        if len(dimensions) == 0:
            for element in range(dim):
                ltmp = (elements + [element])
                ltmp.reverse()
                dict[tuple(ltmp)] = 0
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
    
    
