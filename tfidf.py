import math
from collections import defaultdict
from posting import Posting

class TFIDFSearch:
    def __init__(self, index):
        self.index = index
        self.docFreq = {}
        self.idf = {}
        self.scores = {}
        self._compute_tfidf()


    def _compute_tfidf(self):
        for term, posting_list in self.index.items():
            self.docFreq[term] = len(posting_list)
            for posting in posting_list:
                if posting.docID not in self.scores:
                    self.scores[posting.docID] = defaultdict(float)
                self.scores[posting.docID][term] = posting.freq * math.log(len(self.index) / self.docFreq[term])
        for term, freq in self.docFreq.items():
            self.idf[term] = math.log(len(self.index) / freq)

    def cosine_similarity(self, v1, v2):
        res = sum(v1[term] * v2[term] for term in v1 if term in v2)
        v1_norm = math.sqrt(sum(v1[term]**2 for term in v1))
        v2_norm = math.sqrt(sum(v2[term]**2 for term in v2))
        return res / (v1_norm * v2_norm)

    def search(self, query : list):
        query_tfidf = defaultdict(float)
        for term in query:
            try:
                query_tfidf[term] += 1
            except KeyError:
                continue
        for term in query_tfidf:
            try:
                query_tfidf[term] *= self.idf[term]
            except KeyError:
                continue
        scores = []
        for docID, tfidf in self.scores.items():
            similarity = self.cosine_similarity(query_tfidf, tfidf)
            scores.append((similarity, docID))
        scores.sort(reverse=True)
        return scores

if __name__ ==  "__main__":
    #testing
    inverted_index = {
        "brown": [Posting(0, 2), Posting(1, 1), Posting(2, 2), Posting(3, 2), Posting(4, 1), Posting(5, 1)],
        "fox": [Posting(0, 1), Posting(1, 1), Posting(3, 1)],
        "jumped": [Posting(0, 1), Posting(1, 1), Posting(4, 1), Posting(5, 1)],
        "over": [Posting(0, 1), Posting(4, 1), Posting(5, 1)],
        "the": [Posting(0, 3), Posting(1, 2), Posting(2, 1), Posting(3, 2), Posting(4, 4), Posting(5, 4)],
        "quick": [Posting(1, 1), Posting(4, 1), Posting(5, 1)],
        "lazy": [Posting(2, 1)],
        "dog": [Posting(2, 1), Posting(3, 1), Posting(4, 1), Posting(5, 1)]
    }

    search_engine = TFIDFSearch(inverted_index)

    query = ["quick", "dog", "lazy"] 

    results = search_engine.search(query)

    for score, doc_id in results:
        print(f"Document ID {doc_id} scored {score:.2f}")
