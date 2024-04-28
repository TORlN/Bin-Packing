from decimal import Decimal, getcontext
getcontext().prec = 3

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    for i in range(len(items)):
        best_bin = -1
        min_space = float('inf')
        for j in range(len(free_space)):
            if free_space[j] >= items[i] and round(free_space[j] - items[i],10) < min_space:
                best_bin = j
                initial = Decimal(free_space[j])
                item = Decimal(items[i])
                min_space = float(initial - item)

        if best_bin != -1:
            initial = Decimal(free_space[best_bin])
            item = Decimal(items[i])
            free_space[best_bin] = float(initial - item)
            assignment[i] = best_bin
        else:
            new_bin_index = len(free_space)
            initial = Decimal(1.0)
            item = Decimal(items[i])
            free_space.append(float(initial - item))
            assignment[i] = new_bin_index

    return assignment, free_space

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    # sort in decreasing order
    sorted_items = sorted(range(len(items)), key=lambda i: -items[i])

    # use best-fit
    newItems = [items[i] for i in sorted_items]
    return best_fit(newItems, assignment, free_space)