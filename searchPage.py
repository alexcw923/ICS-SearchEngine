from flask import Flask, render_template, request
from search import get_search_results, get_url_from_docid, NUM_SEARCH_RESULTS, preload

import time

# FIXME: yummy global variables
mapping, positional_index = preload()

app = Flask(__name__)

# Define the routes
@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        user_query = request.form['query']

        start = time.time()
        docids = get_search_results(positional_index, [user_query])
        end = time.time()

        # pages[0] for backwards compat with cli search
        urls = [get_url_from_docid(mapping, docid) for docid in docids[0]]
        pages = urls[0:NUM_SEARCH_RESULTS]

        return render_template('result.html', pages=pages, time=end-start)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
