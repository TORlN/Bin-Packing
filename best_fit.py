from zipzip_tree import ZipZipTree
from printTree import print2D

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items)) 
    
    tree.insert(key=1.0, val=(0, 0.0))
    for i, item in enumerate(items):
        current = findNode(tree.root, item)
        if current is not None:
            deltaSpace = round(current.key - item, 10)
            x = tree.remove(current.key)
            if x is not None:
                update(x)
            if deltaSpace > 0.0:
                x = tree.insert(key=deltaSpace, val=(current.val[0], current.val[1]))
                update(x)
            assignment[i] = current.val[0]
            free_space[current.val[0]] = deltaSpace
        else:
            deltaSpace = round(1.0 - item, 10)
            current = tree.insert(key=deltaSpace, val=(len(free_space), deltaSpace))
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
            update(current)

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return best_fit(items, assignment, free_space)

def findNode(root, item):
    current = root
    best_fit = None
    while current:
        if current.key == item:
            return current
        if current.key >= item:
            if best_fit is None or current.key < best_fit.key:
                best_fit = current
            current = current.left
        else:
            if current.right and current.val[1] >= item:
                current = current.right
            else:
                break  # If no right child or right child does not have a higher key, break the loop
    return best_fit
    
def update(current):
    while current:
        if current.left is None and current.right is None:
            current.val = (current.val[0], 0.0)
        elif current.left is None:
            current.val = (current.val[0], max(current.right.val[1], current.right.key))
        elif current.right is None:
            current.val = (current.val[0], max(current.left.val[1], current.left.key))
        else:
            current.val = (current.val[0], max(current.left.val[1], current.right.val[1], current.left.key, current.right.key))
        current = current.parent