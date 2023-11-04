import socket
import time

database = ['#']*1000
count = 1000

def client_program():
    host = "10.184.47.53"  # as both code is running on same pc
    # host = "10.194.23.104" # piyush
    # host = "10.184.9.249" # ankit
    port = 15000  # socket server port number

    client_socket = socket.socket()  # instantiate
    global_socket = socket.socket()
    client_socket.connect((host, port))  # connect to the server
    global_socket.connect(('10.237.26.109',9801))

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
    host = "10.184.47.53"  # as both code is running on same pc
    # host = "10.194.23.104" # piyush
    # host = "10.184.9.249" # ankit
    port = 16000  # socket server port number
    start = time.time()
    client_socket = socket.socket()  # instantiate
    # global_socket = socket.socket()
    client_socket.connect((host, port))  # connect to the server
    # global_socket.connect(('10.237.26.109',9801))
    global database
    global count
    SIZE = 1048576*8
    print('receiving')

    receivedstring=""
    while count>0:
        data = client_socket.recv(SIZE).decode()
        receivedstring+=data
        if data[-7:]=="__END__":
            break
    submit(receivedstring[0:-7])
    # while count>0:
    #     # client_socket.send(message.encode())  # send message
    #     # print('inloop')
    #     data = client_socket.recv(SIZE).decode()  # receive response
    #     # print(data)
    #     y = data.split('\n')
    #     # database[int(y[0])] = y[1]
    #     # print('Received')
    #     """"""
    #     if len(y)>2 and y[0].isnumeric() and database[int(y[0])] == '#':
    #         database[int(y[0])] = y[1]
    #         count -= 1
    #         client_socket.send("RECEIVED".encode())
    #         # print(count,time.time()-start)
    #     elif len(y) == 2 and y[0].isnumeric() and database[int(y[0])] == '#':
    #         lineno = int(y[0])
    #         string = y[1]
    #         count -= 1
    #         if data[-1]=='\n':
    #             database[lineno] = string
    #             client_socket.send("RECEIVED".encode())
    #             continue
    #         while(True):
    #             data = client_socket.recv(SIZE).decode()
    #             if data == '-1\n':
    #                 continue  # receive response
    #             y = data.split('\n')
    #             if len(y) == 1 and not(y[0].isnumeric()):
    #                 string+= y[0]
    #                 if data[-1] == '\n':
    #                     break
    #             elif not(y[0].isnumeric()):
    #                 string+= y[0]
    #                 break
    #             else:
    #                 break
    #         print(count,time.time()-start)
    #         database[lineno] = string
    #         client_socket.send("RECEIVED".encode())
    # end = time.time()
    # print("TIME TAKEN:", end-start)
    # client_socket.close()

def submit(strg):
    global database
    global count
    local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostbyname("vayu.iitd.ac.in")
    local.connect((host,9801))
    message = "SUBMIT\n"
    local.send(message.encode())
    message = "2021CS10134@Doofinshmertz evil Inc.\n"
    local.send(message.encode())
    message = "1000\n"
    local.send(message.encode())
    local.send(strg.encode())
    
    # for i in range(1000):
    #     message = str(i)+"\n"
    #     local.send(message.encode())
    #     message = database[i]+"\n"
    #     local.send(message.encode())
    # data = local.recv(1048577).decode()  # receive response
    # print(data)
    data = local.recv(1048577).decode()  # receive response
    print(data)
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

if __name__ == '__main__':
    client_program()
    # server_socket = socket.socket()  # get instance
    # # look closely. The bind() function takes tuple as argument
    # server_socket.bind((HOST, port))  # bind HOST address and port together

    # # configure how many client the server can listen simultaneously
    # server_socket.listen(4)
    # conn, address = server_socket.accept()  # accept new connection
    # print("Connection from: " + str(address))
    start = time.time()
    while(time.time()-start<0.1):
        continue
    receive_from_master()
    # submit()