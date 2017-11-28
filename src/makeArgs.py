#coding:utf-8

'''
Created on 2017年9月11日

@author: Moxian
'''

'''
函数调用方式为sayHello.makeVlaue(参数类型,最短长度,最长长度)

参数类型：1为数字类型，2为字母类型
最长最短可以选1位参数或者两位参数

'''

def makeVlaue(*getArg):
    vlaues=[]
    a=''    #最长值
    b=''    #最短值
    c=' '    #空格
    d=''    #空白
    specialStr=''
    typeVlaue=''
    e='[`~!@#$^&*()=|{}\':;\',\\[\\].<>/?~！@#￥……&*（）——|{}【】‘；：”“\'。，、？%+_]'.decode('utf-8')    #特殊字符
    f='123456789'.decode('utf-8')    #数字
    g='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'.decode('utf-8')   #字母
    if(len(getArg)==3):
        for i in range(getArg[2]+1):
            a+='a'
        for i in range(getArg[1]-1):
            b+='b'
        x=0
        y=0
        for i in range(getArg[2]):
            x=i
            y=i
            if(i>len(list(e))-1):
                x=i%len(list(e))
            specialStr+=list(e)[x]
            if(getArg[0]==1):
                if(i>len(list(g))-1):
                    y=i%len(list(g))
                typeVlaue+=list(g)[y]
            else:
                if(i>len(list(f))-1):
                    y=i%len(list(f))
                typeVlaue+=list(f)[y]
                
    else:
        for i in range(getArg[1]+1):
            a+='a'
        for i in range(getArg[1]-1):
            b+='b'
        x=0
        y=0
        for i in range(getArg[1]):
            x=i
            y=i
            if(i>len(list(e))-1):
                x=i%len(list(e))
            specialStr+=list(e)[x]
            if(getArg[0]==1):
                if(i>len(list(g))-1):
                    y=i%len(list(g))
                typeVlaue+=list(g)[y]
            else:
                if(i>len(list(f))-1):
                    y=i%len(list(f))
                typeVlaue+=list(f)[y]
    vlaues.append(a)
    vlaues.append(b)
    vlaues.append(c)
    vlaues.append(d)
    vlaues.append(specialStr)
    vlaues.append(typeVlaue)
    return vlaues