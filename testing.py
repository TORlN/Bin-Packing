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


def generate_test_data(num_items: int, roundNum: int):
    data = []
    for i in range(num_items):
        data.append(round(random.uniform(0.1, 1.0), roundNum))
    return data

def generate_perfect_test_data(num_items: int):
    return [.99999999999999999999] * num_items

def generate_random_free_space():
    return [round(random.random(0.1, 1.0), 2) for _ in range(random.randfloat(1, 10))]


def test_best_fit():
    # Test cases
    test_cases = [
        # Empty list
        [],
        # Single item
        [1.0],
        # Perfect fit
        [0.5, 0.5],
        # Items with different sizes
        [0.3, 0.6, 0.2],
        # Limited available space
        [0.8, 0.3, 0.4],
        # Large number of items
        list(range(1, 101)),
        # Duplicate items
        [0.5, 0.5, 0.5],
        # Randomized input
        generate_test_data(150),
        # Boundary cases
        [1.0] * 100,
        # Negative or zero sizes
        [-1.0, 0.0],
        # Extreme cases
        [1.0, 1e-10],
    ]
    # Run tests
    for i, items in enumerate(test_cases):
        items2 = deepcopy(items)
        assignment = [0] * len(items)
        assignment2 = deepcopy(assignment)
        free_space = []
        free_space2 = []
        best_fit_norm(items, assignment, free_space)
        requirements.best_fit(items2, assignment2, free_space2)
        assert assignment2 == assignment, f"Test case {i+1} failed: assignment mismatch"
        assert [round(x, 10) for x in free_space] == [round(x, 10) for x in free_space2], f"Test case {i+1} failed: free space mismatch"
    
    print("All test cases passed!")
if __name__ == "__main__":
    num_items = 15000
    items = generate_test_data(num_items, 5)
    # items = [0.9, 0.2, 0.3, 0.8, 0.7, 0.7, 0.2, 0.4, 0.7, 0.8, 0.7, 1.0, 0.8, 0.8, 0.8, 0.2, 0.7, 1.0, 0.4, 0.8, 0.5, 1.0, 0.4, 0.8, 0.2, 0.5, 0.8, 1.0, 0.8, 0.5, 0.9, 0.3, 0.1, 1.0, 0.6, 0.2, 0.9, 0.8, 0.2, 0.4, 0.6, 0.6, 0.6, 0.2, 0.5, 0.8, 1.0, 0.6, 0.3, 0.3]
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
    waste1 = len(free_space) - sum(items)
    waste2 = len(free_space2) - sum(items)
    if waste1 == waste2:
        print('Free space matches!')
    
    
    