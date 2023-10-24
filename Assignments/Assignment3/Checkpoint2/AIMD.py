import hashlib
import time
from socket import *

# SNAME = "10.194.49.169"
SNAME = "localhost"
# SNAME = gethostbyname("vayu.iitd.ac.in")
SPORT = 9801
PSIZE = 1448


client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(0.004)


# Receive the file size
timeout = 0.004
while (True):
    try:
        message = "SendSize\nReset\n\n"
        client.sendto(message.encode(), (SNAME, SPORT))
        print("SendSize sent to server")
        data, addr = client.recvfrom(2048*2048)
        break
    except:
        print("[Timeout] Trying again...")
        timeout += 0.001
        client.settimeout(timeout)
        continue

size = int(data.split()[1])
print("[SIZE]", size)

flag = True
k = 4
count = size//PSIZE + 1  # Number of packets to receive
receivedlist = ["#"]*count
remaining = [i for i in range(count)]


# For plotting
initial_time = time.time()
sendtimelist = [0]*count
receivetimelist = [0]*count
burstsizelist = list()

rtt = [0.004]*count
RTT = 0.004

while (flag and count > 0):
    j = 0
    decrease = False
    sleepflag = False
    while j < (size//PSIZE + 1):
        sleepflag = False
        decrease = False

        # Sending a burst
        burstsizelist.append(
            [min(j+k, size//PSIZE + 1)-j, time.time()-initial_time])
        for i in range(j, min(j+k, size//PSIZE + 1)):

            if (receivedlist[i] != "#"):
                continue

            sleepflag = True
            s = i*PSIZE
            message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"

            client.sendto(message.encode(), (SNAME, SPORT))
            sendtimelist[s//PSIZE] = (time.time()-initial_time)
            print("Message sent to server", s, k)

        start = count

        # Receiving Response
        for i in range(j, min(j+k, size//PSIZE + 1)):
            if (receivedlist[i] != "#"):
                continue

            received = False
            try:
                data, addr = client.recvfrom(2048*2048)
                resp = data.decode()
                received = True
            except:
                received = False
            
            if received:
                recv_time = time.time()
                fields = resp.split("\n")
                ans = ""
                if (fields[0].split())[0] == "Size:":
                    continue
                    
                for i in range(4 if ("Squished" == fields[2]) else 3 , len(fields)):
                    if (fields[i] == '\x00'):
                        continue
                    if (i == len(fields)-1):
                        ans += fields[i]
                    else:
                        ans += fields[i]+"\n"

                offset = int(fields[0].split()[1])

                if receivedlist[offset//PSIZE] == "#":
                    receivetimelist[offset//PSIZE] = recv_time-initial_time
                    count -= 1
                    rtt[offset//PSIZE] = receivetimelist[offset//PSIZE] - \
                        sendtimelist[offset//PSIZE]
                receivedlist[offset//PSIZE] = ans
            else:
                decrease = True

        j += k
        if sleepflag:
            time.sleep(0.008)

        if decrease:
            k = max(k//2, 1)
        elif start-count > 0:
            k = min(k+1, count+1)

    time.sleep(0.02)

ans = ""
for i in range(size//PSIZE+1):
    ans += receivedlist[i]

md5_hex = hashlib.md5(ans.encode('utf-8')).hexdigest()
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@joy_maa\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))


msg1 = ""
while (not ("Result" in msg1)):
    wait = True
    while (wait):
        try:
            msg, addr = client.recvfrom(2048*2048)
            wait = False
        except:
            client.sendto(message.encode(), (SNAME, SPORT))
    msg1 = msg.decode()

print(msg.decode())
client.close()
# print(rtt)

with open("sendtimes.txt", "w") as f:
    for i in range(len(sendtimelist)):
        f.write(f"{i*PSIZE}|{sendtimelist[i]}#")

with open("receivetimes.txt", "w") as f:
    for i in range(len(receivetimelist)):
        f.write(f"{i*PSIZE}|{receivetimelist[i]}#")

with open("burstsizes.txt", "w") as f:
    for i in range(len(burstsizelist)):
        f.write(f"{burstsizelist[i][1]}|{burstsizelist[i][0]}#")
