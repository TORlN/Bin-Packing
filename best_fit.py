from zipzip_tree import ZipZipTree
from printTree import print2D
from decimal import Decimal, getcontext
from hybrid_sort3 import hybrid_sort3_desc

getcontext().prec = 20

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = ZipZipTree(capacity=len(items))
    if tree.capacity > 0:
        tree.insert(key=1.0, val=([0], 0.0))
        free_space.append(1.0)
    
    for i, item in enumerate(items):
        item_dec = Decimal(str(item))
        current = findNode(tree.root, item_dec, tree)
        if current and len(current.val[0]) > 1:
            pass
        value = None
        inserted2 = None
        if current:
            delta_space_dec = Decimal(str(current.key)) - item_dec
            delta_space = float(delta_space_dec)
            removed = tree.remove(current.key)
            if removed:
                if isinstance(removed, tuple):
                    update(removed[0])
                    value = removed[1]
                else:
                    update(removed)
            if value is not None:
                inserted = tree.insert(key=current.key, val=(current.val[0], current.val[1]))
                inserted2 = tree.insert(key=delta_space, val=([value], delta_space))
            else:
                inserted = tree.insert(key=delta_space, val=(current.val[0], delta_space))
            if inserted:
                update(inserted)
            if inserted2:
                update(inserted2)
            if value is not None:
                assignment[i] = value
                free_space[value] = delta_space
            else:
                assignment[i] = current.val[0][0]
                free_space[current.val[0][0]] = delta_space
        else:
            delta_space_dec = Decimal("1.0") - item_dec
            delta_space = float(delta_space_dec)
            if delta_space > 0.0:
                current = tree.insert(key=delta_space, val=([len(free_space)], delta_space))
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
            current = current.right
            
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