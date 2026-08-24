#!/usr/bin/env python3
"""Declared vs observed dependencies. usage: reconcile_deps.py <dir>"""
import os, re, sys, json, csv
from collections import defaultdict
KEY = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
PHRASE = re.compile(r"depend|blocked on|waiting on|needs? .{0,30} from|can'?t test until|who owns|does anyone know|before (?:she|he|they) left", re.I)

def load(d, n):
    p = os.path.join(d, n); return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def main(d):
    prd = load(d, "prd.md") or ""; status = load(d, "status.md") or ""
    jira = list(csv.DictReader((load(d, "jira.csv") or "").splitlines()))
    prs = json.loads(load(d, "prs.json") or "[]"); slack = (load(d, "slack.txt") or "").splitlines()
    departed = {l.split()[0].lower(): (l.split()+[""])[1] for l in (load(d, "departed.txt") or "").splitlines() if l.strip()}
    # features: epic key -> name; from PRD headings
    feats = {}
    for line in prd.splitlines():
        h = re.match(r"^#\s*PRD\s*—\s*(.+?)\s*\((.+?)\)", line)
        if h: feats[h.group(2)] = h.group(1)
    if not feats:
        for line in status.splitlines():
            h = re.match(r"^##+\s*(.+)$", line)
            if h: cur = h.group(1)
            for k in KEY.findall(line): feats.setdefault(k, cur)
    children = defaultdict(set); by_key = {}
    for r in jira:
        by_key[r["Issue key"]] = r
        if r.get("Parent"): children[r["Parent"]].add(r["Issue key"])
    keys_of = {e: {e} | children[e] for e in feats}
    def feat_of(k): return next((e for e, ks in keys_of.items() if k in ks), None)
    # declared
    declared = defaultdict(set); sec = None
    for line in prd.splitlines():
        h = re.match(r"^#\s*PRD.*\((.+?)\)", line)
        if h: sec = h.group(1)
        dm = re.search(r"depends on:\s*(.+)", line, re.I)
        if dm and sec: declared[sec] |= {t.strip().lower() for t in dm.group(1).split(",")}
    # observed
    observed = defaultdict(lambda: defaultdict(list))   # feat -> dep -> evidence
    def note(e, dep, ev): observed[e][dep].append(ev)
    texts = [("slack", l) for l in slack] + [("pr #%s" % p["number"], p.get("title","") + " " + p.get("body","")) for p in prs]
    weak = defaultdict(lambda: defaultdict(list))
    for src, t in texts:
        ks = KEY.findall(t); kset = set(ks); feats_here = [feat_of(k) for k in ks]
        uniq = [f for i, f in enumerate(feats_here) if f and f not in feats_here[:i]]
        is_deploy = re.search(r"#releases|deployed|deploy ", t, re.I) is not None
        phrased = PHRASE.search(t) is not None
        if len(uniq) > 1:
            if phrased:      # directional: first feature mentioned depends on the rest
                for o in uniq[1:]: note(uniq[0], f"{feats[o]} ({o})", f"{src}: {t.strip()[:110]}")
            elif not is_deploy:
                for e in uniq:
                    for o in uniq:
                        if o != e: weak[e][f"{feats[o]} ({o})"].append(f"{src}: {t.strip()[:110]}")
        for e in uniq:
            for team in re.findall(r"\b([a-z]+-team)\b", t.lower()):
                (note if phrased else weak)(e, team, f"{src}: {t.strip()[:110]}") if phrased else weak[e][team].append(f"{src}: {t.strip()[:110]}")
    # team-channel mentions
    for l in slack:
        m = re.search(r"#([a-z-]+)", l); ks = set(KEY.findall(l))
        for k in ks:
            e = feat_of(k)
            if e and m and m.group(1).endswith("-team"): note(e, m.group(1), f"slack channel #{m.group(1)}: {l.strip()[:110]}")
    # owner gone
    gaps = []
    for e, ks in keys_of.items():
        for k in ks:
            a = by_key.get(k, {}).get("Assignee", "").lower()
            if a in departed: gaps.append((feats[e], k, by_key[k]["Summary"], a, departed[a]))
    asks = [l for l in slack if re.search(r"who owns|does anyone know|before (she|he|they) left", l, re.I)]
    # table
    print("| Feature | Dependency | Declared | Observed | Status | Evidence |\n|---|---|---|---|---|---|")
    phantoms = []
    for e, name in feats.items():
        deps = set(declared[e]) | set(observed[e].keys()) | set(weak[e].keys())
        for dep in sorted(deps):
            dec = dep in declared[e]
            obs = observed[e].get(dep, []); wk = weak[e].get(dep, [])
            strong = bool(obs)
            if dec and (obs or wk): st = "✔"
            elif dec: st = "?"
            elif obs: st = "✖"
            else: st = "note"
            obs = obs or wk
            if st == "✖": phantoms.append((name, dep, obs[0]))
            ev = obs[0] if obs else "no ticket/PR/message references " + dep
            print(f"| {name} | {dep} | {'y' if dec else 'n'} | {'y (strong)' if strong else ('y (medium)' if obs else 'n')} | {st} | {ev} |")
    print("\n**Phantom dependencies (observed, not declared)**")
    for n, dep, ev in phantoms: print(f"- {n} → {dep} — {ev}")
    if not phantoms: print("- none found by script; check slack.txt for phrase-only signals")
    print("\n**Knowledge gaps**")
    for f, k, s, a, dt in gaps: print(f"- {f}: {k} ({s}) — assignee {a} departed {dt}")
    for l in asks: print(f"- ownership question: {l.strip()}")
    if not gaps and not asks: print("- none")
    if phantoms:
        top = next((n for n, dep, ev in phantoms if any(g[0] == n or dep.startswith(g[0]) for g in gaps)), phantoms[0][0])
        print(f"\nNext: run resolve-blocker on {top} to plan the fix.")

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else ".")
