import time
from socket import *

SNAME = "localhost"
SPORT=9801
client=socket(AF_INET, SOCK_DGRAM)
message="SendSize\nReset\n\n"
# message = f"Offset: 0\nNumBytes: 10\n\n"
for i in range(0,1):
    client.sendto(message.encode(),(SNAME,SPORT))
    print("Message sent to server")
data,addr=client.recvfrom(2048)
print(data.decode())
flag = True
k = 1
message = f"Offset: 0\nNumBytes: 10\n\n"
while (flag):
    for i in range(k):
        client.sendto(message.encode(),(SNAME,SPORT))
        print("Message sent to server",k)
        data,addr=client.recvfrom(2048)
        if ("Squished" in data.decode()):
            flag = False
            break
    time.sleep(10)
    if flag:
        k+=1
    else:
        break
print("Determined rate",k-1)
client.close()