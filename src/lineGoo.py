#coding=utf-8
import rhinoscriptsyntax as rs
import Grasshopper as gh
import Rhino
import System
from math import sqrt

class LineGoo( gh.Kernel.Types.GH_GeometricGoo[Rhino.Geometry.Line], 
               gh.Kernel.IGH_PreviewData ):

    #region construction
    def __init__(self, line):
        self.m_value = line
        self.color = None

    def SetColor(self,color):
        self.color = color
    
    @staticmethod
    def DuplicateLine(original):
        if original is None: return None
        return Rhino.Geometry.Line(original.From, original.To)
    
    def DuplicateGeometry(self):
        return LineGoo(LineGoo.DuplicateLine(self.m_value))
    
    #region properties
    def get_TypeName(self):
        return "colored point3d"
        
    def get_TypeDescription(self):
        return "colored point3d"
 
    def ToString(self):
        if self.m_value is None: return "<null>"
        return self.m_value.ToString()

    def get_Boundingbox(self):
        if self.m_value is None:
            return Rhino.Geometry.BoundingBox.Empty
        return self.m_value.BoundingBox
        
    def GetBoundingBox(self, xform):
        if self.m_value is None:
            return Rhino.Geometry.BoundingBox.Empty
        box = self.m_value.BoundingBox
        corners = xform.TransformList(box.GetCorners())
        return Rhino.Geometry.BoundingBox(corners)
    
    #region preview
    def DrawViewportWires(self, args):
        if self.m_value is None: return
        args.Pipeline.DrawLine(self.m_value,self.color)
  
    def DrawViewportMeshes(self, args):
        pass

