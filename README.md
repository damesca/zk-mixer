# Zero-Knowledge Bitcoin Mixer with Reversible Unlinkability
PrivMix is a decentralized and compliant mixer desing that aims at finding a balance between transaction privacy and fraud analysis.
Specifically, PrivMix enables a designated regulator to re-link the input and output transaction of a private payment.
In order to enable such a re-linkage tool without exposing anything to the public view or to the mixer, PrivMix relies
on compliance proofs, which enforce the payer to send an input transaction to the mixer with a correct format.
We instantiate the proofs using NI-ZKP, which must be verified by the mixer to accept an incoming payment.
