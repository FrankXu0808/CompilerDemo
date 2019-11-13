#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
def DFA(Ge,S,Note):
    Dtran={} #DTRAN
    C={} #状态集
    C[0]=S #初始化
    i=0# 状态坐标
    Jindex=1
    while(i<len(C)):#当C中还有未标记的状态
        status={}#
        word={}#当前状态下可接受的字符
        for s in C[i]:#对当前状态内的所有项目进行遍历
         # print("@@",s)
         if(s.find('.')!=len(s)-1):
           temp=re.split(r'\.',s)[1]
         else:temp=''
         if(len(temp)>0):
            if(temp[0].isupper()):#非终结符
                word[temp[0]]=''
            else:
                isnote=False;
                for note in Note:
                    if(temp.find(note)==0):
                        word[note]=''
                        isnote=True
                if(isnote==False):
                    word[temp[0]]=''


        if(len(word)>0):#有可以接受的字符
          for s in list(word.keys()):
                J=[]
                #求下一状态转移
                J=list(closure(goto(C[i],s),Ge).keys())
                # print(C[i],"->",s,J)
                #是不是新状态
                oldindex=0
                if(len(J)>0):
                    isnew=True
                    for k in C:
                        if(C[k]==J):
                            oldindex=k
                            isnew=False
                            break;

                    if(isnew==True):
                        C[Jindex]=J
                        status[s] = Jindex
                        Jindex=Jindex+1
                        # print("new",Jindex,J)

                    else:
                        status[s] = oldindex
        #记录状态转移
        Dtran[i]=status
        i=i+1
    return Dtran, C
    # print("DFA")
    # for k in C:
    #     print(k,C[k])
    # print("DTran:")
    # for k in Dtran:
    #     print(k,Dtran[k])








def goto(I,X):
    result=[]
    for s in I:

        temp=re.split(r'\.',s)[1]

        if(len(temp)>0):
            if(temp[0]==X ):
                result.append(re.split(r'\.',s)[0]+X+'.'+temp[1::])
            elif(temp[0:len(X)]==X):
                result.append(re.split(r'\.',s)[0]+X+'.'+temp[len(X)::])
    #print(result)
    return result
def closure(I,Ge):
    result={}
    for s in I:
        result[s]=""
    i=0
    while(i<len(result)):
        J=list(result.keys())[i]
        index=J.find('.')
        if(index==len(J)-1):#不可求闭包
            i=i+1
        else:
            if(J[index+1].isupper()):#非终结符
                B=J[index+1]
                for sss in Ge:
                    if(sss[0]==B ):

                        judge=re.split(r'::=',sss)[1]
                        if(judge[0]=='.'):
                          result[sss]=""
        i=i+1

    return result

def LR0(G,Note):
    Ge=[]
    for s in G:
        Le = re.split(r'::=', s)[0]  # Aj
        Ex = re.split(r'\|', re.split(r'::=', s)[1])  # Aj->&1|&2....
        for ss in Ex:
            point=0
            while(point<=len(ss)):
                for note in Note:
                    if(ss[point-1::].find(note)==0):
                        point=point+len(note)
                temp=ss[0:point]+'.'+ss[point::]
                Ge.append(Le+"::="+temp)
                print(Le+"::="+temp,"   ",end="")
                point=point+1
            print()
    # print(Ge)
    return Ge
# G=["E'::=E",'E::=E+T|T', 'T::=T*F|F', 'F::=(E)|-F|id']
# Note=['id']
# Ge=LR0(G,Note)
# S=["E'::=.E"]
# I=closure(S,Ge)
# S0=list(I.keys())
#
# DTRA=DFA(Ge,S0,Note)


