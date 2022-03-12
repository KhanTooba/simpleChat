import socket
import sys
import threading

def sending(connection):
    print(connection.recv(1024))
    while True:
        msg=""
        while len(msg.split(" "))<3:
            msg=input("Enter the message to send:")
        parts = msg.split(" ")
        if parts[0]=="@":
            msgToSend = "SEND "+parts[1]+" Content-length: "+str(len(" ".join(parts[2:])))+" "+" ".join(parts[2:])
            connection.sendall(msgToSend.encode())
            reply = connection.recv(2048).decode()
            print(reply)
        else:
            print("\nThe message format enetered by you is wrong. Please enter the message in correct format.\
                The correct format is: @ [recipient username] [message].")
    return 0

def receiving(connection):
    while True:
        dataRecvd = connection.recv(1024).decode()
        # print("\nReceived: ",dataRecvd)
        parts = dataRecvd.split(" ")
        print("\nReceived: "," ".join(parts[4:]))
        # print(parts)
        if len(parts)>=5 and "FORWARD" in parts[0]:
            connection.send("RECEIVED".encode())
            print("Enter the message to send:")
        else:
            connection.send("\nERROR 103 Header Incomplete".encode())
    return 0




ClientSocketSend = socket.socket()
ClientSocketRecv = socket.socket()
host = sys.argv[1]
port = 1283

print('Waiting for connection')
try:
    ClientSocketSend.connect((host, port))
    ClientSocketRecv.connect((host, port))
except socket.error as e:
    print(str(e))

Input = sys.argv[2]

# Response = ClientSocket.recv(1024)
while True:
    ClientSocketSend.send(str.encode("REGISTER_TOSEND "+Input))
    Response = ClientSocketSend.recv(1024)
    print(Response.decode('utf-8'))
    if "REGISTERED_TOSEND" in Response.decode():
        ClientSocketRecv.send(str.encode("REGISTER_TORECV "+Input))
        Response = ClientSocketRecv.recv(1024)
        print(Response.decode('utf-8'))
        if "REGISTERED_TORECV" in Response.decode():
            print("BINGO! Registered for both.")
            ClientSocketRecv.send("Ending".encode())
            ClientSocketSend.send("Ending".encode())
            break
    else:
        Input = input('What is your username? ')
        # print("Continuing")
        continue



t2 = threading.Thread(target=sending, args=(ClientSocketSend,))
t2.start()
t1 = threading.Thread(target=receiving, args=(ClientSocketRecv,))
t1.start()

# ClientSocketSend.close()
# ClientSocketRecv.close()