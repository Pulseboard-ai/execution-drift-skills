#!/usr/bin/env python3
"""Search the precedent log. Offline.
usage: precedent_search.py --type dependency [--keywords tax api] [--dir resolutions] [--n 3]
"""
import argparse, glob, os, re

def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
    if not m: return None
    fm, body = m.groups()
    meta = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1); v = v.strip()
            if v.startswith("["): v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
            meta[k.strip()] = v
    meta["path"] = path; meta["body"] = body
    return meta

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True); ap.add_argument("--keywords", nargs="*", default=[])
    ap.add_argument("--dir", default=os.path.join(os.path.dirname(__file__), "..", "resolutions"))
    ap.add_argument("--n", type=int, default=3)
    a = ap.parse_args()
    cases = [c for c in (parse(p) for p in glob.glob(os.path.join(a.dir, "**", "*.md"), recursive=True)) if c and "type" in c]
    if not cases: print("Precedent log empty. Continue without precedent; log this case when resolved."); return
    kw = {k.lower() for k in a.keywords}
    def score(c):
        t = 2 if c.get("type") == a.type else (1 if c.get("secondary") == a.type else 0)
        k = len(kw & {x.lower() for x in (c.get("keywords") or [])}) + sum(1 for w in kw if w in c["body"].lower())
        return (t, k, c.get("date", ""))
    ranked = sorted(cases, key=score, reverse=True)
    ranked = [c for c in ranked if score(c)[0] > 0][: a.n]
    if not ranked: print(f"No precedent of type '{a.type}'. Continue without precedent."); return
    for c in ranked:
        print(f"## {os.path.basename(c['path'])}  (type={c.get('type')}, {c.get('date')})")
        for key in ("Blocker", "Chosen", "Why", "Escalated", "Time to resolve", "Outcome"):
            mm = re.search(rf"^{key}:\s*(.+)$", c["body"], re.M)
            if mm: print(f"- {key}: {mm.group(1)}")
        print()

if __name__ == "__main__": main()
