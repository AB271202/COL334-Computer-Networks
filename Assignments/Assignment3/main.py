import time
from socket import *

SNAME = "localhost"
SPORT=9801
client=socket(AF_INET, SOCK_DGRAM)
message="SendSize\nReset\n\n"
client.settimeout(0.05)
# message = f"Offset: 0\nNumBytes: 10\n\n"
for i in range(0,1):
    client.sendto(message.encode(),(SNAME,SPORT))
    print("Message sent to server")
data,addr=client.recvfrom(2048)
print(data.decode())
flag = True
k = 1
message = f"Offset: 0\nNumBytes: 10\n\n"
# while (flag):
#     for i in range(k):
#         client.sendto(message.encode(),(SNAME,SPORT))
#         print("Message sent to server",k)
#         wait = True
#         resp = ""
#         while(wait):
#             # print("back here")
#             try:
#                 # print("going here")
#                 wait = False
#                 data,addr=client.recvfrom(2048)
#                 resp = data.decode()
#                 print("recv")
#             except:
#                 wait = True
#                 client.sendto(message.encode(),(SNAME,SPORT))
#                 # print("wait")
#         print(resp)
#         if ("Squished" in resp):
#             flag = False
#             break
#     time.sleep(0.0001)
#     if flag:
#         k+=1
#     else:
#         break
# print("Determined rate",k-1)
s = 0
ans = ""
flag = True
k = 56
while (flag and s<=876000):
    for i in range(k):
        message = f"Offset: {s}\nNumBytes: 1000\n\n"
        client.sendto(message.encode(),(SNAME,SPORT))
        if(s>876000):
            break
        print("Message sent to server",s)
        wait = True
        resp = ""
        while(wait):
            # print("back here")
            try:
                # print("going here")
                wait = False
                data,addr=client.recvfrom(2048)
                resp = data.decode()
                # print("recv")
            except:
                wait = True
                client.sendto(message.encode(),(SNAME,SPORT))
                # print("wait")
        # print(resp)
        if ("Squished" in resp):
            flag = False
            break
        else:
            fields = resp.split("\n")
            ans+=fields[3]
            if (s>876000):
                flag = False
                break
            s+=1000
    time.sleep(0.0001)
    if flag:
        k += 1
    else:
        # break
        if (s>876000):
            break
        k = max(2,k-10)
        flag  = True
client.close()
f = open("filerecv.txt","w")
f.write(ans)