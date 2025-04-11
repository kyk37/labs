# Make a cache/memoization for the Fibonacci sequence where n = 35

import time

def memoize(func):
    ''' Store the values in the cache using custom decorator '''
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

def recur_fibo(n):
    ''' Fibonachi Sequence '''
    if n <= 1:
        return n
    else:
        return recur_fibo(n-1) + recur_fibo(n-2)

@memoize
def memo_fibo(n):
    ''' Fibonacchi Sequence using the memoization decorator '''
    if n <= 1:
        return n
    else:
        return memo_fibo(n-1) + memo_fibo(n-2)

# Timing comparison
if __name__ == "__main__":
    n = 35

    start = time.time()
    print(f"recur_fibo({n}) =", recur_fibo(n))
    print("Time (no memo):", round(time.time() - start, 4), "seconds")

    start = time.time()
    print(f"memo_fibo({n}) =", memo_fibo(n))
    print("Time (with memo):", round(time.time() - start, 4), "seconds")
