import random
import requirements
from copy import deepcopy
import time
from decimal import Decimal, getcontext

getcontext().prec = 20

def best_fit_norm(items: list[float], assignment: list[int], free_space: list[float]):
    bin_index = 0
    for i, item in enumerate(items):
        item_dec = Decimal(str(item))
        best_bin = -1
        min_space = Decimal('Infinity')
        
        for j, space in enumerate(free_space):
            space_dec = Decimal(str(space))
            if space_dec >= item_dec and (space_dec - item_dec) < min_space:
                best_bin = j
                min_space = space_dec - item_dec

        if best_bin == -1:
            best_bin = bin_index
            new_space_dec = Decimal("1.0") - item_dec
            free_space.append(float(new_space_dec))
            bin_index += 1
        else:
            remaining_space_dec = Decimal(str(free_space[best_bin])) - item_dec
            free_space[best_bin] = float(remaining_space_dec)
        
        assignment[i] = best_bin

def generate_test_data(num_items: int):
    return [random.uniform(0.1, 1.0) for _ in range(num_items)]


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
    
    