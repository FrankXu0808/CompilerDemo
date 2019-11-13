#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import LivePrefix

# 是否是特殊终结符
def isNote(note,temp,index):
    for s in note:
        if(temp.find(s)==index):
            return s
    return  False


#构造非终结符的FIRST集合
def CR_FIRST(str,G,note):
    first={}
    for i in range(len(str))[::-1]:

        aLe = re.split(r'::=', str[i])[0]  # A
        aEx = re.split(r'\|', re.split(r'::=', str[i])[1])  # A->&1|&2....
        fi=[]
        first[aLe]=[]
        if(G[aLe].find('ε')>0):fi.append('ε')
        for s in aEx:
          if(len(s)>0 and s!='ε'):
            temp=s;
            temp=temp.replace(temp[0],'ε'+temp[0])
            temp+='ε'

            for j in range(len(temp)):
                if(temp[j]=='ε'):
                    if(temp[j+1].isupper()==False):
                        judge=isNote(note,temp,j+1)
                        if(judge==False):fi.append(temp[j+1])
                        else:fi.append(temp[j+1:j+1+len(judge)])
                    else:
                        Le=temp[j+1]
                        for k in range(j+1,len(temp)):
                            if(temp[k]=='\''):Le+='\''
                            else:break;
                        # print(first)
                        if(Le in first.keys()):#包含左递归时的处理
                            for s in first[Le]:
                                fi.append(s)



                elif(temp[j].isupper()):
                    Le = temp[j ]
                    for k in range(j , len(temp)):
                        if (temp[k+1] == '\''):
                            Le += '\''
                            j=j+1

                        else:break;

                    if(temp[j+1].isalpha() and G[Le].find('ε')>0):
                        if (temp[j + 1].islower()):
                            judge = isNote(note, temp, j + 1)
                            if (judge == False):fi.append(temp[j + 1])
                            else: fi.append(temp[j + 1:j + 1 + len(judge)])
                        else:
                            Le = temp[j + 1]
                            for k in range(j + 1, len(temp)):
                                if (temp[k+1] == '\''):Le += '\''
                                else: break;

                            for s in first[Le]:
                                fi.append(s)
                    else:
                        # fi=list(set(fi))
                        for h in fi:
                         first[aLe].append(h)
                        first[aLe]=list(set(first[aLe]))

                        break;
                else:
                    # fi = list(set(fi))
                    for h in fi:
                        first[aLe].append(h)
                    first[aLe] = list(set(first[aLe]))
                    break;
    return first


#求指定文法序列的FIRST集合
def FIRST(str,G,note,first):
    result=[]
    i=-1
    aLe=[]
    while(i<len(str)+1):
        i=i+1

        if(i==len(str)):#k>n
            result.append('ε')
            for s in aLe:

                for ss in first[s]:

                    isexist=False
                    for sss in result:
                      if(sss==ss):
                         isexist=True

                         break;
                    if(isexist==False):result.append(ss)
            return result
        if(str[i].isalpha() and str[i].isupper()):#非终结符
            Le=str[i]
            for k in range(i + 1, len(str)):
                if (str[k] == '\''):
                    Le += '\''
                    i=i+1

                else:break;
            aLe.append(Le)
            if(G[Le].find('ε')==-1):#第一个具有性质ε不属于FIRST（XK）的文法符号
                result=first[Le]
                return result
        else:#终结符
            note=isNote(note,str,i)
            if(note==False):
                result.append(str[i])
                return  result
            else:
             i=i+len(note)-1
             result.append(note)
             return result


# 求非终结符的Follow集合
def CR_Follow(str,G,note,First):
    follow={}
    S = re.split(r'::=', str[0])[0]  # A

    # follow[S]=['#']


    for i in range(len(str)):

        Le= re.split(r'::=', str[i])[0]  # A

        fl=[]
        if(i==0):fl.append('#')
        for s in str:
          sLe=re.split(r'::=', s)[0]  # A
          Ex = re.split(r'\|', re.split(r'::=', s)[1])  # A->&1|&2....
          for ss in Ex:
           if(len(ss)>0 and ss.find(Le)>=0):
            if( ss.find(Le)==len(ss)-len(Le)):#B后面没有β

                for k in follow[sLe]:
                    isexist=False
                    for kk in fl:
                        if(kk==k):
                            isexist=True
                            break;
                    if(isexist==False) :

                        if(Le in follow.keys()):

                            fl.append(k)

                        else:
                            fl.append(k)

                            follow[Le]=fl


            else:#αBβ
               #处理E匹配E'的问题
               isexist=False
               index=0
               if(len(Le)==1):
                   for i in range(len(ss)):
                     if(ss[i]==Le  ):
                         if(i==len(ss)-1):
                             isexist=True
                             index=i
                         else:
                             if(ss[i+1]!='\''):
                                 isexist=True
                                 index=i+1
                                 break;




               if(isexist==True):


                resu=FIRST(ss[index:],G,note,First)
                #查看是否有ε，若有先执行条件三的操作再删去
                for index in range(len(resu)):
                    if(resu[index]=='ε'):
                        for k in follow[sLe]:
                            isexist = False
                            for kk in fl:
                                if (kk == k):
                                    isexist = True
                                    break;
                            if (isexist == False):
                                if (Le in follow.keys()):
                                    fl.append(k)

                                else:
                                    fl.append(k)

                                    follow[Le] = fl

                        del resu[index]
                        break;
                #将除ε以外的FIRST（β）加入FOLLOW（B)中

                for k in resu:
                    isexist = False

                    for kk in fl:
                        if (kk == k):
                            isexist = True
                            break;
                    if (isexist == False):
                        if (Le in follow.keys()):

                            fl.append(k)

                            #follow[Le].append(k)

                        else:
                            fl.append(k)
                            follow[Le] = fl
        fl = list(set(fl))
        follow[Le]=fl

    return  follow
def createTable(C,Dtran,G_,first,Str,G,note,follow):
    action={}
    goto={}
    #构造方便计算坐标的文法
    strK=[]
    for s in Str:
        A=re.split(r'::=',s)[0]
        Ex=re.split(r'::=',s)[1]
        B=re.split(r'\|',Ex)
        for k in B:
            if(len(k)>0):
                sss=A+"::="+k
                strK.append(sss)
    #构造过程
    for k in Dtran:
        arow={}
        grow={}
        for s in Dtran[k]:
            if(not s.isupper()):#如果状态转移的纵坐标是非终结符
                num=str(Dtran[k][s])
                temp='S'+num
                arow[s]=temp
            else:#如果是终结符
                grow[s]=Dtran[k][s]
        for Ex in C[k]:
                if(Ex.find('.')==len(Ex)-1):#对于每个属于状态k的可规约项目 A->a
                    if(Ex.find("\'")>=0):#如果是初态
                        # print("@@@",Ex)
                        arow['#']="acc"
                    else:#如果不是初态
                        for index in range(len(strK)):
                            A = re.split(r'::=', strK[index])[0]
                            # A_= re.split(r'::=', Ex)[0]
                            # print("$$",re.split(r'::=',Str[i])[1],Ex , A,A_)
                            # if(re.split(r'::=',Str[i])[1]+'.'==Ex and A==A_):
                            if(strK[index]+'.'==Ex):
                                for f in follow[A]:
                                    arow[f]="R"+str(index+1)
                                break
        action[k]=arow
        goto[k]=grow
    # print("action:")
    # for s in action:
    #     print(s,"   ",end="")
    #     for ss in action[s]:
    #         print(action[s][ss],":",ss,"  ",end="")
    #     print()
    # print("goto:")
    # for s in goto:
    #     print(s,"   ",end="")
    #     for ss in goto[s]:
    #         print(goto[s][ss],":",ss,"  ",end="")
    #     print()

    return action,goto







# strs=['S::=bASB|bA', 'A::=dSa|e', 'B::=cAa|c']
# G = {'S': 'bASB|bA', 'A': 'dSa|e', 'B': 'cAa|c'}
# Note=['id']
#
# first=CR_FIRST(strs, G, Note)
# print(first)
# dd=CR_Follow(strs, G, Note, first)
# print(dd)

