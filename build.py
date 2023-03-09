import os, json
import sys

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from bs4 import BeautifulSoup

from collections import defaultdict
from posting import Posting, PostingDecoder, PostingEncoder

FILE_ALPH = ['a_f', 'g_l', 'm_s', 't_z', 'spec']


def build(args):

    ROOT_DIR = 'DEV'
    ps = PorterStemmer()
    
    mapped_files = {}
    n = 0

    # fp = []
    for i in FILE_ALPH:
        with open(f"{i}.json", "w+") as file:
            json.dump({},file, cls=PostingEncoder)

    try:
        
        for dir in os.listdir(ROOT_DIR):
            directory = os.path.join(ROOT_DIR, dir)
            partial_index = defaultdict(list)
            for f in os.listdir(directory):

                cur_file = os.path.join(directory, f)

                with open(cur_file, 'r') as file:
                    # Load HTML data from json file
                    data = json.load(file)
                    content = data['content']

                    # Parse HTML
                    soup = BeautifulSoup(content, 'lxml')
                    text = soup.get_text()

                    # Tokenize, stem with NLTK
                    # Stemming with only lower case tokens + other filters
                    tokenized = word_tokenize(text)
                    stemmed = [ps.stem(token.lower()) for token in tokenized if not token.isnumeric()]

                    # Get frequency of each token in stemmed list
                    token_counts = indexing(stemmed)

                    # Insert into inverted index
                    for token, freq in token_counts.items():
                        post = Posting(n,freq)
                        partial_index[token].append(post)

                    # Map file to enumerated index and store in file
                    #cur_file
                    mapped_files[n] = data['url']
                    
                    n = n + 1

            #seperating partial dict into term ranges
            a_f, g_l, m_s, t_z, spec = seperateDict(partial_index)

            #writing each term dict into file
            for i, part_index in enumerate([a_f, g_l, m_s, t_z, spec]):
                sortAndWriteToDisk(part_index,FILE_ALPH[i])


    except KeyboardInterrupt:
        with open("mapping.json", 'w+') as mappings:
            #print(mapped_files)
            json.dump(mapped_files, mappings)
        # with open("invertedIndex.json", 'w+') as index:
        #     #print(inverted_index)
        #     json.dump(partial_index, index, cls=PostingEncoder, indent=2)

    
    # with open("mapping.json", 'w') as mappings:
    #     json.dump(mapped_files, mappings)
    # with open("invertedIndex.json", 'w') as index:
    #     json.dump(inverted_index, index, indent=4)
    # writeM1(inverted_index, n)


def indexing(stem : list) -> dict:
    #token : file
    token_counts = defaultdict(int)
    partial_index = dict()

    for s in stem:
        token_counts[s] += 1
    '''
    for token, count in token_counts.items():
        partial_index[token] = [filename + "," + str(count)]
    '''
    return token_counts

def writeM1(inverted_index, numFiles):
    with open('report.txt', 'w') as file:
        file.write("Number of Documents: " + str(numFiles) + "\n")
        file.write("Number of Unique Tokens: " + str(len(inverted_index)) + "\n")
        file.write("Total Size: " + str(sys.getsizeof(inverted_index) / 1024) + " kb\n")
        
#sepearting dictionary into term ranges
def seperateDict(dict):

    a_f, g_l, m_s, t_z, spec = {}, {}, {}, {}, {}
    #splitting indices
    for key, val in dict.items():
        if key[0] >= 'a' and key[0] <= 'f':
            a_f[key] = val
        elif key[0] >= 'g' and key[0] <= 'l':
            g_l[key] = val
        elif key[0] >= 'm' and key[0] <= 's':
            m_s[key] = val
        elif key[0] >= 't' and key[0] <= 'z':
            t_z[key] = val
        else:
            spec[key] = val

    return a_f, g_l, m_s, t_z, spec

def sortAndWriteToDisk(partial_index, fn):
    try:
        with open(f"{fn}.json" , 'r') as old_file:
            old_index = json.load(old_file, cls=PostingDecoder)
    except FileNotFoundError:
        old_index = dict()

    for token, postList in partial_index.items():
        if token in old_index:
            old_index[token].extend(postList)
        else:
            old_index[token] = postList

    with open(f"{fn}.json", 'w') as new_file:
        json.dump( old_index, new_file, cls=PostingEncoder)


'''
#sepearting dictionary into term ranges
def seperateDict(dict):

    #a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, spec = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    a_f, g_l, m_s, t_z, spec = {}, {}, {}, {}, {}
    #splitting indices
    for key, val in dict.items():
        if key[0] >= 'a' and key[0] <= 'f':
            a_f[key] = val
        elif key[0] >= 'g' and key[0] <= 'l':
            g_l[key] = val
        elif key[0] >= 'm' and key[0] <= 's':
            m_s[key] = val
        elif key[0] >= 't' and key[0] <= 'z':
            t_z[key] = val
        else:
            spec[key] = val

    return a_f, g_l, m_s, t_z, spec

def sortAndWriteToDisk(partial_index, filename):
    filename = f"{filename}.json"
    # for key in partial_index:
    #     partial_index[key].sort()

    with open(filename, 'w') as json_file:
        json.dump(partial_index, json_file, cls=Js)'''