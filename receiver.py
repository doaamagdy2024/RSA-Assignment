import socket
import threading
import math

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9090        # The port used by the server


def initiate_connection():
    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    #sock.listen()
    return sock

def send_message(sock):
    # Send the message through the socket
    while True:
        toSend = input()
        sock.send(toSend.encode())
        #sock.send(message)

def receive_message(sock):
    # Receive the message from the socket
    while True:
        message = sock.recv(1024)
        print(message.decode())

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
    




