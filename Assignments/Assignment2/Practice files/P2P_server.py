import socket
import time
import threading
import logging
import concurrent.futures

database = ['#']*1000
count = 1000

def server_program(port):
    # get the hostname
    global arr
    host = "0.0.0.0"
    # port = 15000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(4)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if arr[int(data)-1] == '':
            status = 'OK'
        elif data[0] == 'U':
            data = data[1:]
            status = 'OK'
        else:
            status = 'NOT OK'
        conn.send(status.encode())
        if status == 'OK':
            data2 = conn.recv(1024).decode()
            arr[int(data)-1] = data2
            # if data is not received break
            message = 'DONE'
            conn.send(message.encode())
            break
        # print("from connected user: " + str(data))
        # data = input(' -> ')
        # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection



# if __name__ == '__main__':
#     server_program(15000)

def connectVayu():
    local = socket.socket()
    host = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((host,9801))
    message = "SENDLINE\n"
    start = time.time()
    while True:
        local.send(message.encode())  # send message
        data = local.recv(1048577).decode()  # receive response
        y = data.split()
        # print(count)
        if count == 1000: 
            break
        if ord(data[0])<48 or ord(data[0])>57:
            # lines[prev]+=data
            continue
        if database[int(y[0])-1] == '#':
            prev = int(y[0])-1
            # print('Received from server: ' + data)  # show in terminal
            count -= 1
            print(count,time.time()-start)
            database[int(y[0])-1] = data


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(server_program, range(2))