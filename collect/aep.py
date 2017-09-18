#/usr/bin/env python
#coding=gbk

import paramiko
from  time import strftime,localtime
from telnetlib import Telnet
from os import path,mkdir

#ʱ���ȫ�ֱ���
global NOW_DATE,NOW_TIME
NOW_DATE = strftime ("%Y%m%d", localtime ())#��ǰ���ڣ���ʽ��YYYYmmdd
NOW_TIME = strftime ("%Y-%m-%d %H:%M", localtime ())#��ǰʱ��,��ʽ��YYYY-mm-dd HH:MM

#���ݻ���
class collect:
    """
    Data Collect Class
    """
    #����������OK
    def connect(self,hostname,port,username,password):
        global ssh
        global localhost
        ssh = paramiko.SSHClient ()
        # �������ε������Զ����뵽host_allow �б��˷����������connect������ǰ��
        ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
        ssh.connect (hostname, port, username, password)

        #hostuser = "[ "+hostname+" "+username+" ]"
        localhost = hostname
        return localhost

    #ִ������OK
    def command(self,CMD):
        input, output, err = ssh.exec_command(CMD)
        output = output.read().decode("gbk")
        err = err.read().decode()
        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    # ������ϢOK
    class diskinfo:
        #ϵͳ������Ϣ
        def diskinfo(self):
            CMD = "df -g"
            input, output, err = ssh.exec_command (CMD)
            output = output.read ().decode ()
            err = err.read ().decode ()
            return "\n[ "+CMD+" ]\n\n"+output+err+"\n"


        #����������Ϣ
        def diskarray(self):
            CMD1 = "lspv"
            input, output, err = ssh.exec_command (CMD1)
            output1 = output.read ().decode ()
            err1 = err.read ().decode ()

            #�������и�����Ȼ����ʾ�������е����顣
            CMD2 = "lspv | awk '{print $1}' | wc -l"
            input, output, err = ssh.exec_command(CMD2)
            output2 = output.read().decode()
            err2 = err.read().decode()

            #ѭ�����������������
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


    #������ϢOK
    def process(self):
        #s����
        # CMD1 = "~/bin/s"
        # input,output,err = ssh.exec_command(CMD1)
        # output1 = output.read().decode('gbk')
        # err1 = err.read().decode('gbk')

        #ps����
        CMD2 = 'ps -ef | grep $LOGNAME'
        input,output,err = ssh.exec_command (CMD2)
        output2 = output.read().decode()
        err2 = err.read().decode()

        TEMP = "\n[ "+CMD2+" ]\n\n"+output2+err2+"\n"
        return TEMP

    #�ڴ���ϢOK
    def meminfo(self):
        CMD = 'vmstat 1 10'
        input, output, err = ssh.exec_command (CMD)
        output = output.read ().decode ()
        err = err.read ().decode ()
        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    #�ؼ���������ڴ���ϢOK
    def servicemem(self):
        #ps����
        CMD1 = 'ps auwx | head -n 1;ps auwx | grep appv9 | egrep -v "RSS" | sort +5b -6 -n -r'
        input, output, err = ssh.exec_command (CMD1)
        output1 = output.read()
        err1 = err.read().decode()

        #topas����(����ʽ����ű�������)
        # CMD2 = 'topas'
        # input2,output,err = ssh.exec_command(CMD2)
        # input2.write("q\n")
        # input2.flush ()
        # output2 = output.read().decode()
        # err2 = err.read().decode()

        return "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"

    #��Ӳ��������־OK
    def errlog(self,num):
        CMD1 = 'errpt -d H -s %s | grep ERROR'%(num)
        input, output, err = ssh.exec_command (CMD1)
        output1 = output.read ().decode ()
        err1 = err.read ().decode ()

        # CMD2 = 'errpt -aj BFE4C025'
        # input, output, err = ssh.exec_command (CMD2)
        # output2 = output.read ().decode ()
        # err2 = err.read ().decode ()

        TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"
        return TEMP


    # #���ݿ���ϢNO
    # def dbinfo(self):
    #     #CMD='isql -Usxlottery -Psxlottery -Dsxlottery -i isql.txt -o osql.txt'
    #     input,output,err = ssh.exec_command(CMD)
    #     output = output.read().decode("gbk")
    #     err = err.read().decode()
    #
    #     return "\n[ "+CMD+" ]\n\n"+output+err+"\n"
    #
    # #���ݿⱸ��NO
    # def dbdump(self):
    #
    #     return 0

    #ping��ϢOK
    def ping(self,hostname,num):
        CMD = 'ping -c%d %s'%(num,hostname)
        input,output,err = ssh.exec_command(CMD)
        output = output.read().decode()
        err = err.read().decode()

        return "\n[ "+CMD+" ]\n\n"+output+err+"\n"

    #telnet��ϢOK
    def telnet(self,hostname,port):
        try:
            tn = Telnet (hostname,port,timeout=1)
        except:
            re = hostname+":"+str(port)+" Connect Error\n\n"
            return "[ telnet ]\n" + re
        re = hostname + ":" + str (port) + " Connect Succeed. Time: %s\n\n" % (NOW_TIME)
        return "[ telnet ]\n"+re

    #֤����ϢOK
    def cart(self):
        #֤������
        CMD1 = 'ls -al ~/dat/Crypto/AgentCert*'
        input,output,err = ssh.exec_command(CMD1)
        output1 = output.read().decode()
        err1 = err.read().decode()

        #ÿ��֤�����Ч����
        CMD2 = "for i in `ls -al ~/dat/Crypto/AgentCert* | awk '{print $9}'`;do echo $i;~/src/bin/ShowCert $i | sed -n '17,18'p;done"
        input,output,err = ssh.exec_command(CMD2)
        output2 = output.read ().decode ('gbk')
        err2 = err.read ().decode ('gbk')

        TEMP = "\n[ "+CMD1+" ]\n\n"+output1+err1+"\n"+"\n[ "+CMD2+" ]\n\n"+output2+err2+"\n"
        return TEMP

    #�ļ����ݺ��ڻ��ܱ����ݻ���NO
    def filedata(self):
        return

    #��־��Ϣ
    def loginfo(self):
        CMD1 = "cd ~/log/;ls BK*.log Gateway*.log TM*.log MD*.log T900001.log T900999.log Database.err ~/FlowCtrl.log "
        input1, output1, err1 = ssh.exec_command(CMD1)
        TEMP = output1.read().decode("gbk")
        LogFileList = TEMP.split("\n")
        I = "\n"
        for i in LogFileList[:-1]:
            CMD2 = "cd ~/log/;~/bin/ptail -n 200 %s"%(i)
            input2, output2, err2 = ssh.exec_command (CMD2)
            output2 = output2.read ().decode ("gbk")
            err2 = err2.read ().decode ("gbk")
            I = I+output2+err2+"\n\n"
        return I


    #��Ϣ�浽�ļ�OK
    def filesave(self,data,mode,*FileType):
        #���ݴ���ڵ�ǰĿ¼�µ�dataĿ¼
        if len(FileType) == 1:
            if FileType[0] == "log":
                file_type = "log"
        else:
            file_type = "txt"

        if path.exists("./data"):
            pass
        else:
            mkdir("./data")
        if mode == "add" :
            FILE_NAME1 = './data/%s_%s.%s'%(localhost,NOW_DATE,file_type)
            file = open (FILE_NAME1, 'a')
            file.write (data.encode ('gbk'))
        elif mode == "new":
            FILE_NAME2 = './data/%s_%s.%s'%(localhost,NOW_DATE,file_type)
            file = open(FILE_NAME2,'w')
            file.write(data.encode('gbk'))
        else :
            return "mode [ERROR]"
        file.close()
        return 0

    #���ӶϿ�OK
    def close(self):
        input, output, err = ssh.exec_command ("~/bin/s")
        ssh.close()
        TEMP="\nClose OK!\n"
        return TEMP



if __name__ == '__main__':
    print("local run.....")
    # a = collect()
    # a.connect ('10.13.0.9', 22, 'hebappv9', 'tgbhu567890')#ָ������
    # t=a.command("~/bin/ShowPDA")
    #
    # d=a.diskinfo()
    # t=d.diskinfo()
    # a.filesave (t, 'add')#д���ļ�
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
    # a.filesave (t, 'add')

    # print (t)#����ɼ�����
    # a.close ()#�Ͽ�ssh����




