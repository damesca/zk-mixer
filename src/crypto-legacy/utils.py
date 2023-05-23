def num2bits(a, n):
	out = [0] * n
	lc1 = 0
	e2 = 1
	for i in range(0, n):
		out[i] = (a >> i) & 1
		lc1 += out[i] * e2
		e2 = e2 + e2
	return out
	
def bits2num(a, n):
	lc1 = 0
	e2 = 1
	for i in range(0, n):
		lc1 += a[i] * e2
		e2 = e2 + e2
	return lc1
	
def access_bit(data, num):
	base = int(num // 8)
	shift = int(num % 8)
	return (data[base] >> shift) & 0x1
	
def bytearray_to_bitlist(data):
	return [access_bit(data, i) for i in range(len(data)*8)]
	
def xor_bytearrays(ba1, ba2):
	return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
