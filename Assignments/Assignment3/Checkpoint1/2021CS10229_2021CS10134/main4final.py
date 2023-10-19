import hashlib
import time
from socket import *


SNAME = "localhost"
SPORT = 9801
PSIZE = 1440


def next(s, receivedlist):
    curr_index = s//PSIZE
    found = False
    for i in range(curr_index, len(receivedlist)):
        if receivedlist[i] == "#":
            found = True
            return i*PSIZE
    if not found:
        for i in range(0, len(receivedlist)):
            if receivedlist[i] == "#":
                found = True
                return i*PSIZE
    return 0



client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(0.006)

message = "SendSize\nReset\n\n"
client.sendto(message.encode(), (SNAME, SPORT))

wait = True
while (wait):
    try:
        data, addr = client.recvfrom(2048*2048)
        wait = False
    except:
        pass
size = int(data.split()[1])
print(data.decode())
sendtimelist = []
receivetimelist = []
s = 0
ans = ""
flag = True
k = 10
count = size//PSIZE + 1
receivedlist = ["#"]*(count)
init_time = time.time()
while (flag and count > 0):
    for i in range(size//PSIZE + 1):
        if (receivedlist[i] != "#"):
            continue
        s = i*PSIZE
        message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"
        client.sendto(message.encode(), (SNAME, SPORT))
        sendtimelist.append([time.time()-init_time, s])
        print("Message sent to server", s)

        resp = ""
        received = False
        try:
            data, addr = client.recvfrom(2048*2048)
            receivedtime = time.time()-init_time
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
                offset = fields[0]
                offsetnum = int(offset.split()[1])
                if receivedlist[offsetnum//PSIZE] == "#":
                    receivetimelist.append([receivedtime, offsetnum])
                    count -= 1
                receivedlist[offsetnum//PSIZE] = ans

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
                offset = fields[0]
                offsetnum = int(offset.split()[1])
                if receivedlist[offsetnum//PSIZE] == "#":
                    receivetimelist.append([receivedtime, offsetnum])
                    count -= 1
                receivedlist[offsetnum//PSIZE] = ans
            if (count % 1 == 0):
                time.sleep(0.007)
    time.sleep(0.02)
ans2 = ""
ans2 = ans
ans = ""
for i in range(size//PSIZE+1):
    ans += receivedlist[i]

md5_hex = hashlib.md5(ans.encode('utf-8')).hexdigest()
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))


msg1 = ""
while (not ("Result" in msg1)):
    wait = True
    while (wait):
        try:
            msg, addr = client.recvfrom(2048*2048)
            wait = False
        except:
            pass
    msg1 = msg.decode()

print(msg.decode())
client.close()

with open("sendtime.txt", "w") as f:
    for i in sendtimelist:
        f.write(f"[{i[0]},{i[1]}],")

with open("receivetime.txt", "w") as f:
    for i in receivetimelist:
        f.write(f"[{i[0]},{i[1]}],")
