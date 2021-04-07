import json
import pprint
import socket
import time
from sys import exit


def connect_with_server():
    host = socket.gethostname()
    port = 5000
    global client_socket
    client_socket = socket.socket()
    client_socket.connect((host, port))


def msg_read(login):
    query = "SELECT message_content FROM messages WHERE login = %s"
    cursor.execute(query, (login,))
    result = cursor.fetchall()
    print(result)
    user_dashboard(login)


def msg_send(login):
    while True:
        msg = input("Type message ->")[:255]
        dictionary = {"login:": login, "message:": msg}
        result = json.dumps(dictionary)
        client_socket.send(result.encode())

        message_user.insert({"login": login, "message": msg})
        user_dashboard(login)


def user_dashboard(login):
    if message_user.count(User.login == login) > 5:
        print(f"{login} - inbox overflow \n")
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
    print("Create | Login")
    option = input("->")
    print("\n")

    if option.lower() == "create":
        print("New user - login")
        new_login = input("->")
        print("\n")

        print("New user - password")
        new_password = input("->")
        print("\n")

        table_user.insert({"login": new_login, "password": new_password})
        user_mode()

    elif option.lower() == "login":
        print("Login:")
        login = input("->")
        print("\n")

        print("Password:")
        password = input("->")
        print("\n")

        if table_user.contains(User.login == login) and table_user.contains(
            User.password == password
        ):
            user_dashboard(login)
        else:
            print("Error")
            time.sleep(2)
            user_mode()


def client_program():
    connect_with_server()
    user_mode()
    client_socket.close()  # close the connection


if __name__ == "__main__":
    client_program()
