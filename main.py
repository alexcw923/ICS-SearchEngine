import os, json, string
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict
from json.decoder import JSONDecodeError
import posting
import time

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
    
#getting file name from full path
def getFileName(path):
    return Path(path).stem

#merging two dictionaries
#dict1 should be full index, dict2 is partial 
#dict1 value is list of strings, dict2 value is string
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
    
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, spec = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

    #splitting indices
    for key, val in dict.items():
        if key[0] == 'a':
            a[key] = val
        elif key[0] == 'b':
            b[key] = val
        elif key[0] == 'c':
            c[key] = val
        elif key[0] == 'd':
            d[key] = val
        elif key[0] == 'e':
            e[key] = val
        elif key[0] == 'f':
            f[key] = val
        elif key[0] == 'g':
            g[key] = val
        elif key[0] == 'h':
            h[key] = val
        elif key[0] == 'i':
            i[key] = val
        elif key[0] == 'j':
            j[key] = val
        elif key[0] == 'k':
            k[key] = val
        elif key[0] == 'l':
            l[key] = val
        elif key[0] == 'm':
            m[key] = val
        elif key[0] == 'n':
            n[key] = val
        elif key[0] == 'o':
            o[key] = val
        elif key[0] == 'p':
            p[key] = val
        elif key[0] == 'q':
            q[key] = val
        elif key[0] == 'r':
            r[key] = val
        elif key[0] == 's':
            s[key] = val
        elif key[0] == 't':
            t[key] = val
        elif key[0] == 'u':
            u[key] = val
        elif key[0] == 'v':
            v[key] = val
        elif key[0] == 'w':
            w[key] = val
        elif key[0] == 'x':
            x[key] = val
        elif key[0] == 'y':
            y[key] = val
        elif key[0] == 'z':
            z[key] = val
        else:
            spec[key] = val

    return a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, spec

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
    
def main():
    root_dir = 'ANALYST'
    ps = PorterStemmer()
    inverted_index = {}
    mapped_files = {}
    n = 0
    for dir in os.listdir(root_dir):
        directory = os.path.join(root_dir, dir)
        for f in os.listdir(directory):
            n = n + 1
            cur_file = os.path.join(directory, f)
            mapped_files[n] = cur_file
            print(cur_file)
            with open(cur_file, 'r') as file:
                # parse through file
                data = json.load(file)
                content = data['content']

                soup = BeautifulSoup(content, 'lxml')
                # FIXME: 
                text = soup.get_text()
                # now we must get tokens
                tokenized = word_tokenize(text)
                #make sure tokens are lowercase
                stemmed = [ps.stem(token.lower(), to_lowercase=True) for token in tokenized if token not in string.punctuation]
                token_counts = indexing(stemmed)
                for key, val in token_counts.items():
                    if key not in inverted_index:
                        inverted_index[key] = []
                    inverted_index[key].append(posting.Posting(n, val))
    
    print(mapped_files)
    for k, v in inverted_index.items():
        print(k + ', ' + v)    
        #print(f)
        
    

# import krovetz
'''
def main():
    try:
        #beginning path
        path  = 'DEV/'

        #getting all file names in order to be read n
        files = [f for f in glob(path + "**/*.json", recursive=True)]
        
        #loop thru every file
        # for each file tokenize, stem token, the create rev index for each file
        ps = PorterStemmer()

        all_file_names = ['a.json', 'b.json', 'c.json', 'd.json', 'e.json', 'f.json', 'g.json', 'h.json', 'i.json', 'j.json', 'k.json', 'l.json', 'm.json', 'n.json', 'o.json', 'p.json', 'q.json', 'r.json', 's.json', 't.json', 'u.json', 'v.json', 'w.json', 'x.json', 'y.json', 'z.json', 'spec.json']
        
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

                #splitting partial index into 27 term ranges
                sep_dicts = seperateDict(partial_inverted_index)

                #write to those files and update dictionary from file and current index
                for i, current_dict in enumerate(sep_dicts):
                    if current_dict:
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
'''

    
        
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("Time of execution is: ", (end-start))
