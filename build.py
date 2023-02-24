import os, json, string
import sys

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from bs4 import BeautifulSoup

from collections import defaultdict

def build(args):
    ROOT_DIR = 'DEV'
    ps = PorterStemmer()
    inverted_index = defaultdict(list)
    mapped_files = {}
    n = 0

    for dir in os.listdir(ROOT_DIR):
        directory = os.path.join(ROOT_DIR, dir)
        for f in os.listdir(directory):
            n = n + 1
            cur_file = os.path.join(directory, f)
            print(cur_file)
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

                print("Getting frequency of each token in stemmed list")
                token_counts = indexing(stemmed)
                print("Inserting into inverted index")
                for token, freq in token_counts.items():
                    inverted_index[token].append([n, freq])
                mapped_files[n] = cur_file

    # docID : file
    with open("mapping.json", 'w') as mappings:
        json.dump(mapped_files, mappings)


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

