import json
import pprint
import socket
import time
from sys import exit

from tinydb import Query, TinyDB

db_user = TinyDB("D:/IT/python/SocketApp/user_database.json")
table_user = db_user.table("users")
User = Query()

db_message = TinyDB("D:/IT/python/SocketApp/message_database.json")
message_user = db_message.table("messages")

host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server


def msg_read(login):
    pprint.pprint(message_user.search(User.login == login))
    user_dashboard(login)


def msg_send(login):
    while True:
        msg = input("Type message ->")[:255]
        dictionary = {"login:": login, "message:": msg}
        result = json.dumps(dictionary)  # converting object into a json string
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
    user_mode()
    client_socket.close()  # close the connection


if __name__ == "__main__":
    client_program()
