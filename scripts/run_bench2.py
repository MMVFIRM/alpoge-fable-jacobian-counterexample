import sys, time, os, signal, select
sys.path.insert(0, '/home/claude/geo_verify')
from comparable_bench import build_comparable_benchmark, Label
from core import GeoVerifier, EquivalenceResult
import core, structural

bench = build_comparable_benchmark()
correct = 0
tp = fp = fn = tn = 0
failed = []
methods = {}
PER = 8
t0 = time.time()

for i, inst in enumerate(bench):
    r_fd, w_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r_fd)
        try:
            signal.alarm(PER)
            res = GeoVerifier().verify(inst.reference, inst.prediction)
            signal.alarm(0)
            msg = f"{res.decision.value}|{res.method}"
        except Exception as e:
            msg = f"uncertain|err:{type(e).__name__}"
        try: os.write(w_fd, msg.encode())
        except: pass
        os.close(w_fd); os._exit(0)
    else:
        os.close(w_fd)
        ready,_,_ = select.select([r_fd],[],[],PER+2)
        if ready:
            try:
                data = os.read(r_fd,4096).decode()
                decision_val, method = (data.split("|")+["?"])[:2]
            except:
                decision_val, method = "uncertain","read_err"
        else:
            decision_val, method = "uncertain","timeout"
        os.close(r_fd)
        try: os.kill(pid, signal.SIGKILL)
        except: pass
        try: os.waitpid(pid,0)
        except: pass
    got_equiv = (decision_val == "equivalent")
    expected_equiv = (inst.label == Label.EQUIVALENT)
    ok = (expected_equiv == got_equiv)
    if ok: correct += 1
    else: failed.append((inst, got_equiv))
    if expected_equiv and got_equiv: tp += 1
    elif not expected_equiv and got_equiv: fp += 1
    elif expected_equiv and not got_equiv: fn += 1
    else: tn += 1
    methods[method] = methods.get(method,0)+1
    if (i+1)%40==0:
        print(f"  ...{i+1}/{len(bench)} ({time.time()-t0:.0f}s, {correct} correct)")

total=len(bench); acc=100*correct/total
prec=tp/(tp+fp) if (tp+fp) else 0
rec=tp/(tp+fn) if (tp+fn) else 0
f1=2*prec*rec/(prec+rec) if (prec+rec) else 0
print("="*70)
print(f"ACCURACY: {correct}/{total} = {acc:.2f}%")
print(f"Precision {100*prec:.2f}%  Recall {100*rec:.2f}%  F1 {100*f1:.2f}%")
print(f"TP={tp} FP={fp} FN={fn} TN={tn}")
print(f"Time {time.time()-t0:.1f}s")
print("="*70)
for m,c in sorted(methods.items(), key=lambda x:-x[1])[:12]:
    print(f"  {m:45s} {c}")
fp_cases=[(i,g) for i,g in failed if i.label==Label.NOT_EQUIVALENT]
fn_cases=[(i,g) for i,g in failed if i.label==Label.EQUIVALENT]
print(f"\nFalse positives (called EQUIV, truly NOT): {len(fp_cases)}")
print(f"False negatives (called NOT, truly EQUIV): {len(fn_cases)}")
print("\nSample false positives (verifier WRONGLY said equal):")
for inst,g in fp_cases[:8]:
    print(f"  [{inst.perturbation_type}] {inst.reference[:48]!r} vs {inst.prediction[:48]!r}")
print("\nSample false negatives (verifier missed a true equivalence):")
for inst,g in fn_cases[:8]:
    print(f"  [{inst.perturbation_type}] {inst.reference[:48]!r} vs {inst.prediction[:48]!r}")
