import random
import requirements
from copy import deepcopy
import time

def best_fit_norm(items: list[float], assignment: list[int], free_space: list[float]):
    """Applies the Best Fit algorithm to pack items into bins.
    
    Args:
        items: List of item sizes.
        assignment: List where assignment[i] stores the bin index for items[i].
        free_space: List of available space in each bin.
    """
    bin_index = 0
    for i, item in enumerate(items):
        best_bin = -1
        min_space = float('inf')
        for j, space in enumerate(free_space):
            if space >= item and round(space - item,10) < min_space:
                best_bin = j
                min_space = space - item
        
        if best_bin == -1:
            best_bin = bin_index
            free_space.append(round(1.0 - item,10)) 
            bin_index += 1
        else:
            free_space[best_bin] = round(free_space[best_bin] - item, 10)
        
        assignment[i] = best_bin

def generate_test_data(num_items: int):
    """Generates a list of random item sizes.
    
    Args:
        num_items: The number of items to generate.
        
    Returns:
        List of random item sizes between 0.1 and 0.5.
    """
    return [random.uniform(0.1, 0.5) for _ in range(num_items)]


# Run the benchmark test
if __name__ == "__main__":
    num_items = 150000
    items = generate_test_data(num_items)
    items2 = deepcopy(items)
    
    assignment = [0] * num_items
    assignment2 = deepcopy(assignment)
    free_space = []
    free_space2 = []
    
    start = time.time()
    requirements.best_fit(items2, assignment2, free_space2)
    end = time.time()
    print(f'Best Fit (zip zip) for {num_items} elements: {end - start:.4f} seconds')
    
    start = time.time()
    best_fit_norm(items, assignment, free_space)
    end = time.time()
    print(f'Best Fit O(n^2) for {num_items} elements: {end - start:.4f} seconds')
    
    if items == items2:
        print('Items match!')
    if assignment == assignment2:
        print('Assignments match!')
    if free_space == free_space2:
        print('Free space match!')
    
    