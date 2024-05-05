from zipzip_tree import ZipZipTree
from printTree import print2D
from decimal import Decimal, getcontext

getcontext().prec = 20

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items))
    
    tree.insert(key=0, val=(1.0, 0.0))
    for i, item in enumerate(items):
        item_dec = Decimal(str(item))
        current = findNode(tree.root, item_dec)
        if current is not None:
            delta_space_dec = Decimal(str(current.val[0])) - item_dec
            delta_space = float(delta_space_dec)
            assignment[i] = current.key
            free_space[current.key] = delta_space
            current.val = (delta_space, current.val[1])
            update(current)
        else:
            delta_space_dec = Decimal("1.0") - item_dec
            delta_space = float(delta_space_dec)
            x = tree.insert(key=len(free_space), val=(delta_space, delta_space))
            assignment[i] = len(free_space)
            free_space.append(delta_space)
            update(x)
    return assignment, free_space

def update(current):
    if current.left is None and current.right is None:
        current.val = (current.val[0], 0.0)
    elif current.left is None:
        current.val = (current.val[0], max(current.right.val[1], current.right.val[0]))
    elif current.right is None:
        current.val = (current.val[0], max(current.left.val[1], current.left.val[0]))
    else:
        current.val = (current.val[0], max(current.left.val[1], current.right.val[1], current.left.val[0], current.right.val[0]))
    if current.parent:
        update(current.parent)

def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return first_fit(items, assignment, free_space)

def findNode(current, item: Decimal):
    if current is None:
        return None
    if current.val[0] < float(item) and current.val[1] < float(item):
        return None
    left = findNode(current.left, item)
    if left is not None:
        return left
    if current.val[0] >= float(item):
        return current
    return findNode(current.right, item)
    
    
        
            
            
        

