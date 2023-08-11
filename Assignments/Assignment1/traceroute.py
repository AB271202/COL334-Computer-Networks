#!/usr/bin/env python3

import os
# site="www.google.com"

site=input("Enter site: ")

# Getting the IP Address
if os.system(f"nslookup {site} | awk 'NR == 6'>temp")==0:
	with open("temp","r") as f:
		x=f.readline()
		IP=x.split()[1]

# Simulating traceroute
i=1
print(f"traceroute to {site} ({IP}), 64 hops max")
while os.system(f"ping -c 1 -t {i} {site} > temp") and i<=64:
	with open("temp","r") as f:
		x=f.readlines()
		# print(x)
		try:
			if i==1: print(i,"\t",x[1].split()[2][1:-1])
			else: print(i,"\t",x[1].split()[1])
		except: print(i,"\t","* * *")
		# print()
		i+=1
with open("temp","r") as f:
	x=f.readlines()
	try: print(i,"\t",x[1].split()[4][1:-2])
	except: print(i,"\t","* * *")
	# print()
	i+=1
os.remove("temp")