import socket
import time

MAXLINES = 1000
VAYU = "10.17.51.115"
VPORT = 9801
MASTER = "10.184.47.53"
SPORT = 15000
RPORT = 16000
SIZE = 1048576*8
ENTRYNUMBER = "2021CS10134"


database = ['#']*MAXLINES
string = ""
count = MAXLINES

def client_program(): 

    client_socket = socket.socket()  
    global_socket = socket.socket()
    
    try:
        client_socket.connect((MASTER, SPORT))  
    except:
        print("Err: Connection couldn't be made with master")
    

    
    master=client_socket.recv(1048577).decode()
    command = ""
    if master=="START":
        print('master')
        global_socket.connect((VAYU,VPORT))
        global_socket.send("SESSION RESET\n".encode())
        global_socket.close()
        global_socket = socket.socket()
        global_socket.connect((VAYU,VPORT))
        message2 = "SENDLINE\n"
        try:
            while True:
                data = ''
                try:
                    global_socket.send(message2.encode())  
                    data = global_socket.recv(1048577)  
                except:
                    print("Connection broken with Vayu. Reconnecting ...... ")
                    global_socket.close()
                    global_socket.connect((VAYU, VPORT))
                    global_socket.send(message2.encode())
                    data = global_socket.recv(1048577)  

                client_socket.send(data)
                command = client_socket.recv(1048577)
                if command == 'FINISH':
                    client_socket.close()
                    # return 1
                    # break
                print("Data sent")
        except:
            # if command == 'FINISH':
            #     return 1
            global_socket.close()
            client_socket.close()
            print('master closed')
            # return 0
    # return 1


def receive_from_master():
    global database
    global count,string

    start = time.time()
    client_socket = socket.socket()
    client_socket.connect((MASTER, RPORT))

    
    print('receiving')
    while count>0:
        data = client_socket.recv(SIZE).decode()
        string += data
        if data.endswith('__END__'):
            break
    end = time.time()
    string = string[:-7]
    print("TIME TAKEN:", end-start)
    client_socket.close()


def connectVayu():
    global database
    global count
    global start
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VAYU,VPORT))
    message = "SENDLINE\n"
    start = time.time()

    SIZE = 1048576*8
    while count>0:
        local.send(message.encode())  
        data = local.recv(SIZE).decode()  
        y = data.split('\n')
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
                    continue  
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
    global string

    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    local.connect((VAYU,VPORT))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = f"{ENTRYNUMBER}@doofenshmirtz_evil_inc\n"
    local.send(message.encode())
    message = f"{MAXLINES}\n"
    local.send(message.encode())
    message = string
    local.send(message.encode())
    data = local.recv(1048577).decode()  
    print(data)
    print('DONE test')
    local.close()


def submit_master():
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
    
    data = local.recv(1048577).decode()  
    print(data)
    print('DONE test')
    local.close()

if __name__ == '__main__':
    client_program()
    # if x==0:
    #     connectVayu()
    #     submit_master()
    # else:
    try:
        start = time.time()
        while(time.time()-start<0.1):
            continue
        receive_from_master()
        submit()
    except:
        connectVayu()
        submit_master()