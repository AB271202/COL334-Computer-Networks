import socket
import time
local = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostbyname("vayu.iitd.ac.in")
local.connect((host,9801))
message = "SENDLINE\n"
lines = ['']*1000
count = 1000
# prev = 0
start = time.time()

def getLine():
    local.send(message.encode())  # send message
    data = local.recv(1048577).decode()  # receive response
    return data

while count>0:
    
    y = getLine().split("\n")

    if y[0][0] == '-' or not (y[0].isdigit()):
        continue
    try:
        while (y[-1]!=""):
            # print("In loop")
            # print(y)
            # print("Printing z")
            z=getLine().split("\n")
            # print(z)
            if z[0][0] == '-':
                continue
            y[1]+=z[0]
            if z[-1]=="":
                y.append("")
            # print("Modified y")
            # print(y)
    except Exception as e:
         print(e,y)
         break

    if lines[int(y[0])] == '':
        # prev = int(y[0])
        # print('Received from server: ' , y)  # show in terminal
        count -= 1
        print(count,time.time()-start)
        lines[int(y[0])] = y[1]


end = time.time()
# local.close() 
# print('Time taken : ',-start+end)
# for line in lines: print(line)

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
    message = lines[i]+"\n"
    local.send(message.encode())
data = local.recv(1048577).decode()  # receive response
print(data)
message = "SEND INCORRECT LINES\n"
local.send(message.encode())
data = local.recv(1048577).decode()  # receive response
print(data)
print('DONE test')
local.close()
