import hashlib
import time
from socket import *

SNAME = "localhost"
SPORT=9801

def calculate_md5(filename):
    md5_hash = hashlib.md5()
    with open(filename, "r") as file:
        while True:
            data = file.read(8192)  # Read the file in 8KB chunks
            if not data:
                break
            md5_hash.update(data.encode())
    return md5_hash.hexdigest()


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
while (flag and s<=size):
    for i in range(k):
        message = f"Offset: {s}\nNumBytes: 1440\n\n"
        if(s>size):
            break
        client.sendto(message.encode(),(SNAME,SPORT))
        print("Message sent to server",s)
        wait = True
        resp = ""
        waitflag = False
        while(wait):
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
                client.sendto(message.encode(),(SNAME,SPORT))
                # print("wait")
        # print(resp)
        if waitflag:
            k = max(2,k-10)
        if ("Squished" in resp):
            # print("Squished")
            flag = False
            fields = resp.split("\n")
            for i in range(4,len(fields)):
                if (fields[i] == '\x00'):
                    continue
                if (i==len(fields)-1):
                    ans+=fields[i]
                else:
                    ans+=fields[i]+"\n"
            if (s>size):
                flag = False
                break
            s+=1440
            break
        else:
            fields = resp.split("\n")
            for i in range(3,len(fields)):
                if (fields[i] == '\x00'):
                    continue
                if (i==len(fields)-1):
                    ans+=fields[i]
                else:
                    ans+=fields[i]+"\n"
            if (s>size):
                flag = False
                break
            s+=1440
    time.sleep(0.01)
    if flag:
        k += 1
    else:
        # break
        if (s>size):
            break
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