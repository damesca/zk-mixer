pragma circom 2.0.0;

include "elgamal_hashed.circom";
//include "mimc.circom";
//include "gcm_siv_enc_2_keys.circom";
include "aes_256_ctr_encrypt.circom";

template Hybrid(msg_bit_len) {

	signal input m[msg_bit_len];
	signal input k[256];
	signal input PK[2];
	signal input r;
	//signal input CC1[2];
	//signal input cc2[256];
	//signal input cc[256];

	signal output c[128];
	signal output k_C1[2];
	signal output k_c2[256];

	// AES_GCM_SIV encryption

	var n[128] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

	component aes_enc = AES_256_CTR_ENC(msg_bit_len);
	
	for (var i = 0; i < 256; i++) {
		aes_enc.KEY[i] <== k[i];
	}
	for (var i = 0; i < 128; i++) {
		aes_enc.CTR[i] <== n[i];
	}
	for (var i = 0; i < msg_bit_len; i++) {
		aes_enc.MSG[i] <== m[i];
	}

	for (var i = 0; i < 128; i++) {
		c[i] <== aes_enc.CTX[i];
	}

	// ElGamal encryption of k
	component eg = ElGamal_Hashed();

	eg.Y[0] <== PK[0];
	eg.Y[1] <== PK[1];

	//eg.CC1[0] <== CC1[0];
	//eg.CC1[1] <== CC1[1];

	for (var i = 0; i < 256; i++) {
		//eg.cc2[i] <== cc2[i];
		eg.m[i] <== k[i];
	}

	eg.r <== r;

	k_C1[0] <== eg.C1[0];
	k_C1[1] <== eg.C1[1];

	for (var i = 0; i < 256; i++) {
		k_c2[i] <== eg.c2[i];
	}

}

component main = Hybrid(128);