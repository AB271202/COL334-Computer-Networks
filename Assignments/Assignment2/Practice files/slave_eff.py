import socket
import time

MAXLINES = 1000
database = ['#']*MAXLINES
count = MAXLINES
VayuIP = "10.17.51.115"
VayuPort = 9801

string = ""
def client_program():
    host = "10.184.47.53"  # as both code is running on same pc
    # host = "10.194.23.104" # piyush
    # host = "10.184.9.249" # ankit
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
        # lines = ['']*MAXLINES
        # count = MAXLINES
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
                # command = client_socket.recv(1048577)
                # if command == 'FINISH':
                #     break
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
    
    local.connect((VayuIP,VayuPort))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = "2021CS10134@Doofinshmertz evil Inc.\n"
    local.send(message.encode())
    message = f"{MAXLINES}\n"
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