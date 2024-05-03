from zipzip_tree import ZipZipTree
from printTree import print2D

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items)) 
    
    tree.insert(key=1.0, val=(0, 0.0))
    for i, item in enumerate(items):
        current = findNode(tree.root, item, None)
        if current is not None:
            deltaSpace = round(current.key - item, 10)
            removedParent = current.parent
            tree.remove(current.key)
            if deltaSpace > 0.0:
                x = tree.insert(key=deltaSpace, val=(current.val[0], current.val[1]))
            else:
                pass
            # print2D(tree.root)
            assignment[i] = current.val[0]
            free_space[current.val[0]] = deltaSpace
            # print2D(tree.root)
            if removedParent:
                update(removedParent)
            update(x)
            # print2D(tree.root)
            pass
        else:
            deltaSpace = round(1.0 - item, 10)
            current = tree.insert(key=deltaSpace, val=(len(free_space), deltaSpace))
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
            # print2D(tree.root)
            update(current)
            # print2D(tree.root)
            pass
    return assignment, free_space

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return best_fit(items, assignment, free_space)

def findNode(current, item, best_fit=None):
    if current is None:
        return best_fit
    if current.key == item:
        return current
    if current.key >= item:
        if best_fit is None or current.key < best_fit.key:
            best_fit = current
        leftBest = findNode(current.left, item, best_fit)
        if leftBest and (best_fit is None or leftBest.key < best_fit.key):
            best_fit = leftBest
    if current.key < item and current.val[1] >= item:
        rightBest = findNode(current.right, item, best_fit)
        if rightBest and (best_fit is None or rightBest.key < best_fit.key):
            best_fit = rightBest
    return best_fit
    

        

def update(current):
    if current.left is None and current.right is None:
        current.val = (current.val[0], 0.0)
    elif current.left is None:
        current.val = (current.val[0], max(current.right.val[1], current.right.key))
    elif current.right is None:
        current.val = (current.val[0],max(current.left.val[1], current.left.key))
    else:
        current.val = (current.val[0],max(current.left.val[1], current.right.val[1], current.left.key, current.right.key))
    if current.parent:
        update(current.parent)

    
    