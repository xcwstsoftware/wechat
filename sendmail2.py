#coding:utf-8  #强制使用utf-8编码格式
import smtplib #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
import re
import sys
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

str=[]
fa=open("A.txt",'r')



my_sender='wst584412572@163.com' #发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user='584412572@qq.com' #收件人邮箱账号，为了后面易于维护，所以写成了变量
def mail(to_my_user):
  ret=True
  try:
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject']="天猫内部优惠券" #邮件的主题，也可以说是标题
    msgText=MIMEText('撒旦法第三方放水阀','plain','utf-8')
    msgText['From']=formataddr(["tony",my_sender])  #括号里的对应发件人邮箱昵称、发件人邮箱账号
    print("22okto_my_user=="+to_my_user)
    msgText['To']=formataddr(["美女/帅哥",to_my_user])  #括号里的对应收件人邮箱昵称、收件人邮箱账号
    msgRoot.attach(msgText)
    fp = open('QR.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '')
    msgRoot.attach(msgImage)
    print("44ok")
    server=smtplib.SMTP("smtp.163.com",25) #发件人邮箱中的SMTP服务器，端口是25
    print("55ok")
    server.login(my_sender,"wst1987")  #括号中对应的是发件人邮箱账号、邮箱密码
    print("66ok")
    server.sendmail(my_sender,to_my_user,msgRoot.as_string())  #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    print("77ok")
    server.quit()  #这句是关闭连接的意思
  except Exception:  #如果try中的语句没有执行，则会执行下面的ret=False
    ret=False
  return ret
for line in fa.readlines():

  if line.isspace():
    pass
  else:
    str1=''.join([x for x in line if x != " "]).split('|')[0]
    str1=str1+'@qq.com'
    str1=str1.strip().replace("\n", "")
    print (str1)
    ret=mail(str1)
    if ret:
        print("ok") #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
        time.sleep( 5 )
    else:
        print("filed") #如果发送失败则会返回filed
        time.sleep( 5 )
