from zipzip_tree import ZipZipTree, Rank, Node
from printTree import print2D

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items))
    
    tree.insert(key=0, val=(1.0, 0.0))
    for i, item in enumerate(items):
        # print2D(tree.root)
        current = tree.root
        current = findNode(current, item)
        if current is not None:
            deltaSpace = round(current.val[0] - item,25)
            assignment[i] = current.key
            free_space[current.key] = deltaSpace
            current.val = (deltaSpace, current.val[1])
            update(current)
        else:
            deltaSpace = round(1.0 - item,25)
            x = tree.insert(key=len(free_space), val=(deltaSpace, deltaSpace))
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
            update(x)
    return assignment, free_space

def update(current):
    if current.left is None and current.right is None:
        current.val = (current.val[0], 0.0)
    elif current.left is None:
        current.val = (current.val[0], max(current.right.val[1], current.right.val[0]))
    elif current.right is None:
        current.val = (current.val[0],max(current.left.val[1], current.left.val[0]))
    else:
        current.val = (current.val[0],max(current.left.val[1], current.right.val[1], current.left.val[0], current.right.val[0]))
    if current.parent:
        update(current.parent)

def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return first_fit(items, assignment, free_space)
def findNode(current, item):
    if current is None:
        return None
    if current.val[0] < item and current.val[1] < item:
        return None
    left = findNode(current.left, item)
    if left is not None:
        return left
    if current.val[0] >= item:
        return current
    return findNode(current.right, item)
    
    
    
        
            
            
        

