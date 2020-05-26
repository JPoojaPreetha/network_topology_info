import copy
import re
import datetime
import copy
import configuration as conf
import re

import matplotlib.dates as md
import matplotlib.pyplot as plt
from datetime import datetime
import math
import time
import copy


def network(fname):
    file1 = open(fname,"r")
    lines = file1.readlines()
    file2 = open("temp.txt","w+")
    for i in lines:
        if i!="\n":
            file2.write(i)
    file2.close()
    f3=open("temp.txt","r")
    line=f3.readlines()
    dno=[]
    ip=[]
    for i in line:
        i=i.strip()
        if re.match(r"^-- DB (.*):",i):
            dno.append(i[7:9])
        elif re.match(r"^QCA IEEE 1905.1 device:.*",i):
                ip.append(i[24:41])
    
    
    f3.close()
    dno=[int(i) for i in dno]
    ul=[]
    for x in dno: 
        if x not in ul: 
            ul.append(x) 
    ul.sort(reverse=True)
    
    g = globals()
    for i in range(1,ul[0]+1):
         g['sat_{}'.format(i)] = []
         g['rel_{}'.format(i)] = []
         g['ups_{}'.format(i)] = []
         
    f3=open("temp.txt","r")
    line=f3.readlines()
    f4=open("tmp1.txt","w+")
    #copy=False
    for i in line:
        for j in range(1,ul[0]+1):
            i=i.strip()
            if re.match(r"^#"+str(j)+".*",i):
                      f4.write(i+"\n")
                      break
            elif re.match(r"^Upstream Device:.*",i):
                      f4.write(i+"\n")
                      break
    f4=open("tmp1.txt","r")
    lines=f4.readlines()
    pre=""
    for i in lines:
        for j in range(1,ul[0]+1):
            if re.match(r"^Upstream Device:.*",i)and re.match(r"^#"+str(j)+".*",pre):
                  g['ups_%s' % j].append(i[17:34])
        pre=i
    f3=open("temp.txt","r")
    line=f3.readlines()
    prev=""

    for i in line:
        for j in range(1,ul[0]+1):
            i=i.strip()
            if re.match(r"^#"+str(j)+".*",i):
                  g['sat_%s' % j].append(i[28:45])
                
            elif re.match(r"Relation:.*",i) and re.match(r"^#"+str(j)+".*",prev):
                g['rel_%s' % j].append(i[10:25])
            
        prev=i
    f3.close()
    
    f=False
    trel=[]
    for i in range(0,len(ip)):
        for j in range(1,ul[0]+1):
            if g['rel_%s' % j][i]=="Direct Neighbor" :
                f=True
                continue
            else:
                f=False
                break
        if f==True:
            trel.append("Star")
            
        else:
            trel.append("Daisy chain")

    
    for i in range(0,len(ip)):
            print("\niteration ",i+1)
            print("router : "+ip[i]+" is connected to "+str(dno[i])+" satellites ")
            if trel[i]=="Star":
                    print("Satellites follows Star topology ")
                    
            else:
                    print("Satellites follows Daisy Chain topology ")
                    
       
    print("\n")
    m=0
    for i in range(1,ul[0]+1):
            if all(ele == g['sat_%s' % str(i)][0] for ele in g['sat_%s' % str(i)]):
                m+=1
                print("No change in MAC address of satellite: "+str(i))
                continue
            else:
            
                print("Change in MAC address of satellite: "+str(i))
                continue
    print("\n")
    for i in range(0,len(dno)-1):
        if dno[i]!=dno[i+1]:
                print("change in number of satellite")
                break
        else:
            print("No change in number of satellite")
            break
    print("\n")
    u=0
    for i in range(1,ul[0]+1):
            if all(ele == g['ups_%s' % str(i)][0] for ele in g['ups_%s' % str(i)]):
                u+=1
                print("No change in upstream of satellite: "+str(i))
                continue
            else:
                
                print("Change in upstream of satellite: "+str(i))
                continue
    print("\n")
    t=0
    for i in range(0,len(ip)-1):
        if trel[i]!=trel[i+1]:
            t+=1
    
    for i in range(0,len(dno)-1):
            if u!=ul[0] and m!=ul[0] and t!=len(ip)-1 :
                print("change in topology ")
                break
            else:
                print("No change in topology ")
                break
