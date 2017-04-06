# -*- coding: utf-8 -*-
import sys
import math
from numpy import arange

sys.path.append("g:\\Github\\iapws")
from iapws import IAPWS97

student = {2: 1, 3: 2, 4: 3}
print(student)
print(len(student))
m = student.keys()
n = student.values()
print(m)
print(n)
s = {}
for i in range(0, 2):
    s[i] = 1
print(s)
m_cache = 1
print(m_cache)
with open('niu.txt', 'w') as f:
    for item in student:
        f.write(str(item) + ' ' + str(student[item]) + '\n')
water_sat = IAPWS97(T=100 + 273.15, x=0)

print(water_sat.Prandt)
print(math.e)
h = 1.4
print(type(h))
water_sat = IAPWS97(T=100 + 273.15, x=0)
steam_sat = IAPWS97(T=100 + 273.15, x=1)

g_ = 500.0
u_zhesuan_g = 10.0
u_zhesuan_l = 0.4
k = (water_sat.v / steam_sat.v) ** 0.1
k1 = u_zhesuan_g * (1 + (u_zhesuan_l / u_zhesuan_g) ** k)
k2 = 2.9 * (9.8 * 0.0589 * (water_sat.v - water_sat.v ** 2 / steam_sat.v)) ** 0.25
print(u_zhesuan_g * (k1 + k2) ** -1)
print('hahah')
i=1
def f():
    i=2
    return i
print(i)
print(f())
while mina<=j<=mixa:
    if j <0.01:
        ma.append(j)
        j=j+0.0005
    else:
        ma.append(j)
        j=j+0.001

