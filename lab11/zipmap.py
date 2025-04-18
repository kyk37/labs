from itertools import zip_longest


def zipmap(key_list: list, value_list: list, override=False) -> dict:
    '''
        Creates a dictionary from key_list to value_list
        - If override=True, later duplicate keys overwrite earlier ones.
        - If override=False and there are duplicate keys, return {}.
        - Extra values are discarded.
        - Extra keys are filled with None.
    '''
    #print(f"Keys: {key_list}")
    #print(f"Values: {value_list}")
    
    # Use zip to pair up to the shorter list, or zip_longest if key_list is longer
    if len(key_list) > len(value_list):
        zipped = zip_longest(key_list, value_list, fillvalue=None)
    else:
        zipped = zip(key_list, value_list)
    
    mapped = list(map(lambda pair: (pair[0], pair[1]), zipped))
    #print(f"Zipped pairs: {mapped}")
    
    keys = [k for k, _ in mapped]
    if not override and len(set(keys)) != len(keys):
        return {} 

    result = {}
    for key, val in mapped:
        if not override and key in result:
            return {}
        result[key] = val

    return result

# Example test cases
if __name__ == "__main__":
    list_1 = ['a', 'b', 'c', 'd', 'e', 'f']
    list_2 = [1, 2, 3, 4, 5, 6]
    
    print(f"List_1: {list_1}")
    print(f"List_2: {list_2}")
    print(f"Result: {zipmap(list_1, list_2)}\n")
    
    print(f"zipmap([1, 2, 3, 2], [4, 5, 6, 7], True) => {zipmap([1, 2, 3, 2], [4, 5, 6, 7], True)}")
    print(f"zipmap([1, 2, 3], [4, 5, 6, 7, 8]) => {zipmap([1, 2, 3], [4, 5, 6, 7, 8])}")
    print(f"zipmap([1, 3, 5, 7], [2, 4, 6]) => {zipmap([1, 3, 5, 7], [2, 4, 6])}")
