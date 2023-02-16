import os, json, string
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

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
            
    
        
if __name__ == "__main__":
    main()