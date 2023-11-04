import socket
import time
import threading
import logging
import concurrent.futures

line = '#'
lineNumber = -1
count = 'ququ'
def serverConnect(port2):
    # get the hostname
    global count
    host = "10.184.59.147" # shankh's IP
    port = port2  # initiate port no above 1024

    client_socket = socket.socket()  
    client_socket.connect((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneousl
    while True:
        # print(lineNumber)
        # print(line)
        # receive data stream. it won't accept data packet greater than 1024 bytes
        if(lineNumber != -1 and ord(lineNumber[0]) >= 48 and ord(lineNumber[0]) <= 57):
            client_socket.send(lineNumber.encode())
            data = client_socket.recv(10485763).decode()  # receive response
            # if(data=="CC"):

            #     break
            if(data=="OK"):
                client_socket.send(line.encode())

                # data = client_socket.recv(10485763).decode()  # receive response
                # if(data=="DONE"):
                print("Successfully submitted line number : ", lineNumber)
    client_socket.close()  # close the connection


def connectVayu():
    global line, lineNumber
    local = socket.socket()
    host = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((host,9801))
    message = "SENDLINE\n"
    start = time.time()
    while True:
        if(count=="CC"):
            break
        local.send(message.encode())  # send message
        data = local.recv(1048577).decode()  # receive response
        y = data.split()
        # print(count)
        if ord(data[0])<48 or ord(data[0])>57:
            # lines[prev]+=data
            continue
        prev = int(y[0])-1
        #print('Received from server: ')  # show in terminal

        #print(time.time()-start)
        #dataArray  = data.split()
        lineNumber = y[0]
        line = y[1]


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    serverThread = threading.Thread(target=serverConnect, args=(15000, ))
    serverThread.start()
    VayuThread = threading.Thread(target = connectVayu)
    VayuThread.start()
    serverThread.join()
    VayuThread.join()
