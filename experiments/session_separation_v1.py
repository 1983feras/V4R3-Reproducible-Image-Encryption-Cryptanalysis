"""Frozen confirmatory session-separation experiment for V4-R3.

Evaluates a deliberately simple equivalent-XOR transfer model across four
pre-registered key/nonce relations. This is an empirical diagnostic, not a
formal IND-CPA claim.
"""
from __future__ import annotations
import hashlib, json
import numpy as np
from V4R3_confirmatory_v1 import encrypt_bytes

SEEDS=(17,271,1618,4099,12345)
SHAPE=(32,32,3)


def enc(p,key,nonce):
    return encrypt_bytes(p,key,nonce,rows=SHAPE[0],cols=SHAPE[1],channels=SHAPE[2]).ciphertext


def derive(seed,label,n):
    out=b''; i=0
    while len(out)<n:
        out += hashlib.sha256(f'{seed}|{label}|{i}'.encode()).digest(); i+=1
    return out[:n]


def byte_recovery(a,b):
    x=np.frombuffer(a,np.uint8); y=np.frombuffer(b,np.uint8)
    return float(np.mean(x==y))


def trial(seed):
    n=np.prod(SHAPE); rng=np.random.default_rng(seed)
    p_train=rng.integers(0,256,n,dtype=np.uint8).tobytes()
    p_target=rng.integers(0,256,n,dtype=np.uint8).tobytes()
    k1=derive(seed,'K1',32); k2=derive(seed,'K2',32)
    nu1=derive(seed,'N1',16); nu2=derive(seed,'N2',16)
    c_train=enc(p_train,k1,nu1)
    equivalent=np.bitwise_xor(np.frombuffer(c_train,np.uint8),np.frombuffer(p_train,np.uint8))
    rows=[]
    for name,k,nu in [('same_K_same_nonce',k1,nu1),('same_K_new_nonce',k1,nu2),('new_K_same_nonce',k2,nu1),('new_K_new_nonce',k2,nu2)]:
        c=enc(p_target,k,nu)
        rec=np.bitwise_xor(np.frombuffer(c,np.uint8),equivalent).tobytes()
        rows.append({'seed':seed,'condition':name,'byte_recovery':byte_recovery(rec,p_target)})
    return rows


def main():
    raw=[r for s in SEEDS for r in trial(s)]
    summary={}
    for c in sorted({r['condition'] for r in raw}):
        x=np.asarray([r['byte_recovery'] for r in raw if r['condition']==c],float)
        summary[c]={'n':int(len(x)),'mean':float(x.mean()),'sd':float(x.std(ddof=1))}
    out={'experiment':'V4R3_session_separation_v1','metric':'exact byte recovery fraction','random_byte_reference':1/256,'seeds':list(SEEDS),'raw':raw,'summary':summary,'interpretation_guardrail':'Empirical equivalent-XOR transfer diagnostic only; failure does not prove IND-CPA security.'}
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
