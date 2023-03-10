import json, ijson
import time
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from matrix import InstanceMatrix, InvertedIndex
from posting import PostingDecoder, PickleDecoder

QUERY_SEP = ";"
NUM_SEARCH_RESULTS = 5
FILE_ALPH = ['a_f', 'g_l', 'm_s', 't_z', 'spec']

def search(args):
    queries = args.query.split(QUERY_SEP)

    # with open("invertedIndex.json") as index:
    #     print("loading inverted index")
    #     index = json.load(index, cls=PostingDecoder)
        #print(index)
    with open("mapping.json") as mapFile:
        #print("mapping file")
        mapping = json.load(mapFile)

    newIndex = {}
        
    ps = PorterStemmer()
    for q in queries:
        #print(q)
        tokenized = word_tokenize(q)
        #make sure tokens are lowercase
        stemmed = [ps.stem(token.lower()) for token in tokenized if not token.isnumeric()]
        for tok in stemmed:
            if tok[0] >= 'a' and tok[0] <= 'f':
                to_open = FILE_ALPH[0]
            elif tok[0] >= 'g' and tok[0] <= 'l':
                to_open = FILE_ALPH[1]
            elif tok[0] >= 'm' and tok[0] <= 's':
                to_open = FILE_ALPH[2]
            elif tok[0] >= 't' and tok[0] <= 'z':
                to_open = FILE_ALPH[3]
            else:
                to_open = FILE_ALPH[4]

            with open(f"{to_open}.pkl", 'r+b') as file:
                # start = time.time()
                decoder = PickleDecoder(file)
                index = decoder.load()
                # index = json.load(file, cls=PostingDecoder)
                #index = ijson.items(file, f"{q}.item")
                newIndex[tok] = index[tok]
                # print('Load Time', time.time()-start)
            
    # im = InstanceMatrix(index, mapping)
    # im = InstanceMatrix(newIndex, mapping)
    im = InvertedIndex(newIndex)
    #print("finished")
    docs = []
    for  q in queries:
        tokenized = word_tokenize(q)
        #make sure tokens are lowercase
        stemmed = [ps.stem(token.lower()) for token in tokenized if not token.isnumeric()]
        temp = im.checkQuery(stemmed)

        docs.append(temp[0:5])

    stats = []

    # Printing NUM_SEARCH_RESULTS for each query
    for i in docs:
        urls = []
        
        for j in i:
            with open('mapping.json') as file:
                data = json.load(file)
                urls.append(data[str(j)])

        stats.append(urls)

    for i in range (len(queries)):
        print(f'Search results for "{queries[i]}"')
        for result_number, j in enumerate(range(NUM_SEARCH_RESULTS), 1):
            print(f"{result_number}. {stats[i][j]}")
        print()

