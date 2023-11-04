import socket
import time
import threading
import logging
import concurrent.futures

database = ['#']*1000
count = 1000
line = '#'
lineNumber = -1


def meshServer(port):
    # get the hostname
    global line,lineNumber
    host = "0.0.0.0"
    # port = 15000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(3)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        y = data.split()
        if  y[0].isdigit() and (int(y[0])-1) <1000 and database[int(y[0])-1] == '#':
            status = 'OK'
        # elif data[0] == 'U':
        #     data = data[1:]
        #     status = 'OK'
        else:
            status = 'NOT OK'
        conn.send(status.encode())
        if status == 'OK':
            count -=1
            if(count == 0):
                break
            data2 = conn.recv(1024).decode()
            #z =data2.split()
            database[int(data)-1] = data2
            # if data is not received break
            # message = 'DONE'
            # conn.send(message.encode())
            
            print("Received from connected user: " + y[0])

        # data = input(' -> ')
        # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


def meshClient(connIP, port2):
    #CAUTION : HANDLE RACE CONDITIONS
    # get the hostname
    print("Connecting to ",connIP)
    global count,lineNumber, line
    host = connIP # PEER SERVER's IP
    port = port2  # initiate port no above 1024

    client_socket = socket.socket()
    client_socket.connect((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneousl
    while True:
        # print(lineNumber)
        # print(line)
        # receive data stream. it won't accept data packet greater than 1024 bytes
        if(count == 0):
            break
        if(lineNumber != -1 and ord(lineNumber[0]) >= 48 and ord(lineNumber[0]) <= 57):
            client_socket.send(lineNumber.encode())
            data = client_socket.recv(10485763).decode()  # receive response
            # PROTOCOL:  
            if(data=="OK"):
                client_socket.send(line.encode())
                print("Successfully submitted line number : ", lineNumber)
    client_socket.close()  # close the connection


def connectVayu():

    global line, lineNumber,count,database
    local = socket.socket()
    host = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((host,9801))
    print("Connected to Vayu")
    message = "SENDLINE\n"
    start = time.time()
    while True:
        local.send(message.encode())  # send message
        data = local.recv(1048577).decode()  # receive response
        y = data.split()
        # print(count)
        if count == 0:
            break
        if ord(data[0])<48 or ord(data[0])>57:
            # lines[prev]+=data
            continue
        if y[0].isdigit() and (int(y[0])-1) <1000 and database[int(y[0])-1] == '#':
            prev = int(y[0])-1
            print('Received from server: ' + y[0])  #show in terminal
            count -= 1
            print(count,time.time()-start)
            database[int(y[0])-1] = data
        lineNumber = y[0]
        line = y[1]
            

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    clientConn1 = threading.Thread(target=meshClient, args=("10.194.23.104",15006, ))
    clientConn2 = threading.Thread(target=meshClient, args=("10.194.52.189",15003, ))
    #clientConn3 = threading.Thread(target=meshClient, args=("ip3","port3", ))

    # serverConn1 = threading.Thread(target=meshServer, args=(15000, ))
    serverConn2 = threading.Thread(target=meshServer, args=(15001, ))
    serverConn3 = threading.Thread(target=meshServer, args=(15004, ))

    vayuConn = threading.Thread(target=connectVayu, args=())
    vayuConn.start()
    clientConn1.start()
    clientConn2.start()
    #clientConn3.start()
    # serverConn1.start()
    serverConn2.start()
    serverConn3.start()

    