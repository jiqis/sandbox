#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yuya
#
# Created:     29/08/2018
# Copyright:   (c) yuya 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import json
import os
import sys

class rectanle:
    def ___init__(vertexes):
        if len(vertexes)>0:
            left=vertexes[0][0]
            right=vertexes[0][0]
            top=vertexes[0][1]
            bottom=vertexes[0][1]
            for v in vertexes:
                x=v[0]
                y=v[1]
                if x<left:
                    left=x
                if x>right:
                    right=x
                if y<top:
                    top=y
                if y>bottom:
                    bottom=y
            self.l=left
            self.r=right
            self.t=top
            self.b=bottom
            self.height=bottom-top
            self.width=right-left
            self.center=((left+right)/2,(top+bottom)/2)
    def ind_line_row():
        top=self.t
        bottom=self.b
        center=self.center[1]
        error=self.height*0.1
        ind_top=lambda y: abs(top-y)<error
        ind_bottom=lambda y: abs(bottom-y)<error
        ind_center=lambda t,b: ((t<center) and (b>center))or((top<(t+b)/2)and(bottom>(t+b)/2))
        return lambda rect:ind_top(rect.t) or ind_bottom(rect.b) or ind_center(rect.t,rect.b)
    def ind_line_colomn():
        left=self.l
        right=self.r
        center=self.center[0]
        error=self.width*0.1
        ind_left=lambda x: abs(left-x)<error
        ind_right=lambda y: abs(right-x)<error
        ind_center=lambda l,r: ((l<center) and (r>center))or((left<(l+r)/2)and(right>(l+r)/2))
        return lambda rect:ind_left(rect.l) or ind_right(rect.r) or ind_center(rect.l,rect.r)

class wordbox:
    def __init__(word,vertexes):
        self.rect=Rect(vertexes)
        self.rect=word

def main(filename):
    f=open(filename,'r')
    json_data=json.load(f)

    f.close()
    pass

if __name__ == '__main__':
    filename=sys.argv[1]
    main(filename)
