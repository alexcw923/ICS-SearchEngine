from flask import Flask, render_template, request
from search import get_search_results, get_url_from_docid, NUM_SEARCH_RESULTS

app = Flask(__name__)

# Define the routes
@app.route('/', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        user_query = request.form['query']
        docids = get_search_results([user_query])

        # pages[0] for backwards compat with cli search
        urls = [get_url_from_docid(docid) for docid in docids[0]]
        # pages = urls[0:NUM_SEARCH_RESULTS]
        pages = urls

        return render_template('result.html', pages=pages)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
