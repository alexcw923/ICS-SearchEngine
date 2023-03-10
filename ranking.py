import numpy as np

def pageRank(links, d=0.85, tol=1e-6):
    """
    Computes the PageRank for each node in a directed graph represented by links.

    Args:
        links (dict): A dictionary where the keys are the node IDs and the values are lists of the IDs of the nodes that the key node links to.
        d (float): The damping factor (default 0.85).
        tol (float): The tolerance for the convergence of the algorithm (default 1e-6).

    Returns:
        dict: A dictionary where the keys are the node IDs and the values are their corresponding PageRank scores.
    """

    n = len(links)
    A = np.zeros((n, n))
    nodes = list(links.keys())

    # Create adjacency matrix A
    for i, node in enumerate(nodes):
        for neighbor in links[node]:
            j = nodes.index(neighbor)
            A[j, i] = 1 / len(links[node])

    # Add teleportation
    v = np.ones(n) / n
    A = d * A + (1 - d) * v.reshape(-1, 1)

    # Power iteration
    x = np.ones(n) / n
    while True:
        x_new = np.dot(A, x)
        if np.linalg.norm(x_new - x, ord=1) < tol:
            break
        x = x_new

    # Normalize PageRank scores
    pr = dict(zip(nodes, x / sum(x)))

    return pr

def hits(links, max_iters=100, tol=1e-6):
    """
    Computes the HITS (Hyperlink-Induced Topic Search) scores for each node in a graph.

    Args:
        links (dict): A dictionary where the keys are the node IDs and the values are lists of the IDs of the nodes that the key node links to.
        max_iters (int): The maximum number of iterations to perform (default 100).
        tol (float): The tolerance for the convergence of the algorithm (default 1e-6).

    Returns:
        tuple: A tuple containing two dictionaries: the first contains the authority scores for each node, and the second contains the hub scores for each node.
    """

    nodes = list(links.keys())
    n = len(nodes)
    A = np.zeros((n, n))

    # Create adjacency matrix A
    for i, node in enumerate(nodes):
        for neighbor in links[node]:
            j = nodes.index(neighbor)
            A[j, i] = 1

    # Initialize authority and hub scores
    a = np.ones(n)
    h = np.ones(n)

    # Power iteration
    for i in range(max_iters):
        a_new = np.dot(A.T, h)
        h_new = np.dot(A, a_new)

        # Normalize scores
        a_new /= np.linalg.norm(a_new, ord=2)
        h_new /= np.linalg.norm(h_new, ord=2)

        # Check for convergence
        if np.linalg.norm(a_new - a, ord=1) < tol and np.linalg.norm(h_new - h, ord=1) < tol:
            break

        a = a_new
        h = h_new

    # Create authority and hub score dictionaries
    auth_scores = dict(zip(nodes, a))
    hub_scores = dict(zip(nodes, h))

    return auth_scores, hub_scores



if __name__ == '__main__':
    # Example usage
    links = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['B', 'C']
    }
    pr = pageRank(links)
    print(pr)