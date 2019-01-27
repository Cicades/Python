#元组和列表区别在于元组中的元素的不可以被改变，而列表的元素可以被改变或重新赋值
#对于字符串、整型、元组等不可变的数据类型的值，python会保存值得本身，否则python进行值引用
a = type(tuple(['cat', 'dog', 'duck']))#tuple
b = type(list(('cat', 'dog', 'duck')))#list
print(a,b,sep='\r')
