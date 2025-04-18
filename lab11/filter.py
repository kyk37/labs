from functools import reduce

def my_filter(func, seq):
    '''
        Implements a filter using reduce.
        Returns a list of items in which func(item) is True.
    '''
    return reduce(lambda acc, x: acc + [x] if func(x) else acc, seq, [])

if __name__ == "__main__":
    print(f"\nfilter (x % 2 == 0, [1, 2, 3, 4, 5, 6]) => {my_filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])}")
    print(f"filter: (x > 3, [1, 2, 3, 4, 5]) => {my_filter(lambda x: x > 3, [1, 2, 3, 4, 5])}")
    print(f"filter: ('a' in s, ['cat', 'weasel', 'mousey', 'owl']) => {my_filter(lambda s: 'a' in s, ['cat', 'weasel', 'rat', 'owl'])}")