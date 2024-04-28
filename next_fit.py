# Example file: next_fit.py

# explanations for member functions are provided in requirements.py
from decimal import Decimal, getcontext
getcontext().prec = 3
def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
    bin_index = 0
    free_space.append(1.0)  

    for i in range(len(items)):
        if free_space[bin_index] >= items[i]:
            initial = Decimal(free_space[bin_index])
            item = Decimal(items[i])
            free_space[bin_index] = float(initial - item)
            assignment[i] = bin_index
        else:
            bin_index += 1  
            free_space.append(1.0)
            initial = Decimal(free_space[bin_index])
            item = Decimal(items[i])
            free_space[bin_index] = float(initial - item)
            assignment[i] = bin_index

    return assignment, free_space
