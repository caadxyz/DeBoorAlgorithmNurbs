#coding=utf-8
import rhinoscriptsyntax as rs
import Grasshopper as gh
import Rhino
import System
from math import sqrt

class TextGoo( gh.Kernel.Types.GH_GeometricGoo[Rhino.Display.Text3d], 
               gh.Kernel.IGH_BakeAwareData, 
               gh.Kernel.IGH_PreviewData ):

    #region construction
    def __init__(self, text):
        self.m_value = text
    
    @staticmethod
    def DuplicateText3d(original):
        if original is None: return None
        text = Rhino.Display.Text3d(original.Text, original.TextPlane, original.Height)
        text.Bold = original.Bold,
        text.Italic = original.Italic,
        text.FontFace = original.FontFace
        return text
    
    def DuplicateGeometry(self):
        return TextGoo(TextGoo.DuplicateText3d(self.m_value))
    
    #region properties
    def get_TypeName(self):
        return "3D Text"
        
    def get_TypeDescription(self):
        return "3D Text"
    
    def ToString(self):
        if self.m_value is None: return "<null>"
        return self.m_value.Text
        
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
    
    #region methods
    def Transform(self, xform):
        text = TextGoo.DuplicateText3d(self.m_value)
        if text is None: return TextGoo(None)
        
        plane = text.TextPlane
        point = plane.PointAt(1, 1)
        
        plane.Transform(xform)
        point.Transform(xform)
        dd = point.DistanceTo(plane.Origin)
        
        text.TextPlane = plane
        text.Height *= dd / sqrt(2)
        return TextGoo(text)
        
    def Morph(self, xmorph):
        return self.DuplicateGeometry()

    #region preview
    def get_ClippingBox(self):
        return self.get_Boundingbox()
        
    def DrawViewportWires(self, args):
        if self.m_value is None: return
        args.Pipeline.Draw3dText(self.m_value, args.Color)
      
    def DrawViewportMeshes(self, args):
        # Do not draw in meshing layer.
        pass

    #region baking
    def BakeGeometry(self, doc, att, id):
        id = System.Guid.Empty
        if self.m_value is None:
            return False, id
        if att is None:
            att = doc.CreateDefaultAttributes()
        id = doc.Objects.AddText(self.m_value, att)
        return True, id
