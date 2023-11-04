import socket
import time
import threading
import multiprocessing
import logging

database = ['#']*1000
count = 1000
HOST = "0.0.0.0"

def server_program(conn):
    global database
    global count

    conn.send("START".encode())

    begin = time.time()
    SIZE = 1048576*8
    
    while count>0:
        data = conn.recv(SIZE).decode()  # receive response
        conn.send("CONTINUE".encode())
        y = data.split('\n')

        if len(y)>2 and y[0].isnumeric() and database[int(y[0])] == '#':
            database[int(y[0])] = y[1]
            count -=1
            print("RECIEVED FROM CLIENT:", count, time.time()-begin)

        elif len(y) == 2 and y[0].isnumeric() and database[int(y[0])] == '#':
            lineno = int(y[0])
            string = y[1]
            count -=1
            if data[-1]=='\n':
                    continue
            while(True):
                data = conn.recv(SIZE).decode()
                conn.send("CONTINUE".encode())
                if data == '-1\n':
                    continue  # receive response
                y = data.split('\n')
                if len(y) == 1 and not(y[0].isnumeric()):
                    string+= y[0]
                elif not(y[0].isnumeric()):
                    string+= y[0]
                    break
                else:
                    break
            database[lineno] = string
            print("RECIEVED FROM CLIENT:", count, time.time()-begin)
    conn.send("FINISH".encode())
    end = time.time()
    print("TIME:", end-begin)
    conn.close()  # close the connection

def connectSlave(port):
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((HOST, port))  # bind HOST address and port together
    print("Binding done")
    # configure how many client the server can listen simultaneously
    server_socket.listen(4)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    return conn,address

def connectVayu():
    global database
    global count
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    HOST = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((HOST,9801))
    message = "SENDLINE\n"
    start = time.time()

    SIZE = 1048576*8
    while count>0:
        local.send(message.encode())  # send message
        data = local.recv(SIZE).decode()  # receive response
        y = data.split('\n')
        # print('Received')
        if len(y)>2 and y[0].isnumeric() and database[int(y[0])] == '#':
            database[int(y[0])] = y[1]
            count -= 1
            print(count,time.time()-start)
        elif len(y) == 2 and y[0].isnumeric() and database[int(y[0])] == '#':
            lineno = int(y[0])
            string = y[1]
            count -= 1
            if data[-1]=='\n':
                    continue
            while(True):
                data = local.recv(SIZE).decode()
                if data == '-1\n':
                    continue  # receive response
                y = data.split('\n')
                if len(y) == 1 and not(y[0].isnumeric()):
                    string+= y[0]
                elif not(y[0].isnumeric()):
                    string+= y[0]
                    break
                else:
                    break
            print(count,time.time()-start)
            database[lineno] = string
    end = time.time()
    print("TIME TAKEN:", end-start)
    local.close()


def submit():
    global database
    global count
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    HOST = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((HOST,9801))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = "2021CS11010@Doofinshmertz evil Inc.\n"
    local.send(message.encode())
    message = "1000\n"
    local.send(message.encode())
    for i in range(1000):
        message = str(i)+"\n"
        local.send(message.encode())
        message = database[i]+"\n"
        local.send(message.encode())
    data = local.recv(1048577).decode()  # receive response
    print(data)
    print('DONE test')
    local.close()

def client_submit(conn, start, end):
    for i in range(start,end):
        print("line sent : ", i)
        string = str(i)+'\n'+database[i]+'\n'
        conn.send(string.encode())
        data = conn.recv(1048576).decode()
        if data == "RECEIVED":
            continue
    # time.sleep(3)
    return

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    conn_arr=[]
    NUMCONN=3
    for i in range(0,NUMCONN):
        conn_arr.append(connectSlave(15000+i))
    
    slave1 = threading.Thread(target=server_program, args=(conn_arr[0][0], ))
    slave2 = threading.Thread(target=server_program, args=(conn_arr[1][0], ))
    slave3 = threading.Thread(target=server_program, args=(conn_arr[2][0], ))
    vayu = threading.Thread(target=connectVayu, args=())
    
    
    slave1.start()
    slave2.start()
    slave3.start()
    vayu.start()
    
    slave1.join()
    slave3.join()
    slave2.join()
    vayu.join()

    submit()

    broad_arr=[]
    NUMCONN=3
    for i in range(2*NUMCONN):
        broad_arr.append(connectSlave(16000+i))
    # s=input("Start?")
    send10 = threading.Thread(target=client_submit, args=(broad_arr[0][0], 0, MAXLINES//2 ))
    send11 = threading.Thread(target=client_submit, args=(broad_arr[1][0], MAXLINES//2, MAXLINES ))

    send20 = threading.Thread(target=client_submit, args=(broad_arr[2][0], 0, MAXLINES//2 ))
    send21 = threading.Thread(target=client_submit, args=(broad_arr[3][0], MAXLINES//2, MAXLINES ))
    
    send30 = threading.Thread(target=client_submit, args=(broad_arr[4][0], 0, MAXLINES//2 ))
    send31 = threading.Thread(target=client_submit, args=(broad_arr[5][0], MAXLINES//2, MAXLINES ))
    
    # send3 = threading.Thread(target=client_submit, args=(broad_arr[2][0], ))

    send10.start()
    send11.start()
    send20.start()
    send21.start()
    send30.start()
    send31.start()
    
    # vayu.start()
    
    send1.join()
    send2.join()
    send3.join()
