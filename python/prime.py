import sys
from math import ceil, sqrt

# used by next_prime() and prev_prime()
global _primes, _cur
_primes = []
_cur = 1

def prime(n):
    """Returns a list of the first n primes."""
    nums = [2]
    a = 3
    while len(nums) < n:
        for i in range(2, int(ceil(sqrt(a)) + 1)):
            if a % i == 0:
                break
        else:
            nums.append(a)
        a += 2 
    return nums

def prime_until(n):
    """Returns a list of all primes less than n."""
    nums = [2]
    for i in range(3, n, 2):
        for j in range(2, int(ceil(sqrt(i)) + 1)):
            if i % j == 0:
                break
        else:
            nums.append(i)
    return nums

def is_prime(n):
    """Returns True if n is prime, and False otherwise. Also, returns True if n is 1."""
    if n == 1 or n == 2:
        return True
    else:
        primes = prime_until(int(ceil(sqrt(n))) + 1)
        for i in primes:
            if n % i == 0:
                return False
        return True

def next_prime():
    global _primes, _cur
    _cur += 1
    while not is_prime(_cur):
        _cur += 1
    _primes.append(_cur)
    return _cur

def prev_prime():
    global _primes, _cur
    try:
        _cur = _primes[-2]
    except IndexError:
        _cur = 1
        return 2
    return _primes.pop()

def reset_prime():
    global _primes, _cur
    _primes = []
    _cur = 1

def factorize(n):
    """Returns a list of the prime factors of n. If n is prime, returns n."""
    if is_prime(n):
        return [n]
    factors = []
    primes = prime_until(int(ceil(sqrt(n))))
    for i in primes:
        while n % i == 0:
            n //= i
            factors.append(i)
    if n != 1:
        factors.append(n)
    return factors

if __name__ == '__main__':
    print('This module contains utility functions for prime numbers.')
    if len(sys.argv) > 1:
        print(factorize(int(sys.argv[1])))
    
