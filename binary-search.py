def binary_search(list, item):
    low = 0
    high = len(list) -1

    num_try = 0
    while low <= high:
        mid = (low + high) / 2
        mid = int(mid)
        guess = list[mid]

        num_try += 1
        print(f"Try number: {num_try}")
        print(f"low: {low}\nhigh: {high}\nmid: {mid}\nguess: {guess}")
        print("=============================")
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None

my_list = list(range(0, 100000000))

response = binary_search(my_list, 95)
print(response)