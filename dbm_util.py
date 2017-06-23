#!/usr/bin/env python3
# coding: utf-8

from wxpy import *
from config import *
import re
from wxpy.utils import start_new_thread
import time
import os
from kick_votes import KickVotes
import sys
#python dbm

#Author : Hongten
#MailTo : hongtenzone@foxmail.com
#QQ     : 648719819
#Blog   : http://www.cnblogs.com/hongten
#Create : 2013-08-09
#Version: 1.0

import dbm
'''
    在python的应用程序中，不需要关系型数据库时，如MySQL
    可以使用python提供的持久字典dbm来存储名称和值(键值对)
    这个类似于java的中的java.util.Map对象。
    区别如下：

        存储在硬盘上面
        dbm的键值对必须是字符串类型

    python支持的dbm模块

        dbm         -- 常用的dbm模块
        dbm.dumb    -- 可移植的，简单的dbm库
        dbm.gnu     -- GNU dbm库

    创建一个dbm对象
    db = dbm.open('c:\\test\\Hongten.pag', 'c')

        'r'         --  open existing database for reading only(default)
        'w'         --  open existing database for reading and writing
        'c'         --  open database for reading and writing,creating it if it does'n exist
        'n'         --  always creat a new,empty database,open for reading and writing

    给dbm对象赋值，dbm中的键值对都是以字符串形式出现
    db['name'] = 'Hongten'
    db['gender'] = 'M'

    保存,在dbm对象关闭的时候即可保存数据
    db.close()

    删除值：
    del db['name']
    会把db对象中的key = 'name'的值删除

    遍历整个db对象：
    for key in db.keys():
        print(key)

'''

#print(sys.path[0]+'\\Hongten.pag')
#db = dbm.open(sys.path[0]+'\\Hongten.pag', 'c')

def get_dbm():
    '''Open database, creating it if necessary.'''
    return dbm.open(sys.path[0]+'\\Hongten.pag', 'c')

def save(db):
    '''保存数据'''
    print('保存数据...')
    db['name'] = 'Hongten'
    db['gender'] = 'M'
    db['address'] = '广东省广州市'
    db['isaddress'] = 'True'
    db.close()

def fetchall(db):
    '''遍历所有'''
    print('遍历所有数据...')
    if db is not None:
        for key in db.keys():
            print('{} = {}'.format(key.decode('utf-8'), db[key].decode('utf-8')))
    else:
        print('dbm object is None!')

def fetchone(db, key):
    '''获取某个键值对'''
    print('获取[{}]键值对数据...'.format(key))
    if db is not None:
        print(db[key])
    else:
        print('dbm object is None!')

def delete(db, key):
    '''删除某个键值对'''
    print('删除[{}]键值对数据...'.format(key))
    if db is not None:
        del db[key]
    else:
        print('dbm object is None!')

def deleteall(db):
    '''删除所有键值对'''
    print('删除所有键值对数据...')
    if db is not None:
        for key in db.keys():
            del db[key]
    else:
        print('dbm object is None!')
'''
def main():
    db = get_dbm()
    save(db)
    print('#' * 50)
    db = get_dbm()
    fetchall(db)
    print('#' * 50)
    fetchone(db, 'name')
    print('#' * 50)
#    delete(db, 'gender')
    fetchall(db)
    print('#' * 50)
#    deleteall(db)
    fetchall(db)

if __name__ == '__main__':
    main()
'''
