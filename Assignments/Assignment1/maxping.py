#!/usr/bin/python3

import os
site=input("Enter the site: ")
l=1
r=65007
while l<r:
    mid=(l+r)//2
    if os.system("ping -c 1 -s "+str(mid)+" "+site)==0:
        l=mid+1
    else:
        r=mid
print("\n\nMax ping size is: "+str(l-1))
