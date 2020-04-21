#coding=utf-8
################################################################################
# DeBoorAlgorithmNurbs.py
# Copyright (c) 2020.4 mahaidong
# Supported by ikuku.cn & caad.xyz 
# See License in the root of this repository for details.
################################################################################
import rhinoscriptsyntax as rs
import Rhino

def calculatePoint4d(p0, factor0,p1,factor1):
    return Rhino.Geometry.Point4d(
        p0.X*factor0+p1.X*factor1,
        p0.Y*factor0+p1.Y*factor1,
        p0.Z*factor0+p1.Z*factor1,
        p0.W*factor0+p1.W*factor1)
def findKnotIndexByU(u,knots):
    s = 0
    index = 0 
    if u<knots[0] or u>knots[-1]:
        return
    for i in range(len(knots)):
        if knots[i]>u:
            if s==0 :
                return s,i-1
        elif knots[i] == u:
            index = i
            s += 1
    if s>0:
        return s,index
def getKnotValue(isPeriodic,knots,i):
    if isPeriodic == True:
        if i>=len(knots):
            return knots[-1]+knots[i+1-len(knots)]
        elif i<0:
            return -knots[-1]+knots[i-1]
    return knots[i]


def calculateNurbsPoint(u):
    lines = []
    p = degree
    s,k = findKnotIndexByU(u,knots)
    h = p-s
    pt = {}

    # initialize pt[i][0] for starting calculation
    for i in range(k-p+1,k-s+2):
        pt[i]={}
        if i < len(points):
            j = i
        else:
            j = i-len(points)
        if isRational:
            x = points[j].X*weights[j]
            y = points[j].Y*weights[j]
            z = points[j].Z*weights[j]
            w = weights[j]
        else:
            x = points[j].X
            y = points[j].Y
            z = points[j].Z
            w = 1
        pt[i][0] = Rhino.Geometry.Point4d(x,y,z,w)

    # starting calculation
    a = {}
    for r in range (1,h+1):
        for i in range(k-p+r+1,k-s+2) :
            a[i]={}
            Vai_1  = getKnotValue( isPeriodic,knots,i-1)
            Vaip_r = getKnotValue( isPeriodic,knots,i+p-r)
            a[i][r] = (u-Vai_1)/( Vaip_r-Vai_1)
            pt[i][r] = calculatePoint4d(pt[i-1][r-1],(1-a[i][r]),pt[i][r-1],a[i][r])
            lines.append(rs.AddLine( 
                Rhino.Geometry.Point3d(pt[i-1][r-1]),
                Rhino.Geometry.Point3d(pt[i][r-1]) ))
    return Rhino.Geometry.Point3d(pt[k-s+1][p-s]), lines

curvePoints = []
for f in rs.frange(knots[0],knots[-1],1/20.0):
    pt,_ = calculateNurbsPoint(f)
    curvePoints.append(pt)
pointAtU, deBoorlines = calculateNurbsPoint(u)
