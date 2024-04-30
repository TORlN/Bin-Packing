from zipzip_tree import ZipZipTree, Rank, Node
from printTree import print2D

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items))
    
    tree.insert(key=0, val=1.0)
    for i, item in enumerate(items):
        current = tree.root
        
        current = findNode(current, item)
        if current is not None:
            deltaSpace = round(current.val - item,10)
            assignment[items.index(item)] = current.key
            free_space[current.key] = deltaSpace
            current.val = deltaSpace
        else:
            deltaSpace = round(1.0 - item,10)
            tree.insert(key=len(free_space), val=deltaSpace)
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
    return assignment, free_space


def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return first_fit(items, assignment, free_space)
def findNode(root, item):
    stack = []
    current = root
    
    while current is not None or stack:
        while current is not None:
            stack.append(current)
            current = current.left
            
        current = stack.pop()

        if current.val >= item:
            return current
        
        current = current.right

    return None

