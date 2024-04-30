from zipzip_tree import ZipZipTree, Rank, Node
from printTree import print2D
import os

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)  # Initialize each bin with 1.0 unit of space
    tree = ZipZipTree(capacity=len(items))  # Initialize the tree with the capacity equal to the number of bins
    
    tree.insert(key=1.0, val=0)
    
    for item in items:
        current = findNode(tree.root, item)
        if current is not None:
            deltaSpace = round(current.key - item,10)
            tree.remove(current.key)
            if deltaSpace > 0:
                tree.insert(key=deltaSpace, val=current.val)
            assignment[items.index(item)] = current.val
            free_space[current.val] = deltaSpace
        else:
            deltaSpace = round(1.0 - item,10)
            tree.insert(key=deltaSpace, val=len(free_space))
            assignment[items.index(item)] = len(free_space)
            free_space.append(deltaSpace)
        # os.system('cls')
        # print2D(tree.root)
    return assignment, free_space
        
    

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return best_fit(items, assignment, free_space)

def findNode(current, item, best_fit=None):
    if current is None:
        return best_fit
    if current.key >= item:
        if best_fit is None or current.key < best_fit.key:
            best_fit = current 
        return findNode(current.left, item, best_fit)
    else:
        return findNode(current.right, item, best_fit)
    
    
    
    