---
status: current
last-verified: 2026-11-04
owner: Face-Research maintainers
---

# Verifying Chapter 13 and the November 2026 avatar-product update

A step-by-step guide for checking the avatar-product material (Chapter 13, plus the related edits to Chapters 06, 10, 11 and 14 and the README) before relying on it or sharing it. No coding is needed beyond copy-pasting the commands. Run everything from the repository root.

## What changed

- New `13-avatar-product-world.md`. Conclusions moved from `13-conclusions.md` to `14-conclusions.md`.
- `06-talking-heads.md`: new section *Open-Weight Presenter Models, Mid-2025 to Late 2026*, plus "Update, November 2026" notes in *What Still Does Not Exist*.
- `10-decision-trees.md`:
  - Use Case 3: build-or-buy, latency note, open-source stack, revised 500 ms target.
  - Use Case 4: InfiniteTalk.
- `11-market-and-community.md`: updated *Key players*; per-minute pricing in *Where the money flows*.
- `14-conclusions.md`: two update notes.
- `README.md` and `00-introduction.md`: chapter index, chapter map, new curated links.
- Research archive in `docs/research/`:
  - `sources/`: saved pages.
  - `agents/`: dossiers and the audit.
- Tools in `tools/`.

## Happy path: the references hold together

1. Check every citation in the new chapter resolves and every saved source exists:

   ```bash
   python3 -I tools/check_refs.py 13-avatar-product-world.md
   python3 -I tools/check_refs.py 06-talking-heads.md 27
   python3 -I tools/check_refs.py 11-market-and-community.md 5
   ```

   **Expected:**
   - Chapter 13 prints `cited-not-defined: []`, `defined-not-cited: [21, 84]` and `missing-saved: []`. References 21 and 84 are deliberately marked "removed during audit".
   - The other two commands print three empty lists.

2. Check no stale link to the old Conclusions file remains:

   ```bash
   grep -rn "13-conclusions" --include=*.md . | grep -v docs/research
   ```

   **Expected:** no output.

3. Open `README.md` on GitHub or in a Markdown viewer. Confirm:
   - the chapter table lists 13 *The Avatar Product World* and 14 *Conclusions*;
   - both links open the right files;
   - the new *Avatar Products* link group appears above *Proprietary / Enterprise*.

## Spot-check claims against the saved sources

Every reference in Chapter 13 ends with `Saved: <slug>`. The saved text is in `docs/research/sources/text/<slug>.txt`; the raw page and a metadata card (URL, fetch date, HTTP status, checksum) are alongside in `raw/` and `cards/`.

4. **HeyGen Avatar V figures** (reference [1]):

   ```bash
   grep -n "8.97\|0.840\|5,000\|24 steps\|22.2%" docs/research/sources/text/heygen-avatarv-tech-report.txt | head
   ```

   **Expected:** lines with the Sync-C/face-similarity table, the GPU fleet, the step count and the Turing-test rate.

5. **The two Anam latency studies** (reference [10]):

   ```bash
   grep -n "1.24\|2.12\|2.20\|same speech-to-text" docs/research/sources/text/anam-ai-tools-latency-benchmark.txt | head
   ```

   **Expected:** both the default-pipeline medians (1.24 s …) and the shared-pipeline medians (2.12 s, 2.20 s …).

6. **Duix licence contradiction** (references [39]–[41]):

   ```bash
   grep -n "100,000 users" docs/research/sources/text/raw-githubusercontent-com-duixcom-duix-avatar-main-readme-md.txt
   grep -n "Monthly Active Users" docs/research/sources/text/duix-avatar-LICENSE.txt | head -3
   grep -n "Non-Commercial" docs/research/sources/text/duix-avatar-model-community-licence-pdf.txt | head -3
   ```

   **Expected:** three different commercial-use terms.

7. **Independent benchmark numbers** (reference [64]):

   ```bash
   grep -n "204.64\|48.77\|331.93" docs/research/sources/text/tight-benchmark-report.txt
   ```

8. **Wan open weights are Apache-2.0** (reference [61]):

   ```bash
   grep -o '"license:[^"]*"' docs/research/sources/text/hf-api-wan-ai-models-list.txt | sort | uniq -c
   ```

   **Expected:** only `license:apache-2.0`.

## Edge cases worth checking by eye

9. **Vendor-claim labelling.** Read *Live Conversational Avatars* in Chapter 13. Every latency figure should either say "vendor", "Anam-run" or "own benchmark", or come from the shared-pipeline study. Any bare number is a bug.
10. **Name collision.** Search Chapter 13 for `LiveAvatar`. Each use should say either "HeyGen LiveAvatar" (HeyGen's live product) or "Quark LiveAvatar" (Alibaba's open model). Exception: the HeyGen engine table row and the Wan-section design paragraph, where the context is HeyGen's product.
11. **Hedges carried across chapters.** Compare these statements in Chapters 10, 11 and 13; each should be scoped to "found":
    - D-ID self-hosting;
    - the 500 ms target;
    - Duix's licence;
    - Simli as the 3DGS vendor.
12. **Failed fetches are recorded, not hidden:**

    ```bash
    grep -c '"error"' docs/research/sources/log.jsonl
    grep '"error"' docs/research/sources/log.jsonl | head -5
    ```

    **Expected:** a count of about 24, with 403/404/429 errors listed.

## Round trip: re-fetch a source and compare

13. Re-save one source under a new slug, and compare checksums with the stored card:

    ```bash
    python3 -I tools/save_source.py https://www.simli.com/pricing simli-pricing-recheck
    grep sha256 docs/research/sources/cards/simli-com-pricing.md docs/research/sources/cards/simli-pricing-recheck.md
    diff <(grep -i "per min\|\$0" docs/research/sources/text/simli-com-pricing.txt) <(grep -i "per min\|\$0" docs/research/sources/text/simli-pricing-recheck.txt)
    ```

    **Expected:** the checksums may differ, since pages change. The price lines should match. If prices changed, update the Chapter 13 table and record the date. Delete the recheck files afterwards if nothing changed.

14. Re-saving an existing slug reuses it rather than overwriting:

    ```bash
    python3 -I tools/save_source.py https://www.simli.com/pricing simli-com-pricing
    ```

    **Expected:** `REUSED …`.

## Where the audit lives

- `docs/research/agents/audit/ch13-adversarial-review.md`: claim-by-claim critique of the draft.
- `docs/research/agents/audit/ch13-citation-check.md`: per-reference check against the saved sources.
- `docs/research/agents/audit/ch13-remediation.md`: what was fixed and what was deferred.
