# coding: utf-8
#フィボナッチ(リストでメモ化)
def fiblist(n):
    def fiblist_sub(n,l):
        if(len(l)>n):
            return l[0]
        else:
            return fiblist_sub(n,[l[0]+l[1]]+l)
    
    return fiblist_sub(n,[1,1])

print fiblist(20)
