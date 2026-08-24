#!/usr/bin/env python3
"""First-pass Done Chain table from exported files. Deterministic, shallow, offline.

usage: python reconcile.py <dir> [--sprint-days 14]   (formats: references/input-modes.md)
Cells: ✔ confirmed · ✖ conflicting · ? unverified · ○ in progress (expected for non-Done) · – n/a · manual
"""
import csv, json, os, re, sys
from collections import defaultdict
from datetime import datetime, timezone

KEY = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
DONE = {"done", "closed", "resolved", "released"}
BUG_TYPES = {"bug", "defect"}
SEV = re.compile(r"(sev|p)-?\s?([12])\b", re.I)
NOW = datetime.now(timezone.utc)

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
    return feats

def parse_jira(text):
    rows = list(csv.DictReader(text.splitlines()))
    by_key = {r["Issue key"]: r for r in rows}
    children = defaultdict(list)
    for r in rows:
        if r.get("Parent"): children[r["Parent"]].append(r)
    return by_key, children

def age_days(iso):
    try: return (NOW - datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    except Exception: return None

def main(d, sprint_days=14):
    status = load(d, "status.md"); jira = load(d, "jira.csv"); prs = load(d, "prs.json")
    slack = load(d, "slack.txt"); prd = load(d, "prd.md"); deploys = load(d, "deploys.txt")
    if not status: sys.exit("status.md required for first pass")
    feats = parse_status(status)
    by_key, children = parse_jira(jira) if jira else ({}, {})
    prlist = json.loads(prs) if prs else []
    slack_lines = slack.splitlines() if slack else []
    deploy_lines = deploys.splitlines() if deploys else []
    if prd:
        sec_keys = set()
        for line in prd.splitlines():
            if line.startswith("#"): sec_keys = set(KEY.findall(line))
            dm = re.search(r"depends on:\s*(.+)", line, re.I)
            if dm:
                for f in feats.values():
                    if f["keys"] & sec_keys: f["deps"] |= {t.strip() for t in dm.group(1).split(",")}
    findings, notes, undeclared = [], [], []
    print("| Feature | Reported | 1 PRD | 2 Subtasks | 3 PR | 4 Tested | 5 Prod | 6 Defects | 7 Exercised | 8 Notified |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, f in feats.items():
        keys = set(f["keys"])
        for k in list(keys): keys |= {c["Issue key"] for c in children.get(k, [])}
        is_done = f["reported"].lower() == "done"
        ev, stale = [], False
        def has(k, line): return k in line
        # 2 subtasks
        open_sub = [k for k in keys if by_key.get(k) and by_key[k]["Status"].lower() not in DONE
                    and by_key[k].get("Issue Type","").lower() not in BUG_TYPES | {"epic"}]
        wont = [k for k in keys if by_key.get(k) and by_key[k].get("Resolution","").lower().replace("'", "") in {"wont do", "won't do", "cancelled", "canceled"}]
        if wont: notes.append(f"{name}: {', '.join(wont)} resolved Won't Do — scope cut; confirm the status doc says so")
        if open_sub:
            if is_done: l2 = "✖"; ev.append("open tickets " + ", ".join(open_sub))
            else: l2 = "○"
        else: l2 = "✔" if keys and by_key else "?"
        # 3 PRs
        rel = [p for p in prlist if any(has(k, p.get("title","") + p.get("body","")) for k in keys)]
        reverts = [p for p in rel if p.get("title","").lower().startswith("revert") and p.get("state","").upper() == "MERGED"]
        real = [p for p in rel if p not in reverts]
        unmerged = [p for p in real if p.get("state","").upper() != "MERGED" or p.get("isDraft")]
        offbranch = [p for p in real if p.get("state","").upper() == "MERGED" and p.get("baseRefName") not in ("main", "master", "develop", "release")]
        if reverts: l3 = "✖"; ev.append("reverted by " + ", ".join(f"#{p['number']}" for p in reverts))
        elif offbranch: l3 = "✖"; ev.append("merged to non-main branch " + ", ".join(f"#{p['number']}→{p['baseRefName']}" for p in offbranch))
        elif unmerged:
            old = [p for p in unmerged if (age_days(p.get("createdAt","")) or 0) > sprint_days]
            if is_done: l3 = "✖"; ev.append("unmerged PR " + ", ".join(f"#{p['number']}" for p in unmerged))
            elif old: l3 = "✖"; stale = True; ev.append("PR open > sprint: " + ", ".join(f"#{p['number']} ({age_days(p['createdAt'])}d)" for p in old))
            else: l3 = "○"
        else: l3 = "✔" if rel else "?"
        # 4 tested
        tested = any(re.search(r"\bqa\b|test", by_key[k]["Summary"], re.I) and by_key[k]["Status"].lower() in DONE for k in keys if k in by_key)
        if any(any(k in line for k in keys) and re.search(r"qa passed|tested|test pass", line, re.I) for line in slack_lines): tested = True
        l4 = "✔" if tested else "?"
        # 5 prod
        dep_hits = [line for line in deploy_lines if any(k in line for k in keys)]
        rev_hits = [line for line in dep_hits if "revert" in line.lower()]
        slack_dep = any(any(k in line for k in keys) and re.search(r"deployed|shipped to prod|released", line, re.I) and "revert" not in line.lower() for line in slack_lines)
        if rev_hits: l5 = "✖"; ev.append("deploy reverted " + rev_hits[-1].split()[1])
        elif dep_hits or slack_dep: l5 = "✔"
        elif is_done: l5 = "✖"; ev.append("no deploy evidence")
        else: l5 = "?"
        # 6 defects
        open_bugs = [k for k in keys if k in by_key and by_key[k].get("Issue Type","").lower() in BUG_TYPES and by_key[k]["Status"].lower() not in DONE]
        sev_bugs = [k for k in open_bugs if SEV.search(by_key[k].get("Priority","") + by_key[k]["Summary"])]
        minor = [k for k in open_bugs if k not in sev_bugs]
        if sev_bugs: l6 = "✖"; ev.append("open Sev-1/2 " + ", ".join(sev_bugs))
        else: l6 = "✔" if by_key else "?"
        if minor: notes.append(f"{name}: open Sev-3+ {', '.join(minor)} (note, not a conflict)")
        # 8 notified — only meaningful once deployed
        deployed = l5 == "✔"
        if f["deps"] and deployed:
            notified = {t for t in f["deps"] if any(t.lower() in line.lower() and any(k in line for k in keys) for line in slack_lines)}
            missing = f["deps"] - notified
            if slack_lines: l8 = "✖" if missing else "✔"
            else: l8 = "?"
            if missing and slack_lines: ev.append("no notification to " + ", ".join(sorted(missing)))
        elif f["deps"]: l8 = "–"
        else: l8 = "?"
        # undeclared dependencies: slack lines mentioning this feature + 'depend'/'blocked on' + a key outside this feature
        for line in slack_lines:
            if any(k in line for k in keys) and re.search(r"depend|blocked on", line, re.I):
                others = set(KEY.findall(line)) - keys
                if others and line.strip() not in {u.split(": ",1)[1] for u in undeclared}:
                    undeclared.append(f"{name} → {', '.join(sorted(others))}: {line.strip()}")
        print(f"| {name} | {f['reported']} | manual | {l2} | {l3} | {l4} | {l5} | {l6} | manual | {l8} |")
        conflict_links = [i for i, v in zip((2,3,5,6,8), (l2,l3,l5,l6,l8)) if v == "✖"]
        if conflict_links: findings.append((name, f["reported"], conflict_links[0], ev, stale, len(conflict_links) + (2 if sev_bugs else 0) + (1 if is_done else 0)))
        elif f["reported"].lower() in ("at risk", "blocked") and all(v == "✔" for v in (l2,l3,l4,l5,l6)):
            findings.append((name, f["reported"], None, ["all machine-checkable links confirmed — reported status is more pessimistic than the tools; confirm what the risk actually is"], False, 0))
    print("\nLegend: ✔ confirmed · ✖ conflicting · ? unverified · ○ in progress (expected) · – n/a until deployed · manual = human check\n")
    if findings:
        print("## Findings")
        for name, rep, link, ev, stale, _ in findings:
            head = f"reported {rep}, chain open at link {link}" if link else f"reported {rep}, chain complete"
            if stale: head += " (stalled beyond sprint)"
            print(f"\n**{name} — {head}**\n- Evidence: " + "; ".join(ev))
    if undeclared:
        print("\n## Undeclared dependencies (feed reconcile-dependencies)")
        for u in undeclared: print(f"- {u}")
    if notes:
        print("\n## Notes")
        for n in notes: print(f"- {n}")
    ranked = sorted((x for x in findings if x[2]), key=lambda x: -x[5])
    first = ranked[0][0] if ranked else None
    if first: print(f"\nNext: run resolve-blocker on {first} to plan the fix.")
    elif not findings: print("\nNo conflicting rows in machine-checkable links. Manual checks (1, 7) still required.")

if __name__ == "__main__":
    args = sys.argv[1:]
    sd = 14
    if "--sprint-days" in args:
        i = args.index("--sprint-days"); sd = int(args[i+1]); del args[i:i+2]
    main(args[0] if args else ".", sd)
