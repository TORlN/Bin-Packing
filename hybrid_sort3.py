
def insertion_sort_desc(nums):
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and key > nums[j]:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
    return nums

def hybrid_sort3_desc(arr):
    H = len(arr) ** 0.6
    h_sort(arr, H)

def h_sort(arr, H):
    if len(arr) <= 1:
        return
    if len(arr) > H:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        h_sort(left_half, H)
        h_sort(right_half, H)
        
        merge_desc(arr, left_half, right_half)
    else:
        insertion_sort_desc(arr)  

def merge_desc(arr, left, right):
    i = j = k = 0

    while i < len(left) and j < len(right):
        if left[i] > right[j]:  
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
