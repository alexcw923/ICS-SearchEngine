from json import JSONEncoder, JSONDecoder
import json
from collections import defaultdict

class Posting():
    def __init__(self, docID, freq):
        #dict.__init__(self, docID = docID,freq = freq)
        #url name
        self.docID = docID
        self.freq = freq
        # self.tfIdf = tfIdf
        
        #frequency of the number of pages appeared
        # self.importantWord = False
        #W x,y = term frequecy X log(total number of document/number of document containing x)
    #updating freqency
    def __str__(self):
        return f"{self.docID},{self.freq}"
    
    def __repr__(self) -> str:
        return f"Posting<DocID:{self.docID}, Freq:{self.freq}>"
    
    def updateFreq(self):
        self.freq += 1
    
    def getFreq(self):
        return self.freq
    #FIXME backwardfs compat with search if key = 
    # def __getitem__(self, key):
    #     if key==0:
    #         return self.docID

class PostingEncoder(JSONEncoder):
    def default(self, obj : Posting):
        return f"{obj.docID},{obj.freq}"

class PostingDecoder(JSONDecoder):
    def decode(self, json_str):
        data = super().decode(json_str)
        postings_dict = {}
        for key, value in data.items():
            postings_dict[key] = []
            for posting_str in value:
                docID, freq = posting_str.split(',')
                postings_dict[key].append(Posting(int(docID), float(freq)))
        return postings_dict
    

if __name__ == '__main__':
    index = defaultdict(list)
    index['a'].append(Posting(0,1))
    index['a'].append(Posting(1,1))
    dump = json.dumps(index, cls=PostingEncoder)
    load = json.loads(dump, cls=PostingDecoder)
    print(type(load['a'][0]))
