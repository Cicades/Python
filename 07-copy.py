import copy
spam = ['dog', 'cat', 'duck']
newSpam = copy.copy(spam)#拷贝，与之对应得是deepcopy() 深拷贝
spam[0] = 'anotherdog'
print(spam,newSpam)