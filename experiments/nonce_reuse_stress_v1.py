"""Frozen nonce-reuse stress diagnostic for experimental V4-R3.

Deliberately reuses a nonce to test whether simple reusable-XOR relations emerge.
This does NOT claim nonce-misuse resistance; the construction requires nonce uniqueness.
"""
from __future__ import annotations
import hashlib,json
import numpy as np
from V4R3_confirmatory_v1 import encrypt_bytes
SEEDS=(17,271,1618,4099,12345); ROWS=COLS=32; CH=3

def d(seed,label,n): return hashlib.sha256(f"NR|{seed}|{label}".encode()).digest()[:n]

def br(a,b): return float(np.mean(np.frombuffer(a,dtype=np.uint8)==np.frombuffer(b,dtype=np.uint8)))

def main():
    n=ROWS*COLS*CH; raw=[]
    for seed in SEEDS:
        rng=np.random.default_rng(seed); key=d(seed,'K',32); nonce=d(seed,'N',16)
        p1=rng.integers(0,256,n,dtype=np.uint8).tobytes(); p2=rng.integers(0,256,n,dtype=np.uint8).tobytes(); target=rng.integers(0,256,n,dtype=np.uint8).tobytes()
        c1=encrypt_bytes(p1,key,nonce,rows=ROWS,cols=COLS,channels=CH).ciphertext
        ct=encrypt_bytes(target,key,nonce,rows=ROWS,cols=COLS,channels=CH).ciphertext
        mask=bytes(x^y for x,y in zip(c1,p1)); guess=bytes(x^y for x,y in zip(ct,mask))
        # two-known-pair consistency: if a reusable XOR mask existed, masks would agree broadly.
        c2=encrypt_bytes(p2,key,nonce,rows=ROWS,cols=COLS,channels=CH).ciphertext
        mask2=bytes(x^y for x,y in zip(c2,p2))
        raw.append({'seed':seed,'target_byte_recovery':br(guess,target),'mask_consistency':br(mask,mask2)})
    out={'experiment':'nonce_reuse_stress_v1','random_byte_reference':1/256,'raw':raw,
         'summary':{'target_byte_recovery_mean':float(np.mean([r['target_byte_recovery'] for r in raw])),'mask_consistency_mean':float(np.mean([r['mask_consistency'] for r in raw]))},
         'guardrail':'Deliberate misuse diagnostic for a simple reusable-XOR relation only. V4-R3 still requires unique nonces; failure of this diagnostic is not nonce-misuse-resistance proof.'}
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
