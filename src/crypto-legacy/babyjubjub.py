from sage.all_cmdline import *
from point import Point

# BabyJubJub #
class BabyJubJub:

	def __init__(self):
		self._q = Integer(21888242871839275222246405745257275088548364400416034343698204186575808495617)
		self._Fq = GF(self._q)['x, y']
		(self._x, self._y) = self._Fq._first_ngens(2)
		self._MontCurve = EllipticCurve(self._y**Integer(2) -(self._x**Integer(3) +Integer(168698) *self._x**Integer(2) +self._x))
		self._Bedw = Point(Integer(5299619240641551281634865583518297030282874472190772894086521144482721001553), Integer(16950150798460657717958625567821834550301663161624707787222815936182638968203))
		self._Bmont = self.EdwToMont(self._Bedw)
		
	def EdwToMont(self, pe):
		u = (self._Fq(Integer(1))+self._Fq(pe.y))/(self._Fq(Integer(1))-self._Fq(pe.y))
		v = (self._Fq(Integer(1))+self._Fq(pe.y))/((self._Fq(Integer(1))-self._Fq(pe.y))*self._Fq(pe.x))
		return Point(u, v)
		
	def MontToEdw(self, pm):
		x = self._Fq(pm.x)/self._Fq(pm.y)
		y = (self._Fq(pm.x)-self._Fq(Integer(1)))/(self._Fq(pm.x)+self._Fq(Integer(1)))
		return Point(x,y)
		
	def EdwToMontCurvePoint(self, pe):
		pm = self.EdwToMont(pe)
		return self.getCurvePoint(pm)

	def printCurve(self):
		print(self._MontCurve)
		
	def getBaseCoordEdw(self):
		return self._Bedw
		
	def getBaseCoordMont(self):
		return self._Bmont
		
	def getCurvePoint(self, p):
		return self._MontCurve(p.x, p.y)
