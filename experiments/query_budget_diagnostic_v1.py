"""Frozen query-budget diagnostic for the confirmatory campaign.

V0W is the positive control with an analytical recovery threshold. V4-R3 is
probed with a fixed family of encoded-index chosen plaintexts and a simple
per-position lookup predictor. This is an empirical structural diagnostic only;
it is not a proof of CPA security or insecurity.
"""
from __future__ import annotations
import hashlib,json
import numpy as np
from V4R3_confirmatory_v1 import encrypt_bytes
from v0w_positive_control import encrypt as weak_encrypt, recover_structure, recover_plaintext, required_queries

SEEDS=(17,271,1618,4099,12345)
BUDGETS=(1,2,4,8,16,32,64)
SHAPE=(32,32,3)
N=int(np.prod(SHAPE))

def derive(seed,label,n):
    out=b'';i=0
    while len(out)<n:
        out+=hashlib.sha256(f'{seed}|{label}|{i}'.encode()).digest();i+=1
    return out[:n]

def v4(pt,key,nonce):
    return encrypt_bytes(pt,key,nonce,rows=SHAPE[0],cols=SHAPE[1],channels=SHAPE[2]).ciphertext

def queries(seed,q):
    rng=np.random.default_rng(seed+7000)
    base=[bytes(N)]
    idx=np.arange(N,dtype=np.uint64)
    for d in range(3): base.append(((idx//(256**d))%256).astype(np.uint8).tobytes())
    while len(base)<q: base.append(rng.integers(0,256,N,dtype=np.uint8).tobytes())
    return base[:q]

def lookup_predict(train_p,train_c,target_c):
    # For each ciphertext position, learn observed C->P byte pairs only.
    # Unseen ciphertext bytes fall back to zero; the intentionally limited
    # model is fixed before confirmatory execution.
    tp=np.stack([np.frombuffer(x,np.uint8) for x in train_p])
    tc=np.stack([np.frombuffer(x,np.uint8) for x in train_c])
    z=np.frombuffer(target_c,np.uint8); out=np.zeros(N,dtype=np.uint8)
    for i in range(N):
        hits=np.flatnonzero(tc[:,i]==z[i])
        if hits.size: out[i]=tp[hits[-1],i]
    return out

def main():
    raw=[]
    for seed in SEEDS:
        key=derive(seed,'MASTER',32);nonce=derive(seed,'NONCE',16)
        rng=np.random.default_rng(seed+9000);target=rng.integers(0,256,N,dtype=np.uint8).tobytes()
        target_c=v4(target,key,nonce)
        for q in BUDGETS:
            qp=queries(seed,q);qc=[v4(p,key,nonce) for p in qp]
            pred=lookup_predict(qp,qc,target_c)
            br=float(np.mean(pred==np.frombuffer(target,np.uint8)))
            raw.append({'variant':'V4-R3','seed':seed,'Q':q,'byte_recovery':br})
        # V0W analytical positive control is evaluated at the registered budgets.
        wk=derive(seed,'V0W',32);oracle=lambda p:weak_encrypt(p,wk)
        rp,mask=recover_structure(N,oracle);ct=oracle(target);rec=recover_plaintext(ct,rp,mask)
        for q in BUDGETS:
            # Full structural recovery becomes available once analytical query count is met.
            br=float(np.mean(np.frombuffer(rec,np.uint8)==np.frombuffer(target,np.uint8))) if q>=required_queries(N) else None
            raw.append({'variant':'V0W','seed':seed,'Q':q,'byte_recovery':br,'analytical_threshold':required_queries(N)})
    out={'experiment':'query_budget_diagnostic_v1','shape':SHAPE,'budgets':BUDGETS,'random_byte_reference':1/256,'raw':raw,'guardrail':'V4 lookup attack is a fixed limited diagnostic; failure is not a general CPA-security proof.'}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
