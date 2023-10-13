import hashlib
import time
from socket import *

SNAME = "localhost"
SPORT = 9801
NUMDATA = 1440


def next(s, receivedlist):
    curr_index = s//NUMDATA
    found = False
    for i in range(curr_index, len(receivedlist)):
        if receivedlist[i] == "#":
            found = True
            return i*NUMDATA
    if not found:
        for i in range(0, len(receivedlist)):
            if receivedlist[i] == "#":
                found = True
                return i*NUMDATA
    return 0


client = socket(AF_INET, SOCK_DGRAM)
message = "SendSize\nReset\n\n"
client.settimeout(0.1)

client.sendto(message.encode(), (SNAME, SPORT))
data, addr = client.recvfrom(2048*2048)
size = int(data.split()[1])
print("Filesize: ", size)

s = 0
ans = ""
flag = True
k = 10
count = size//NUMDATA + 1
receivedlist = ["#"]*(count)
while (flag and count > 0):
    for i in range(size//NUMDATA + 1):
        if (receivedlist[i] != "#"):
            continue
        s = i*NUMDATA
        message = f"Offset: {s}\nNumBytes: {NUMDATA}\n\n"
        client.sendto(message.encode(), (SNAME, SPORT))
        print("Message sent to server", s)
        resp = ""
        received = False
        try:
            data, addr = client.recvfrom(2048*2048)
            resp = data.decode()
            received = True
        except:
            received = False
        if received:
            if ("Squished" in resp):
                fields = resp.split("\n")
                ans = ""
                for i in range(4, len(fields)):
                    if (fields[i] == '\x00'):
                        continue
                    if (i == len(fields)-1):
                        ans += fields[i]
                    else:
                        ans += fields[i]+"\n"
                receivedlist[s//NUMDATA] = ans
                count -= 1
            else:
                ans = ""
                fields = resp.split("\n")
                for i in range(3, len(fields)):
                    if (fields[i] == '\x00'):
                        continue
                    if (i == len(fields)-1):
                        ans += fields[i]
                    else:
                        ans += fields[i]+"\n"
                receivedlist[s//NUMDATA] = ans
                count -= 1
        time.sleep(0.001)

ans2 = ""
ans2 = ans
ans = ""
for i in range(size//NUMDATA+1):
    ans += receivedlist[i]

md5_hex = hashlib.md5(ans.encode('utf-8')).hexdigest()
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))


msg, addr = client.recvfrom(2048)
print(msg.decode())
client.close()
