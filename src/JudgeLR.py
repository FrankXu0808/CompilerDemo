#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
def judgeLR(DFA,follow):
    for k in DFA:
        for i in range(len(DFA[k])-1):
            for j in range(i+1,len(DFA[k])):
                A=DFA[k][i]
                B=DFA[k][j]
                #规约规约冲突
                if(A.find('.')==len(A)-1 and B.find('.')==len(B)-1):
                    ALe=re.split(r'::=',A)[0]
                    BLe=re.split(r'::=',B)[0]
                    if(len(follow[ALe] & follow[BLe])>0):return False
                #移进规约
                elif(A.find('.')==len(A)-1 or B.find('.')==len(B)-1):
                    if(A.find('.')!=len(A)-1):
                        index=A.find('.')+1
                        BLe = re.split(r'::=', B)[0]
                        if(A[index] in follow[BLe]):return False
                    elif (B.find('.') != len(B) - 1):
                        index =B.find('.') + 1
                        ALe = re.split(r'::=', A)[0]
                        if (B[index] in follow[ALe]): return False
    return True





