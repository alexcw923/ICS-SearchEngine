import numpy as np
from posting import Posting
class InstanceMatrix:
    def __init__(self, index : dict, map : dict):
        self.matrix = np.zeros((len(index), len(map)))
        self.queries = np.fromiter(index.keys(), dtype='object')
        self._setMatrix(index)


    #initialize matrix
    def _setMatrix(self, index : dict) -> None:
        """Set the matrix to 1 if the query is in the document.

        Args:
            index (dict): index of the documents
        """
        for query, ls in index.items():
            #print(index)
            for p in ls:
                self.matrix[self.queries == query, p.docID] = 1
                
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
    
class InvertedIndex:
    def __init__(self, index):
        self.index = index
        self.documents = set([pair.docID for term in index.values() for pair in term])
        
    def checkQuery(self, query):
        """Check which documents contain all the words in the query.

        Args:
            query (list): list of words

        Returns:
            list: document ids that contain all the words in the query
        """
        query_indices = [set([pair.docID for pair in self.index.get(q, [])]) for q in query]
        docs = set.intersection(*query_indices)
        return list(docs)

# class InvertedIndex:
#     def __init__(self, index):
#         self.index = index
#         self.documents = set()
#         for postings_list in self.index.values():
#             for postings in postings_list:
#                 self.documents.add(postings.docID)
#         self.documents = sorted(list(self.documents))
#         self.matrix = self._setMatrix()

#     def _setMatrix(self) -> np.ndarray:
#         """Set the sparse matrix to 1 if the document contains the term.

#         Returns:
#             np.ndarray: sparse matrix
#         """
#         matrix = np.zeros((len(self.index), len(self.documents)), dtype=np.int8)
#         for i, (term, postings_list) in enumerate(self.index.items()):
#             for postings in postings_list:
#                 matrix[i, postings.docID] = 1
#         return matrix

#     def checkQuery(self, query):
#         """Check which documents contain all the words in the query.

#         Args:
#             query (list): list of words

#         Returns:
#             list: document ids that contain all the words in the query
#         """
#         query_indices = [i for i, term in enumerate(self.index.keys()) if term in query]
#         query_matrix = self.matrix[query_indices, :]
#         docs = np.where(np.all(query_matrix == 1, axis=0))[0]
#         return docs.tolist()
        
        
    
    
if __name__ == '__main__':
    index = {"caesar": [Posting(0, 1), Posting(2, 3)], "julius": [Posting(0,2), Posting(2, 3)], "jason": [Posting(0, 3), Posting(3,2)]}
    map = {0:"caesar.txt", 1:"julius.txt", 2:"jason.txt", 3:"julius2.txt"}
    # im = InstanceMatrix(index, map)
    # '''
    #             0 1 2 3
    # caesar    [[1 0 1 0], 
    # julius     [1 0 1 0], 
    # jason      [1 0 0 1]]
    # '''
    # im.checkQuery(["caesar", "julius", "jason"]) #[0]
    # im.checkQuery(["julius", "jason"])           #[0]
    # im.checkQuery(["julius", "caesar"])          #[0, 2]
    
    # user_input = input("Enter a query: ")
    # user_input = user_input.split()
    
    # im2 = InstanceMatrix(index, map)
    # print(im2.checkQuery(user_input))
    
    n = InvertedIndex(index)
    
    print(n.checkQuery(["julius", "jason"])) 
    print(n.checkQuery(["julius", "caesar"]))