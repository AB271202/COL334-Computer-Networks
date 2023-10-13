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


def next(s,receivedlist):
    curr_index = s//1440
    found = False
    for i in range(curr_index,len(receivedlist)):
        if receivedlist[i]=="#":
            found = True
            return i*1440
    if not found:
        for i in range(0,len(receivedlist)):
            if receivedlist[i]=="#":
                found = True
                return i*1440
    return 0

SNAME = "localhost"
SPORT=9801
client=socket(AF_INET, SOCK_DGRAM)
message="SendSize\nReset\n\n"
client.settimeout(0.05)

client.sendto(message.encode(),(SNAME,SPORT))
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
count = size//1440 + 1
receivedlist = ["#"]*(count)
while (flag and count>0):
    for i in range(40):
        if (count<=0):
            break
        message = f"Offset: {s}\nNumBytes: 1440\n\n"
        client.sendto(message.encode(),(SNAME,SPORT))
        print("Message sent to server",s)
        resp = ""
        received = False
        try:
            data,addr=client.recvfrom(2048*2048)
            resp = data.decode()
            received = True
        except:
            received = False
        if received:
            # print(resp)
            if ("Squished" in resp):
                # print("Squished")
                fields = resp.split("\n")
                ans = ""
                for i in range(4,len(fields)):
                    if (fields[i] == '\x00'):
                        continue
                    if (i==len(fields)-1):
                        ans+=fields[i]
                    else:
                        ans+=fields[i]+"\n"
                receivedlist[s//1440]=ans
                # s+=1440
                count -=1
                s = next(s,receivedlist)
            else:
                ans = ""
                fields = resp.split("\n")
                for i in range(3,len(fields)):
                    if (fields[i] == '\x00'):
                        continue
                    if (i==len(fields)-1):
                        ans+=fields[i]
                    else:
                        ans+=fields[i]+"\n"
                receivedlist[s//1440]=ans
                # s+=1440
                count-=1
                s = next(s,receivedlist)
    time.sleep(0.01)
# client.close()
f = open("filerecv.txt","w")
f.write(ans)
ans2 = ""
ans2 = ans
# for i in range(len(ans)-1,-1,-1):
#     if ans[i] == "\n":
#         ans2 = ans[:i+1]
# print(receivedlist[0])
ans  = ""
for i in range(size//1440+1):
    ans+=receivedlist[i]
    # print("ans",i)
    # print(ans)
f.write(ans)
md5_hex = calculate_md5("filerecv.txt")
print(hashlib.md5(ans2.encode('utf-8')).hexdigest())
# print(ans2)
# print("Current answer\n",ans)
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