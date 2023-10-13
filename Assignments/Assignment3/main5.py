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
client.settimeout(0.05)

message="SendSize\nReset\n\n"
client.sendto(message.encode(),(SNAME,SPORT))
data,addr=client.recvfrom(2048*2048)
filesize=int(data.split()[1])
print("Filesize: ", filesize)

burst_size = 10
NumBytees = 1440
while(True):
    for i in range(burst_size):
        message = f"Offset: {i*NumBytes}\nNumBytes: {NumBytes}\n\n"