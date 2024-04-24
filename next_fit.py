# Example file: next_fit.py

# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
    bin_index = 0
    free_space.append(1.0)  

    for i in range(len(items)):
        if free_space[bin_index] >= items[i]:
            free_space[bin_index] = round(free_space[bin_index] - items[i], 10) 
            assignment[i] = bin_index
        else:
            bin_index += 1  
            free_space.append(1.0)
            free_space[bin_index] = round(free_space[bin_index] - items[i], 10) 
            assignment[i] = bin_index

    return assignment, free_space
