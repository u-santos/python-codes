def binary_search(ordened_list, searching):
    low = 0
    high = len(ordened_list) - 1
    
    while low <= high:
        mid = (low + high) / 2
        mid = int(mid)
        guess = ordened_list[mid]
        
        if guess == searching:
            return mid
        if guess > searching:
            high = mid - 1
        else:
            low = mid + 1
    return None
my_list = list(range(1,10))
print(binary_search(my_list, 9))