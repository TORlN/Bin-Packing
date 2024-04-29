from zipzip_tree import ZipZipTree, Rank, Node
from printTree import print2D

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)  # Initialize each bin with 1.0 unit of space
    tree = ZipZipTree(capacity=len(items))  # Initialize the tree with the capacity equal to the number of bins
    
    # Populate the tree with initial free space values
    for index, space in enumerate(items):
        if space > 0:
            tree.insert(key=1.0, val=index)
    print2D(tree.root)
    

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    # sort in decreasing order
    sorted_items = sorted(range(len(items)), key=lambda i: -items[i])

    # use best-fit
    newItems = [items[i] for i in sorted_items]
    return best_fit(newItems, assignment, free_space)

def findNode(current, item):
    if current is None:
        return None

    if current.key >= item:
        return current