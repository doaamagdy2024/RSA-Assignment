import socket
import threading
import math
import RSA as rsa
import sender as sd

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server

global er, nr

er, d, nr = rsa.generate_keys()


def initiate_connection():
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    #sock.listen()
    return sock

def send_message(sock):
    # Send the message through the socket
    while True:
        message = input()
        toSend = rsa.encode_encrypt_message(message, sd.es, sd.ns)
        for i in range(len(toSend)):
            toSend[i] = toSend[i].__str__()
        toSend = "".join(toSend)
        sock.send(toSend.encode())
        #sock.send(message)

def receive_message(sock):
    # Receive the message from the socket
    while True:
        cipher = sock.recv(1024)
        cipher = cipher.decode()
        cipher = cipher.split(" ")
        print("message after splitting: ", cipher)
        for i in range(len(cipher)):
            cipher[i] = int(cipher[i])
        message = rsa.decode_decrypt_message(cipher, d, nr)
        print(message)

    return message


    

if __name__ == "__main__":
    # we will have 2 threads
    # one for sending messages
    # one for receiving messages

    sock = initiate_connection()
    

    
    # TODO: apply the encryption function to the message before sending it
    send_thread = threading.Thread(target=send_message, args=(sock,))
    send_thread.start()
    

    receive_thread = threading.Thread(target=receive_message, args=(sock, )) # to keep the return value of the function, 
    receive_thread.start()
    
    

    # wait for the return value of the function
    #send_thread.join()

    # wait for the return value of the function
    #receive_thread.join()
    #received_message = receive_thread.result()
    # TODO: apply the decryption function to the received message

 


    


    
    # if I want to send a message to the server
    # take the message from the user
    




