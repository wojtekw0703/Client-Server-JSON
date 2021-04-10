import socket
import pickle
import time
from sys import exit
from concurrent.futures import ThreadPoolExecutor


def connect_with_server():
    host = socket.gethostname()
    port = 5000
    global client_socket
    client_socket = socket.socket()
    client_socket.connect((host, port))


def msg_read(login):
    pass


def msg_send(login):
    pass


def user_dashboard(login):
    # request to the server to check if the inbox is overflowed:
    # code
    user_mode()
    print("Send message (msg-send) | Read message (msg-read)")
    option = input("->")

    if option.lower() == "msg-send":
        msg_send(login)
    elif option.lower() == "msg-read":
        msg_read(login)
    else:
        exit(0)


def user_mode():
    data = []
    print("Create | Login")
    option = input("->")
    print("\n")

    if option.lower() == "create":
        print("New user - enter login")
        new_login = input("->")
        print("\n")

        print("New user - enter password")
        new_password = input("->")
        print("\n")

        data.append("insert_person")
        data.append(new_login)
        data.append(new_password)

        to_send = pickle.dumps(data)
        client_socket.send(to_send.encode())

        user_mode()

    elif option.lower() == "login":
        print("Login:")
        login = input("->")
        print("\n")

        print("Password:")
        password = input("->")
        print("\n")

        # send data to server + condition
        # code
        user_dashboard(login)
    else:
        print("Error")
        time.sleep(2)
        user_mode()


def receive_data_from_server():
    while client_socket.recv(1024).decode() is None:
        data = client_socket.recv(1024).decode()


def client_program():
    user_mode()
    client_socket.close()


if __name__ == "__main__":
    connect_with_server()
    client_program()
