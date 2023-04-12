import math
import random as rd
import sympy as sp
import numpy as np
import os
import time
import matplotlib.pyplot as plt



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
        p = rd.randint(69343956, 69343956*1000000)  # best min number for p & q to be secure enough --> 1048576
    while(sp.isprime(q) == False or p == q):
        q = rd.randint(69343956, 69343956*1000000)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # select integer e that is relatively prime to n and ranges 1 < e < n
    e = phi # initial value so that the loop runs at least once
    while(math.gcd(e, phi) != 1):
        e = rd.randint(2, phi)  # the public key is (e, n)
    
    # calculate d such that d * e = 1 mod phi
    d = multiplicative_inverse(e, phi) # the private key is (d, n)
    return e, d, n


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

def decode_decrypt_group_message(group, d, n):
    message = ""
    #encoded_message[0:] = encoded_message[0:][::-1]
    #for group in encoded_message:
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



# the following functions are used to analyze the speed of the encryption and decryption algorithms
# and to analyze the security of the encryption algorithm


def factorize_n(n):
    # get the prime factorizatoin of n
    a = sp.factorint(n)
    return a


def _generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # select integer e that is relatively prime to n and ranges 1 < e < n
    e = phi # initial value so that the loop runs at least once
    while(math.gcd(e, phi) != 1):
        e = rd.randint(2, phi)  # the public key is (e, n)
    # calculate d such that d * e = 1 mod phi
    d = multiplicative_inverse(e, phi) # the private key is (d, n)
    return e, d, n


def generate_pq_for_n_bits(large_n_bits):
    # if the file already exists, delete it
    try:
        os.remove("n_e_d.txt")
    except OSError:
        pass
    #n_bits = []
    n_bits_min = 0
    n_bits_max = 0
    if(large_n_bits == True):
        n_bits_min = 27
        n_bits_max = 1024
        #n_bits = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    else:
        n_bits_min = 27
        n_bits_max = 64
        #n_bits = [8, 16, 32, 64]
    for bit in range(n_bits_min, n_bits_max):  #, 32, 64, 128, 256, 512, 1024, 2048, 4096
        p = 4
        q = 4
        mini = 2 ** (bit - 1)
        while(sp.isprime(p) == False or p < mini):
            p = rd.getrandbits(bit)
        while(sp.isprime(q) == False or p == q or q < mini):
            q = rd.getrandbits(bit)
        
        e, d, n = _generate_keys(p, q)
        # write in the file the p, q, n in addition to the bit and the private key d
        with open("n_e_d.txt", "a") as f:
            f.write("n: " + str(n) + " e: " + str(e) + " d: " + str(d) + " bit: " + str(bit) + "\n")


def plot_to_analyze(filepath, title, time_unit):
    # plot the data in the file
    with open(filepath, "r") as f:
        data = f.readlines()
        x = []
        y = []
        for line in data:
            x.append(int(line.split(" ")[1]))
            if time_unit == "s":
                y.append(float(line.split(" ")[-1]))
            else:
                y.append((10.0**3)*float(line.split(" ")[-1]))
        plt.plot(x, y)
        plt.xlabel("n bits")
        if(time_unit == "s"):
            plt.ylabel("time (s)")
        else:
            plt.ylabel("time (ms)")
        plt.title(title)
        plt.show()