import rhinoscriptsyntax as rs
import Rhino

class BezierCurve(object):

    def __init__(self, pts):
        self.pts = pts

    def calculatePoint( self, u ): 
        p = None
        n = len(pts)
        for i in range(n):
            if i == 0:
                p = BezierCurve.binomial(n-1,i)*(u**i)*((1-u)**(n-1-i))*self.pts[i]
            else: 
                p += BezierCurve.binomial(n-1,i)*(u**i)*((1-u)**(n-1-i))*self.pts[i]
        return p

    def draw(self,nums):
        pts = []
        for i in range(nums+1):
            pts.append(rs.AddPoint( self.calculatePoint( i/float(nums) ) ) )
        return pts

    @staticmethod
    def binomial(n, k):
        """
        A fast way to calculate binomial coefficients by Andrew Dalke.
        See http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
        """
        if 0 <= k <= n:
            ntok = 1
            ktok = 1
            for t in xrange(1, min(k, n - k) + 1):
                ntok *= n
                ktok *= t
                n -= 1
            return ntok // ktok
        else:
            return 0

bc = BezierCurve(pts)
curvePoints = bc.draw(nums)