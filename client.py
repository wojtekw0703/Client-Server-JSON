import socket
import json
from sys import exit

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input
    while message.lower().strip() != 'stop':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        json_object = json.loads(data)
        print('Received from server: ', json_object)  # show in terminal
        message = input(" -> ")  # again take input
        
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()