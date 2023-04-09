import socket
import threading
import math
import rsa


def generate_keys():
    primes = rsa.generate_primes(1000)
    
    # Generate a public/ private key pair using 1024 bits key length (128 bytes)
    new_key = rsa.generate(1024, e=65537)
    # The private key in PEM format
    private_key = new_key.exportKey("PEM")
    # The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")
    return public_key, private_key

def encrypt_message(message, public_key):
    # Encrypt the message with the public RSA key
    crypto = rsa.encrypt(message, public_key)
    return crypto

def decrypt_message(crypto, private_key):
    # Decrypt the message with the private RSA key
    message = rsa.decrypt(crypto, private_key)
    return message

def send_message(sock, message):
    # Send the message through the socket
    sock.send(message)

def receive_message(sock):
    # Receive the message from the socket
    message = sock.recv(1024)
    return message

def connect_to_server():
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((' ', 5000))

def RSA():
