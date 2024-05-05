from zipzip_tree import ZipZipTree
from printTree import print2D
from decimal import Decimal, getcontext
from hybrid_sort3 import hybrid_sort3_desc

getcontext().prec = 20

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items))
    
    tree.insert(key=1.0, val=(0, 0.0))
    for i, item in enumerate(items):
        item_dec = Decimal(str(item))
        current = findNode(tree.root, item_dec, tree)
        if current:
            delta_space_dec = Decimal(str(current.key)) - item_dec
            delta_space = float(delta_space_dec)
            removed = tree.remove(current.key)
            if removed:
                update(removed)
            if delta_space > 0.0:
                inserted = tree.insert(key=delta_space, val=(current.val[0], delta_space))
                update(inserted)
            
            assignment[i] = current.val[0]
            free_space[current.val[0]] = delta_space
        else:
            delta_space_dec = Decimal("1.0") - item_dec
            delta_space = float(delta_space_dec)
            current = tree.insert(key=delta_space, val=(len(free_space), delta_space))
            assignment[i] = len(free_space)
            free_space.append(delta_space)
            update(current)

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    hybrid_sort3_desc(items)
    return best_fit(items, assignment, free_space)

def findNode(root, size: Decimal, tree):
    current = root
    best_fit = None

    while current:
        if size <= Decimal(str(current.key)):
            if current.val[1] < float(size):
                return current
            elif not best_fit or (Decimal(str(current.key)) - size < Decimal(str(best_fit.key)) - size):
                best_fit = current
            current = current.left
        else:
            if current.right:
                current = current.right
            else:
                break
            
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