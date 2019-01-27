#与系统文件的有关的操作
#import os
#1.获取当前工作目录 os.getcwd
#2.改变目录 os.chdir()
#3.创建文件夹 os.makedirs('C:\\delicious\\walnut\\waffles')
#4.os.path 是os下的模块其中包含许多重要的函数
#5.os.path.abspath(path) 返回一个路径的绝对路径
#6.os.path.relpath(path，start) 返回从start到path的绝对路径
#7.文件读写
#	7.1 打开文件 open(filename[,options]) 返回一个File对象,options可以指定文件的打开模式
#	7.2 读取文件内容，
#		7.2.1调用File对象的方法——read() 将文件内容作为一整个字符串返回
#		7.2.2调用File对象的方法——readlines() 取得一个字符串列表
#8.利用shelve模块可以将数据保存到一个二进制文件