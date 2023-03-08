import os, json, string
import sys

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from bs4 import BeautifulSoup

from collections import defaultdict
import posting

def build(args):
    ROOT_DIR = 'DEV'
    ps = PorterStemmer()
    inverted_index = defaultdict(list)
    mapped_files = {}
    n = 0
    for dir in os.listdir(ROOT_DIR):
        directory = os.path.join(ROOT_DIR, dir)

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
                    inverted_index[token].append([n, freq])

                # Map file to enumerated index and store in file
                mapped_files[n] = cur_file
                n = n + 1

    with open("mapping.json", 'w') as mappings:
        json.dump(mapped_files, mappings)
    with open("invertedIndex.json", 'w') as index:
        json.dump(inverted_index, index, indent=4)
    writeM1(inverted_index, n)


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
