import os, json, string
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict
from json.decoder import JSONDecodeError
import time

def indexing(stem : str, filename : str) -> dict:
    #token : file 
    partial_index = defaultdict(list)
    
    for s in stem:
        partial_index[s].append(getFileName(filename))

    return partial_index
    
#getting file name from full path
def getFileName(path):
    return Path(path).stem

#merging two dictionaries
def mergeDict(d1, d2):
    
    #merged_dict = defaultdict(list)
    
    #merging two dicts
    
    for key, value in d2.items():
        if key in d1:
            d1[key] += value
        else:
            d1[key] = value
    #sorting values which is a list object
    

    return d1

#sepearting dictionary into term ranges
def seperateDict(dict):
    a_f, g_l, m_s, t_z = {}, {}, {}, {}

    #splitting indices
    for k, v in dict.items():
        if k[0] >= 'a' and k[0] <= 'f':
            a_f[k] = v
        elif k[0] >= 'g' and k[0] <= 'l':
            g_l[k] = v
        elif k[0] >= 'm' and k[0] <= 's':
            m_s[k] = v
        else:
            t_z[k] = v

    return a_f, g_l, m_s, t_z

#writing report to file
def writeReport(files, file_names):

    #holding stats
    num_of_docs = len(files)
    num_of_tokens = 0
    file_size = 0
    
    #Generate stats report for deliverable
    with open('report.txt', 'w') as file:

        for name in file_names:
            
            #getting data from index
            with open(name, "r+") as f:
                d = json.load(f)
                num_of_tokens += len(d.keys())
                file_size += os.path.getsize(name) / 1024
        
        #actually writing to file now
        file.write("Number of Documents: " + str(num_of_docs) +"\n")
        file.write("Number of Unique Tokens: " + str(num_of_tokens) + "\n")
        file.write("Total Size: " + str(file_size) + " kb\n")
    
# import krovetz
def main():
    try:
        #beginning path
        path  = 'DEV/'

        #getting all file names in order to be read n
        files = [f for f in glob(path + "**/*.json", recursive=True)]
        
        #loop thru every file
        # for each file tokenize, stem token, the create rev index for each file
        ps = PorterStemmer()

        all_file_names = ['a_f.json', 'g_l.json', 'm_s.json', 't_z.json']
        
        # Removing Files if rerunning
        try:
            for f in all_file_names:
                os.remove(f)
        except FileNotFoundError:
            pass
        
        #looping thru each file in DEV path
        for file in files:
            with open(file, 'r') as f:
                print(f.name)
                data = json.load(f)
                content = data['content']

                soup = BeautifulSoup(content, 'lxml')
                # FIXME: 
                text = soup.get_text()

                tokenized = word_tokenize(text)
                #make sure tokens are lowercase
                stemmed = [ps.stem(token.lower(), to_lowercase=True) for token in tokenized if token not in string.punctuation]
                #allows stemming to work with lowercase words
                #stemmed = [ps.stem(s, to_lowercase=True) for s in tokenized]
                #getting partial_index from current html
                partial_inverted_index = indexing(stemmed, file)
                #json_data = json.dumps(partial_inverted_index, indent=2)

                #splitting partial index into 4 term ranges
                sep_dicts = seperateDict(partial_inverted_index)

                #write to those files and update dictionary from file and current index
                for i, current_dict in enumerate(sep_dicts):
                    try:
                        with open(all_file_names[i], 'r') as infile:
                            try:
                                #getting index from file
                                old_index = json.load(infile)
                            except JSONDecodeError:
                                old_index = dict()
                    except FileNotFoundError:
                        old_index = dict()

                    #merging dictionaries
                    merged_dict = mergeDict(old_index, current_dict)
                    with open(all_file_names[i], 'w') as outfile:
                        #dumping dict into json file
                        json.dump(merged_dict, outfile, indent=4)
        #writing report at the end
        writeReport(files, all_file_names)
        print("Program terminated. Tokens have been indexed successfully.")
    #FIXME: The token doesn't look good.        
    except KeyboardInterrupt:
        #Write report if we stop index halfway through
        writeReport(files, all_file_names)


    
        
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Time of execution is: ", (end-start))
