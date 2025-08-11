#!/usr/bin/env python3
import argparse, os, pickle, math
from collections import defaultdict

def g(m,n): return 4 + 3*m + 3*n + 2*m*n

def is_prime(n):
    if n < 2: return False
    small = (2,3,5,7,11,13,17,19,23,29)
    for p in small:
        if n == p: return True
        if n % p == 0: return False
    if n % 2 == 0: return False
    r = int(math.isqrt(n))
    f = 3
    while f <= r:
        if n % f == 0: return False
        f += 2
    return True

def load_state(fn):
    if os.path.exists(fn):
        with open(fn,"rb") as fh:
            return pickle.load(fh)
    return {"seen":{}, "last_m":0}

def save_state(state, fn):
    tmp = fn + ".tmp"
    with open(tmp,"wb") as fh:
        pickle.dump(state, fh)
    os.replace(tmp, fn)

def generate(M,N,state_file,checkpoint):
    st = load_state(state_file)
    seen = st.get("seen",{})
    start_m = st.get("last_m",0)
    for m in range(start_m, M+1):
        for n in range(m, N+1):  # unordered pairs
            val = g(m,n)
            seen[val] = seen.get(val,0)+1
        st["last_m"] = m+1
        st["seen"] = seen
        if (m-start_m+1) % checkpoint == 0:
            save_state(st,state_file)
    save_state(st,state_file)
    maxv = max(seen.keys()) if seen else 0
    T = [0]*(maxv+1)
    for k,c in seen.items():
        T[k] = k if c==1 else 0
    return seen, T

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument("--M",type=int,default=300)
    p.add_argument("--N",type=int,default=None)
    p.add_argument("--state-file",default="outputs/state.pkl")
    p.add_argument("--checkpoint",type=int,default=10)
    args=p.parse_args()
    if args.N is None: args.N = args.M
    os.makedirs("outputs",exist_ok=True)
    seen,T = generate(args.M, args.N, args.state_file, args.checkpoint)
    maxv = len(T)-1
    primes = [k for k in range(2, maxv+1) if T[k]==k and is_prime(k)]
    print("maxv",maxv,"primes_in_T",len(primes))
    import csv
    with open("outputs/seen_counts_sample.csv","w",newline='') as fh:
        w=csv.writer(fh); w.writerow(["value","count"])
        for k in sorted(list(seen)[:2000]):
            w.writerow([k,seen[k]])
    with open("outputs/primes_in_T_sample.csv","w",newline='') as fh:
        w=csv.writer(fh); w.writerow(["prime"])
        for p in primes[:5000]: w.writerow([p])
