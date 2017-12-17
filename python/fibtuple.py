# coding: utf-8
#フィボナッチ(タプルでメモ化)
def fibtuple(n):
    def fibtuple_sub(n,t,i):
        if(i>n):
            return t[0]
        else:
            return fibtuple_sub(n,(t[0]+t[1],t[0]),i+1)
    
    return fibtuple_sub(n,(1,1),2)

for i in range(21):
    print fibtuple(i)
