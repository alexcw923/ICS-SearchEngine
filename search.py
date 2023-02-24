import json

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from matrix import InstanceMatrix

QUERY_SEP = ";"
NUM_SEARCH_RESULTS = 5

def search(args):
    queries = args.query.split(QUERY_SEP)

    with open("invertedIndex.json") as index:
        print("loading inverted index")
        index = json.load(index)

    with open("mapping.json") as mapFile:
        print("mapping file")
        mapping = json.load(mapFile)

    newIndex = {}

    ps = PorterStemmer()
    for q in queries:
        tokenized = word_tokenize(q)
        #make sure tokens are lowercase
        stemmed = [ps.stem(token.lower()) for token in tokenized if not token.isnumeric()]
        for tok in stemmed:
            newIndex[tok] = index[tok]

    # im = InstanceMatrix(index, mapping)
    im = InstanceMatrix(newIndex, mapping)
    print("finished")
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
            with open(mapping[str(j)]) as file:
                data = json.load(file)
                urls.append(data["url"])

        stats.append(urls)

    for i in range (len(queries)):
        print(f'Search results for "{queries[i]}"')
        for result_number, j in enumerate(range(NUM_SEARCH_RESULTS), 1):
            print(f"{result_number}. {stats[i][j]}")
        print()
