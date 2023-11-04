import socket
import time
local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostbyname("vayu.iitd.ac.in")
local.connect((host,9801))
message = "SENDLINE\n"
lines = ['']*1000
count = 1000
prev = 0
start = time.time()
while count>0:
    local.send(message.encode())  # send message
    data = local.recv(1048577).decode()  # receive response
    y = data.split()
    # print(count)
    # if prev == -1:
        # continue
    if ord(data[0])<48 or ord(data[0])>57:
        if prev == -1:
            continue
        if data[0] == '-':
            continue
        lines[prev]+=data
        continue
    if lines[int(y[0])-1] == '':
        prev = int(y[0])-1
        # print('Received from server: ' + data)  # show in terminal
        count -= 1
        print(count,time.time()-start)
        lines[int(y[0])-1] = data[len(y[0])+1:]
        while data[-1]!='\n':
            data = local.recv(1048577).decode()
            lines[prev]+= data
    else:
        prev = -1
end = time.time()
# local.close() 
print('Time taken : ',-start+end)
print('Starting test')
# while True:
#     s = input()
#     if s == "0":
#         break
#     else:
#         print(lines[int(s)-1])
# message = input(" -> ")  # again take input
message = "SUBMIT\n"
local.send(message.encode())
message = "2021CS10229@Doofinshmertz evil Inc.\n"
local.send(message.encode())
message = "1000\n"
local.send(message.encode())
for i in range(1000):
    message = str(i)+"\n"
    local.send(message.encode())
    message = lines[i]
    local.send(message.encode())
data = local.recv(1048577).decode()  # receive response
print(data)
message = "SEND INCORRECT LINES\n"
local.send(message.encode())
data = local.recv(1048577).decode()  # receive response
print(data)
print('DONE test')
local.close()