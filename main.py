import os, json, string
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict
from json.decoder import JSONDecodeError

def indexing(stem : str, filename : str) -> dict:
    #token : file 
    partial_index = defaultdict(list)
    
    for s in stem:
        partial_index[s].append(getFileName(filename))

    return partial_index
    
#getting file name from full path
def getFileName(path):
    return Path(path).stem

def mergeDict(d1, d2):
    #merging two dicts
    merged_dict = defaultdict(list)
    for d in (d1, d2):
        for k, v in d.items():
            merged_dict[k].append(v)

    #sorting values which is a list object
    for ls in merged_dict.values():
        ls.sort()

    return merged_dict

#sepearting dictionary into term ranges
def seperateDict(dict):
    a_f = {}
    g_l = {}
    m_s = {}
    t_z = {}

    for k, v in dict.items():
        if k[0] >= 'a' and k[0] <= 'f':
            a_f[k] = v
        elif k[0] >= 'g' and k[0] <= 'l':
            g_l[k] = v
        elif k[0] >= 'm' and k[0] <= 's':
            m_s[k] = v
        else:
            t_z[k] = v

    return [a_f, g_l, m_s, t_z]

# import krovetz
def main():
    
    #beginning path
    path  = 'DEV/'

    #getting all file names in order to be read n
    files = [f for f in glob(path + "**/*.json", recursive=True)]
    
    #loop thru every file
    # for each file tokenize, stem token, the create rev index for each file
    ps = PorterStemmer()

    all_file_names = ['a_f.json', 'g_l.json', 'm_s.json', 't_z.json']
    
    # UNCOMMENT AFTER FIRST RUN
    #for f in all_file_names:
    #   os.remove(f)

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            content = data['content']

            soup = BeautifulSoup(content, 'lxml')
            # FIXME: 
            text = soup.get_text()

            tokenized = word_tokenize(text)
            #make sure tokens are lowercase
            tokenized = [token.lower() for token in tokenized if token not in string.punctuation]
            #allows stemming to work with lowercase words
            stemmed = [ps.stem(s, to_lowercase=True) for s in tokenized]

            #getting partial_index from current html
            partial_inverted_index = indexing(stemmed, file)
            #json_data = json.dumps(partial_inverted_index, indent=2)

            #splitting partial index into 4 term ranges
            sep_dicts = seperateDict(partial_inverted_index)

            #write to those files and update dictionary from file and current index
            
            for i, current_dict in enumerate(sep_dicts):
                
                with open(all_file_names[i], 'w+') as infile, open(all_file_names[i], 'w') as outfile:
                    try:
                        old_index = json.load(infile)
                        merged_dict = mergeDict(old_index, current_dict)
                        json.dump(merged_dict, outfile, indent=4)
                    except JSONDecodeError:
                        json.dump(current_dict, outfile, indent=4)


                
                #file name to write to
                # with open(all_file_names[i], 'r') as f:
                #     #getting dict from file
                #     old_index = json.load(f)

                # #merging dict
                # merged_dict = mergeDict(old_index, current_dict)

                #     #writing dict back to file
                #     #f.seek(0)
                    
                # with open(all_file_names[i], 'w') as f:
                #     json.dump(merged_dict, f, indent=4)

            
    #TODO 
    
    num_of_docs = len(files)
    num_of_tokens = 0
    file_size = 0
    
    #Generate stats report for deliverable
    with open('report.txt', 'w') as file:

        for name in all_file_names:
            
            with open(name, "r+") as f:
                d = json.load(f)
                num_of_tokens += len(d.keys())
                file_size += os.path.getsize(name) / 1000
        
        file.write("Number of Documents: " + str(num_of_docs) +"\n")
        file.write("Number of Unique Tokens: " + str(num_of_tokens) + "\n")
        file.write("Total Size: " + str(file_size) + " kb\n")
    
    #FIXME: The token doesn't look good. E.g. ''": [
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0",
    #     "dc596b968c5a2187c988ca8f001404b13ce74964f23eca221520abc9ecc0e3f0"
    # ],
                

    

            
        
if __name__ == "__main__":
    main()
