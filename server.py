import socket
import json
import time
from sys import exit
from tinydb import TinyDB,Query
import datetime

db_user = TinyDB('D:/IT/python/SocketApp/user_database.json')
table_user = db_user.table('users')

# Launch program date
created = datetime.datetime.now() 
start = time.perf_counter() 


# get the hostname
host = socket.gethostname()
port = 5000  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together
server_socket.listen(2)
conn, address = server_socket.accept()  

def msg_read(login):
    pass

def msg_send(login):
    pass

def user_dashboard(login):
    print("Send message (msg-send) | Read message (msg-read)")
    option = input("->")
    if option.lower() == "msg-send":
        msg_send(login)
    elif option.lower() == "msg-read":
        msg_read(login)


def uptime_fun(): 
    end = time.perf_counter()
    duration = end-start
    duration = round(duration,2)
    dictionary = {
        "life time:" : str(duration) +"s"
    }
    result = json.dumps(dictionary) # converting object into a json string
    return result


def info_fun():  
    dictionary = {
        "created:" : str(created)
    }
    result = json.dumps(dictionary)
    return result


def help_fun(): 
    dictionary = {
        "options: " :     
        {
            "option 1": "uptime - zwraca czas zycia serwera",
            "option 2": "info - zwraca date utworzenia serwera",
            "option 3": "stop - zatrzymuje serwer i klienta",
            "option 4": "msg-read - read all messages",
            "option 5": "msg-send - send a message" 
        }
    }
    result = json.dumps(dictionary)
    return result

# switch-case declaration
switcher = {
    "uptime":  uptime_fun,
    "info":  info_fun,
    "help":  help_fun,
    "msg-read":  msg_read,
    "msg-send":  msg_send,
    }


def user_mode():
    print("Create | Login")
    option = input("->")
    if option.lower()=="create":
        print("New user - login")
        new_login = input("->")
       
        print("New user - password")
        new_password = input("->")
       
        table_user.insert({'login': new_login, 'password': new_password})
        user_mode()

    elif option.lower()=="login":
        print("Login:")
        login = input("->")
       
        print("Password:")
        password = input("->")
       
        user_existing = db_user.search((login == login) & (password == password))
        if not user_existing:
            print("Error")
            time.sleep(2)
            user_mode()
        else:
            user_dashboard(login)    



def admin_mode():
    pass




def server_program():
    print("Connection from: " + str(address))
    
    print("User | Admin ?")
    mode = input("->")
    
    if mode.lower()=="user":
        user_mode()
    elif mode.lower()=="admin":
        admin_mode()
    
    #conn.close()  # close the connection

   
if __name__ == '__main__':
    server_program() 