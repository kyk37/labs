import math

def make_set(data):
    '''
        Create a set from a list of numbers
    '''
    temp = []
    for val in data:
        if val not in temp:
            temp.append(val)
            
    return temp

def is_set(data):
    '''
        Check if data is a set.
        If it is, return true.
        If it is not return false.
        If it's an empty set return True
        If it's "None" return False
    '''
    temp = []
    if data != None:
        for val in data:
            if val not in temp:
                temp.append(val)
    
    if temp == data:
        return True
    return False

def union(setA, setB):
    '''
        Test A & B to see if they are a set if not return empty list
        Combine both lists
        Make them into a set and return
    '''
    temp = []
    tempB = []
    union_set = []
    if setA != None:
        for val in setA:
            if val not in temp:
                temp.append(val)
    
    
    if setB != None:
            for val in setB:
                if val not in tempB:
                    tempB.append(val)
    
    if temp != setA:
        return []
    
    if tempB != setB:
        return []
    
    # Combine both sets and remove identicals
    combined = setA + setB
    if combined != None:
        for val in combined:
            if val not in union_set:
                union_set.append(val)
                
    return union_set


def intersection(setA, setB):
    '''
        Check if both inputs are a set
        if not a set, return empty list
        If a set, repeated elements get returned
        if both sets have no repeating items, return empty list
    '''
    temp = []
    tempB = []
    inter_set = []
    if setA != None:
        for val in setA:
            if val not in temp:
                temp.append(val)
    
    
    if setB != None:
            for val in setB:
                if val not in tempB:
                    tempB.append(val)
    
    if temp != setA:
        return []
    
    if tempB != setB:
        return []
    
    for val in setA:
        if val in setB:
            inter_set.append(val)

    return inter_set

if __name__ == "__main__":
    my_list = [1, 2, 3, 4, 4, 5]
    print(f"Starting List: {my_list}")
    
    my_set = make_set(my_list)
    print(f"Set made from list {my_set}")
    
    print(f"\nPerforming is_set tests.")
    print(is_set([1,2,3,4,5]))
    print(is_set([5,5]))
    print(is_set([]))
    print(is_set(None))
    
    print(f"\nPerforming Union tests")
    print(union([1,2],[2,3]))
    print(union([],[2,3]))
    print(union([1,1,1],[2,3]))
    
    print(f"\n Intersection Tests")
    print(intersection([1,2],[2,3]))
    print(intersection([],[2,3]))
    print(intersection([1,1,1],[2,3]))