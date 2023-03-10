import json, time, mmap
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from posting import PostingDecoder
from tfidf import TFIDFSearch
QUERY_SEP = ";"
NUM_SEARCH_RESULTS = 5
FILE_ALPH = ['a_f', 'g_l', 'm_s', 't_z', 'spec']

MAPPING = "mapping.json"

def _preload_mapping():
    mapping = None
    with open(MAPPING) as file:
        mapping = json.load(file)

    return mapping

def _preload_positional_json():
    positional_file_names = [f"{f}.json" for f in FILE_ALPH]
    positional_file_pointers = [open(f) for f in positional_file_names]

    positional_json = {FILE_ALPH[i]:json.load(fp) for i, fp in enumerate(positional_file_pointers)}

    return positional_json


def preload():
    return {"mapping": _preload_mapping(), "positional": _preload_positional_json()}

def print_search_results(queries, search_results):
    assert len(queries) == len(search_results)
    stats = []
    # Printing NUM_SEARCH_RESULTS for each query
    for i in search_results:
        urls = []

        for j in i[0:NUM_SEARCH_RESULTS]:
            with open('mapping.json') as file:
                data = json.load(file)
                urls.append(data[str(j[1])])

        stats.append(urls)
    
    for i in range(len(search_results)):
        print(f'Search results for "{queries[i]}"')
        for result_number, j in enumerate(range(min(NUM_SEARCH_RESULTS, len(search_results[i]))), 1):
            print(f"{result_number}. {stats[i][j]}")
        print()



def search(args):
    queries = args.query.split(QUERY_SEP)
    search_results = get_search_results(queries)
    print_search_results(queries, search_results)
    


def get_search_results(queries: list):
    docs = []

    newIndex = {}

    ps = PorterStemmer()
    for q in queries:
        #print(q)
        tokenized = word_tokenize(q)
        #make sure tokens are lowercase
        stemmed = [ps.stem(token.lower()) for token in tokenized if not token.isnumeric()]
        no_search_result = []
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

            with open(f"{to_open}_pos.json", 'rb') as posFile:
                
                posIndex = json.load(posFile)
                #json_string = mmap.mmap(posFile.fileno(), 0, access=mmap.ACCESS_READ)
                #getting possistion of toke
                #json_string = json_string.read().decode('utf-8')
                #posIndex = json.loads(json_string)
                try:
                    pos = posIndex[tok]
                except KeyError:
                    no_search_result.append(tok)
                    continue
                with open(f"{to_open}.json", 'r+b') as f:
                    mapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                    mapped_file.seek(pos)
                    #f.seek(pos)
                    posting = mapped_file.readline().decode("utf-8").strip()
                    posting = posting[:posting.find(']')+1]

                    d = "{" + '"' + posting +"}"

                    #d = '{{"{}": {}}}'.format(tok, posting)
                    dumping = json.loads(d, cls=PostingDecoder)
                    
                    for token, postList in dumping.items():
                        newIndex[token] = postList
                    
    tfidf = TFIDFSearch(newIndex)
    for q in queries:
        tokenized = word_tokenize(q)
        #make sure tokens are lowercase
        stemmed = [ps.stem(token.lower()) for token in tokenized if not token.isnumeric()]
        docs.append(tfidf.search(stemmed))
    
    if len(no_search_result) != 0:
        print("No Search Result for the query: ", end='')
        for q in no_search_result:
            print(f"{q} ", end ="")
        print()
    return docs