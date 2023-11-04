import socket
import time

database = ['#']*1000
count = 1000
VayuIP = "10.17.51.115"
VayuPort = 9801
MAXLINES = 1000

string = ""

def client_program():
    host = "10.184.47.53"
    port = 15000  # socket server port number

    client_socket = socket.socket()  # instantiate
    global_socket = socket.socket()
    try:
        client_socket.connect((host, port))  # connect to the server
    except:
        print("Err: Connection couldn't be made with master")
    global_socket.connect((VayuIP,9801))

    master=client_socket.recv(1048577).decode()
    if master=="START":
        print('master')
        message2 = "SENDLINE\n"
        # lines = ['']*1000
        # count = 1000
        # prev = 0
        # start = time.time()
        try:
            while True:
                data = ''
                try:
                    global_socket.send(message2.encode())  # send message
                    data = global_socket.recv(1048577)  # receive response
                except:
                    print("Connection broken with Vayu. Reconnecting ...... ")
                    global_socket.close()
                    global_socket.connect((VayuIP, VayuPort))
                    global_socket.send(message2.encode())  # send message again 
                    data = global_socket.recv(1048577)  # receive response

                client_socket.send(data)
                command = client_socket.recv(1048577)
                if command == 'FINISH':
                    break
                print("Data sent")
        except:
            global_socket.close()
            client_socket.close()
            print('master closed')  # close the connection


def receive_from_master():
    host = "10.184.47.53"  # as both code is running on same pc
    # host = "10.184.31.107" # piyush
    # host = "10.184.9.249" # ankit
    port = 16000  # socket server port number
    start = time.time()
    client_socket = socket.socket()  # instantiate
    # global_socket = socket.socket()
    client_socket.connect((host, port))  # connect to the server
    # global_socket.connect(('10.237.26.109',9801))
    global database
    global count,string
    SIZE = 1048576*8
    print('receiving')
    # string = ""
    while count>0:
        # client_socket.send(message.encode())  # send message
        # print('inloop')
        data = client_socket.recv(SIZE).decode()  # receive response
        # print(data)
        string += data
    # print(data)
        if data.endswith('__END__'):
            break
    end = time.time()
    string = string[:-7]
    print("TIME TAKEN:", end-start)
    client_socket.close()

def submit():
    global database
    global count
    global string

    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VayuIP,9801))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = "2021CS10134@Doofinshmertz evil Inc.\n"
    local.send(message.encode())
    message = "1000\n"
    local.send(message.encode())
    message = string
    local.send(message.encode())
    data = local.recv(1048577).decode()  # receive response
    print(data)
    # data = local.recv(1048577).decode()  # receive response
    # print(data)
    # message = "SEND INCORRECT LINES\n"
    # local.send(message.encode())
    # data = local.recv(1048577).decode()  # receive response
    # print(data)
    # with open('output.txt', 'w') as f:
    #     for i in range(1000):
    #         f.write(str(i))
    #         f.write(database[i])
    print('DONE test')
    local.close()

def connectVayu():
    global database
    global count
    global start
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VayuIP,9801))
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

def submit_master():
    global database
    global count
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VayuIP,9801))
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
    data = local.recv(1048577).decode()  # receive response
    print(data)
    print('DONE test')
    local.close()

if __name__ == '__main__':
    client_program()
    # server_socket = socket.socket()  # get instance
    # # look closely. The bind() function takes tuple as argument
    # server_socket.bind((HOST, port))  # bind HOST address and port together

    # # configure how many client the server can listen simultaneously
    # server_socket.listen(4)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))
    try:
        start = time.time()
        while(time.time()-start<1):
            continue
        receive_from_master()
        submit()
    except:
        connectVayu()
        submit_master()