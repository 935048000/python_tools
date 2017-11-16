#/usr/bin/env python
#coding=gbk
#Use python 2 And python 3

import paramiko
from  time import strftime,localtime
from datetime import date,timedelta
from telnetlib import Telnet
from os import path,mkdir,getcwd
from sys import argv

# 时间的全局变量
global NOW_DATE,NOW_TIME
NOW_DATE = strftime ("%Y%m%d", localtime ())#当前日期，格式：YYYYmmdd
NOW_TIME = strftime ("%Y-%m-%d %H:%M", localtime ())#当前时间,格式：YYYY-mm-dd HH:MM

# 路径相关的全局变量
global USERPATH,WORKPATH,DATAPATH
USERPATH = argv[0] # 执行脚本的脚本文件路径
WORKPATH = getcwd() # 执行脚本的当前目录路径
DATAPATH = WORKPATH+"\data" #执行脚本当前路径下的data目录

#数据汇总
class collect:
    """
    Data Collect Class
    """
    #服务器连接OK
    def connect(self, hostname, port, username, password):
        # type: (object, object, object, object) -> object
        global ssh
        global localhost
        ssh = paramiko.SSHClient ()
        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
        ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
        ssh.connect (hostname, port, username, password)

        #hostuser = "[ "+hostname+" "+username+" ]"
        localhost = hostname
        return localhost

    #执行命令OK
    def command(self,CMD,*title):
        cmd = "source ~/.bash_profile;%s" % (CMD)
        input, output, err = ssh.exec_command (cmd)
        output1 = output.read().decode('gbk')
        err1 = err.read()
        if len(title) == 1 and title[0] == "notitle":
            return output1
        else:
            pass
        return "\n[ "+CMD+" ]\n\n"+output1+"\n"

    # 磁盘信息OK
    class diskinfo:
        #系统磁盘信息
        def diskinfo(self):
            CMD = "df -g"
            input, output, err = ssh.exec_command (CMD)
            output = output.read ().decode ()
            err = err.read ().decode ()
            return "\n[ "+CMD+" ]\n\n"+output+err+"\n"


        #磁盘阵列信息
        def diskarray(self):
            CMD1 = "lspv"
            input, output, err = ssh.exec_command (CMD1)
            output1 = output.read ().decode ()
            err1 = err.read ().decode ()

            #计算阵列个数，然后显示单个阵列的详情。
            CMD2 = "lspv | awk '{print $1}' | wc -l"
            input, output, err = ssh.exec_command(CMD2)
            output2 = output.read().decode()
            err2 = err.read().decode()

            #循环输出单个阵列详情
            i = int(output2)
            I = "\n"
            for x in range(i):
                CMD3 = 'lspv hdisk%d'%(x)
                input,output,err = ssh.exec_command(CMD3)
                output3 = output.read().decode()
                err3 = err.read ().decode ()
                I = I+"[ "+CMD3+" ]\n\n"+output3+"\n"+err3+"\n"

            TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"+I
            return TEMP


    # 进程信息OK
    def process(self):

        #ps命令
        CMD2 = 'ps -ef | grep $LOGNAME'
        input,output,err = ssh.exec_command (CMD2)
        output2 = output.read().decode()
        err2 = err.read().decode()

        TEMP = "\n[ lps ]\n\n"+output2+err2+"\n"
        return TEMP

    # 内存信息OK
    def meminfo(self):
        CMD = 'vmstat 1 10'
        input, output, err = ssh.exec_command (CMD)
        output = output.read ().decode ()
        err = err.read ().decode ()
        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    # 关键服务进程内存信息OK
    def servicemem(self):
        #ps命令
        CMD1 = 'ps auwx | head -n 1;ps auwx | grep appv9 | egrep -v "RSS" | sort +5b -6 -n -r'
        input, output, err = ssh.exec_command (CMD1)
        output1 = output.read()
        err1 = err.read().decode()

        return "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"

    # 软硬件错误日志OK
    def errlog(self,num):
        CMD1 = 'errpt -d H -s %s | grep ERROR'%(num)
        input, output, err = ssh.exec_command (CMD1)
        output1 = output.read ().decode ()
        err1 = err.read ().decode ()

        CMD2 = 'errpt -aj BFE4C025 | head -n 56'
        input, output, err = ssh.exec_command (CMD2)
        output2 = output.read ().decode ()
        err2 = err.read ().decode ()

        TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"+"\n[ "+CMD2+" ]\n\n"+output2+err2+"\n"
        return TEMP

    #ping信息OK
    def ping(self,hostname,num):
        CMD = 'ping -c%d %s'%(num,hostname)
        input,output,err = ssh.exec_command(CMD)
        output = output.read().decode()
        err = err.read().decode()

        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    # telnet信息OK
    def telnet(self,hostname,port):
        try:
            tn = Telnet (hostname,port,timeout=10)
        except:
            re = hostname+":"+str(port)+" Connect Error\n\n"
            return "[ telnet ]\n" + re
        re = hostname + ":" + str (port) + " Connect Succeed. Time: %s\n\n" % (NOW_TIME)
        return "[ telnet ]\n"+re

    def telnetexe(self,ip,user,passwd,cmd):
        tn = Telnet (ip)
        tn.read_until ("login: ")
        tn.write (user + "\n")
        tn.read_until ("Password: ")
        tn.write (passwd + "\n")
        tn.write (cmd + "\n")
        tn.write ("exit\n")

        return tn.read_all()

    # 证书信息OK
    def cart(self):
        #证书总数
        CMD1 = 'ls -al ~/dat/Crypto/AgentCert*'
        input,output,err = ssh.exec_command(CMD1)
        output1 = output.read().decode()
        err1 = err.read().decode()

        #每个证书的有效日期
        CMD2 = "for i in `ls -al ~/dat/Crypto/AgentCert* | awk '{print $9}'`;do echo $i;~/src/bin/ShowCert $i | sed -n '17,18'p;done"
        input,output,err = ssh.exec_command(CMD2)
        output2 = output.read ().decode ('gbk')
        err2 = err.read ().decode ('gbk')

        TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"+"\n[ "+CMD2+" ]\n\n"+output2+err2+"\n"
        return TEMP


    # 日志信息
    def loginfo(self,STSTEM):
        #input,output,err = ssh.exec_command(CMD1)
        # if system == "linux":
        #     STSTEM = "tail"
        # else:
        #     STSTEM = "~/bin/ptail"
        CMD1 = "cd ~/log/;ls BK*.log Gateway*.log TM*.log MD*.log T900001.log T900999.log Database.err ~/FlowCtrl.log "
        input1, output1, err1 = ssh.exec_command(CMD1)
        TEMP = output1.read().decode("gbk")
        LogFileList = TEMP.split("\n")
        I = "\n"
        for i in LogFileList[:-1]:
            CMD2 = "cd ~/log/;%s -n 200 %s"%(STSTEM,i)
            input2, output2, err2 = ssh.exec_command (CMD2)
            output2 = output2.read ().decode ("gbk")
            err2 = err2.read ().decode ("gbk")
            I = I+output2+err2+"\n\n"
        return I

    def loganalyze(self,logtxt):
        Today = date.today()
        Yesterday = Today - timedelta(days=1)
        if logtxt == "T900001.log":
            CMD1 = "cd ~/log/;~/bin/ptail -n 100 %s | grep %s | wc -l"%(logtxt,Yesterday)
            #CMD1 = "cd ~/log/;~/bin/ptail -n 100 T900001.log | grep 2017-10-13 | wc -l"
            input1, output1, err1 = ssh.exec_command (CMD1)
            TEMP = output1.read ().decode ("gbk")
            if int (TEMP) >= 1:
                return "T900001.log OK!\n"
            else:
                return "T900001.log NO!\n"
        elif logtxt == "FlowCtrl.log":
            CMD1 = "~/bin/ptail -n 200 ~/FlowCtrl.log | grep 'kill -9' | wc -l"
            input1, output1, err1 = ssh.exec_command (CMD1)
            TEMP = output1.read ().decode ("gbk")
            if int (TEMP) >= 1:
                return "FlowCtrl.log NO!\n"
            else:
                return "FlowCtrl.log OK!\n"



    # 信息存到文件OK
    def filesave(self,data,mode,*FileType):
        #数据存放在当前目录下的data目录
        if path.exists(DATAPATH):
            pass
        else:
            mkdir(DATAPATH)

        if len(FileType) == 1:
            if FileType[0] == "log":
                file_type = "log"
            elif FileType[0] == "txt":
                file_type = "txt"

            elif FileType[0] == "set":
                FILE_NAME1 = '%s/set_%s.txt' % (DATAPATH, NOW_DATE)
                file = open (FILE_NAME1, 'a')
                file.write (data.encode ('gbk'))

            elif FileType[0] == "sql":
                FILE_NAME1 = '%s/pgsql_%s.sql' % (DATAPATH, NOW_DATE)
                file = open (FILE_NAME1, 'a')
                file.write (data)

            file.close ()
            return 0
        elif len(FileType) == 0:
            file_type = "txt"

        if mode == "add" :
            FILE_NAME1 = '%s/%s_%s.%s'%(DATAPATH,localhost,NOW_DATE,file_type)
            file = open (FILE_NAME1, 'a')
            file.write (data.encode('gbk'))
        elif mode == "new":
            FILE_NAME2 = '%s/%s_%s.%s'%(DATAPATH,localhost,NOW_DATE,file_type)
            file = open(FILE_NAME2,'w')
            file.write(data.encode('gbk'))
        else :
            return "mode [ERROR]"
        file.close()
        return 0

    #连接断开OK
    def close(self):
        ssh.close()
        TEMP="\nClose OK!\n"
        return TEMP



if __name__ == '__main__':
    print("local run script.....")
    #print DATAPATH
    ## 程序测试代码
    # a = collect()
    # a.connect ('10.13.0.9', 22, 'xxxx', 'xxxxxx')#指定主机
    # t=a.command("df -g|head -n 1'","notitle")
    #
    # d=a.diskinfo()
    # t=d.diskinfo()
    # a.filesave (t, 'add')#写入文件
    # t=d.diskarray()
    # a.filesave (t, 'add')
    #
    # t = a.process ()
    # a.filesave (t, 'add')
    #
    # t=a.meminfo()
    # a.filesave (t, 'add')
    #
    # t=a.servicemem()
    # a.filesave (t, 'add')
    #
    # t=a.errlog("0701000017")
    # a.filesave (t, 'add')
    #
    #t = a.dbinfo()
    # #t=a.dbdump()
    #
    # t=a.ping("127.0.0.1",3)
    # a.filesave (t, 'add')
    #
    #
    # t=a.cart()
    # a.filesave (t, 'add')

    #t = a.telnet("10.13.0.9",7000)
    #a.filesave (t, 'add')

    # t=a.loginfo()
    # a.filesave (t, 'add','set')
    #
    #t = a.loganalyze("FlowCtrl.log")
    # print (t)#输出采集内容
    # a.close ()#断开ssh连接





