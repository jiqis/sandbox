# coding: utf-8

import math as m
#平均の計算
def average(xs):
    n=len(xs)
    s=0.0
    for i in range(n):
        s+=xs[i]
    return s/n

#標準偏差の計算
def stdev(xs):
    n=len(xs)
    s=0.0
    ax=average(xs)
    for i in range(n):
        s+=(xs[i]-ax)**2
    return m.sqrt(s/n)

#相関係数の計算
def correlative (xs,ys):
    #xs,ys: list
    nx=len(xs)
    ny=len(ys)
    if(nx!=ny):
        print("correlative: xsの要素数とysの要素数が一致しません")
        return 0.0
    else:
        s=0.0
        sx=0.0
        sy=0.0
        ax=average(xs)
        ay=average(ys)
        for i in range(nx):
            s+=(xs[i]-ax)*(ys[i]-ay)
            sx+=(xs[i]-ax)**2
            sy+=(ys[i]-ay)**2
        return s/m.sqrt(sx*sy)
