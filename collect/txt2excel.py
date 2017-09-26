# -*- coding:utf-8 -*-

import xlsxwriter
import collect
from os import getcwd

#该版本开发版V1.0.1

# 获取服务器最新的性能数据
def datafilename():
    a = collect.collect()
    a.connect ('x.x.x.x', 22, 'xxxx', 'xxxxx')
    t=a.command("ls ~/log/Check/T913714.*.dat | tail -n 1")
    print t
    a.close()

# 数据文本转化为Excel表格并绘折线图
def txt2xlsx(txtfile,xlsxfile):
    #path = getcwd()
    datafile = txtfile # 数据文件名
    xltfile = xlsxfile # xlsx文件名
    tablename = txtfile[1:7] # 取文件的主要名字作为表名


    #数据行数
    f = open (datafile, 'r')
    dataL = len(f.readlines())
    f.close()

    #数据列数
    f = open (datafile, 'r')
    temp=f.readline()
    dataL2 = len(temp.strip("\n").split("\t"))
    f.close ()

    work = xlsxwriter.Workbook(xltfile)
    worksheet = work.add_worksheet()

    f = open (datafile, 'r')
    row = 0
    col = 0

    if dataL2 != 4:#判断列数，根据不同列数生成不同的表格
        for i in f.readlines():
            l = i.strip("\n").split("\t")
            A,B,C = l
            worksheet.write_number(row,col,int(A))
            worksheet.write_number (row, col + 1,int(B) )
            worksheet.write_number (row, col + 2,int(C))
            row = row + 1
        f.close()

        chartdict = { 'categories': '=Sheet1!$A$1:$A$10','values':'=Sheet1!$C$1:$C$10'}
        chartdict['categories'] = '=Sheet1!$A$1:$A$%d'%(dataL)
        chartdict['values'] = '=Sheet1!$C$1:$C$%d'%(dataL)
    else:
        for i in f.readlines ():#生成表格
            l = i.strip ("\n").split ("\t")
            A,B,C,D = l
            worksheet.write_number (row, col, int (A))
            worksheet.write_number (row, col + 1, int (B))
            worksheet.write_number (row, col + 2, int (C))
            worksheet.write_number (row, col + 3, int (D))
            row = row + 1
        f.close ()

        chartdict = {'categories': '=Sheet1!$C$1:$C$10', 'values': '=Sheet1!$D$1:$D$10'}
        chartdict['categories'] = '=Sheet1!$C$1:$C$%d' % (dataL)
        chartdict['values'] = '=Sheet1!$D$1:$D$%d' % (dataL)
    #绘图
    chartname = { 'name':'chartname' }
    chartname['name'] = '%s' %(tablename)
    chart = work.add_chart ({"type": "line"})
    chart.set_size ({'width': 800, 'height': 350})
    chart.set_title (chartname)
    chart.add_series(chartdict,)
    worksheet.insert_chart('F7',chart)
    work.close()
    return 0

# 测试
if __name__ == '__main__':
	txt2xlsx("T913714.201709.dat","Test.xlsx")
