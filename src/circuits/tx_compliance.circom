pragma circom 2.0.0;

include "escalarmulany.circom";
include "bitify.circom";
include "babyjub.circom";
include "elgamal.circom";

/*
 * Proves that a linkage param fulfils compliance requirements,
 * according to a decryption mixnet-based mixer
 *
 * Public input l: linkage param
 * Public input Enc_m: Message encrypted with the mixnet keys
 * Public input PK[n]: List of mixnet public keys
 * Public input PK_reg: Regulator's public key
 * Private input k: Regulator's encryption symmetric key
 * Private input m: Message sent, where m = (Enc_l || o)
 * Private input Enc_l: linkage param encrypted with PK_reg
 * Private input o: receiver's address
 * Private input r_l: randomness used to encrypt l
 * Private input r[n]: randomness used to encrypt the message for the mixnet
 * Private input k[n]: symmetric key for encryption
 */
 
 template Compliance(n) {
 
 	signal input l;
 	signal input cm;
 	signal input PK[n][2];
 	signal input PK_reg[2];
 	signal input k;
 	
 	signal input cl;
 	signal input m;
 	signal input o;
 	signal input r_l;
 	signal input r[n];
 	signal input k[n];
 	
 	// Encrypt l with regulator's key
 	
 	component h_reg = HybridEG();
 	h_reg.m <== l;
 	h_reg.k <== k;
 	h_reg.pk0 <== PK_reg[0];
 	h_reg.pk1 <== PK_reg[1];
 	
 	signal o_cl <== h_reg.c;
 	
 	o_cl === cl;
 	
 	// Check the message passed
 	
 	component concat = Concat();
 	concat.a <== o_cl;
 	concat.b <== o;
 	
 	signal o_m <== concat.c;
 	
 	o_m === m;
 	
 	// Sequential encryption
 	
 	component  h_enc[n];
 	for (var i = 0; i < n; i++) {
		h_enc[i] = HybridEG();
	}
	
	signal input_m[n+1];
	input_m[0] = o_m;
	
	for (var i = 0; i < n; i++) {
	
		h_enc[i].m <== input_m[i];
		h_enc[i].k <== k[i];
		h_enc[i].pk0 <== PK[i][0];
		h_enc[i].pk1 <== PK[i][1];
		
		input_m[i+1] <== h_enc[i].c;
		
	}
	
	input_m[n] === cm;
 
 }
 
 component main {public [l, cm, PK, PK_reg]} = Compliance(2);
