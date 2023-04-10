import socket
import threading
import math
import RSA as rsa

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


def send_message(sock):
    # Send the message through the socket
    # receive es and ns from the server
    ns = int(sock.recv(1024).decode())
    es = int(sock.recv(1024).decode())
    while True:
        message = input()
        toSend = rsa.encode_encrypt_message(message, es, ns)
        for i in range(len(toSend)):
            toSend[i] = toSend[i].__str__()
        toSend = " ".join(toSend)
        print("encrypt using e = ", es, " and n = ", ns)

        sock.send(toSend.encode())
        #sock.send(message)


def receive_message(sock):
    # Receive the message from the socket
    # send e and n to the server
    sock.send(str(nr).encode())
    sock.send(str(er).encode())
    while True:
        cipher = sock.recv(1024)
        cipher = cipher.decode()
        cipher = cipher.split(" ")
        print("message after splitting: ", cipher)
        for i in range(len(cipher)):
            cipher[i] = int(cipher[i])
        print("cipher to int: ", cipher)
        message = rsa.decode_decrypt_message(cipher, d, nr)
        print("decrypt using d = : ",d, " and n = ", nr)
        print(message)



if __name__ == "__main__":
    # we will have 2 threads
    # one for sending messages
    # one for receiving messages

    print('the generated keys are: e = ', er, " d = ",  d, " nr = ", nr)
    sock = initiate_connection()

    
    # TODO: apply the encryption function to the message before sending it
    send_thread = threading.Thread(target=send_message, args=(sock,))
    send_thread.start()
    

    receive_thread = threading.Thread(target=receive_message, args=(sock, )) # to keep the return value of the function, 
    receive_thread.start()
    