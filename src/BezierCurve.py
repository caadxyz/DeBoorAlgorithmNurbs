#coding=utf-8
################################################################################
# BezierCurve.py
# Copyright (c) 2020.6 mahaidong
# Supported by ikuku.cn & caad.xyz 
# See License in the root of this repository for details.
################################################################################

import rhinoscriptsyntax as rs
import Rhino
from textGoo import TextGoo
from pointGoo import PointGoo
import ghpythonlib.treehelpers as th
from System.Drawing import Color

#debug
import textGoo
import pointGoo
reload(textGoo)
reload(pointGoo)

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
            text3d = TextGoo( Rhino.Display.Text3d( text, plane, self.textHeight ))
            hslColor = Rhino.Display.ColorHSL(i/(n+1),1,0.5)
            text3d.SetColor(hslColor.ToArgbColor())
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

    def drawCurvePts(self,nums,u, colorLimit):
        pts = []
        for i in range(nums+1):
            if i/float(nums+1)<=u:
                pt = self.calculatePoint( i/float(nums) )
                ptGoo = PointGoo(pt)
                hslColor = Rhino.Display.ColorHSL( colorLimit*i/float(nums+1),1,0.5 )
                ptGoo.SetColor(hslColor.ToArgbColor())
                pts.append( ptGoo ) 
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
crvPoints = bc.drawCurvePts(nums,u,(len(pts)-1)/(len(pts)+1) )
u2p = []
u2p.append(bc.calculatePoint(u))
u2p.append(funPosition+Rhino.Geometry.Point3d(u*funLength,0,0))

basisFunction = []
for i in range(len(pts)):
    basisPts = bc.basisFunction(i,funLength,funPosition,nums) 
    basisPtGooList = []
    for pt in basisPts:
        ptGoo = PointGoo(pt)
        hslColor = Rhino.Display.ColorHSL(i/(len(pts)+1),1,0.5)
        ptGoo.SetColor(hslColor.ToArgbColor())
        basisPtGooList.append(ptGoo)
    basisFunction.append( basisPtGooList )
basisFunction = th.list_to_tree(basisFunction, source=[0,0])


