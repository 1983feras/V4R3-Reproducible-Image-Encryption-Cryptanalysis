"""G4 frozen red-team campaign for V4-R3.

This module attacks the frozen confirmatory implementation without modifying
its architecture. It measures same-session equivalent-transform reuse,
nonce-reuse behavior, cross-session transfer, query-budget behavior, and
ciphertext influence from one-byte perturbations.

The diagnostics are empirical cryptanalysis, not a formal IND-CPA proof.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import asdict
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from V4R3_confirmatory_v1 import encrypt_bytes

Q_BUDGETS=(1,2,4,8,16,32,64)
MASTER=bytes(range(32))
NONCE_A=bytes(range(16))
NONCE_B=bytes(reversed(range(16)))
ROWS=32; COLS=32; CH=3; N=ROWS*COLS*CH


def enc(p:bytes,nonce:bytes)->bytes:
    return encrypt_bytes(p,MASTER,nonce,rows=ROWS,cols=COLS,channels=CH).ciphertext


def xor(a:bytes,b:bytes)->bytes:return bytes(x^y for x,y in zip(a,b))
def byte_recovery(a:bytes,b:bytes)->float:return sum(x==y for x,y in zip(a,b))/len(a)
def npcr(a:bytes,b:bytes)->float:return 100.0*sum(x!=y for x,y in zip(a,b))/len(a)
def uaci(a:bytes,b:bytes)->float:return 100.0*sum(abs(x-y) for x,y in zip(a,b))/(255*len(a))


def reusable_xor_attack(target:bytes,queries:list[bytes],nonce_train:bytes,nonce_test:bytes)->dict:
    """Attempt to learn a reusable XOR-equivalent transform from chosen pairs.

    For each chosen plaintext P and ciphertext C, derive candidate Z=P xor C.
    Apply the bytewise majority candidate across Q queries to target ciphertext.
    This is intentionally simple and should break a reusable-XOR control but is
    not claimed to span all CPA strategies.
    """
    masks=[]
    for p in queries:
        c=enc(p,nonce_train);masks.append(np.frombuffer(xor(p,c),dtype=np.uint8))
    A=np.stack(masks)
    # deterministic per-position mode
    mode=np.empty(N,dtype=np.uint8)
    for j in range(N):
        mode[j]=np.bincount(A[:,j],minlength=256).argmax()
    ct=enc(target,nonce_test)
    rec=np.bitwise_xor(np.frombuffer(ct,dtype=np.uint8),mode).tobytes()
    return {'byte_recovery':byte_recovery(rec,target),'recovered_sha256':hashlib.sha256(rec).hexdigest()}


def influence_diagnostics(base:bytes,nonce:bytes,positions=(0,255,256,257,511,512,513,1023,1024,1025))->list[dict]:
    c0=enc(base,nonce);out=[]
    for pos in positions:
        if pos>=len(base):continue
        p=bytearray(base);p[pos]^=1;c1=enc(bytes(p),nonce)
        diff=np.fromiter((a!=b for a,b in zip(c0,c1)),dtype=np.uint8,count=N)
        changed=np.flatnonzero(diff)
        out.append({'position':pos,'npcr_percent':npcr(c0,c1),'uaci_percent':uaci(c0,c1),'changed_bytes':int(diff.sum()),'first_changed':None if not len(changed) else int(changed[0]),'last_changed':None if not len(changed) else int(changed[-1])})
    return out


def run()->dict:
    rng=np.random.default_rng(20261009)
    target=rng.integers(0,256,N,dtype=np.uint8).tobytes()
    pool=[rng.integers(0,256,N,dtype=np.uint8).tobytes() for _ in range(max(Q_BUDGETS))]
    budgets={}
    for q in Q_BUDGETS:
        chosen=pool[:q]
        budgets[str(q)]={
            'same_session':reusable_xor_attack(target,chosen,NONCE_A,NONCE_A),
            'cross_session':reusable_xor_attack(target,chosen,NONCE_A,NONCE_B),
        }
    zero=bytes(N);ca=enc(zero,NONCE_A);cb=enc(zero,NONCE_B)
    # Deliberate nonce-reuse observation: deterministic construction under same
    # key+nonce yields identical ciphertext for identical plaintext.
    ca2=enc(zero,NONCE_A)
    return {
      'experiment':'V4R3_G4_redteam_v1',
      'frozen':True,
      'shape':[ROWS,COLS,CH],
      'query_budgets':list(Q_BUDGETS),
      'reusable_xor_cpa':budgets,
      'session_separation':{
        'same_key_same_nonce_same_plaintext_ciphertext_equal':ca==ca2,
        'same_key_different_nonce_same_plaintext_ciphertext_equal':ca==cb,
        'different_nonce_npcr_percent':npcr(ca,cb),
        'different_nonce_uaci_percent':uaci(ca,cb),
      },
      'influence':influence_diagnostics(target,NONCE_A),
      'interpretation_policy':{
        'attack_failure':'Only the implemented reusable-XOR-equivalent CPA failed; do not claim general CPA security.',
        'nonce_reuse':'Nonce uniqueness remains a requirement; deterministic same-nonce behavior is not nonce-misuse resistance.',
        'influence':'Diffusion diagnostics are not a security proof.'
      }
    }

if __name__=='__main__':
    result=run();out=ROOT/'results'/'g4_redteam_v1.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2));print('RESULT',out)
