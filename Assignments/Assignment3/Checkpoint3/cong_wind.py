import hashlib
import time
from socket import *

# SNAME = "10.194.49.169"
# SNAME = "localhost"
SNAME = gethostbyname("vayu.iitd.ac.in")
# SNAME = "10.17.7.218"
SPORT = 9802
PSIZE = 1448


client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(0.01)
dec_count = 0

# Receive the file size
timeout = 0.01
sleeptime = 0.008
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
squishedlist=list()
sq_count = 0
rtt = [0.004]*count
RTT = 0.004
k1 = 4.0
start = 0
end = 10
rate = 0.01
s = start*PSIZE
# message = f"Offset: {s}\nNumBytes: {PSIZE}\n\nOffset: {s+1}\nNumBytes: {PSIZE}\n\nOffset: {s+2}\nNumBytes: {PSIZE}\n\nOffset: {s+3}\nNumBytes: {PSIZE}\n\n"
# client.sendto(message.encode(), (SNAME, SPORT))
for i in range(end):
    message = f"Offset: {i*PSIZE}\nNumBytes: {PSIZE}\n\n"
    client.sendto(message.encode(), (SNAME, SPORT))
    time.sleep(0.01)
rates = [0.01]
while (flag and count > 0):
    j = 0
    decrease = False
    sleepflag = False
    while end <= (size//PSIZE + 1) and start < (size//PSIZE + 1):
        print(start*PSIZE,end,size//PSIZE + 1,size)
        if receivedlist[start]!="#":
            start += 1
            continue
        sleepflag = False
        decrease = False

        # Sending a burst
        burstsizelist.append([min(j+k, size//PSIZE + 1)-j, time.time()-initial_time])
        wait = True
        init_time = -1
        count = 0
        while wait:
            print("waiting for start")
            try:
                # s = start*PSIZE
                # message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"
                # client.sendto(message.encode(), (SNAME, SPORT))
                data, addr = client.recvfrom(2048*2048)
                # print("something received")
                resp = data.decode()
                recv_time = time.time()
                if init_time != -1:
                    rate = recv_time-init_time
                    rates.append(rate)
                fields = resp.split("\n")
                ans = ""
                if (fields[0].split())[0] == "Size:":
                    continue
                '''
                Offset: [offset]\n 
                NumBytes: [number of bytes]\n 
                Squished\n 
                \n 
                NUMBYTES OF DATA 
                '''
                decrease=decrease or ("Squished" == fields[2])
                sq_count+=int("Squished" == fields[2])
                squishedlist.append([int(("Squished" == fields[2])), time.time()-initial_time])
                # print("start to process")
                for i in range(4 if ("Squished" == fields[2]) else 3 , len(fields)):
                    if (fields[i] == '\x00'):
                        continue
                    if (i == len(fields)-1):
                        ans += fields[i]
                    else:
                        ans += fields[i]+"\n"
                # print("done processing")
                offset = int(fields[0].split()[1])

                if receivedlist[offset//PSIZE] == "#":
                    receivetimelist[offset//PSIZE] = recv_time-initial_time
                    count -= 1
                    rtt[offset//PSIZE] = receivetimelist[offset//PSIZE] - sendtimelist[offset//PSIZE]
                    RTT = RTT*0.875+rtt[offset//PSIZE]*0.125
                    # client.settimeout(0.01*RTT)
                receivedlist[offset//PSIZE] = ans
                if (offset//PSIZE == start):
                    start += 1
                    wait = False
                    sleeptime=min(0.01,sleeptime+0.001)
                # print("finished this")
            except:
                init_time = time.time()
                count += 1
                if count >= 3:
                    s = start*PSIZE
                    message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"
                    # time.sleep(0.004)
                    client.sendto(message.encode(), (SNAME, SPORT))
                    print("Message sent to server", s)
                wait = True
        if (end<(size//PSIZE + 1)):
            s = end*PSIZE
            message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"
            # time.sleep(sleeptime)
            client.sendto(message.encode(), (SNAME, SPORT))
            end+=1
        # time.sleep(max(0.001,max(rates)))
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

with open("squished.txt", "w") as f:
    for i in range(len(squishedlist)):
        f.write(f"{squishedlist[i][1]}|{squishedlist[i][0]}#")

# print(rates)
