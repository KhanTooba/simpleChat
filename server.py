import socket
import os
from _thread import *
import threading
from protocol import getProtocolID


toSend = {}
toRecv = {}

def sending(connection, username):
    print("Entered the sending funtion.")
    connection.send("Begin sending.".encode())
    while True:
        msg = connection.recv(2048).decode()
        parts = msg.split(" ")
        # print(parts)
        # print(len(parts))
        if len(parts)>=5 and "SEND" in parts[0]:
            recepient = parts[1]
            length = int(parts[3])
            actual_msg = " ".join(parts[4:])
            if "all" in recepient:
                print("Broadcasting.")
                for name, sendConnect in toRecv.items():
                    # print(name, ":", sendConnect)
                    try:
                        sendingConnection = sendConnect
                        msgToForward = "FORWARD "+username+" Content-length: "+str(length)+" "+actual_msg
                        sendingConnection.send(msgToForward.encode())
                        replyFromRecepient = sendingConnection.recv(2048).decode()
                        if "RECEIVED" in replyFromRecepient:
                            connection.send(str.encode("SENT "+recepient))
                        else:
                            connection.send(str.encode(replyFromRecepient))
                    except:
                        print("Username not found.")
                        connection.send("ERROR 102 Unable to send".encode())
            else:
                try:
                    sendingConnection = toRecv[recepient]
                    msgToForward = "FORWARD "+username+" Content-length: "+str(length)+" "+actual_msg
                    sendingConnection.send(msgToForward.encode())
                    replyFromRecepient = sendingConnection.recv(2048).decode()
                    if "RECEIVED" in replyFromRecepient:
                        connection.send(str.encode("SENT "+recepient))
                    else:
                        connection.send(str.encode(replyFromRecepient))
                except:
                    print("Username not found.")
                    connection.send("ERROR 102 Unable to send".encode())
        else:
            connection.send("ERROR 102 Unable to send message defected".encode())
    return 0

def threaded_client(connection):
    # connection.send(str.encode('Welcome to the Server.'))
    # print("Entering")
    sendingEnabled = -1
    username = ""
    while True:
        data = connection.recv(2048).decode()
        protocol, username = getProtocolID(data.split(" ")[0]), data.split(" ")[1]
        if protocol==0 and username.isalnum()==True:
            reply = "REGISTERED_TOSEND "
            connection.sendall(str.encode(reply))
            toSend[username]=connection
            sendingEnabled = 1
        elif protocol==2 and username.isalnum()==True:
            reply = "REGISTERED_TORECV "
            connection.sendall(str.encode(reply))
            toRecv[username]=connection
        else:
            if username.isalnum()==False:
                connection.sendall(str.encode("ERROR 100 Malformed username"))
            else:
                connection.sendall(str.encode("ERROR 101 No user registered"))
            continue
        data = connection.recv(2048).decode()
        if "Ending" in data:
            break
    # connection.close()
    print("Send and recv connections established.")
    if sendingEnabled==1:
        sending(connection, username)

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1283

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

clientThreads = []
ThreadCount = 0

while True:  
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        t1 = threading.Thread(target=threaded_client, args=(Client,))
        t1.start()
        # ThreadCount += 1

# callingmain()
ServerSocket.close()