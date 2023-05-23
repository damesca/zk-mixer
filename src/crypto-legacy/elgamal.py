from sage.all_cmdline import *
from point import Point
from babyjubjub import BabyJubJub
import secrets
from hashlib import sha256

# ElGamal #	
class ElGamal:
	
	# Interfaces edwards points by default (else montgomery)
	def __init__(self, privKey, edwards = True):
		self._montCurve = BabyJubJub()
		self._privKey = Integer(privKey)
		montB = self._montCurve.getBaseCoordMont()
		self._montB = self._montCurve.getCurvePoint(montB)
		self._pubKey = self._privKey * self._montB
		self._edwards = edwards
		
	def getPrivateKey(self):
		return self._privKey
	
	def getPublicKey(self):
		if(self._edwards):
			return self._montCurve.MontToEdw(Point(self._pubKey[0], self._pubKey[1]))
		else:
			return Point(self._pubKey[0], self._pubKey[1])
		
	def encrypt(self, M):
		if(self._edwards):
			Mmont = self._montCurve.EdwToMontCurvePoint(M)
		else:
			Mmont = self._montCurve.getCurvePoint(M)
			
		r = secrets.randbits(256)
		C1 = r * self._montB
		preC2 = r * self._pubKey
		C2 = preC2 + Mmont
		
		if(self._edwards):
			C1p = self._montCurve.MontToEdw(Point(C1[0], C1[1]))
			C2p = self._montCurve.MontToEdw(Point(C2[0], C2[1]))
		else:
			C1p = Point(C1[0], C1[1])
			C2p = Point(C2[0], C2[1])
		
		return C1p, C2p
		
	def decrypt(self, C1p, C2p):
		if(self._edwards):
			C1 = self._montCurve.EdwToMontCurvePoint(C1p)
			C2 = self._montCurve.EdwToMontCurvePoint(C2p)
		else:
			C1 = self._montCurve.getCurvePoint(C1p)
			C2 = self._montCurve.getCurvePoint(C2p)
	
		S = self._privKey * C1
		M = C2 - S
		if(self._edwards):
			Mp = self._montCurve.MontToEdw(Point(M[0], M[1]))
		else:
			Mp = Point(M[0], M[1])
		
		return Mp

# ElGamalHashed #
# TODO: Accept more than integers: to_bytes() only works for int
class ElGamalHashed:
	
	# Interfaces edwards points by default (else montgomery)
	def __init__(self, pubKey = None, edwards = True):
		if pubKey == None:		# Init to decrypt
			self._montCurve = BabyJubJub()
			self._privKey = Integer(secrets.randbits(256))
			montB = self._montCurve.getBaseCoordMont()
			self._montB = self._montCurve.getCurvePoint(montB)
			self._pubKey = self._privKey * self._montB
			self._edwards = edwards
		else:					# Init to encrypt
			self._montCurve = BabyJubJub()
			self._privKey = None
			if edwards:
				self._pubKey = self._montCurve.getCurvePoint(self._montCurve.EdwToMont(pubKey))
			else:
				self._pubKey = self._montCurve.getCurvePoint(pubKey)
			montB = self._montCurve.getBaseCoordMont()
			self._montB = self._montCurve.getCurvePoint(montB)
			self._edwards = edwards
		
	def getPrivateKey(self):
		return self._privKey
	
	def getPublicKey(self):
		if(self._edwards):
			return self._montCurve.MontToEdw(Point(self._pubKey[0], self._pubKey[1]))
		else:
			return Point(self._pubKey[0], self._pubKey[1])
		
	def encrypt(self, M):
	
		if type(M) is bytes:
			plaintext = M
		elif type(M) is int:
			plaintext = M.to_bytes(32, 'little')
		else:
			print('Error in plaintext type')
		
		r = secrets.randbits(256)
		C1 = r * self._montB
		preC2 = r * self._pubKey
		h = sha256()
		h.update(int(preC2[0]).to_bytes(32, 'little'))
		h.update(int(preC2[1]).to_bytes(32, 'little'))
		res = h.digest()
		c2 = self._byte_xor(plaintext, res)
		
		if(self._edwards):
			C1p = self._montCurve.MontToEdw(Point(C1[0], C1[1]))
		else:
			C1p = Point(C1[0], C1[1])
		
		return C1p, c2
	
	def decrypt(self, C1p, c2):
		if(self._privKey == None):
			return None
		else:
			if(self._edwards):
				C1 = self._montCurve.EdwToMontCurvePoint(C1p)
			else:
				C1 = self._montCurve.getCurvePoint(C1p)
		
			S = self._privKey * C1
			h = sha256()
			h.update(int(S[0]).to_bytes(32, 'little'))
			h.update(int(S[1]).to_bytes(32, 'little'))
			res = h.digest()
			M = self._byte_xor(c2, res)
			
			return M
		
	def _byte_xor(self, ba1, ba2):
		return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
