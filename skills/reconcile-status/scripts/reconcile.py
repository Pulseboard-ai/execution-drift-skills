#!/usr/bin/env python3
"""First-pass Done Chain table from exported files. Deterministic, shallow, offline.

usage: python reconcile.py <dir>   (see references/input-modes.md for file formats)
Prints a markdown table + findings. Links 1 and 7 are always 'manual'.
"""
import csv, json, os, re, sys
from collections import defaultdict

KEY = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
DONE = {"done", "closed", "resolved", "released"}
BUG_TYPES = {"bug", "defect"}
SEV = re.compile(r"(sev|p)-?\s?([12])\b", re.I)

def load(d, name):
    p = os.path.join(d, name)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def parse_status(text):
    feats, cur = {}, None
    for line in text.splitlines():
        h = re.match(r"^##+\s*(.+)$", line)
        if h:
            cur = h.group(1).strip(); feats[cur] = {"reported": "unknown", "keys": set(), "deps": set()}; continue
        if cur is None: continue
        m = re.search(r"\b(done|on track|at risk|blocked|in progress)\b", line, re.I)
        if m and feats[cur]["reported"] == "unknown": feats[cur]["reported"] = m.group(1).title()
        feats[cur]["keys"] |= set(KEY.findall(line))
        dm = re.search(r"depends on:\s*(.+)", line, re.I)
        if dm: feats[cur]["deps"] |= {t.strip() for t in dm.group(1).split(",")}
    return feats

def parse_jira(text):
    rows = list(csv.DictReader(text.splitlines()))
    by_key = {r["Issue key"]: r for r in rows}
    children = defaultdict(list)
    for r in rows:
        if r.get("Parent"): children[r["Parent"]].append(r)
    return by_key, children

def main(d):
    status = load(d, "status.md"); jira = load(d, "jira.csv"); prs = load(d, "prs.json")
    slack = load(d, "slack.txt"); prd = load(d, "prd.md"); deploys = load(d, "deploys.txt")
    if not status: sys.exit("status.md required for first pass")
    feats = parse_status(status)
    by_key, children = parse_jira(jira) if jira else ({}, {})
    prlist = json.loads(prs) if prs else []
    if prd:
        sec_keys, sec = set(), None
        for line in prd.splitlines():
            if line.startswith("#"):
                sec_keys = set(KEY.findall(line))
            dm = re.search(r"depends on:\s*(.+)", line, re.I)
            if dm:
                for f in feats.values():
                    if f["keys"] & sec_keys:
                        f["deps"] |= {t.strip() for t in dm.group(1).split(",")}
    findings = []
    print("| Feature | Reported | 1 PRD | 2 Subtasks | 3 PR | 4 Tested | 5 Prod | 6 Defects | 7 Exercised | 8 Notified |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, f in feats.items():
        keys = set(f["keys"])
        for k in list(keys): keys |= {c["Issue key"] for c in children.get(k, [])}
        ev = []
        # 2 subtasks
        open_sub = [k for k in keys if by_key.get(k) and by_key[k]["Status"].lower() not in DONE
                    and by_key[k].get("Issue Type","").lower() not in BUG_TYPES | {"epic"}]
        l2 = "✖" if open_sub else ("✔" if keys and by_key else "?")
        if open_sub: ev.append("open tickets " + ", ".join(open_sub))
        # 3 PRs
        rel = [p for p in prlist if any(k in (p.get("title","")+p.get("body","")) for k in keys)]
        unmerged = [p for p in rel if p.get("state","").upper() != "MERGED" or p.get("isDraft")]
        l3 = "✖" if unmerged else ("✔" if rel else "?")
        if unmerged: ev.append("unmerged PR " + ", ".join(f"#{p['number']}" for p in unmerged))
        # 4 tested: any QA/test ticket done, or 'tested'/'qa passed' in slack
        tested = any(("qa" in by_key[k]["Summary"].lower() or "test" in by_key[k]["Summary"].lower())
                     and by_key[k]["Status"].lower() in DONE for k in keys if k in by_key)
        if slack and any(k in line and re.search(r"qa passed|tested|test pass", line, re.I) for line in slack.splitlines() for k in keys): tested = True
        l4 = "✔" if tested else "?"
        # 5 prod
        l5 = "?"
        if deploys:
            hit = any(k in line for line in deploys.splitlines() for k in keys)
            l5 = "✔" if hit else "✖" if f["reported"].lower() == "done" else "?"
        elif slack and any(k in line and re.search(r"deployed|shipped to prod|released", line, re.I) for line in slack.splitlines() for k in keys):
            l5 = "✔"
        elif f["reported"].lower() == "done": l5 = "✖"; ev.append("no deploy evidence")
        # 6 defects
        open_bugs = [k for k in keys if k in by_key and by_key[k].get("Issue Type","").lower() in BUG_TYPES
                     and by_key[k]["Status"].lower() not in DONE]
        sev_bugs = [k for k in open_bugs if SEV.search(by_key[k].get("Priority","") + by_key[k]["Summary"])]
        l6 = "✖" if sev_bugs else ("✔" if by_key else "?")
        if sev_bugs: ev.append("open Sev-1/2 " + ", ".join(sev_bugs))
        # 8 notified
        l8 = "?"
        if f["deps"]:
            if slack:
                notified = {t for t in f["deps"] if any(t.lower() in line.lower() and any(k in line for k in keys) for line in slack.splitlines())}
                missing = f["deps"] - notified
                l8 = "✖" if missing else "✔"
                if missing: ev.append("no notification to " + ", ".join(sorted(missing)))
        print(f"| {name} | {f['reported']} | manual | {l2} | {l3} | {l4} | {l5} | {l6} | manual | {l8} |")
        if "✖" in (l2, l3, l5, l6, l8):
            first = [i for i, v in zip((2,3,5,6,8), (l2,l3,l5,l6,l8)) if v == "✖"][0]
            findings.append((name, f["reported"], first, ev))
    print("\nLegend: ✔ confirmed · ✖ conflicting · ? unverified · manual = human check\n")
    if findings:
        print("## Findings")
        for name, rep, link, ev in findings:
            print(f"\n**{name} — reported {rep}, chain open at link {link}**\n- Evidence: " + "; ".join(ev))
        print(f"\nNext: run resolve-blocker on {findings[0][0]} to plan the fix.")
    else:
        print("No conflicting rows in machine-checkable links. Manual checks (1, 7) still required.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
