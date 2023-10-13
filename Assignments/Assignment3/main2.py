import hashlib
import time
from socket import *


def calculate_md5(filename):
    md5_hash = hashlib.md5()
    with open(filename, "r") as file:
        while True:
            data = file.read(8192)  # Read the file in 8KB chunks
            if not data:
                break
            md5_hash.update(data.encode())
    return md5_hash.hexdigest()

SNAME = "localhost"
SPORT=9801
client=socket(AF_INET, SOCK_DGRAM)
message="SendSize\nReset\n\n"
client.settimeout(0.05)
# message = f"Offset: 0\nNumBytes: 10\n\n"
for i in range(0,1):
    client.sendto(message.encode(),(SNAME,SPORT))
    print("Message sent to server")
data,addr=client.recvfrom(2048*2048)
size=int(data.split()[1])
print(data.decode())
flag = True
k = 1
message = f"Offset: 0\nNumBytes: 10\n\n"

s = 0
ans = ""
flag = True
k = 10
received_list = [""]*(size//1440)
count = size//1440
while (flag and count > 0):
    for i in range(k):
        message = f"Offset: {s}\nNumBytes: 1440\n\n"
        # if(s>size):
        #     break
        client.sendto(message.encode(),(SNAME,SPORT))
        print("Message sent to server",s)
        wait = True
        resp = ""
        waitflag = False
        # while(wait):
            # print("back here")
        try:
            # print("going here")
            wait = False
            data,addr=client.recvfrom(2048*2048)
            resp = data.decode()
            # print("recv")
        except:
            wait = True
            waitflag = True
            # client.sendto(message.encode(),(SNAME,SPORT))
            # print("wait")
        # print(resp)
        if waitflag:
            k = max(2,k-10)
        if not wait:
            count -= 1
        if ("Squished" in resp):
            # print("Squished")
            flag = False
            fields = resp.split("\n")
            # print(resp)
            # print(hashlib.md5(resp).hexdigest())
            # print(hashlib.md5("This is a string").hexdigest())
            # print(hashlib.md5("This is a string".encode('utf-8')).hexdigest())
            # print(hashlib.md5(resp.encode('utf-8')).hexdigest())
            # print(fields)
            ans = ""
            for i in range(4,len(fields)):
                if (fields[i] == '\x00'):
                    continue
                if (i==len(fields)-1):
                    ans+=fields[i]
                else:
                    ans+=fields[i]+"\n"
            received_list[s//1440] = ans
            if (s>size):
                flag = False
                s = 0
                # break
            found = False
            for i in range(s//1440,len(received_list)):
                if received_list[i]=="":
                    s = i*1440
                    found = True
            if not found:
                s = 0
                for i in range(s//1440,len(received_list)):
                    if received_list[i]=="":
                        s = i*1440
                        found = True
            if not found:
                flag = False
                break
            # s+=1440
            break
        elif not wait:
            fields = resp.split("\n")
            # print(resp)
            # print(hashlib.md5(resp).hexdigest())
            # print(hashlib.md5("This is a string").hexdigest())
            # print(hashlib.md5("This is a string".encode('utf-8')).hexdigest())
            # print(hashlib.md5(resp.encode('utf-8')).hexdigest())
            # print(fields)
            ans = ""
            for i in range(3,len(fields)):
                if (fields[i] == '\x00'):
                    continue
                if (i==len(fields)-1):
                    ans+=fields[i]
                else:
                    ans+=fields[i]+"\n"
            received_list[s//1440] = ans
            # if (s>size):
            #     flag = False
            #     break
            # s+=1440
            found = False
            for i in range(s//1440,len(received_list)):
                if received_list[i]=="":
                    s = i*1440
                    found = True
            if not found:
                s = 0
                for i in range(s//1440,len(received_list)):
                    if received_list[i]=="":
                        s = i*1440
                        found = True
            if not found:
                flag = False
                break
        else:
            found = False
            for i in range(s//1440+1,len(received_list)):
                if received_list[i]=="":
                    s = i*1440
                    found = True
            if not found:
                s = 0
                for i in range(s//1440,len(received_list)):
                    if received_list[i]=="":
                        s = i*1440
                        found = True
            if not found:
                flag = False
                break
    time.sleep(0.01)
    if flag:
        k += 1
    else:
        # break
        # if (s>size):
        #     break
        # k = max(2,k-10)
        flag  = True
# client.close()
f = open("filerecv.txt","w")
f.write(ans)
ans2 = ""
ans2 = ans
# for i in range(len(ans)-1,-1,-1):
#     if ans[i] == "\n":
#         ans2 = ans[:i+1]
ans = ""
for i in received_list:
    ans+=i
f.write(ans)
print(received_list)
md5_hex = calculate_md5("filerecv.txt")
print(hashlib.md5(ans2.encode('utf-8')).hexdigest())
md5_hex = hashlib.md5(ans.encode('utf-8')).hexdigest()
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))

msg,addr = client.recvfrom(2048)
print(msg.decode())
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))

msg,addr = client.recvfrom(2048)
print(msg.decode())
client.close()