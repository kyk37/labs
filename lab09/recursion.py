# recursion.py

def product_of_digits(x) -> int:
    ''' Returns a product of an int '''
    x = abs(x)
    if x < 10:
        return x
    return (x % 10) * product_of_digits(x // 10)


def array_to_string(a, index) -> str:
    ''' Converts an array with commas to a string'''
    if index >= len(a):
        return ""
    if index == len(a) - 1:
        return str(a[index])
    return str(a[index]) + ',' + array_to_string(a, index + 1)


def log(base, value) -> int:
    ''' Returns the floor of the log of "value" using the "base", recursively '''
    if value <= 0 or base <= 1:
        raise ValueError("Value must be > 0 and base must be > 1")
    if value < base:
        return 0
    if isinstance(base, int) == False or isinstance(value, int) == False:
        raise ValueError("Base or Value is not an int")
    
    return 1 + log(base, value // base)


# Optional test cases to verify the behavior
if __name__ == "__main__":
    print("product_of_digits(234):", product_of_digits(234))  # 24
    print("product_of_digits(12):", product_of_digits(-12))  # 2
    print("product_of_digits(-12):", product_of_digits(-12))  # 2

    print("array_to_string([1,2,3,4], 0):", array_to_string([1,2,3,4], 0), type(array_to_string([1,2,3,4], 0)))  # "1,2,3,4"
    print("array_to_string([], 0):", array_to_string([], 0))  # ""

    print("log(10, 123456):", log(10, 123456))  # 5
    print("log(2, 64):", log(2, 64))            # 6
    print("log(10, 4567):", log(10, 4567))      # 3
    print("log(10, 4567):", log(10.5, 45.67))   # Error