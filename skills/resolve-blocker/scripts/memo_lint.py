#!/usr/bin/env python3
"""Leader mode: lint an escalation memo. usage: memo_lint.py memo.md"""
import re, sys
CHECKS = [
 ("blocker with evidence", r"(blocker|problem)[^\n]*\n?[^\n]*([A-Z]{2,}-\d+|#\d+|\d{4}-\d{2}-\d{2})", True),
 ("blocker type named", r"type:\s*(decision|dependency|resource|information|alignment|priority|environment)", True),
 ("2-3 options", None, True),
 ("pros and cons per option", r"\bpros\b.*\bcons\b", True),
 ("reversibility tagged", r"(two-way|one-way)", True),
 ("data or estimate labeled", r"(estimate|data|basis)", True),
 ("cost of delay per week", r"cost of delay[^\n]*week", True),
 ("pre-wired stakeholders", r"pre-wired", True),
 ("recommendation or explicit balanced call", r"(recommendation|balanced)", True),
 ("the ask", r"\bask\b", True),
 ("deadline", r"by \w+ ?\d|by \d{4}-\d{2}-\d{2}", True),
 ("default if no decision", r"default", True),
 ("under one page (~450 words)", None, False),
]
def main(p):
    t = open(p, encoding="utf-8").read(); low = t.lower(); fails = []
    for name, rx, hard in CHECKS:
        if name == "2-3 options": ok = 2 <= len(re.findall(r"option [a-c]\b", low)) // 1 and len(set(re.findall(r"option ([a-c])\b", low))) in (2, 3)
        elif name.startswith("under one page"): ok = len(t.split()) <= 450
        else: ok = re.search(rx, low, re.S) is not None
        print(("PASS " if ok else "FAIL ") + name)
        if not ok: fails.append((name, hard))
    sendback = [n for n, h in fails if n in ("the ask", "deadline", "default if no decision")]
    if sendback: print("\nVerdict: SEND BACK — missing " + ", ".join(sendback))
    elif fails: print("\nVerdict: DECIDE, note gaps: " + ", ".join(n for n, _ in fails))
    else: print("\nVerdict: DECIDE NOW — memo complete")
if __name__ == "__main__": main(sys.argv[1])
