#coding=utf-8
################################################################################
# BezierCurve.py
# Copyright (c) 2020.6 mahaidong
# Supported by ikuku.cn & caad.xyz 
# See License in the root of this repository for details.
################################################################################

import rhinoscriptsyntax as rs
import Rhino
import os
import sys
sys.path.append( os.path.dirname( ghenv.Component.OnPingDocument().FilePath ) )
from TextGoo import TextGoo
import ghpythonlib.treehelpers as th


class BezierCurve(object):

    def __init__(self, pts, textHeight):
        self.pts = pts
        self.legend = []
        self.textHeight = textHeight
        self.basisStr()
    
    def basisStr(self):
        n = len(self.pts)
        for i in range(n):
            text0 = BezierCurve.superscript("",'u',i)
            text1 = BezierCurve.superscript(text0, '(1-u)',n-1-i)
            if BezierCurve.binomial(n-1,i)==1:
                text = text0+text1+"•P"+str(i)
            else:
                text = str(BezierCurve.binomial(n-1,i))+"•"+text0+text1+"•P"+str(i)

            plane = Rhino.Geometry.Plane(self.pts[i], Rhino.Geometry.Vector3d(0,0,1))
            text3d = TextGoo(Rhino.Display.Text3d( text, plane, self.textHeight ))
            self.legend.append(text3d)
    
    def basisFunction(self,i,l, origin,nums ):
        pts = []
        n = len(self.pts)
        for j in range(nums+1):
            x = origin.X + l*j/nums
            y = origin.Y + l*BezierCurve.binomial(n-1,i)*( (j/nums)**i)*((1-j/nums)**(n-1-i))
            pts.append( Rhino.Geometry.Point3d(x,y,0) )
        return pts

    # algorithm: https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/notes.html
    def calculatePoint( self, u ): 
        p = None
        n = len(self.pts)
        for i in range(n):
            if i == 0:
                p = BezierCurve.binomial(n-1,i)*(u**i)*((1-u)**(n-1-i))*self.pts[i]
            else: 
                p += BezierCurve.binomial(n-1,i)*(u**i)*((1-u)**(n-1-i))*self.pts[i]
        return p

    def drawCurvePts(self,nums):
        pts = []
        for i in range(nums+1):
            pts.append(rs.AddPoint( self.calculatePoint( i/float(nums) ) ) )
        return pts
    

    @staticmethod
    def superscript(p,u,i):
        result =""
        if i==0:
            pass
        elif i==1:
            result +=u 
        elif i==2:
            result +=u+'\xB2'
        elif i==3:
            result +=u+'\xB3'
        else:
            result +=u+'^'+str(i)
        if p is "":
            return result
        else:
            if result is "":
                return ""
            else:
                return '•'+result

    @staticmethod
    def binomial(n, k):
        """
        A fast way to calculate binomial coefficients by Andrew Dalke.
        See http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
        """
        if 0 <= k <= n:
            ntok = 1
            ktok = 1
            for t in range(1, min(k, n - k) + 1):
                ntok *= n
                ktok *= t
                n -= 1
            return ntok // ktok
        else:
            return 0

bc = BezierCurve(pts, textHeight)
legend = bc.legend
curvePoints = bc.drawCurvePts(nums)
pointAtU = []
pointAtU.append(bc.calculatePoint(u))
pointAtU.append(funPosition+Rhino.Geometry.Point3d(u*funLength,0,0))

basisFunction = []
for i in range(len(pts)):
    basisFunction.append(bc.basisFunction(i,funLength,funPosition,nums))
basisFunction = th.list_to_tree(basisFunction, source=[0,0])


