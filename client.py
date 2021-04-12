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
    data_to_send = "read_message" + "-" + login
    client_socket.send(data_to_send.encode())
    messages = receive_data_from_server()
    for data in messages:
        print(data)


def msg_send(login):
    message = input("Enter a message -> ")
    data_to_send = "insert_message" + "-" + message + "-" + login
    client_socket.send(data_to_send.encode())


def user_dashboard(login):
    print("Send message (msg-send) | Read message (msg-read)")
    option = input("->")

    if option.lower() == "msg-send":
        msg_send(login)
    elif option.lower() == "msg-read":
        msg_read(login)


def user_mode():
    data_to_send = ""

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

        data_to_send = "insert_person" + "-" + new_login + "-" + new_password
        client_socket.send(data_to_send.encode())

        user_mode()

    elif option.lower() == "login":
        print("Login:")
        login = input("->")
        print("\n")

        print("Password:")
        password = input("->")
        print("\n")

        data_to_send = "check_user" + "-" + login + "-" + password
        client_socket.send(data_to_send.encode())

        result = receive_data_from_server()
        if result == "True":
            user_dashboard(login)
        else:
            user_mode()
    else:
        print("Error")
        time.sleep(2)
        user_mode()


def receive_data_from_server():
    while client_socket.recv(1024).decode() is None:
        data = client_socket.recv(1024).decode()
    return data


def client_program():
    connect_with_server()
    user_mode()
    client_socket.close()


if __name__ == "__main__":
    client_program()
