# -*- coding:utf-8 -*-

import xlsxwriter
import aep
from  time import strftime, localtime
from os import getcwd,path,mkdir

# 该版本开发版V1.0.1

class dataswitch ():
    # 将服务器的数据转存本地
    def SFile2CFile(self, hostname, port, username, password):
        global DATAPATH
        NOW_DATE = strftime ("%Y%m", localtime ())  # 取当前年月
        WORKPATH = getcwd ()  # 执行脚本的当前目录路径
        DATAPATH = WORKPATH + "\data"  # 执行脚本当前路径下的data目录
        if path.exists(DATAPATH): # 目录不存在就创建
            pass
        else:
            mkdir(DATAPATH)

        a = aep.collect ()
        a.connect (hostname, port, username, password)
        CMD1 = "ls ~/log/Check/*.%s.dat" % (NOW_DATE)  # 根据年月查找对应的日志命令
        SFile = a.command (CMD1, "notitle")
        SFile = SFile.split ('\n')  # 获取文件列表，带路径
        CFileNameTEMP = []  # 用于函数返回的文件名
        for i in SFile[:-1]:  # 文件转存
            CFileName = i[-18:-4]  # 获取文件名
            CFileName = "%s\%s"%(DATAPATH,CFileName) # 文件的绝对路径
            CMD2 = "cat %s " % (i)
            SData = a.command (CMD2, "notitle")
            CFile = open (CFileName, 'w')
            CFile.write (SData)
            CFile.close ()
            CFileNameTEMP.append (CFileName)
        a.close ()
        return CFileNameTEMP

    # 将本地的数据文本转化为Excel表格并绘折线图
    def txt2xlsx(self,txtfile, xlsxfile):
        # path = getcwd()
        datafile = txtfile  # 数据文件名
        xltfile = "%s\%s"%(DATAPATH,xlsxfile)  # xlsx文件名
        tablename = txtfile[-13:-7]  # 取文件的主要名字作为表名

        # 数据行数
        f = open (datafile, 'r')
        dataL = len (f.readlines ())
        f.close ()

        # 数据列数
        f = open (datafile, 'r')
        temp = f.readline ()
        dataL2 = len (temp.strip ("\n").split ("\t"))
        f.close ()

        work = xlsxwriter.Workbook (xltfile)
        worksheet = work.add_worksheet (tablename)

        f = open (datafile, 'r')
        row = 0
        col = 0

        if dataL2 != 4:  # 判断列数，根据不同列数生成不同的表格
            for i in f.readlines ():
                l = i.strip ("\n").split ("\t")
                A, B, C = l
                worksheet.write_number (row, col, int (A))
                worksheet.write_number (row, col + 1, int (B))
                worksheet.write_number (row, col + 2, int (C))
                row = row + 1
            f.close ()

            chartdict = {'categories': '=Sheet1!$A$1:$A$10', 'values': '=Sheet1!$C$1:$C$10'}
            chartdict['categories'] = '=%s!$A$1:$A$%d' % (tablename, dataL)
            chartdict['values'] = '=%s!$C$1:$C$%d' % (tablename, dataL)
        else:
            for i in f.readlines ():  # 生成表格
                l = i.strip ("\n").split ("\t")
                A, B, C, D = l
                worksheet.write_number (row, col, int (A))
                worksheet.write_number (row, col + 1, int (B))
                worksheet.write_number (row, col + 2, int (C))
                worksheet.write_number (row, col + 3, int (D))
                row = row + 1
            f.close ()

            chartdict = {'categories': '=Sheet1!$C$1:$C$10', 'values': '=Sheet1!$D$1:$D$10'}
            chartdict['categories'] = '=%s!$C$1:$C$%d' % (tablename, dataL)
            chartdict['values'] = '=%s!$D$1:$D$%d' % (tablename, dataL)
        # 绘图
        chartname = {'name': 'chartname'}
        chartname['name'] = '%s' % (tablename)
        chart = work.add_chart ({"type": "line"})
        chart.set_size ({'width': 800, 'height': 350})
        chart.set_title (chartname)
        chart.add_series (chartdict, )
        worksheet.insert_chart ('F7', chart)
        work.close ()
        return 0


# 测试
if __name__ == '__main__':
    print "local run>...."
    # server2local ()
    # txt2xlsx("","Test.xlsx")

    # DataFileList = SFile2CFile()
    # print DataFileList
    # for i in DataFileList:
    #     EFileName = i+".xlsx"
    #     txt2xlsx (i,EFileName)

