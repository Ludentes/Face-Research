#!/usr/bin/env python3
"""Save a web source durably into the repo, mechanically.

Usage:  python3 -I tools/save_source.py <url> [slug]

Writes, under docs/research/sources/:
  raw/<slug>.<ext>     the bytes as served (curl)
  text/<slug>.txt      extracted clean text (HTML via bs4/stdlib, PDF via pdftotext)
  cards/<slug>.md      metadata card: URL, fetch date, HTTP status, content type, sha256, size
  log.jsonl            one line per fetch attempt, failures included

Prints the text path (or the failure) so the caller can read the text once.
If the slug already exists with status 200, it reuses the saved copy instead of re-fetching.
"""
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "research" / "sources"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def slugify(url: str) -> str:
    s = re.sub(r"^https?://(www\.)?", "", url)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:90]


def html_to_text(raw: bytes) -> tuple[str, str]:
    html = raw.decode("utf-8", errors="replace")
    title = ""
    try:
        from bs4 import BeautifulSoup  # type: ignore

        soup = BeautifulSoup(html, "html.parser")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        for t in soup(["script", "style", "noscript", "svg", "nav", "footer", "header"]):
            t.decompose()
        text = soup.get_text("\n")
    except ImportError:
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
        title = m.group(1).strip() if m else ""
        text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", "\n", text)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    out, blank = [], False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return title, "\n".join(out).strip() + "\n"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    url = sys.argv[1]
    slug = sys.argv[2] if len(sys.argv) > 2 else slugify(url)
    for d in ("raw", "text", "cards"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    card = ROOT / "cards" / f"{slug}.md"
    txt = ROOT / "text" / f"{slug}.txt"
    if card.exists() and txt.exists() and "status: 200" in card.read_text():
        print(f"REUSED {txt}")
        return 0

    tmp = ROOT / "raw" / f"{slug}.part"
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    r = subprocess.run(
        ["curl", "-sSL", "--max-time", "60", "-A", UA, "-o", str(tmp),
         "-w", "%{http_code}\t%{content_type}\t%{url_effective}", url],
        capture_output=True, text=True,
    )
    status, ctype, final = (r.stdout.split("\t") + ["", "", ""])[:3]
    entry: dict[str, object] = {"url": url, "final_url": final, "slug": slug, "fetched": now,
             "status": status, "content_type": ctype}
    if r.returncode != 0 or not tmp.exists() or status != "200":
        entry["error"] = (r.stderr or f"HTTP {status}").strip()[:300]
        tmp.unlink(missing_ok=True)
        with open(ROOT / "log.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"FAILED {url}: {entry['error']}")
        return 1

    raw = tmp.read_bytes()
    is_pdf = "pdf" in ctype or raw[:4] == b"%PDF"
    ext = "pdf" if is_pdf else ("json" if "json" in ctype else "html")
    rawp = ROOT / "raw" / f"{slug}.{ext}"
    tmp.rename(rawp)
    if is_pdf:
        subprocess.run(["pdftotext", "-layout", str(rawp), str(txt)], check=False)
        title = ""
    elif ext == "json":
        title, _ = "", txt.write_text(raw.decode("utf-8", errors="replace"))
    else:
        title, text = html_to_text(raw)
        txt.write_text(text)
    sha = hashlib.sha256(raw).hexdigest()
    entry.update({"sha256": sha, "bytes": len(raw), "raw": str(rawp.relative_to(ROOT)),
                  "title": title})
    card.write_text(
        f"---\nslug: {slug}\nurl: {url}\nfinal_url: {final}\ntitle: {json.dumps(title)}\n"
        f"fetched: {now}\nstatus: {status}\ncontent_type: {ctype}\nsha256: {sha}\n"
        f"bytes: {len(raw)}\nraw: raw/{rawp.name}\ntext: text/{txt.name}\n---\n"
    )
    with open(ROOT / "log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"SAVED {txt} ({len(raw)} bytes, {title[:80]!r})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
