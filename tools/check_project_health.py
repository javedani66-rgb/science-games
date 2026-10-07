#!/usr/bin/env python3
"""Project health audit for science-games (read-only, stdlib only).

Run from the repo root:  python3 tools/check_project_health.py
Exit code 1 if any HARD check fails. WARN items never fail the run.

Checks
  1. every commit SHA cited in docs/*.md and *.md exists in this repo
  2. first-visit download size (files listed in sw.js) vs budget
  3. external hosts referenced by shipped files (offline / no-CDN principle)
  4. license files present (LICENSE, font licenses)
  5. a STATE.md exists and is not older than the newest handoff
"""
import os, re, subprocess, sys, glob, gzip

ROOT = os.getcwd()
BUDGET_FIRST_VISIT_MB = float(os.environ.get("FIRST_VISIT_BUDGET_MB", "3"))  # proposal, not an owner decision
ALLOWED_HOSTS = ("www.w3.org", "w3.org", "aparat.com", "www.aparat.com",
                 "youtube.com", "www.youtube.com", "youtu.be", "phet.colorado.edu",
                 "github.com", "javedani66-rgb.github.io")
hard, warn = [], []

def git(*a):
    r = subprocess.run(["git", *a], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout.strip()

# 1. cited SHAs ---------------------------------------------------------
sha_re = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{7,40})(?![0-9A-Za-z])")
missing = {}
for path in glob.glob("**/*.md", recursive=True):
    if path.startswith(("node_modules", ".git")):
        continue
    try:
        text = open(path, encoding="utf-8").read()
    except Exception:
        continue
    for m in sha_re.finditer(text):
        s = m.group(1)
        if not (re.search(r"\d", s) and re.search(r"[a-f]", s)):
            continue          # pure digits or pure letters: not a SHA
        if len(s) == 8 and s.isdigit():
            continue
        code, _ = git("cat-file", "-e", s + "^{commit}")
        if code != 0:
            missing.setdefault(s, set()).add(path)
if missing:
    warn.append("SHA cited in docs but absent from this repo (local-only or rewritten history):")
    for s, files in sorted(missing.items()):
        warn.append(f"    {s}  <- {', '.join(sorted(files))[:110]}")

# 2. first-visit size ---------------------------------------------------
def precache_files():
    if not os.path.exists("sw.js"):
        return []
    txt = open("sw.js", encoding="utf-8").read()
    out = []
    for p in re.findall(r"""['"](\./[^'"]*)['"]""", txt):
        p = p[2:] or "index.html"
        if p.endswith("/"):
            p += "index.html"
        out.append(p)
    return out

total = gz_total = 0
for p in precache_files():
    if os.path.isfile(p):
        b = open(p, "rb").read()
        total += len(b)
        gz_total += len(gzip.compress(b, 6))
if total:
    mb, gmb = total / 1e6, gz_total / 1e6
    line = f"first visit: {mb:.2f} MB raw / {gmb:.2f} MB gzip (budget {BUDGET_FIRST_VISIT_MB} MB raw)"
    (hard if mb > BUDGET_FIRST_VISIT_MB else warn).append(line) if mb > BUDGET_FIRST_VISIT_MB else print("OK  ", line)
else:
    warn.append("no sw.js precache list found; first-visit size not measured")

# 3. external hosts in shipped files -----------------------------------
shipped = ["index.html", "sw.js", "manifest.webmanifest"] + glob.glob("physics/**/*.html", recursive=True)
hosts = {}
for p in shipped:
    if os.path.isfile(p):
        t = open(p, encoding="utf-8", errors="ignore").read()
        for h in re.findall(r"https?://([A-Za-z0-9.-]+)", t):
            hosts.setdefault(h.lower(), set()).add(p)
bad = {h: f for h, f in hosts.items() if not h.endswith(ALLOWED_HOSTS)}
if bad:
    hard.append("unexpected external hosts in shipped files (offline principle): " +
                "; ".join(f"{h} in {sorted(f)[0]}" for h, f in bad.items()))
else:
    print("OK   external hosts:", ", ".join(sorted(hosts)) or "none")

# 4. licenses -----------------------------------------------------------
for need, why in [("LICENSE", "code license (owner chose GPL-3.0)"),
                  ("LICENSE-ART-TEXT", "art/text license (owner chose CC-BY-SA 4.0)"),
                  ("CREDITS.md", "credits/sources page")]:
    if not (os.path.exists(need) or glob.glob(need + ".*")):
        warn.append(f"missing {need}: {why}")
if not glob.glob("assets/fonts/*OFL*") and not glob.glob("assets/fonts/LICENSE*"):
    warn.append("no font license text next to assets/fonts")

# 5. state ledger -------------------------------------------------------
if not os.path.exists("docs/STATE.md"):
    warn.append("docs/STATE.md missing (single current-state ledger)")
else:
    _, last_state = git("log", "-1", "--format=%ct", "--", "docs/STATE.md")
    _, last_hand = git("log", "-1", "--format=%ct", "--", "docs/handoffs")
    if last_hand and last_state and int(last_hand) > int(last_state):
        warn.append("docs/STATE.md is older than the newest handoff")

# 6. principles must be reachable from every entry file ------------------
ledger = open("docs/PRINCIPLES.md", encoding="utf-8").read() if os.path.exists("docs/PRINCIPLES.md") else ""
ledger_ids = set(re.findall(r"^\| ([A-Z]\d+) \|", ledger, re.M))
for entry in ("CLAUDE.md", "AGENTS.md", "START_HERE_FA.md"):
    if not os.path.exists(entry):
        hard.append(f"{entry} missing (entry file for AI sessions)")
        continue
    t = open(entry, encoding="utf-8").read()
    if "PRINCIPLES.md" not in t:
        hard.append(f"{entry} does not point to docs/PRINCIPLES.md")
    if entry != "START_HERE_FA.md":
        m = re.search(r"principles-digest:start -->(.*?)<!-- principles-digest:end", t, re.S)
        if not m:
            hard.append(f"{entry} has no principles digest block")
        else:
            ids = set(re.findall(r"\b([A-Z]\d+)\b", m.group(1)))
            gone = sorted(i for i in ids if i not in ledger_ids)
            if gone:
                hard.append(f"{entry} digest cites principle IDs missing from PRINCIPLES.md: {gone}")
            else:
                print(f"OK   {entry} digest ({len(ids)} principle IDs, all in ledger)")

# 7. research references: every R-code cited by a principle must be logged -
refdoc = open("docs/research/DESIGN_EVIDENCE_REFERENCES_FA.md", encoding="utf-8").read() if os.path.exists("docs/research/DESIGN_EVIDENCE_REFERENCES_FA.md") else ""
logged = set(re.findall(r"^\| (R\d+) \|", refdoc, re.M))
cited = set(re.findall(r"\bR(\d+)\b", " ".join(l for l in ledger.splitlines() if re.match(r"\| [A-Z]\d+ \|", l))))
cited = {"R" + c for c in cited}
unlogged = sorted(cited - logged, key=lambda x: int(x[1:]))
if unlogged:
    hard.append(f"principles cite research codes missing from DESIGN_EVIDENCE_REFERENCES_FA.md: {unlogged}")
else:
    print(f"OK   research references: {len(cited)} cited, {len(logged)} logged")

print()
for w in warn:
    print("WARN", w)
for h in hard:
    print("FAIL", h)
print(f"\n{len(hard)} fail, {len(warn)} warn")
sys.exit(1 if hard else 0)
