import math
import random as rd
import sympy as sp
import numpy as np


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


def generate_keys():
    p = 2
    q = 2
    while(sp.isprime(p) == False):
        p = rd.randint(11, 12345)  # best min number for p & q to be secure enough --> 1048576
    while(sp.isprime(q) == False & p != q):
        q = rd.randint(11, 12345)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # select integer e that is relatively prime to n and ranges 1 < e < n
    e = p # initial value so that the loop runs at least once
    while(math.gcd(e, n) != 1):
        e = rd.randint(2, n)  # the public key is (e, n)
    
    # calculate d such that d * e = 1 mod phi
    d = multiplicative_inverse(e, phi) # the private key is (d, n)
    return e, d, n


def convert_to_int(message):
    # Convert the message to an integer
    message = int.from_bytes(message.encode(), byteorder='big')
    return message


def convert_to_string(message):
    # Convert the integer to a string
    message = message.to_bytes((message.bit_length() + 7) // 8, byteorder='big')
    message = message.decode()
    return message


def encrypt(message, e, n):
    message_int = convert_to_int(message)
    c = pow(message_int, e, n)
    return c


def decrypt(cipher, d, n):
    m = pow(cipher, d, n)
    message = convert_to_string(m)
    return message

