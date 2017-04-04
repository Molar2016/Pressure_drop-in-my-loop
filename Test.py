# -*- coding: utf-8 -*-
import sys
import math
sys.path.append("g:\\Github\\iapws")
from iapws import IAPWS97

student = {2:1,3:2,4:3}
print(student)
print(len(student))
m=student.keys()
n=student.values()
print(m)
print(n)
s={}
for i in range(0,2):
    s[i]=1
print(s)
m_cache =1
print(m_cache)
with open('niu.txt','w') as f:
    for item in student:
        f.write(str(item)+' '+str(student[item])+'\n')
water_sat=IAPWS97(T=100+273.15,x=0)
print('hahah')
print(water_sat.Prandt)
print(math.e)