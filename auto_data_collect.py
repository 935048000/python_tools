#/usr/bin/env python
#coding=gbk

import paramiko
import time
import telnetlib
from os import path,mkdir

#数据汇总
class collect:
    #服务器连接OK
    def connect(self,hostname,port,username,password):
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
    def command(self,CMD):
        input, output, err = ssh.exec_command(CMD)
        output = output.read().decode("gbk")
        err = err.read().decode("gbk")
        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    # 磁盘信息OK
    class diskinfo:
        #系统磁盘信息
        def diskinfo(self):
            CMD = "df -g"
            input, output, err = ssh.exec_command (CMD)
            output = output.read ().decode ()
            err = err.read ().decode ()
            return "\n[ "+CMD+" ]\n\n"+output+err+"\n[ "+CMD+" END ]\n"


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
                I = I+"[ "+CMD3+" ]\n\n"+output3+"\n"+"[ "+CMD3+" END ]\n\n"

            TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n[ "+CMD1+" END ]\n"+I+err3+"\n"
            return TEMP


    #进程信息OK
    def process(self):
        #s命令
        CMD1 = "~/bin/s"
        input,output,err = ssh.exec_command(CMD1)
        output1 = output.read().decode('gbk')
        err1 = err.read().decode('gbk')

        #ps命令
        CMD2 = 'ps -ef | grep $LOGNAME'
        input,output,err = ssh.exec_command (CMD2)
        output2 = output.read().decode()
        err2 = err.read().decode()

        TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"+"\n[ "+CMD2+" ]\n\n"+output2+err2+"\n"
        return TEMP

    #内存信息OK
    def meminfo(self):
        CMD = 'vmstat 1 10'
        input, output, err = ssh.exec_command (CMD)
        output = output.read ().decode ()
        err = err.read ().decode ()
        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    #CPU信息OK
    def cpuinfo(self):
        #ps命令
        CMD1 = 'ps auwx | head -n 1;ps auwx | grep appv9 | egrep -v "RSS" | sort +5b -6 -n -r'
        input, output, err = ssh.exec_command (CMD1)
        output1 = output.read()
        err1 = err.read().decode()

        #topas命令(交互式命令，脚本不可用)
        # CMD2 = 'topas'
        # input2,output,err = ssh.exec_command(CMD2)
        # input2.write("q\n")
        # input2.flush ()
        # output2 = output.read().decode()
        # err2 = err.read().decode()

        return "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"

    #错误日志OK
    def errlog(self,num):
        CMD1 = 'errpt -d H -s %s'%(num)
        input, output, err = ssh.exec_command (CMD1)
        output1 = output.read ().decode ()
        err1 = err.read ().decode ()

        CMD2 = 'errpt -aj BFE4C025'
        input, output, err = ssh.exec_command (CMD2)
        output2 = output.read ().decode ()
        err2 = err.read ().decode ()

        TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"+"\n[ "+CMD2+" ]\n\n"+output2+err2+"\n"
        return TEMP


    #数据库信息NO
    def dbinfo(self):
        # a,b,c = ssh.exec_command ('cd ~/')
        CMD='isql -Usxlottery -Psxlottery -Dsxlottery -i isql.txt -o osql.txt'
        input,output,err = ssh.exec_command(CMD)
        output = output.read().decode()
        err = err.read().decode()

        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    #数据库备份NO
    def dbdump(self):

        return 0

    #ping信息OK
    def ping(self,hostname,num):
        CMD = 'ping -c%d %s'%(num,hostname)
        input,output,err = ssh.exec_command(CMD)
        output = output.read().decode()
        err = err.read().decode()

        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    #telnet信息OK
    def telnet(self,hostname,port):
        try:
            tn = telnetlib.Telnet (hostname,port,timeout=1)
            tn.set_debuglevel (3)
            re = hostname+":"+str(port)+" Connect Succeed\n\n"
        except:
            re = hostname+":"+str(port)+" Connect Error\n\n"
        return "[ telnet ]\n"+re

    #证书信息OK
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

    #文件数据和期汇总表数据稽核NO
    def filedata(self):
        return

    #信息存到文件OK
    def filesave(self,data,mode):
        NOW_DATE = time.strftime ("%Y%m%d", time.localtime ())
        #数据存放在当前目录下的data目录
        if path.exists("./data"):
            pass
        else:
            mkdir("./data")
        if mode == "add" :
            FILE_NAME1 = './data/%s_%s.txt'%(localhost,NOW_DATE)
            file = open (FILE_NAME1, 'a')
            file.write (data.encode ('gbk'))
        elif mode == "new":
            FILE_NAME2 = './data/%s_%s.txt'%(localhost,NOW_DATE)
            file = open(FILE_NAME2,'w')
            file.write(data.encode('gbk'))
        else :
            return "mode [ERROR]"
        file.close()
        return 0

    #连接断开OK
    def close(self):
        input, output, err = ssh.exec_command ("~/bin/s")
        ssh.close()
        TEMP="\nClose OK!\n"
        return TEMP

#class filter:


if __name__ == '__main__':
    print("local run.....")
    a = collect()
    a.connect ('10.13.0.9', 22, 'hebappv9', 'tgbhu567890')
    #t=a.command("bash temp.sh ~/bin/s")

    # d=a.diskinfo()
    # t=d.diskinfo()
    # a.filesave (t, 'add')
    # t=d.diskarray()
    # a.filesave (t, 'add')
    #
    # t = a.process ()
    # a.filesave (t, 'add')
    #
    # t=a.meminfo()
    # a.filesave (t, 'add')
    #
    # t=a.cpuinfo()
    # a.filesave (t, 'add')
    #
    # t=a.errlog("0701000017")
    # a.filesave (t, 'add')
    #
    # #t = a.dbinfo()
    # #t=a.dbdump()
    #
    # t=a.ping("127.0.0.1",3)
    # a.filesave (t, 'add')
    #
    #
    # t=a.cart()
    # a.filesave (t, 'add')

    t = a.telnet("10.13.0.9",200)
    a.filesave (t, 'add')

    print (t)
    a.close ()



