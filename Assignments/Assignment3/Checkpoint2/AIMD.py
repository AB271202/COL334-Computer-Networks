import hashlib
import time
from socket import *

SNAME = "localhost"
SPORT = 9801

# For plotting
sendtimelist = []
receivetimelist = []




# Initialize client
client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(0.05)


# Receive the file size
while(True):
    try:
        message = "SendSize\nReset\n\n"
        client.sendto(message.encode(), (SNAME, SPORT))
        print("SendSize sent to server")
        data, addr = client.recvfrom(2048*2048)
    except:
        print("[Timeout] Trying again...")
        continue

SIZE = int(data.split()[1])
print("[SIZE]", SIZE)



offset = 0
ans = ""
flag = True
k = 2
initial_time = time.time()
while (flag and offset <= SIZE):
    for i in range(k):
        if (offset > SIZE):
            break

        message = f"Offset: {offset}\nNumBytes: 1440\n\n"
        client.sendto(message.encode(), (SNAME, SPORT))
        sendtimelist.append([time.time()-initial_time, offset])
        print("Message sent to server", offset)
        wait = True
        resp = ""
        waitflag = False
        while (wait):
            # print("back here")
            try:
                # print("going here")
                wait = False
                data, addr = client.recvfrom(2048*2048)
                resp = data.decode()
                # print("recv")
            except:
                wait = True
                waitflag = True
                client.sendto(message.encode(), (SNAME, SPORT))
                # print("wait")
        # print(resp)
        recvtime = time.time()-initial_time
        if waitflag:
            flag = False
            k = max(2, k-10)

        if ("Squished" in resp):
            # print("Squished")
            flag = False
            fields = resp.split("\n")
            receivetimelist.append([recvtime, int(fields[0].split()[1])])
            for i in range(4, len(fields)):
                if (fields[i] == '\x00'):
                    continue
                if (i == len(fields)-1):
                    ans += fields[i]
                else:
                    ans += fields[i]+"\n"
            if (offset > SIZE):
                flag = False
                break
            offset += 1440
            break
        else:
            fields = resp.split("\n")
            receivetimelist.append([recvtime, int(fields[0].split()[1])])
            for i in range(3, len(fields)):
                if (fields[i] == '\x00'):
                    continue
                if (i == len(fields)-1):
                    ans += fields[i]
                else:
                    ans += fields[i]+"\n"
            if (offset > SIZE):
                flag = False
                break
            offset += 1440
    time.sleep(0.01)
    if flag:
        k += 1
    else:
        # break
        if (offset > SIZE):
            break
        # k = max(2,k-10)
        flag = True




md5_hex = hashlib.md5(ans.encode('utf-8')).hexdigest()
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))

msg, addr = client.recvfrom(2048)
print(msg.decode())
client.close()

# with open("sendtimes.txt", "w") as f:
#     for i in sendtimelist:
#         f.write(f"{i[0]}|{i[1]}#")

# with open("receivetimes.txt", "w") as f:
#     for i in receivetimelist:
#         f.write(f"{i[0]}|{i[1]}#")
