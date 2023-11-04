import socket

def client_program():
    host = "10.184.59.147"  # as both code is running on same pc
    host = "10.194.23.104" # piyush
    # host = "10.184.9.249" # ankit
    port = 15000  # socket server port number

    client_socket = socket.socket()  # instantiate
    global_socket = socket.socket()
    client_socket.connect((host, port))  # connect to the server
    global_socket.connect(('10.237.26.109',9801))
    # message = input(" -> ")  # take input
    message2 = "SENDLINE\n"
    lines = ['']*1000
    count = 1000
    prev = 0
    # start = time.time()
    try:
        while True:
            global_socket.send(message2.encode())  # send message
            data = global_socket.recv(1048577)  # receive response
            client_socket.send(data)
            print("Data sent")
        # y = data.split()
        
        # # print(count)
        # # if prev == -1:
        #     # continue
        # if ord(data[0])<48 or ord(data[0])>57:
        #     if prev == -1:
        #         continue
        #     if data[0] == '-':
        #         continue
        #     message  = "U"+str(prev)
        #     client_socket.send(message.encode())
        #     resp = client_socket.recv(1024).decode()
        #     if resp == "OK":
        #         message = data[len(y[0])+1:]
        #         client_socket.send(message.encode())
        #     resp = client_socket.recv(1024).decode()
        #     # lines[prev]+=data
        #     continue
        # if lines[int(y[0])] == '':
        #     prev = int(y[0])
        #     # print('Received from server: ' + data)  # show in terminal
        #     count -= 1
        #     # print(count,time.time()-start)
        #     message  = str(int(y[0]))
        #     client_socket.send(message.encode())
        #     resp = client_socket.recv(1024).decode()
        #     if resp == "OK":
        #         message = data[len(y[0])+1:]
        #         client_socket.send(message.encode())
        #         print("Sent to server")

        # else:
        #     prev = -1
    except:
        global_socket.close()
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
