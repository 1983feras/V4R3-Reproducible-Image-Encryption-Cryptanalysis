"""Frozen V4-R3 differential/influence diagnostic.

Measures ciphertext avalanche from one-byte plaintext perturbations at boundary-directed
positions. It is a diagnostic of implemented diffusion only; it is not a security proof.
"""
from __future__ import annotations
import hashlib, json
import numpy as np
from V4R3_confirmatory_v1 import encrypt_bytes

POSITIONS=(255,256,257,511,512,513,1023,1024,1025)
SEEDS=(17,271,1618,4099,12345)
ROWS,COLS,CH=32,32,3

def d(seed,label,n):
    return hashlib.sha256(f"DIFF|{seed}|{label}".encode()).digest()[:n]

def main():
    n=ROWS*COLS*CH
    raw=[]
    for seed in SEEDS:
        key=d(seed,'K',32); nonce=d(seed,'N',16)
        rng=np.random.default_rng(seed)
        p=rng.integers(0,256,size=n,dtype=np.uint8)
        c0=np.frombuffer(encrypt_bytes(p.tobytes(),key,nonce,rows=ROWS,cols=COLS,channels=CH).ciphertext,dtype=np.uint8)
        for pos in POSITIONS:
            q=p.copy(); q[pos]^=np.uint8(1)
            c1=np.frombuffer(encrypt_bytes(q.tobytes(),key,nonce,rows=ROWS,cols=COLS,channels=CH).ciphertext,dtype=np.uint8)
            changed=(c0!=c1)
            npcr=float(changed.mean())
            uaci=float(np.abs(c0.astype(np.int16)-c1.astype(np.int16)).mean()/255.0)
            raw.append({'seed':seed,'position':pos,'npcr':npcr,'uaci':uaci,'changed_bytes':int(changed.sum()),'n':n})
    out={'experiment':'differential_influence_v1','shape':[ROWS,COLS,CH],'seeds':list(SEEDS),'positions':list(POSITIONS),'raw':raw,
         'summary':{'npcr_mean':float(np.mean([r['npcr'] for r in raw])),'npcr_min':float(np.min([r['npcr'] for r in raw])),'uaci_mean':float(np.mean([r['uaci'] for r in raw])),'uaci_min':float(np.min([r['uaci'] for r in raw]))},
         'guardrail':'Ciphertext avalanche/diffusion diagnostic only; high NPCR/UACI does not establish cryptographic security.'}
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
