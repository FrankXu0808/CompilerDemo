#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
# 是否是特殊终结符
def isNote(note,temp,index):
    for s in note:
        if(temp.find(s)==index):
            return s
    return  False
def LRan(w,action,goto,note,strK):
    stack=['#',0]
    i=0
    while(len(stack)>0):
        #判断w的当前输入是否是特殊字符
        print(stack,w[i::],end="")
        a=w[i]
        temp=isNote(note,w[i::],0)
        # print("@@",temp,end="")
        if(temp!=False):
            a=temp
            i=i+len(temp)-1
        # print("   a=",a,end="")
        #查找表失败，错误
        if(a not in action[stack[-1]].keys()):
            print()
            print("error")
            return 0
        if(action[stack[-1]][a][0]=='S'):#移进
            stack.append(a)
            stack.append(int(action[stack[-2]][a][1::]))
            i=i+1
            print("   shift by:",action[stack[-3]][a])
            continue
        if(action[stack[-1]][a][0]=='R'):#规约
            index=int(action[stack[-1]][a][1::])-1
            str=strK[index]
            le=re.split(r'::=',str)[0]
            Ex=re.split(r'::=',str)[1]
            print("   reduce by:", action[stack[-1]][a],'(',strK[index],')')
            #计算Ex包含符号个数
            count=0
            k=0
            while(k < len(Ex)):
                temp1 = isNote(note, Ex, k)
                if(temp1==False):
                    count=count+1
                    k=k+1
                else:
                    count=count+1
                    k=k+len(temp1)
            count=count*2
            # print(Ex,count)
            #弹栈
            for count1 in range(count):
                stack.pop()
            s_=stack[-1]
            #产生式左部符号进栈
            stack.append(le)
            #新栈顶状态进栈
            stack.append(goto[s_][le])

            continue
        if(action[stack[-1]][a]=='acc'):
            print("   success!")
            return 1
        else:
            print("   error")
            return  0





