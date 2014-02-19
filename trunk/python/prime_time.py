import prime, sys, time, random, pickle

def prime_time(n):
    print('Factorizing', n)
    start = time.clock()
    print(prime.factorize(n))
    stop = time.clock() - start
    print('Factorization took {:.2f} seconds.'.format(stop))

if __name__ == '__main__':
    f = open('primes', 'rb')
    primes = pickle.load(f)
    n = random.choice(primes) * random.choice(primes)
    prime_time(n)
    f.close()
