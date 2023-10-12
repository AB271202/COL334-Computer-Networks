import time
from socket import *
import hashlib

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
data,addr=client.recvfrom(2048)
size=int(data.split()[1])
print(data.decode())
flag = True
k = 1
message = f"Offset: 0\nNumBytes: 10\n\n"

s = 0
ans = ""
flag = True
k = 56
while (flag and s<=size):
    for i in range(k):
        message = f"Offset: {s}\nNumBytes: 1000\n\n"
        client.sendto(message.encode(),(SNAME,SPORT))
        if(s>211000):
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
            print("Squished")
            flag = False
            break
        else:
            fields = resp.split("\n")
            for i in range(3,len(fields)):
                if (i==len(fields)-1):
                    ans+=fields[i]
                else:
                    ans+=fields[i]+"\n"
            if (s>876000):
                flag = False
                break
            s+=1000
    time.sleep(0.001)
    if flag:
        k += 1
    else:
        # break
        if (s>size):
            break
        k = max(2,k-10)
        flag  = True
# client.close()
f = open("filerecv.txt","w")
f.write(ans)

md5_hex = calculate_md5("filerecv.txt")

print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: 6bf11f1400185696a3a43a495987756d\n\n"
client.sendto(message.encode(), (SNAME, SPORT))

msg,addr = client.recvfrom(2048)
print(msg.decode())
client.close()