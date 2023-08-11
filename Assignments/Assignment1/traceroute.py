#!/usr/bin/env python3

import os
import subprocess
site="www.google.com"
# site="157.240.12.35"

# site=input("Enter site: ")

# Getting the IP Address
result=subprocess.run(f"nslookup {site}".split(), stdout=subprocess.PIPE, text=True)
try: IP = result.stdout.split("\n")[5].split()[1]
except: IP = site

# # Simulating traceroute
i=1
print(f"traceroute to {site} ({IP}), 64 hops max")

def regcheck(s):
	try:
		# print(s[-2:],s[0:-2],(s[-2:]=="ms" and s[0:-2].isdigit()))
		return (s[-2:]=="ms")
	except:
		return False
def app(s):
	if regcheck(l3.split()[2]): return s
	else: return "*"

while i<=64:
	times=[]
	try:
		s=subprocess.run(f"nping -c 1 -ttl {i} {site}".split(), stdout=subprocess.PIPE, text=True)
		l1,l2,l3=s.stdout.split('\n')[2],s.stdout.split('\n')[3],s.stdout.split('\n')[5]
		times.append(app(l3.split()[2]))
		s=subprocess.run(f"nping -c 2 -ttl {i} {site}".split(), stdout=subprocess.PIPE, text=True)
		l3=s.stdout.split('\n')[7]
		times.append(app(l3.split()[2]))
		times.append(app(l3.split()[6]))
		print(i,l2.split()[3][1:],times[0],times[1],times[2],sep="  ")
		if l1.split()[5]==l2.split()[3][1:]:break
	except:
		print(f"{i}  * * *")
	i+=1

print()
print("Trace Complete")

# if os.system(f"nslookup {site} | awk 'NR == 6'>temp")==0:
# 	with open("temp","r") as f:
# 		x=f.readline()
# 		IP=x.split()[1]

# print(s.stdout)
# # while os.system(f"ping -c 1 -t {i} {site} > temp") and i<=64:
# # 	with open("temp","r") as f:
# # 		x=f.readlines()
# # 		# print(x)
# # 		try:
# # 			if i==1: print(i,"\t",x[1].split()[2][1:-1])
# # 			else: print(i,"\t",x[1].split()[1])
# # 		except: print(i,"\t","* * *")
# # 		# print()
# # 		i+=1
# # with open("temp","r") as f:
# # 	x=f.readlines()
# # 	try: print(i,"\t",x[1].split()[4][1:-2])
# # 	except: print(i,"\t","* * *")
# # 	# print()
# # 	i+=1
# # os.remove("temp")

# while os.system(f"nping -c 3 -ttl {i} {site} > temp") and i<=64:
# 	with open("temp","r") as f:
# 		x=f.readlines()
# 		print(x)
# 		# try:
# 		# 	if i==1: print(i,"\t",x[1].split()[2][1:-1])
# 		# 	else: print(i,"\t",x[1].split()[1])
# 		# except: print(i,"\t","* * *")
# 		# print()
# 		i+=1

