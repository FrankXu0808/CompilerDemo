#!/usr/bin/python
# -*- coding: UTF-8 -*-
import LivePrefix
import SLRTable
import LRanly
import re
import JudgeLR
Gs=[['E::=E+T|T', 'T::=T*F|F',  'F::=(E)|-F|id'],
 ['S::=aABe',  'A::=b|Abc' , 'B::=d']]
# markflow="(id+id)*id+id/#"
markflow="id-id-#"
#读取文法G，得到文法的描述
for fo in Gs:
    # fo = open("G.txt", "r+")
    print()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print()
    # str = fo.readlines()
    str = fo
    for i in range(0,len(str)):
        str[i]=str[i].replace('\n','')
        str[i] = str[i].replace('!', 'ε')
    print ("读取的文法是 : ", str)

    fnote=open("Note.txt","r+")
    note=fnote.readlines()
    for i in range(0,len(note)):
        note[i]=note[i].replace('\n','')
    print ("多个字符作为一个终结符的是 : ", note)

    #前缀
    S=re.split(r'::=',str[0])[0]
    addStr=S+'\'::='+S
    newStr=[]
    G={}
    G_={}
    newStr.append(addStr)
    for s in str:
        newStr.append(s)

        G[re.split(r'::=',s)[0]]=re.split(r'::=',s)[1]
    for s in newStr:
        G_[re.split(r'::=', s)[0]] = re.split(r'::=', s)[1]

    print("拓广文法:",newStr)
    # print(G)
    # G=["E'::=E",'E::=E+T|T', 'T::=T*F|F', 'F::=(E)|-F|id']
    # Note=['id']
    print("构造LR（0）项目:")
    Ge=LivePrefix.LR0(newStr,note)
    # S=["E'::=.E"]
    print("构造DFA:")
    S0=[]
    S0.append(S+'\'::=.'+S)
    print("初态:S0",S0)
    I=LivePrefix.closure(S0,Ge)
    S0=list(I.keys())
    Dtran=LivePrefix.DFA(Ge,S0,note)[0]
    C=LivePrefix.DFA(Ge,S0,note)[1]

    print("DFA")
    for k in C:
        print(k,C[k])
    print("DTran:")
    for k in Dtran:
        print(k,Dtran[k])

    S=re.split(r'::=',str[0])[0]
    G[S+'\'']=S
    first=SLRTable.CR_FIRST(newStr,G,note)
    follow=SLRTable.CR_Follow(newStr,G,note,first)
    print("FIRST集合:")
    print(first)
    print("FOLLOW集合:")
    print(follow)
    #判断是否是合法LR文法
    if(JudgeLR.judgeLR(C,follow)):
        print("经判断，该文法是合法LR文法")
    else:
        print("经判断，该文法不是合法LR文法")
        break
    table=SLRTable.createTable(C,Dtran,G_,first,str,G,note,follow)
    action=table[0]
    goto=table[1]

    print("action:")
    for s in action:
            print(s,"   ",end="")
            for ss in action[s]:
                print(action[s][ss],":",ss,"  ",end="")
            print()
    print("goto:")
    for s in goto:
            print(s,"   ",end="")
            for ss in goto[s]:
                print(goto[s][ss],":",ss,"  ",end="")
            print()


    # 构造方便计算坐标的文法
    strK = []
    for s in str:
        A = re.split(r'::=', s)[0]
        Ex = re.split(r'::=', s)[1]
        B = re.split(r'\|', Ex)
        for k in B:
            if (len(k) > 0):
                sss = A + "::=" + k
                strK.append(sss)
    print("LR分析:")
    result=LRanly.LRan(markflow,action,goto,note,strK)
    if(result==1):
        print("符合语法!")
        break;
    else:
        print("该记号流不匹配本文法！")
    print()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print()