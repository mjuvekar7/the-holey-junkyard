# used by next_fib() and prev_fib()
_fibs = []
global _a, _b
_a, _b = 0, 1

def fib(n):
    """Returns a list of the first n Fibonacci numbers."""
    nums = []
    a, b = 0, 1
    while len(nums) < n:
        a, b = b, a + b
        nums.append(a)
    return nums

def fib_until(n):
    """Returns a list of all Fibonacci numbers less than n."""
    nums = []
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
        nums.append(a)
    return nums

def is_fib(n):
    """Returns True if n is a Fibonacci number, and False otherwise."""
    if n in fib_until(n + 1):
        return True
    return False

def next_fib():
    global _a, _b
    temp = _a + _b
    _a = _b
    _b = temp
    _fibs.append(_a)
    return _a

def prev_fib():
    global _a, _b
    try:
        _a = _fibs[-3]
        _b = _fibs[-2]
    except IndexError:
        _a, _b = 0, 1
        return 1
    return _fibs.pop()

def reset_fib():
    global _a, _b
    _fibs = []
    _a, _b = 0, 1

if __name__ == '__main__':
    print('This module contains utility functions for Fibonacci numbers.')

