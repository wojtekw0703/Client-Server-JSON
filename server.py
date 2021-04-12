import datetime
import socket
import time
from sys import exit
import psycopg2
from psycopg2 import Error
from concurrent.futures import ThreadPoolExecutor

created = datetime.datetime.now()
start = time.perf_counter()


def connect_database():
    try:
        global connection, cursor
        connection = psycopg2.connect(
            host="127.0.0.1",
            database="client_server_database",
            user="postgres",
            password="postgres",
        )
        cursor = connection.cursor()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL database:", error)


def init_connection():
    host = socket.gethostname()
    port = 5000
    global conn, address, server_socket
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()


def uptime_fun():
    end = time.perf_counter()
    duration = end - start
    duration = round(duration, 2)
    print("life time: {0}s".format(str(duration)) + "\n")
    # display_admin_panel()


def info_fun():
    print("created: {0}".format(str(created)) + "\n")
    # display_admin_panel()


def read_messages_as_admin():
    query = """SELECT login, message_content FROM messages"""
    cursor.execute(
        query,
    )
    messages = cursor.fetchall()
    for data in messages:
        print(data)
    print("\n")
    # display_admin_panel()


# def display_admin_panel():
#     print(
#         "--------ADMIN PANEL--------\n",
#         "option 1: uptime - returns server lifetime\n",
#         "option 2: info - returns the date the server was created\n",
#         "option 3: read_msg - displays all messages and their senders",
#         "option 4: stop - end of program working",
#     )
#     option = input("->")
#     return option


def admin_dashboard():
    # option = display_admin_panel()
    # while option not in ["uptime", "info", "read_msg"]:
    #     option = display_admin_panel()
    # redirection = command_handlers.get(option.lower(), "Invalid command")
    # redirection()
    while True:
        print(
            "--------ADMIN PANEL--------\n",
            "option 1: uptime - returns server lifetime\n",
            "option 2: info - returns the date the server was created\n",
            "option 3: read_msg - displays all messages and their senders\n",
            "option 4: stop - end of program working",
        )
        option = input("->")
        if option.lower == "stop":
            exit(1)
        else:
            redirection = command_handlers.get(option.lower(), "Invalid command")
            redirection()


def check_inbox(login):
    query = """SELECT COUNT(login) FROM messages WHERE login = %s"""
    cursor.execute(
        query,
        login,
    )
    result = cursor.fetchone()
    connection.commit()
    if result < 5:
        return True
    return False


def check_user(data):
    query = """SELECT login, passwd FROM users WHERE login = %s AND passwd = %s"""
    cursor.execute(
        query,
        data[0],
        data[1],
    )
    result = cursor.fetchone()

    if result is not None:
        msg = "OK"
        conn.send(msg.encode())


def read_message(data):
    if check_inbox(data[0]):
        query = """SELECT message_content FROM messages WHERE login = %s"""
        cursor.execute(
            query,
            data[0],
        )
        result = cursor.fetchall()
    result = "{0} - inbox overflow !".format(data[0])
    conn.send(result.encode())
    connection.commit()


def insert_message(data):
    query = """INSERT INTO messages(login, message_content) VALUES (%s, %s)"""
    cursor.execute(
        query,
        (data[0], data[1]),
    )
    connection.commit()


def insert_person(data):
    query = """INSERT INTO users(login, passwd) VALUES (%s, %s)"""
    cursor.execute(
        query,
        (data[0], data[1]),
    )
    connection.commit()


command_handlers = {
    "uptime": uptime_fun,  # returns the server life time
    "info": info_fun,  # returns date when the server was created
    "read_msg": read_messages_as_admin,  # displays all messages from user's inbox
}

database_operations = {
    "check_user": check_user,  # if any user wants to log in, server checks if user is already in database
    "read_message": read_message,  # if any user want to read a message - retrieve all messages for specific user
    "insert_message": insert_message,  # if any user send a message - insert to database
    "insert_person": insert_person,  # if client created a new user - add to database
}


def receive_query_from_client():
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = server_socket.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        # print("Command from connected user: " + str(data))
        # if data == "stop":
        #     exit(0) # stop server app
        else:
            redirection = database_operations.get(data[0].lower(), "Invalid command")
            redirection(data[1::])


def server_program():
    connect_database()
    init_connection()
    print("Connection from: " + str(address))
    admin_dashboard()

    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(receive_query_from_client())

    cursor.close()
    conn.close()


if __name__ == "__main__":
    server_program()
