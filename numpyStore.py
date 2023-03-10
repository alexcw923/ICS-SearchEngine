import numpy as np
from posting import Posting

def writeToNPY(partial_index, filename):
    dtype = [('token', 'U50'), ('postings', np.object)]

    # Create a list of token-posting pairs
    tokens = ['apple', 'banana', 'orange']
    postings = [[Posting(1, 0.2), Posting(2, 0.4)], [Posting(1, 0.1), Posting(3, 0.3)], [Posting(2, 0.5)]]
    data = list(zip(tokens, postings))

    # Create the record array
    arr = np.array(data, dtype=dtype)

    # Save the record array to a file
    np.save('index.npy', arr)

    # Load the record array from the file
    arr = np.load('index.npy', allow_pickle=True)

    # Access the postings for a token
    token = 'apple'
    postings = arr[arr['token'] == token]['postings'][0]
    for posting in postings:
        print(posting.doc_id, posting.score)
    np.save("partial_index.npy", partial_index)
    
if __name__ == '__main__':
    writeToNPY()