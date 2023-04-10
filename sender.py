import socket
import threading
import math
import RSA as rsa
import receiver as rc


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server

global es, ns

es, d, ns = rsa.generate_keys()

def initiate_connection():
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    return sock

def send_message(receiver):
    # Send the message through the socket
    #receiver, addr = sock.accept()
    while True:
        msg = input()
        toSend = rsa.encode_encrypt_message(msg, rc.er, rc.nr)
        for i in range(len(toSend)):
            toSend[i] = toSend[i].__str__()
        toSend = "".join(toSend)
        receiver.send(toSend.encode())


def receive_message(receiver):
    # Receive the message from the socket
    #receiver, addr = sock.accept()
    while True: 
        cipher = receiver.recv(1024)
        cipher = cipher.decode()
        cipher = cipher.split(" ")
        print("message after splitting: ", cipher)
        for i in range(len(cipher)):
            cipher[i] = int(cipher[i])
        message = rsa.decode_decrypt_message(cipher, d, ns)
        # TODO: apply the decryption function to the received message
        print(message)


    

if __name__ == "__main__":
    # we will have 2 threads
    # one for sending messages
    # one for receiving messages

    sock = initiate_connection()
    receiver, addr = sock.accept()
    
    # TODO: apply the encryption function to the message before sending it
    send_thread = threading.Thread(target=send_message, args=(receiver, ))
    send_thread.start()
    
    
    receive_thread = threading.Thread(target=receive_message, args=(receiver, )) # to keep the return value of the function, 
    receive_thread.start()
    
    

    # wait for the return value of the function
    #send_thread.join()

    # wait for the return value of the function
    #receive_thread.join()
    #received_message = receive_thread.result()
    

 


    


    
    # if I want to send a message to the server
    # take the message from the user
    




