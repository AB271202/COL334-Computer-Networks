from matplotlib import pyplot as plt

sendtimelist=[]
receivetimelist=[]
burstsizes=[]

with open("sendtimes.txt", "r") as f:
    sendtimelist = f.readline().split("#")
    sendtimelist.pop()
    for i in range(len(sendtimelist)):
        offset,time = map(float, sendtimelist[i].split("|"))
        sendtimelist[i] = [time, offset]

with open("receivetimes.txt", "r") as f:
    receivetimelist = f.readline().split("#")
    receivetimelist.pop()
    for i in range(len(receivetimelist)):
        offset, time = map(float, receivetimelist[i].split("|"))
        receivetimelist[i] = [time, offset]

with open("burstsizes.txt", "r") as f:
    burstsizes = f.readline().split("#")
    burstsizes.pop()
    for i in range(len(burstsizes)):
        time, burst = map(float, burstsizes[i].split("|"))
        burstsizes[i] = [time, burst]
'''
# Send times
x1 = [sendtimelist[i][0] for i in range(len(sendtimelist))]
y1 = [sendtimelist[i][1] for i in range(len(sendtimelist))]

# Receive times
x2 = [receivetimelist[i][0] for i in range(len(receivetimelist))]
y2 = [receivetimelist[i][1] for i in range(len(receivetimelist))]

plt.scatter(x1, y1, label='Requests', color='blue', linestyle='-', marker='o')
plt.scatter(x2, y2, label='Replies', color='orange',
            linestyle='--', marker='x')

plt.xlabel("Time (s)")
plt.ylabel("Offset")
plt.title('Sequence-number Trace')
plt.legend()

plt.show()
plt.close()

# Graph 2
x1 = []
y1 = []
x2 = []
y2 = []
for i in range(len(sendtimelist)):
    if sendtimelist[i][0] > 0.5:
        continue
    x1.append(sendtimelist[i][0]*1000)
    y1.append(sendtimelist[i][1])

# Send times
for i in range(len(receivetimelist)):
    if receivetimelist[i][0] > 0.5:
        continue
    x2.append(receivetimelist[i][0]*1000)
    y2.append(receivetimelist[i][1])

plt.scatter(x1, y1, label='Requests', color='blue', linestyle='-', marker='o')
plt.scatter(x2, y2, label='Replies', color='orange',
            linestyle='--', marker='x')

plt.xlabel("Time (ms)")
plt.ylabel("Offset")
plt.title('Zoomed in Sequence-number Trace')
plt.legend()

plt.show()

plt.close()
'''

xb=[burstsizes[i][0] for i in range(len(burstsizes))]
yb=[burstsizes[i][1] for i in range(len(burstsizes))]

plt.plot(xb,yb)
plt.xlabel("Time (ms)")
plt.ylabel("Burstsizes")
plt.title('Burstsizes v/s time')
plt.legend()

plt.show()