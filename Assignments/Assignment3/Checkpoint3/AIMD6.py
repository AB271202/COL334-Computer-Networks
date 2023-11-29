import hashlib
import time
from socket import *


'''
10.17.7.218
10.17.7.134
10.17.51.115
10.17.6.5
'''

SNAME = "localhost"
SPORT = 9802
PSIZE = 1448


client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(0.008)
dec_count = 0

# Receive the file size
timeout = 0.004
sleeptime = 0.008

tries=0
while (tries<20):
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
        tries+=1
        continue
if tries==20:
    raise Exception("Server not reachable")
rtt=[]
for _ in range(10):
    meas_time=time.time()
    while (tries<20):
        try:
            message = "SendSize\nReset\n\n"
            client.sendto(message.encode(), (SNAME, SPORT))
            print("SendSize sent to server")
            rtt.append(time.time()-meas_time)
            data, addr = client.recvfrom(2048*2048)
            break
        except:
            print("[Timeout] Trying again...")
            tries+=1
            continue

avdrtt = sum(rtt)/len(rtt)
client.settimeout(avdrtt+0.003)


size = int(data.split()[1])
print("[SIZE]", size)

flag = True
k = 4
count = size//PSIZE + 1  # Number of packets to receive
receivedlist = ["#"]*count
remaining = [i for i in range(count)]


# For plotting
initial_time = time.time()
sendtimelist = []
receivetimelist = [0]*count
burstsizelist = list()
squishedlist=list()

sq_count = 0
rtt = [0.004]*count
RTT = 0.004
k1 = 4.0
decreasecount=0
while (flag and count > 0):
    j = 0
    decrease = False
    sleepflag = False
    while j < (size//PSIZE + 1):
        sleepflag = False
        decrease = False

        # Sending a burst
        burst=0
        for i in range(j, min(j+k, size//PSIZE + 1)):

            if (receivedlist[i] != "#"):
                continue
            sleepflag = True
            s = i*PSIZE
            message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"

            client.sendto(message.encode(), (SNAME, SPORT))
            burst+=1
            sendtimelist.append([s,time.time()-initial_time])
            print("Requested [Offset]", s, "\t [Burst Size]", k)
        burstsizelist.append([burst, time.time()-initial_time])
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
                '''
                Offset: [offset]\n 
                NumBytes: [number of bytes]\n 
                Squished\n 
                \n 
                NUMBYTES OF DATA 
                '''
                decrease = decrease or ("Squished" == fields[2])
                sq_count+=int("Squished" == fields[2])
                squishedlist.append([int("Squished" == fields[2]), time.time()-initial_time])
                for i in range(4 if "Squished" == fields[2] else 3 , len(fields)):
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
                    # rtt[offset//PSIZE] = receivetimelist[offset//PSIZE] - sendtimelist[offset//PSIZE]
                    RTT = RTT*0.125+rtt[offset//PSIZE]*0.875
                receivedlist[offset//PSIZE] = ans
            else:
                decrease = True
                decreasecount+=1

        j += k
        if sleepflag:
            time.sleep(sleeptime)
        if decrease:
            if k<=1:
                sleeptime = min(0.02,sleeptime+0.003) # Increase sleeptime if burst size at 1
            dec_count += max(1,k-start+count) # This tells us how many we expected but didn't get
            k = max(k//2, 1)
            k1 = k
        elif start-count > 0:
            # sleeptime = max(0.008,sleeptime-0.001)
            # k = min(k+1, count+1)
            if dec_count>int(2000*RTT) or sq_count>0:
                sleeptime = max(0.01,sleeptime-0.001)
                k1 = k1+(1/k1)
                # k1+=1
            # k+=1
            else:
                sleeptime = max(0.006,sleeptime-0.001)
                k1 = k1+1
            k = int(k1)

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
print(decreasecount)

with open("sendtimes.txt", "w") as f:
    for i in range(len(sendtimelist)):
        f.write(f"{sendtimelist[i][0]}|{sendtimelist[i][1]}#")

with open("receivetimes.txt", "w") as f:
    for i in range(len(receivetimelist)):
        f.write(f"{i*PSIZE}|{receivetimelist[i]}#")

with open("burstsizes.txt", "w") as f:
    for i in range(len(burstsizelist)):
        f.write(f"{burstsizelist[i][1]}|{burstsizelist[i][0]}#")

with open("squished.txt", "w") as f:
    for i in range(len(squishedlist)):
        f.write(f"{squishedlist[i][1]}|{squishedlist[i][0]}#")
