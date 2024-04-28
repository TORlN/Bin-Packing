from decimal import Decimal, getcontext
getcontext().prec = 3

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    for i in range(len(items)):
        placed = False
        for j in range(len(free_space)):
            if free_space[j] >= items[i]:
                initial = Decimal(free_space[j])
                item = Decimal(items[i])
                free_space[j] = float(initial - item)
                assignment[i] = j
                placed = True
                break
        if not placed:
            free_space.append(round(1.0 - items[i], 10))
            assignment[i] = len(free_space) - 1

    return assignment, free_space
def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    # sort in decreasing order
    sorted_items = sorted(range(len(items)), key=lambda i: -items[i])

    # use first-fit
    newItems = [items[i] for i in sorted_items]
    return first_fit(newItems, assignment, free_space)