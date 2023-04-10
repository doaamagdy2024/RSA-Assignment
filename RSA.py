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
    p = 4
    q = 4
    while(sp.isprime(p) == False):
        p = rd.randint(757, 12345)  # best min number for p & q to be secure enough --> 1048576
    while(sp.isprime(q) == False or p == q):
        q = rd.randint(757, 12345)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # select integer e that is relatively prime to n and ranges 1 < e < n
    e = phi # initial value so that the loop runs at least once
    while(math.gcd(e, phi) != 1):
        e = rd.randint(2, phi)  # the public key is (e, n)
    
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
    c = pow(message, e, n)
    return c


def decrypt(cipher, d, n):
    message = pow(cipher, d, n)  
    return message


def encode_encrypt_message(message, e, n):
    # convert the message to an integer
    encoded_message = []
    group = 0
    num = 0
    counter = 4
    for char in message:
        #i += 1
        if(char >= '0' and char <= '9'):
            num = ord(char) - ord('0')  # ord('0') = 48
        elif(char >= 'a' and char <= 'z'):
            num = ord(char) - ord('a') + 10 # ord('a') = 97
        else:
            num = 36  # Convert any extra characters to spaces as specified.
        group += num * (37 ** counter)
        counter -= 1
        if counter < 0:
            encoded_message.append(encrypt(group, e, n))
            # concatenate the group to the message
            group = 0
            counter = 4
    
    if counter < 4:
        while(counter != -1 ):
            group += 36 * (37 ** counter)
            counter -= 1
        encoded_message.append(encrypt(group, e, n))

    #encoded_message.__str__()
    return encoded_message


def decode_decrypt_message(encoded_message, d, n):
    message = ""
    encoded_message[0:] = encoded_message[0:][::-1]
    for group in encoded_message:
        group = decrypt(group, d, n)
        for i in range(5):
            num = group % 37
            group = group // 37
            if(num == 36):
                message = ' ' + message
            elif(num < 10):
                message = chr(ord('0') + num) + message
            else:
                message = chr(ord('a') + num - 10) + message
    return message

