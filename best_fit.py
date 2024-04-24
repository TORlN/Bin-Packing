def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    for i in range(len(items)):
        best_bin = -1
        min_space = float('inf')
        for j in range(len(free_space)):
            if free_space[j] >= items[i] and round(free_space[j] - items[i],10) < min_space:
                best_bin = j
                min_space = round(free_space[j] - items[i],10)

        if best_bin != -1:
            free_space[best_bin] = round(free_space[best_bin] - items[i], 10)
            assignment[i] = best_bin
        else:
            new_bin_index = len(free_space)
            free_space.append(round(1.0 - items[i], 10))
            assignment[i] = new_bin_index

    return assignment, free_space

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    # sort in decreasing order
    sorted_items = sorted(range(len(items)), key=lambda i: -items[i])

    # use best-fit
    newItems = [items[i] for i in sorted_items]
    return best_fit(newItems, assignment, free_space)