import socket
import time

MAXLINES=1000
database = ['#']*1000
count = 1000

string = ""
HOST="10.184.47.53"
VAYU="10.17.51.115"
VPORT=9801
SPORT=15000
RPORT=16000

def client_program():


    client_socket = socket.socket()  # instantiate
    global_socket = socket.socket()
    client_socket.connect((HOST, SPORT))  # connect to the server
    global_socket.connect((VAYU,VPORT))

    master=client_socket.recv(1048577).decode()
    if master=="START":
        print('master')
        message2 = "SENDLINE\n"
        try:
            while True:
                global_socket.send(message2.encode())  # send message
                data = global_socket.recv(1048577)  # receive response
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


def receive_from_master():
    start = time.time()
    client_socket = socket.socket()
    client_socket.connect((HOST, RPORT))
    global database
    global count,string
    SIZE = 1048576*8

    print('receiving')
    while count>0:
        data = client_socket.recv(SIZE).decode()  # receive response
        string += data
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
    local.connect((VAYU,VPORT))
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
    print('DONE test')
    local.close()

if __name__ == '__main__':
    client_program()
    start = time.time()
    while(time.time()-start<1):
        continue
    receive_from_master()
    submit()
