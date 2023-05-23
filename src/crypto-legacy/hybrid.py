from elgamal import ElGamalHashed
from point import Point
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sage.all_cmdline import *
import secrets

# Hybrid encryption for one message

# TODO: implement encrypt and decrypt
'''
Encrypt
	Input: (m, pk)
	Output: (ciphertext, c1, c2)

Decrypt
	Input: (ciphertext, c1, c2, sk)
	Output: (m)
'''
class Hybrid:

	def __init__(self, pubKey = None):
		if pubKey == None:		# Init to decrypt
			self._elgamal = ElGamalHashed()
			self._privKey = self._elgamal.getPrivateKey()
			self._pubKey = self._elgamal.getPublicKey()
			self._symmKey = None
		else:					# Init to encrypt
			self._elgamal = ElGamalHashed(pubKey)
			self._privKey = None
			self._pubKey = pubKey
			self._symmKey = secrets.randbits(256)
			self._encryptKey()
		
	def getPublicKey(self):
		return self._pubKey
		
	def _encryptKey(self):
		self._C1p, self._c2 = self._elgamal.encrypt(int(self._symmKey))
		
	def encrypt(self, data):
		if self._symmKey == None:
			return None
		else:
			cipher = AES.new(self._symmKey.to_bytes(32, 'little'), AES.MODE_EAX)
			nonce = cipher.nonce
			ciphertext, tag = cipher.encrypt_and_digest(data)
			return ciphertext, tag, nonce, self._C1p, self._c2
		
	def decrypt(self, ciphertext, tag, nonce, C1p, c2):
		self._symmKey = self._elgamal.decrypt(C1p, c2)
		cipher = AES.new(self._symmKey, AES.MODE_EAX, nonce)
		data = cipher.decrypt_and_verify(ciphertext, tag)
		return data

