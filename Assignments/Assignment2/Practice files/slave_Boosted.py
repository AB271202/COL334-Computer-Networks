import socket
import time
import threading

MAXLINES=1000
database = ['#']*MAXLINES
count = MAXLINES

def client_program():
    host = "10.184.59.147"  # as both code is running on same pc
    # host = "10.194.23.104" # piyush
    # host = "10.184.9.249" # ankit
    port = 15000  # socket server port number

    client_socket = socket.socket()  # instantiate
    global_socket = socket.socket()
    client_socket.connect((host, port))  # connect to the server
    global_socket.connect(('10.237.26.109',9801))

    master = client_socket.recv(1048577).decode()
    if master=="START":
        print('master')
        message2 = "SENDLINE\n"
        try:
            while True:
                global_socket.send(message2.encode())  # send message
                data = global_socket.recv(1048577)  
                client_socket.send(data)
                command = client_socket.recv(1048577)
                if command == 'FINISH':
                    break
                print("Data sent")
            return
        except:
            global_socket.close()
            client_socket.close()
            print('master closed')  # close the connection

def receive_from_master(client_socket):
    # host = "10.184.59.147"  # shankh
    
    start = time.time()
    # client_socket = socket.socket() 
    # client_socket.connect((host, port))  
    
    global database
    global count
    SIZE = 1048576*8
    
    print('receiving')
    while count>0:
        data = client_socket.recv(SIZE).decode()  
        
        y = data.split('\n')
        if len(y)>2 and y[0].isnumeric() and database[int(y[0])] == '#':
            database[int(y[0])] = y[1]
            count -= 1
            client_socket.send("RECEIVED".encode())

        elif len(y) == 2 and y[0].isnumeric() and database[int(y[0])] == '#':
            lineno = int(y[0])
            string = y[1]
            count -= 1
            if data[-1]=='\n':
                database[lineno] = string
                client_socket.send("RECEIVED".encode())
                continue
            while(True):
                data = client_socket.recv(SIZE).decode()
                if data == '-1\n':
                    continue  
                y = data.split('\n')
                if len(y) == 1 and not(y[0].isnumeric()):
                    string+= y[0]
                    if data[-1] == '\n':
                        break
                elif not(y[0].isnumeric()):
                    string+= y[0]
                    break
                else:
                    break
            print(count,time.time()-start)
            database[lineno] = string
            client_socket.send("RECEIVED".encode())
    end = time.time()
    print("TIME TAKEN:", end-start)
    client_socket.close()

def submit():
    global database
    global count

    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((host,9801))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = "2021CS10134@Doofinshmertz evil Inc.\n"
    local.send(message.encode())
    message = f"{MAXLINES}\n"
    local.send(message.encode())
    for i in range(MAXLINES):
        message = str(i)+"\n"
        local.send(message.encode())
        message = database[i]+"\n"
        local.send(message.encode())
    data = local.recv(1048577).decode()  
    print(data)
    print('DONE test')
    local.close()

if __name__ == '__main__':
    client_program()
    start = time.time()
    while(time.time()-start<0.1):
        continue
    
    RPORT1 = 16000
    RPORT2 = 16001
    host = "10.184.59.147"

    client_socket1 = socket.socket()
    client_socket1.connect((host, RPORT1))

    client_socket2 = socket.socket()
    client_socket2.connect((host, RPORT2))

    recv0 = threading.Thread(target=receive_from_master, args=(client_socket1, ))
    recv1 = threading.Thread(target=receive_from_master, args=(client_socket2,  ))
    
    # receive_from_master(16001)
    
    recv0.start()
    recv1.start()

    recv0.join()
    recv1.join()

    submit()