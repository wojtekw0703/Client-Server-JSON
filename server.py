import datetime
import socket
import time
from sys import exit
import psycopg2
from psycopg2 import Error
from concurrent.futures import ThreadPoolExecutor

created = datetime.datetime.now()
start = time.perf_counter()

command_handlers = {
    "uptime": uptime_fun,
    "info": info_fun,
    "read_msg": read_messages,
}


operation_database = {
    "read": read_data,
    "insert": insert_data,
}


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
    server_program()


def info_fun():
    print("created: {0}".format(str(created)) + "\n")

    server_program()


def read_messages():
    query = """SELECT login, message_content FROM messages"""
    cursor.execute(
        query,
    )
    messages = cursor.fetchall()
    for data in messages:
        print(data)
    print("\n")
    server_program()


def admin_dashboard():
    print(
        "--------ADMIN PANEL--------\n",
        "option 1: uptime - returns server lifetime\n",
        "option 2: info - returns the date the server was created\n",
        "option 3: read_msg - displays all messages and their senders",
    )
    option = input("->")
    if option.lower() not in ["uptime", "info", "read_msg"]:
        print("Not known command")
        server_program()
    else:
        redirection = command_handlers.get(option.lower(), "Invalid command")
        redirection()


def read_data():
    pass


def insert_data(data):
    query = """INSERT INTO messages(login, message_content) VALUES (%s, %s)"""
    cursor.execute(
        query,
        (data[1], data[2]),
    )
    connection.commit()
    print("New message !")


def receive_query():
    while True:
        data = None
        data = server_socket.recv(1024).decode()
        if data is not None:
            redirection = operation_database.get(data[0].lower(), "Invalid command")
            redirection(data)


def server_program():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(admin_dashboard())
        executor.submit(receive_query())

    cursor.close()
    conn.close()


if __name__ == "__main__":
    connect_database()
    init_connection()
    print("Connection from: " + str(address))
    server_program()
