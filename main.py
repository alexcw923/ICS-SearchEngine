import os, json, sys, time
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict
from json.decoder import JSONDecodeError
from matrix import InstanceMatrix
import argparse

from build import build
from search import search
from posting import JSONDecoder, JSONEncoder


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Subcommand build to construct index with optional argument
    # to specify output file to write index to
    parser_build = subparsers.add_parser("build")
    parser_build.set_defaults(func=build)

    # Subcommand search to query index
    # FIXME: ensure index is built/user error if no index found
    parser_search = subparsers.add_parser("search")
    parser_search.add_argument("query", type=str)
    parser_search.set_defaults(func=search)

    args = parser.parse_args()
    start = time.time()

    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()
    args.func(args)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
    end = time.time()
    print('Time', (end-start))
    
    # for i in ['a_f', 'g_l', 'm_s', 't_z', 'spec']:
    #     with open (f"{i}.json", 'r+') as file:
    #         index = json.load(file, cls=JSONDecoder)
    #         sorted_index = dict(sorted(index.items()))
    #         json.dump(sorted_index, file, cls=JSONEncoder)
    # Open the JSON file in read mode
    
    #pos = find_key_positions("test.json")
    #print(pos)

    
        
    

    """
    with open('test.json', 'r') as f:

        # Initialize variables
        current_char = ''
        current_pos = f.tell()

        # Iterate over each line in the file
        line = f.readline()

        # Load the JSON object from the line
        obj = json.loads(line)

        # Get the first character of the object's key
        char = list(obj.keys())[0][0]
        

        # Check if the character has changed
        if char != current_char:
            print(f"New character: {char} at position {current_pos}")
            current_char = char
            current_pos = f.tell()
    """
