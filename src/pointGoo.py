#coding=utf-8
import rhinoscriptsyntax as rs
import Grasshopper as gh
import Rhino
import System
from math import sqrt

class PointGoo( gh.Kernel.Types.GH_GeometricGoo[Rhino.Geometry.Point3d], 
               gh.Kernel.IGH_PreviewData ):

    #region construction
    def __init__(self, point):
        self.m_value = point
        self.color = None

    def SetColor(self,color):
        self.color = color
    
    @staticmethod
    def DuplicatePoint(original):
        if original is None: return None
        return Rhino.Geometry.Point3d(original.X,original.Y,original.Z)
    
    def DuplicateGeometry(self):
        return PointGoo(PointGoo.DuplicatePoint(self.m_value))
    
    #region properties
    def get_TypeName(self):
        return "colored point3d"
        
    def get_TypeDescription(self):
        return "colored point3d"
 
    def ToString(self):
        if self.m_value is None: return "<null>"
        return str(self.m_value.X)+','+str(self.m_value.Y)+','+str(self.m_value.Z)
       
    #region preview
    def DrawViewportWires(self, args):
        if self.m_value is None: return
        args.Pipeline.DrawPoint(self.m_value,self.color)
  
    def DrawViewportMeshes(self, args):
        pass


