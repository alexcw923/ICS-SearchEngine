import numpy as np

class InstanceMatrix:
    def __init__(self, index : dict, map : dict):
        
        self.matrix = np.zeros((len(index), len(map)))
        self.queries = np.array(list(index.keys()))
        
    # def createMatrix(self, index):
    #     matrix = np.array((len(index)))
    
    
    
    
if __name__ == '__main__':
    index = {"caesar": [[0, 1], [2, 3]], "Julius": [[0,2], [2, 3]], "Jason": [[0, 3], [2, 3]]}
    map = {"caesar.txt": 0, "julius.txt": 1, "jason.txt": 2, "julius2.txt": 3}
    im = InstanceMatrix(index, map)
    print(im.matrix.shape)
    print(im.matrix)
    print(im.queries.shape)
    print(im.queries)
    