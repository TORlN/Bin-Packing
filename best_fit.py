from zipzip_tree import ZipZipTree, Rank, Node
from printTree import print2D
import os

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items)) 
    
    tree.insert(key=1.0, val=0)
    
    for i, item in enumerate(items):
        current = findNode(tree.root, item)
        if current is not None:
            deltaSpace = round(current.key - item,10)
            tree.remove(current.key)
            if deltaSpace > 0:
                tree.insert(key=deltaSpace, val=current.val)
            assignment[i] = current.val
            free_space[current.val] = deltaSpace
        else:
            deltaSpace = round(1.0 - item,10)
            tree.insert(key=deltaSpace, val=len(free_space))
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
        # os.system('cls')
        # print2D(tree.root)
    return assignment, free_space
        
    

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return best_fit(items, assignment, free_space)

def findNode(current, item):
    best_fit = None
    while current is not None:
        if current.key >= item:
            if best_fit is None or current.key < best_fit.key:
                best_fit = current
            current = current.left
        else:
            current = current.right
    return best_fit
    
    
    
    