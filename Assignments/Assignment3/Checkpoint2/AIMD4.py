import hashlib
import time
from socket import *

# SNAME = "10.194.49.169"
# SNAME = "localhost"
SNAME = gethostbyname("vayu.iitd.ac.in")
# SNAME = "10.17.7.218"
SPORT=9801
PSIZE=1448




def next(s,receivedlist):
    curr_index = s//PSIZE
    found = False
    for i in range(curr_index,len(receivedlist)):
        if receivedlist[i]=="#":
            found = True
            return i*PSIZE
    if not found:
        for i in range(0,len(receivedlist)):
            if receivedlist[i]=="#":
                found = True
                return i*PSIZE
    return 0


client=socket(AF_INET, SOCK_DGRAM)
client.settimeout(0.004)

# message="SendSize\nReset\n\n"
# client.sendto(message.encode(),(SNAME,SPORT))

# wait = True
# while(wait):
#     try:
#         data,addr=client.recvfrom(2048*2048)
#         wait = False
#     except:
#         pass
# size=int(data.split()[1])
# print(data.decode())

# Receive the file size
while(True):
    try:
        message = "SendSize\nReset\n\n"
        client.sendto(message.encode(), (SNAME, SPORT))
        print("SendSize sent to server")
        data, addr = client.recvfrom(2048*2048)
        break
    except:
        print("[Timeout] Trying again...")
        continue

size = int(data.split()[1])
print("[SIZE]", size)


s = 0
ans = ""
flag = True
k = 4
count = size//PSIZE + 1
receivedlist = ["#"]*(count)
remaining = [i for i in range(count)]
initial_time=time.time()
sleeptime = 0.008

# For plotting
sendtimelist = [0]*count
receivetimelist = [0]*count
rtt = [0.004]*count
k1 = k
RTT = 0.004

while (flag and count>0):
    j = 0
    # for i in range(size//PSIZE + 1):
    decrease = False
    sleepflag = False
    while j<(size//PSIZE + 1):
        sleepflag = False
        decrease = False
        # temp = 0
        for i in range(j,min(j+k,size//PSIZE + 1)):
            # if (temp>k or temp>count):
            #     break
            if (receivedlist[i]!="#"):
                continue
            # temp+=1
            sleepflag = True
            s = i*PSIZE
            message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"
            
            client.sendto(message.encode(),(SNAME,SPORT))
            sendtimelist[s//PSIZE]=(time.time()-initial_time)
            print("Message sent to server",s,k,sleeptime,RTT)
        start = count
        for i in range(j,min(j+k,size//PSIZE + 1)):
            if (receivedlist[i]!="#"):
                continue
            # s = i*PSIZE
            # message = f"Offset: {s}\nNumBytes: {PSIZE}\n\n"
            # client.sendto(message.encode(),(SNAME,SPORT))
            # print("Message sent to server",s)
            # resp = ""
            received = False
            try:
                data,addr=client.recvfrom(2048*2048)
                resp = data.decode()
                received = True
            except:
                received = False
            if received:
                recv_time=time.time()
                
                if ("Squished" in resp):
                    fields = resp.split("\n")
                    ans = ""
                    if (fields[0].split())[0]=="Size:":
                        continue
                    for i in range(4,len(fields)):
                        if (fields[i] == '\x00'):
                            continue
                        if (i==len(fields)-1):
                            ans+=fields[i]
                        else:
                            ans+=fields[i]+"\n"
                    offset = fields[0]
                    offsetnum = int(offset.split()[1])
                    # if receivedlist[offsetnum//PSIZE] == "#":
                    #     receivetimelist[offsetnum//PSIZE]=recv_time-initial_time
                    #     count-=1
                    # receivedlist[offsetnum//PSIZE]=ans
                    decrease = True
                else:
                    ans = ""
                    fields = resp.split("\n")
                    if (fields[0].split())[0]=="Size:":
                        continue
                    for i in range(3,len(fields)):
                        if (fields[i] == '\x00'):
                            continue
                        if (i==len(fields)-1):
                            ans+=fields[i]
                        else:
                            ans+=fields[i]+"\n"
                    offset = fields[0]
                    offsetnum = int(offset.split()[1])
                # if (count%3 == 0):
                #     time.sleep(0.02)
                if receivedlist[offsetnum//PSIZE] == "#":
                    receivetimelist[offsetnum//PSIZE]=recv_time-initial_time
                    count-=1
                    rtt[offsetnum//PSIZE] = receivetimelist[offsetnum//PSIZE]-sendtimelist[offsetnum//PSIZE]
                    # client.settimeout(sum(rtt)/(size//PSIZE + 1)*0.5+0.004)
                    # client.settimeout(RTT*0.125+rtt[offsetnum//PSIZE]*0.875)
                    RTT = RTT*0.125+rtt[offsetnum//PSIZE]*0.875
                receivedlist[offsetnum//PSIZE]=ans
            else:
                decrease = True
        # time.sleep(0.01)
        # print("received",start-count)
        j += k
        if sleepflag :
            # if 55*RTT<0.03:
            #     x = 55*RTT
            # else:
            #     x=sleeptime
            # time.sleep(min(55*RTT,sleeptime))
            time.sleep(sleeptime)
        if decrease:
            if k<=1:
                sleeptime = min(0.02,sleeptime+0.003)
                # time.sleep(0.1)
            k = max(k//2,1)
            # k = 1
            # k1 = 1
        elif start-count>0:
            sleeptime = max(0.008,sleeptime-0.001)
            k+=1
            # k = int(k1)
    
    time.sleep(0.02)
ans2 = ""
ans2 = ans
ans  = ""
for i in range(size//PSIZE+1):
    ans+=receivedlist[i]

md5_hex = hashlib.md5(ans.encode('utf-8')).hexdigest()
print("MD5 Hash of the file:", md5_hex)
message = f"Submit: 2021CS10134@teamname\nMD5: {md5_hex}\n\n"
client.sendto(message.encode(), (SNAME, SPORT))


msg1 = ""
while(not ("Result" in msg1 )):
    wait = True
    while(wait):
        try:
            msg,addr=client.recvfrom(2048*2048)
            wait = False
        except:
            # pass
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
