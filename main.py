import time
from glob import glob
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import argparse

from build import build
from search import search

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