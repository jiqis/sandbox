# coding: utf-8
#フィボナッチ(再帰)

def fibrec(n):
    if n<2:
        return 1
    else:
        return fibrec(n-1)+fibrec(n-2)


print fibrec(20)
