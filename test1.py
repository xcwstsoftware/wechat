#将A.txt，以空格为分隔符，每行最后一个数据读出，写到B.txt中
#-*- coding: UTF-8 -*-
import re
import sys
import os

str=[]
fa=open("A.txt",'r')

for line in fa.readlines():
    print (line)
    str1=line.split(" ")[-1]
    print (str1)
    str.append(str1)
fb=open("B.txt",'a')
for i in str:
    fb.write(i)

fa.close()
fb.close()
