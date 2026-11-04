#!/bin/bash
# Scratch helper (oss-avatar agent): print title, abstract and submission history from saved arXiv abs text files.
for f in "$@"; do echo "=== $f"; awk '/^Title:/{p=1} /^\[Submitted/{print} /^Abstract:/{a=1} a{print} /^Comments:|^Subjects:/{a=0} /^Submission history/{s=1} s&&n<8{print;n++}' "$f" | grep -v '^\s*$' | head -40; done
