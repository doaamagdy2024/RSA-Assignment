import socket
import threading
import math
import RSA as rsa


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server


nr = 0
er = 0

es, d, ns = rsa.generate_keys()


def initiate_connection():
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    return sock


def send_message(receiver, semaphore):
    # Send the message through the socket
    # first get the n and e from the receiver
    nr = int(receiver.recv(1024).decode())
    er = int(receiver.recv(1024).decode())
    semaphore.set()
    while True:
        msg = input()
        toSend = rsa.encode_encrypt_message(msg, er, nr)
        for i in range(len(toSend)):
            toSend[i] = toSend[i].__str__()
        toSend = " ".join(toSend)
        print("toSend: ", toSend)
        print("encrypt using e = ", er, " and n = ", nr)
        receiver.send(toSend.encode())


def receive_message(receiver, semaphore):
    # Receive the message from the socket
    # first send the n and e to the receiver
    receiver.send(str(ns).encode())
    receiver.send(str(es).encode())
    while(semaphore.is_set() == False):
        continue
    while True: 
        cipher = receiver.recv(1024)
        cipher = cipher.decode()
        cipher = cipher.split(" ")
        print("message after splitting: ", cipher)
        for i in range(len(cipher)):
            cipher[i] = int(cipher[i])
        message = rsa.decode_decrypt_message(cipher, d, ns)
        print("decrypt using d = : ",d, " and n = ", ns)

        # TODO: apply the decryption function to the received message
        print(message)


    

if __name__ == "__main__":
    # we will have 2 threads
    # one for sending messages
    # one for receiving messages

    print('the generated keys are: e = ', es, " d = ",  d, " nr = ", ns)
    sock = initiate_connection()
    receiver, addr = sock.accept()

    semaphore = threading.Event()
    semaphore.clear()

    send_thread = threading.Thread(target=send_message, args=(receiver,semaphore, ))
    send_thread.start()
    
    
    receive_thread = threading.Thread(target=receive_message, args=(receiver, semaphore, )) # to keep the return value of the function, 
    receive_thread.start()