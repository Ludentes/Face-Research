---
status: done
last-verified: 2026-11-04
owner: main session
---

# Ch13 audit: remediation record

Inputs: `ch13-adversarial-review.md` (26 claims rated: 3 solid, 8 soft, 11 overstated, 1 understated, 3 circular) and `ch13-citation-check.md` (Ch13: 46 faithful, 10 generous, 10 misattributed, 3 overreach, 6 unverifiable). Draft commit e634645; the fixes are in the following commit. The main session checked the reviewers' key evidence against the saved sources before acting on it.

## Fixed

- **Anam benchmark cited selectively.** Both studies are now reported, including the shared-pipeline study (2.12–2.70 s, Synthesia 2.20 s), plus LemonSlice's self-reported 2.04 s and its counter-claim.
- **Cost inference contradicted the chapter (LemonSlice 20B).** Narrowed to "Simli's price is hard to reconcile…; Anam's and Tavus's are not". Added the caveat that price is not cost. Cold-run dollar figures are labelled as upper bounds.
- **Tavus classified as 3DGS on the phrase "Gaussian diffusion".** Now undisclosed; Simli is the only self-described splat vendor (Ch13, Ch10, Ch14 note).
- **Reference design "mirrors what vendors do".** Recast as this review's proposal; HeyGen LiveAvatar described as consistent but undisclosed; cross-mode quality risk added.
- **Ch10/Ch14 contradictions.**
  - Ch10's 500 ms target is amended openly.
  - "Pure diffusion cannot hit real time" is updated.
  - SadTalker gets a 2026 note.
  - Ch14 claim 4 and prediction 5 get update notes.
- **Taxonomies presented as exhaustive.** Two shapes became "most products" plus broadcast. Identity regimes gained the synthetic-identity regime and the hybrid case. Face-model families went from two to four (warping/motion+renderer and rendered 3D heads added). Live-vendor families are labelled as our own construction from a few disclosures.
- **"Moved decisively" / "commercial leader" / "gap collapsed".** Scoped to what is disclosed; the conclusion is now "the recipe converged; whether quality has is unmeasured".
- **"Only D-ID self-hosted" / "nobody near 500 ms" / "no vendor states".** All now carry "found"/"measured" scoping. Hedra per-engagement and Avaturn's open source are added, and D-ID's self-hosted licence is noted as including streaming minutes. The data-residency claim about Chinese vendors is removed.
- **DINet corroboration was circular.** The text now says one decompile, with weights from the second extraction, plus the weight filename. The bullet lead is hedged ("reportedly"), and the DINet paper (AAAI 2023) is now cited.
- **Duix licences.** Added the model-version scope, the output carve-out and PRC law; Ch10 now says the licences are contradictory.
- **"Licensing is not the blocker".** Scoped to the Wan generator tier; HunyuanVideo-Avatar's EU/UK/South Korea exclusion added.
- **Tight table.** Added FlashTalk, warm-chunk times and the benchmark's limits; EchoMimic's 12 GB phrased as the project's advertised mode.
- **"LiveAvatar" name collision.** Disambiguated as "HeyGen LiveAvatar" vs "Quark LiveAvatar".
- **Scope gap.** Added a Scope paragraph and an open question naming the Chinese commercial vendors not covered. The "Chinese ecosystem" generalisation is limited to the two projects examined.
- **Citation fixes:**
  - HeyGen dates (research page 2026-04-08; roundup 2026-05-06); Avatar III pricing; "phone" recording; unsourced Avatar IV/Phoenix-4/Omnia/Character-3/duix-skills dates dropped.
  - Tavus prices re-cited to the third-party summary; Ch11 $0.35 re-cited.
  - Moved citations: Duix 200 ms → `duix-com`; 1.21 s and 32 fps → arXiv copies; 512² → Tight; LiteAvatar training → issues 3/24; LongCat MIT → HF metadata; Duix-Mobile 1.5 s → repo JSON; repo stats → gh JSON.
  - Removed unsupported details: "54 participants", Cara-4.1 "diffusion-based", Fay back-ends, bitHuman "CPU-only Linux", the "fake open source" quotation.
  - Kandinsky "MIT" scoped to code; MuseTalk dependency-licence caveat added; Ch06 OmniAvatar/StableAvatar/FlashHead licence sources added.
  - Ch06 audio-encoder sentence corrected (Qwen-Omni); OmniHuman 1.5 and Wan API-only now cited.
  - Ch11 hedges restored ("leads" removed, the 32.2% claim scoped, "many" instead of "most").
- **Ch10 Use Case 4 InfiniteTalk.** Speed now stated as unmeasured; the I2V-only scope of the one-minute caveat is noted; the head-motion re-synthesis trade-off is flagged.
- **Ch10 buy-side risk.** Vendor failure, SDK paywall and price changes added.

## Deferred (not fixed)

- No survey of the Chinese commercial digital-human vendors (Tencent, Baidu, iFlytek, SenseTime, ByteDance) or livestream commerce. Listed in the chapter's Scope and Open Questions.
- No research on regional hosting / data residency for the cloud vendors.
- No measured warm-server speed for InfiniteTalk or the distilled Wan models. This would need a spike on real hardware.
- No quality comparison of commercial vs open output.
- Ditto is named in the face-model families but not added to the open-stack tier table.
- Refs [21] and [84] are kept as "removed during audit" markers so the reference numbers stay stable.
