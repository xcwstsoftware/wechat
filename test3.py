#!/usr/bin/env python3
# coding: utf-8
from selenium import webdriver
import re
import  time  #调入time函数
key = r"javapythonhtmlvpythonhdpythonl"#这是源文本
p1 = r"python"#这是我们写的正则表达式
pattern1 = re.compile(p1)#同样是编译
matcher1 = re.search(pattern1,key)#同样是查询
print (matcher1.group(0))


key = r"<html><body><h1>hello world<h1></body></html>"#这段是你要匹配的文本
p1 = r"(?<=<h1>).+?(?=<h1>)"#这是我们写的正则表达式规则，你现在可以不理解啥意思
pattern1 = re.compile(p1)#我们在编译这段正则表达式
matcher1 = re.search(pattern1,key)#在源文本中搜索符合正则表达式的部分
print (matcher1.group(0))#打印出来







browser = webdriver.Firefox()

browser.get("http://www.baidu.com")
time.sleep(0.3)  #休眠0.3秒
browser.find_element_by_id("kw").send_keys("selenium")
browser.find_element_by_id("su").click()
time.sleep(3)  # 休眠3秒
browser.quit()
