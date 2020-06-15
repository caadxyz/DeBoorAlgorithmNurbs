#coding=utf-8
################################################################################
# DeBoorAlgorithmNurbs.py
# Copyright (c) 2020.4 mahaidong
# Supported by ikuku.cn & caad.xyz 
# See License in the root of this repository for details.
################################################################################
import rhinoscriptsyntax as rs
import Rhino
from textGoo import TextGoo
from lineGoo import LineGoo
import ghpythonlib.treehelpers as th
from System.Drawing import Color

# debug
import textGoo
import lineGoo
reload(textGoo)
reload(lineGoo)

class DeBoorAlgorithmNurbs(object):
    def __init__( self,degree, pts,weights,knots,isPeriodic, isRational):
        self.degree = degree
        self.pts = pts
        self.weights = weights
        self.knots = knots
        self.isPeriodic = isPeriodic
        self.isRational = isRational

    def findKnotIndexByU(self, u):
        s = 0
        index = 0 
        if u<self.knots[0] or u>self.knots[-1]:
            return
        for i in range(len(self.knots)):
            if self.knots[i]>u:
                if s==0 :
                    return s,i-1
            elif self.knots[i] == u:
                index = i
                s += 1
        if s>0:
            return s,index

    def getKnotValue(self,i):
        if self.isPeriodic == True:
            if i>=len(self.knots):
                return self.knots[-1]+( self.knots[i+1-len(self.knots)]-self.knots[0] )
            elif i<0:
                return self.knots[0]-( self.knots[-1]-self.knots[len(self.knots)+i-1] )
        return self.knots[i]

    def calculateNurbsPoint(self,u, haveLines=0):
        """
        parameters:
            havelines: 0=nolines, 1=drawLines
        """
        p = self.degree
        s,k = self.findKnotIndexByU(u)
        h = p-s
        pt = {}
        ptsGoo=[]

        # initialize pt[i][0] for starting calculation
        for i in range(k-p+1,k-s+2):
            pt[i]={}
            if i < len(self.pts):
                j = i
            else:
                j = i-len(self.pts)

            if self.isRational:
                x = self.pts[j].X*self.weights[j]
                y = self.pts[j].Y*self.weights[j]
                z = self.pts[j].Z*self.weights[j]
                w = weights[j]
            else:
                x = self.pts[j].X
                y = self.pts[j].Y
                z = self.pts[j].Z
                w = 1
            pt[i][0] = Rhino.Geometry.Point4d(x,y,z,w)
            if haveLines==1:

                plane = Rhino.Geometry.Plane(self.pts[j], Rhino.Geometry.Vector3d(0,0,1))
                text3d = TextGoo( Rhino.Display.Text3d( "P"+str(i), plane, 3 ))
                hslColor = Rhino.Display.ColorHSL(0,1,0.5)
                text3d.SetColor(hslColor.ToArgbColor())
                ptsGoo.append(text3d)

        def calculatePoint4d( p0, factor0,p1,factor1 ):
            return Rhino.Geometry.Point4d(
                p0.X*factor0+p1.X*factor1,
                p0.Y*factor0+p1.Y*factor1,
                p0.Z*factor0+p1.Z*factor1,
                p0.W*factor0+p1.W*factor1)

        # starting calculation
        a = {}
        lines = []
        for r in range (1,h+1):
            lines.append([])
            for i in range(k-p+r+1,k-s+2) :
                a[i]={}
                Vai_1  = self.getKnotValue( i-1 )
                Vaip_r = self.getKnotValue( i+p-r )
                a[i][r] = (u-Vai_1)/( Vaip_r-Vai_1)
                pt[i][r] = calculatePoint4d( pt[i-1][r-1],(1-a[i][r]),pt[i][r-1],a[i][r] )
                if haveLines == 1:
                    line = Rhino.Geometry.Line(
                        Rhino.Geometry.Point3d(pt[i-1][r-1]),
                        Rhino.Geometry.Point3d(pt[i][r-1]) )
                    lineGoo = LineGoo(line)
                    hslColor = Rhino.Display.ColorHSL((r-1)/(h+1),1,0.5)
                    lineGoo.SetColor(hslColor.ToArgbColor())
                    lines[r-1].append(lineGoo)
                    
        return Rhino.Geometry.Point3d(pt[k-s+1][p-s]), ptsGoo, lines

    # draw curves and lines
    def drawNurbsCurvePts(self,nums,u):
        pts = []
        for f in rs.frange( self.knots[0],self.knots[-1],(self.knots[-1]-self.knots[0])/float(nums) ):
            if f<u:
                pt, _, _ = nurbs.calculateNurbsPoint(f)
                pts.append(pt)
        pointAtU, ptsGoo, deBoorlines = nurbs.calculateNurbsPoint(u,1)
        return pts,pointAtU, ptsGoo, deBoorlines


### main ###
nurbs = DeBoorAlgorithmNurbs(degree, points, weights, knots, isPeriodic, isRational)
curvePoints, pointAtU, deBoorPts, colorlines= nurbs.drawNurbsCurvePts(80,u)
deBoorlines = th.list_to_tree( colorlines, source=[0,0])

