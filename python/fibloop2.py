# coding: utf-8
#フィボナッチ(ループ:for)

def fibloop2(n):
    if n<2:
        return 1
    else:
        a=1
        b=1
        c=0
        for i in range(n-1):
            c=a
            a=a+b
            b=c
        return a
        

print fibloop2(20)
