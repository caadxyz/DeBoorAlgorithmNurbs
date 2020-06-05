#coding=utf-8
################################################################################
# DeBoorAlgorithmNurbs.py
# Copyright (c) 2020.4 mahaidong
# Supported by ikuku.cn & caad.xyz 
# See License in the root of this repository for details.
################################################################################
import rhinoscriptsyntax as rs
import Rhino

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

    def calculateNurbsPoint(self,u):
        lines = []
        p = self.degree
        s,k = self.findKnotIndexByU(u)
        h = p-s
        pt = {}

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

        def calculatePoint4d( p0, factor0,p1,factor1 ):
            return Rhino.Geometry.Point4d(
                p0.X*factor0+p1.X*factor1,
                p0.Y*factor0+p1.Y*factor1,
                p0.Z*factor0+p1.Z*factor1,
                p0.W*factor0+p1.W*factor1)

        # starting calculation
        a = {}
        for r in range (1,h+1):
            for i in range(k-p+r+1,k-s+2) :
                a[i]={}
                Vai_1  = self.getKnotValue( i-1 )
                Vaip_r = self.getKnotValue( i+p-r )
                a[i][r] = (u-Vai_1)/( Vaip_r-Vai_1)
                pt[i][r] = calculatePoint4d( pt[i-1][r-1],(1-a[i][r]),pt[i][r-1],a[i][r] )
                lines.append(rs.AddLine( 
                    Rhino.Geometry.Point3d(pt[i-1][r-1]),
                    Rhino.Geometry.Point3d(pt[i][r-1]) ))
        return Rhino.Geometry.Point3d(pt[k-s+1][p-s]), lines

### main ###
curvePoints = []
nurbs = DeBoorAlgorithmNurbs(degree, points, weights, knots, isPeriodic, isRational)
for f in rs.frange( nurbs.knots[0],nurbs.knots[-1],1/20.0 ):
    pt,_ = nurbs.calculateNurbsPoint(f)
    curvePoints.append(pt)
pointAtU, deBoorlines = nurbs.calculateNurbsPoint(u)
