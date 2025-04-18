
def group_by(f, target_list):
    '''
        Groups elements of target_list based on the result of function f.
        Returns a dictionary where each key is a result of f, and the value is a list of items.
    '''
    result = {}
    for item in target_list:
        key = f(item)
        result.setdefault(key, []).append(item)
    return result

if __name__ == "__main__":
    print(f'\ngroup_by(len, ["hi", "dog", "me", "bad", "good"]): => {group_by(len, ["hi", "dog", "me", "bad", "good"])}')