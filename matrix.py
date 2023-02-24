import numpy as np

class InstanceMatrix:
    def __init__(self, index : dict, map : dict):
        
        self.matrix = np.zeros((len(index), len(map)))
        self.queries = np.array(list(index.keys()))
        self._setMatrix(index)
        
    #initialize matrix
    def _setMatrix(self, index : dict) -> None:
        """Set the matrix to 1 if the query is in the document.

        Args:
            index (dict): index of the documents
        """
        for query, ls in index.items():
            for id in ls:
                self.matrix[self.queries == query, id[0]] = 1
                
    def checkQuery(self, query :list) -> list:
        """Check which documents contain all the words in the query.

        Args:
            query (list): list of words

        Returns:
            list: document ids that contain all the words in the query
        """
        for q in query:
            if q not in self.queries:
                return []
        query_indices = [np.where(self.queries == q)[0][0] for q in query]
        
        docs = np.where(np.all(self.matrix[query_indices, :] == 1, axis=0))[0]
        
        return docs
        
        
    
    
if __name__ == '__main__':
    index = {"caesar": [[0, 1], [2, 3]], "julius": [[0,2], [2, 3]], "jason": [[0, 3], [3,2]]}
    map = {0:"caesar.txt", 1:"julius.txt", 2:"jason.txt", 3:"julius2.txt"}
    im = InstanceMatrix(index, map)
    print(im.matrix.shape)
    print(im.queries.shape)
    '''
                0 1 2 3
    caesar    [[1 0 1 0], 
    julius     [1 0 1 0], 
    jason      [1 0 0 1]]
    '''
    im.checkQuery(["caesar", "julius", "jason"]) #[0]
    im.checkQuery(["julius", "jason"])           #[0]
    im.checkQuery(["julius", "caesar"])          #[0, 2]
    
    