# -*- coding: utf-8 -*-
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
k=input('input something')
print(k)
with open('niu.txt','w') as f:
    for item in student:
        f.write(str(item)+' '+str(student[item])+'\n')