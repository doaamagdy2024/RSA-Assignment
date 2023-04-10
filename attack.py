import sympy as sp
import random as rd
import numpy as np
import math
import time


def factorize_n(n):
    # get the prime factorizatoin of n
    a = sp.factorint(n)
    return a


def multiplicative_inverse(e, phi):
    rem = [phi, e]
    quotient = [0, phi // e] # integer division
    x = [1, 0]
    y = [0, 1]

    while(rem[1] != 1):
        x_0 = x[1]
        y_0 = y[1]
        q_0 = quotient[1]
        rem_0 = rem[1]

        x[1] = x[0] - quotient[1] * x[1]
        y[1] = y[0] - quotient[1] * y[1]
        rem[1] = rem[0] % rem[1] 
        quotient[1] = rem_0 // rem[1]
        

        x[0] = x_0
        y[0] = y_0
        quotient[0] = q_0
        rem[0] = rem_0
    
    d = y[1]
    
    return d


def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # select integer e that is relatively prime to n and ranges 1 < e < n
    e = phi # initial value so that the loop runs at least once
    while(math.gcd(e, phi) != 1):
        e = rd.randint(2, phi)  # the public key is (e, n)
    
    # calculate d such that d * e = 1 mod phi
    d = multiplicative_inverse(e, phi) # the private key is (d, n)
    return e, d, n


def generate_pq_for_n_bits():
    for bit in (2, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        p = 4
        q = 4
        mini = 2 ** (bit - 1)
        while(sp.isprime(p) == False or p < mini):
            p = rd.getrandbits(bit)
        while(sp.isprime(q) == False or p == q or q < mini):
            q = rd.getrandbits(bit)
        
        e, d, n = generate_keys(p, q)
        # write in the file the p, q, n in addition to the bit and the private key d
        with open("n_e_d.txt", "a") as f:
            f.write("n: " + str(n) + " e: " + str(e) + " d: " + str(d) + " bit: " + str(bit) + "\n")



def attack(n, e):
    # get the prime factorization of n
    start = time.time()

    factors = factorize_n(n)
    p = factors.popitem()[0]
    q = factors.popitem()[0]
    phi = (p - 1) * (q - 1)
    d = multiplicative_inverse(e, phi)

    end = time.time()
    total_time = end - start

    return d, total_time
