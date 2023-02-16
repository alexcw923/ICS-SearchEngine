import os, json, string
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict

def indexing(stem : str, filename : str) -> dict:
    #token : file 
    partial_index = defaultdict(list)
    
    for s in stem:
        partial_index[s].append(getFileName(filename))

    return partial_index
    
#getting file name from full path
def getFileName(path):
    return Path(path).stem


# import krovetz
def main():
    
    #beginning path
    path  = 'DEV/'

    #getting all files to be read

    files = [f for f in glob(path + "**/*.json", recursive=True)]
    
    #loop thru every file
    # for each file tokenize, stem token, the create rev index for each file
    ps = PorterStemmer()
    
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            content = data['content']

            soup = BeautifulSoup(content, 'lxml')
            # FIXME: 
            text = soup.get_text()

            # punct_set =set(['!', '"', '#', '$' , '%', '&', "'", '(', ')','*', '+', ',', '-', '.', '/' , 
            #                 ':' , ';' , '<', '=', '>' '?','@','[','\\',']','^','_','`','{','|','}','~', '-'])

            tokenized = word_tokenize(text)
            tokenized = [token for token in tokenized if token not in string.punctuation]
            stemmed = [ps.stem(s) for s in tokenized]

            partial_inverted_index = indexing(stemmed, file)
            json_data = json.dumps(partial_inverted_index, indent=2)
            print(json_data)
            
            #write into files
            #with open(f'', 'w') as 
            #sorting with alphabet 4 files ( 2 files with 6 letters and 2 files with 7 letters)
    
        
if __name__ == "__main__":
    main()