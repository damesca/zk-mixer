from sage.all_cmdline import *
from secrets import randbits

# Additive Secret Sharing #
class SecretSharing:

	def __init__(self, s, n):
		#self._q = Integer(21888242871839275222246405745257275088548364400416034343698204186575808495617)
		self._q = Integer(8864636379641307987985582655993892125665954886639156314962949313547533029400547411406265429646812064672002946472067268869633225969806321590557478802774207323884570485379928282206644760402266682209472353933681352679372637254752717498141909964176598352222875644485687285283916382943)
		self._Fq = GF(self._q)
		self.s = self._Fq(s)
		self.n = n
		
	def share(self):
		shares = []
		for i in range(0, self.n-1):
			shares.append(self._Fq(randbits(928)))
		last = self.s
		for i in range(0, self.n-1):
			last = last - shares[i]
		shares.append(last)
		return shares
		
	def recombine(self, shares):
		res = self._Fq(0)
		for i in shares: res = res + i
		return res
		
ss = SecretSharing(25, 5)
sh = ss.share()
print(sh)
print(ss.recombine(sh))
