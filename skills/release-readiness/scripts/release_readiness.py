#!/usr/bin/env python3
"""Release readiness first pass: commitment vs delivery. usage: release_readiness.py <dir>
Reuses reconcile.py from ../../reconcile-status/scripts for the Done Chain."""
import os, re, sys, json, csv, io, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("reconcile", os.path.join(HERE, "..", "..", "reconcile-status", "scripts", "reconcile.py"))
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
KEY = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")

def main(d):
    rel = rc.load(d, "release.md")
    if not rel: sys.exit("release.md required — committed scope cannot be guessed")
    target = (re.search(r"target:\s*(\S+)", rel, re.I) or [None, "?"])[1]
    name = (re.search(r"^#\s*(.+?)\s*—", rel, re.M) or [None, "release"])[1]
    committed = []
    for line in rel.splitlines():
        m = re.match(r"-\s*([A-Z][A-Z0-9]+-\d+)\s*(.*)", line.strip())
        if m: committed.append((m.group(1), m.group(2).strip()))
    told = [t.strip() for t in (re.search(r"communicated to:\s*(.+)", rel, re.I) or [None, ""])[1].split(",") if t.strip()]
    pm = re.search(r"from (\d{2})-(\d{2})", rel)
    plan_date = f"{target[:4]}-{pm.group(1)}-{pm.group(2)}" if pm and target != "?" else "0000"
    # done chain via reconcile.py (capture its table)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): rc.main(d)
    table = {}
    for line in buf.getvalue().splitlines():
        if line.startswith("| ") and not line.startswith("| Feature"):
            c = [x.strip() for x in line.strip("|").split("|")]
            table[c[0]] = c
    status = rc.load(d, "status.md") or ""
    feats = rc.parse_status(status)
    key2feat = {k: n for n, f in feats.items() for k in f["keys"]}
    jira = rc.load(d, "jira.csv"); by_key, children = rc.parse_jira(jira) if jira else ({}, {})
    prs = json.loads(rc.load(d, "prs.json") or "[]")
    slack = (rc.load(d, "slack.txt") or "").splitlines()
    committed_keys = set()
    for k, _ in committed:
        committed_keys.add(k); committed_keys |= {c["Issue key"] for c in children.get(k, [])}
    rows, reasons, ready = [], [], 0
    for k, title in committed:
        feat = key2feat.get(k, title)
        c = table.get(feat)
        if not c: rows.append((feat, ["?"]*6, "?", "not in status doc — unverified")); continue
        l2, l3, l4, l5, l6, l8 = c[3], c[4], c[5], c[6], c[7], c[9]
        bad = [n for n, v in zip((2,3,5,6,8), (l2,l3,l5,l6,l8)) if v in ("✖", "○")]
        sev = 2 if l6 == "✖" else 0
        cut = [x["Issue key"] for x in children.get(k, []) if x.get("Resolution","").lower().replace("'","") in ("wont do","won't do")]
        why = []
        if bad: why.append("link " + "/".join(map(str, bad)) + " open")
        if l4 == "✖": why.append("tested → conflicting"); bad.append(4)
        if cut: why.append(f"scope cut {', '.join(cut)} " + ("undisclosed" if not any(x in rel for x in cut) else "disclosed"))
        if cut and not any(x in rel for x in cut): bad.append("cut")
        ok = not bad
        ready += ok
        rows.append((feat, [l2,l3,l4,l5,l6,l8], "✔" if ok else "✖", "; ".join(why) or "ready"))
        if not ok: reasons.append((feat, len(bad) + sev))
    # uncommitted
    extra = [p for p in prs if p.get("state","").upper()=="MERGED" and p.get("baseRefName") in ("main","master") and not p.get("title","").lower().startswith("revert")
             and (p.get("mergedAt") or "")[:10] >= plan_date
             and not (set(KEY.findall(p.get("title","")+p.get("body",""))) & committed_keys)]
    # comms after last change
    last_change = max([p.get("mergedAt","")[:10] for p in prs if p.get("mergedAt")] + ["0000"])
    comms = []
    for t in told:
        msgs = [l for l in slack if t.lower() in l.lower()]
        after = [l for l in msgs if l[:10] >= last_change]
        comms.append((t, msgs[-1][:16] if msgs else "never", "y" if after else "n"))
    verdict = "GO" if ready == len(committed) and not extra and all(c[2]=="y" for c in comms) else "NO-GO"
    print(f"# {name} — target {target} — **{verdict}**\n")
    print("| Committed feature | 2 | 3 | 4 | 5 | 6 | 8 | Ready? | Reason |\n|---|---|---|---|---|---|---|---|---|")
    for feat, cells, ok, why in rows: print(f"| {feat} | " + " | ".join(cells) + f" | {ok} | {why} |")
    print(f"\nReady: {ready} of {len(committed)} committed.\n")
    print(f"**Uncommitted in release** (merged since planning {plan_date})")
    for p in extra:
        ks = ", ".join(sorted(set(KEY.findall(p['title']+p['body'])))) or "no key"
        print(f"- #{p['number']} {p['title']} — {ks} — merged {p['mergedAt'][:10]} — disclosed in release doc: {'y' if ks.split(', ')[0] in rel else 'n'}")
    if not extra: print("- none")
    print("\n**Stakeholder comms** (last change in release: " + last_change + ")")
    for t, last, after in comms: print(f"- {t}: last told {last}; told after last change: {after}")
    print("\n**Manual checks owed**: link 1 (PRD coverage) and link 7 (exercised in prod) for every committed feature.")
    if reasons:
        top = sorted(reasons, key=lambda x: -x[1])[0][0]
        print(f"\nNext: run resolve-blocker on {top} to plan the fix.")

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else ".")
