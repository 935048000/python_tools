#!/usr/bin/env python
#coding=utf-8

import paramiko
import threading
#import sys,getopt
from os import path
from sys import argv


#多线程锁
lock = threading.RLock()

#读取主机个数
def hostcount(FILE):
    j=1
    file = open(FILE,"r")
    for i in file:
        if i.endswith("\n"):
            j = j+1
    file.close()
    return j


#执行命令
def ssh(ip,username,passwd,CMD):
    lock.acquire()
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ip,22,username,passwd,timeout=5)
        stdin,stdout,stderr = s.exec_command(CMD)
        out = stdout.read()
        err = stderr.read()
        print '================ START ==================='
        print '[SUCCEED] Connect Succeed. IP = %s \n' % (ip)
        print out
        if err != " ":
            print err
        print '================= END ===================='
        s.close()
    except:
        print '================ START ==================='
        print '[Error] Connect False. IP = %s \n' %(ip)
        print '================= END ===================='

    lock.release()
def main(FILE,CMD):
    #cmd = "date"
    f = open(FILE,'r')
    j = hostcount(FILE)
    threads = j
    while True:
        t = f.readline()
        host = t.strip(",").split(",")
        if len(host) == 1:
            break
        ip = host[0]
        username = host[1]
        passwd = host[2]
        a = threading.Thread(target=ssh,args=(ip,username,passwd,CMD))
        a.start()
    f.close()
    return 0

#功能测试
if __name__ == '__main__':
    try:
        if path.exists(argv[1]) == False:
            print "[ERROR] file not found. Please enter the correct file"
            exit(1)
        FILE = argv[1]
        CMD = argv[2]
        main (FILE, CMD)
    except:
        print "[ERROR] Please input command"
        print "Hello:"
        print "usage: "+argv[0]+" <hostname file> <command>"
        print "Rigorous host name file format."
        print "ip,username,password,(3 a ',')"










