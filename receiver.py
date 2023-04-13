import socket
import threading
import math
import RSA as rsa
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server

global ns, es
ns = 0
es = 0

er, d, nr = rsa.generate_keys()


def initiate_connection():
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


def send_message(sock, semaphore):
    # Send the message through the socket
    # but first receive es and ns from the server to encrypt the message with them
    ns = int(sock.recv(1024).decode())
    es = int(sock.recv(1024).decode())
    semaphore.set()
    while True:
        message = input()
        toSend = rsa.encode_encrypt_message(message, es, ns)
        for i in range(len(toSend)):
            toSend[i] = toSend[i].__str__()
            sock.send(toSend[i].encode())
            time.sleep(0.001)
        # then send new line
        sock.send("\n".encode())



def receive_message(sock, semaphore):
    # Receive the message from the socket
    # send e and n to the server to encrypt the message with them
    sock.send(str(nr).encode())
    sock.send(str(er).encode())
    while(semaphore.is_set() == False):
        continue
    while True:
        cipher = sock.recv(1024)
        cipher = cipher.decode()
        message = "> "
        while(cipher != '\n'):
            cipher = int(cipher)
            message += rsa.decode_decrypt_group_message(cipher, d, nr)
            cipher = sock.recv(1024)
            cipher = cipher.decode()

        print(message)



if __name__ == "__main__":
    # we will have 2 threads
    # one for sending messages
    # one for receiving messages

    sock = initiate_connection()

    # semaphore = threading.Semaphore(1)
    semaphore = threading.Event()
    semaphore.clear()

    send_thread = threading.Thread(target=send_message, args=(sock, semaphore, ))
    send_thread.start()
    

    receive_thread = threading.Thread(target=receive_message, args=(sock, semaphore, )) # to keep the return value of the function, 
    receive_thread.start()
    