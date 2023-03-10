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