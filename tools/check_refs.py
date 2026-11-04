#!/usr/bin/env python3
"""Check a chapter's [N] citations against its References list and saved-source slugs.
Usage: python3 -I tools/check_refs.py <chapter.md> [first_ref_number]"""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
p = pathlib.Path(sys.argv[1]); first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
s = p.read_text(); body, _, refs = s.partition("\n## References")
cited = {int(n) for grp in re.findall(r"\[(\d+(?:\]\[\d+)*)\]", body) for n in grp.split("][")}
defined = {int(n) for n in re.findall(r"^\[(\d+)\]", refs, re.M)}
cited = {c for c in cited if c >= first}; defined = {d for d in defined if d >= first}
print("cited-not-defined:", sorted(cited - defined)); print("defined-not-cited:", sorted(defined - cited))
missing = []
for slug in re.findall(r"Saved: (.*)", refs):
    for t in re.findall(r"`([^`]+)`", slug):
        f = root / "docs/research/sources/text" / f"{t}.txt"
        g = root / "docs/research/agents/duix-realtime" / t
        if not (f.exists() or g.exists()): missing.append(t)
print("missing-saved:", missing)
