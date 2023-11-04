import socket
import time
import threading
import logging
import matplotlib.pyplot as plt

MAXLINES=1000
HOST = "0.0.0.0"
VAYU = "10.17.51.115"
VPORT = 9801
SIZE = 1048576*8
ENTRYNUMBER = "2021CS10134"


count=MAXLINES
database = ['#']*MAXLINES
# times=[0]
start=0


def server_program(conn):
    global database
    global count
    # global times

    conn.send("START".encode())

    
    while count>0:
        data = conn.recv(SIZE).decode()
        conn.send("CONTINUE".encode())
        y = data.split('\n')

        if len(y)>2 and y[0].isnumeric() and database[int(y[0])] == '#':
            database[int(y[0])] = y[1]
            # times.append(time.time()-start)
            count -=1
            print("RECIEVED FROM CLIENT:", count, time.time()-start)

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
            # times.append(time.time()-start)
            print("RECIEVED FROM CLIENT:", count, time.time()-start)
    conn.send("FINISH".encode())
    end = time.time()
    print("TIME:", end-start)
    conn.close()  

def connectSlave(port):
    server_socket = socket.socket() 
    server_socket.bind((HOST, port))  
    print("Binding done")
    server_socket.listen(4)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    return conn,address

def connectVayu():
    global database
    global count
    global start
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VAYU,VPORT))
    message = "SENDLINE\n"
    start = time.time()

    local.send('SESSION RESET\n'.encode())
    local.close()
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VAYU,VPORT))

    while count>0:
        data = ''
        try:
            local.send(message.encode())  # send message
            data = local.recv(SIZE).decode()  # receive response
        except:
            print("Connection broken with Vayu. Reconnecting ...... ")
            local.close()
            local.connect((VAYU,VPORT))
            local.send(message.encode())  # send message again
            data = local.recv(SIZE).decode()  # receive response

        y = data.split('\n')
        # print('Received')
        if len(y)>2 and y[0].isnumeric() and database[int(y[0])] == '#':
            database[int(y[0])] = y[1]
            # times.append(time.time()-start)
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
            # times.append(time.time()-start)
            
    end = time.time()
    print("TIME TAKEN:", end-start)
    local.close()


def submit():
    global database
    global count
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VAYU,VPORT))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = f"{ENTRYNUMBER}@doofenshmirtz_evil_inc\n"
    local.send(message.encode())
    message = f"{MAXLINES}\n"
    local.send(message.encode())
    for i in range(MAXLINES):
        message = str(i)+"\n"
        local.send(message.encode())
        message = database[i]+"\n"
        local.send(message.encode())
    data = local.recv(1048577).decode()  # receive response
    print(data)
    print('DONE test')
    local.close()

def client_submit(conn):
    string = ''
    for i in range(0,MAXLINES):
        # print("line sent : ", i)
        string += str(i)+'\n'+database[i]+'\n'
    string += "__END__"
    conn.send(string.encode())
    return
'''
def plot_graph():
    plt.plot([i for i in range(0,MAXLINES+1)],times)
    plt.xlabel('Number of unique lines read (n)')
    plt.ylabel('Time (s)')
    plt.grid(True) 
    no=input("Run number: ")
    name=input("Name: ")
    plt.title(f'Run #{no}')
    plt.savefig(f'{name}.png')
    with open(f"{name}.txt","w") as f:
        for i in range(0,MAXLINES+1):
            f.write(str(times[i])+" ")
'''


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
    # slave4 = threading.Thread(target=server_program, args=(conn_arr[3][0], ))
    vayu = threading.Thread(target=connectVayu, args=())
    
    slave1.start()
    slave2.start()
    slave3.start()
    # slave4.start()
    vayu.start()
    
    slave1.join()
    slave2.join()
    slave3.join()
    # slave4.join()
    vayu.join()

    submit()

    broad_arr=[]
    for i in range(0,NUMCONN):
        broad_arr.append(connectSlave(16000+i))
    # # s=input("Start?")
    send1 = threading.Thread(target=client_submit, args=(broad_arr[0][0], ))
    send2 = threading.Thread(target=client_submit, args=(broad_arr[1][0], ))
    send3 = threading.Thread(target=client_submit, args=(broad_arr[2][0], ))
    # send4 = threading.Thread(target=client_submit, args=(broad_arr[3][0], ))
    
    send1.start()
    send2.start()
    send3.start()
    # send4.start()
    # vayu.start()
    
    send1.join()
    send2.join()
    send3.join()
    # send4.join()

    # plot_graph()
    #master efficient version -- final draft
