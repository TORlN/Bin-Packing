from zipzip_tree import ZipZipTree
from printTree import print2D

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    free_space.append(1.0)
    tree = ZipZipTree(capacity=len(items)) 
    
    tree.insert(key=1.0, val=(0, 0.0))
    for i, item in enumerate(items):
        # print2D(tree.root)
        current = findNode(tree.root, item, tree)
        if current:
            deltaSpace = round(current.key - item, 25)
            removed = tree.remove(current.key)
            if removed:
                update(removed)
            if deltaSpace > 0.0:
                inserted = tree.insert(key=deltaSpace, val=(current.val[0], current.val[1]))
                update(inserted)
            
            assignment[i] = current.val[0]
            free_space[current.val[0]] = deltaSpace
        else:
            deltaSpace = round(1.0 - item, 25)
            current = tree.insert(key=deltaSpace, val=(len(free_space), deltaSpace))
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
            update(current)

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items.sort(reverse=True)
    return best_fit(items, assignment, free_space)

def findNode(root, size, tree):
    current = root
    best_fit = None

    while current:
        if size <= current.key:
            if current.val[1] < size:
                return current
            elif not best_fit or (current.key - size < best_fit.key - size):
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
    

# def update(current):
#     while current:
#         new_max = calculate_new_max(current)
#         if new_max != current.val[1]:
#             current.val = (current.val[0], new_max)
#         current = current.parent

# def calculate_new_max(current):
#         if current.left is None and current.right is None:
#             return 0.0
#         elif current.left is None:
#             return max(current.right.val[1], current.right.key)
#         elif current.right is None:
#             return max(current.left.val[1], current.left.key)
#         else:
#             return max(current.left.val[1], current.right.val[1], current.left.key, current.right.key)