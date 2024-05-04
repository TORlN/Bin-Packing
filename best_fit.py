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
            tree.remove(current.key)
            if deltaSpace > 0.0:
                tree.insert(key=deltaSpace, val=(current.val[0], current.val[1]))
            assignment[i] = current.val[0]
            free_space[current.val[0]] = deltaSpace
        else:
            deltaSpace = round(1.0 - item, 10)
            current = tree.insert(key=deltaSpace, val=(len(free_space), deltaSpace))
            assignment[i] = len(free_space)
            free_space.append(deltaSpace)
        update(tree.root)
        valid, _ = is_valid_max_heap(tree.root)
        if not valid:
            print2D(tree.root)
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
    
def update(node):
    if not node:
        return float('-inf')  # If the node does not exist, return negative infinity
    
    if not node.left and not node.right:
        # If the node is a leaf, its val[1] should be 0.0
        node.val = (node.val[0], 0.0)
        return node.key
    
    # Recursively update the left and right subtrees
    left_max = update(node.left)
    right_max = update(node.right)
    
    # Set the node's val[1] to the maximum key found in its children
    node.val = (node.val[0], max(left_max, right_max))
    
    # Return the maximum key found in the subtree rooted at this node, including the node itself
    return max(node.key, left_max, right_max)
    
def is_valid_max_heap(node):
    if not node:
        return True, float('-inf')
    
    if not node.left and not node.right:
        # Leaf node check
        return node.val[1] == 0.0, node.key

    # Recursive check on child nodes
    if node.left:
        left_is_valid, left_max = is_valid_max_heap(node.left)
    else:
        left_is_valid, left_max = True, float('-inf')

    if node.right:
        right_is_valid, right_max = is_valid_max_heap(node.right)
    else:
        right_is_valid, right_max = True, float('-inf')

    # Check current node's condition
    current_is_valid = node.val[1] == max(left_max, right_max)

    # Overall validity of this subtree
    is_valid = current_is_valid and left_is_valid and right_is_valid

    # Return the overall validity and the max key in this subtree
    return is_valid, max(node.key, left_max, right_max)