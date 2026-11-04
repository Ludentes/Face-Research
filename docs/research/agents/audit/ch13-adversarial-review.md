# Adversarial review: Chapter 13 (The Avatar Product World) and the November 2026 additions to Ch06, Ch10 and Ch11

Reviewed 2026-11-04 against commit e634645. I read the chapter in full, the diffs to Ch06, Ch10 and Ch11, all three dossiers, and Ch14's predictions. I tested claims against the saved sources in `docs/research/sources/text/` and did not fetch anything from the web.

## Summary

**Counts (26 claims rated in Pass 1):** 3 SOLID, 8 SOFT, 11 OVERSTATED, 1 UNDERSTATED, 3 CIRCULAR. There are 7 unflagged assumptions in Pass 2. Five cross-chapter contradictions are listed in Pass 3.

**Top 5 fixes:**
1. **The Anam benchmark is cited selectively.** The same saved page (`anam-ai-tools-latency-benchmark`, lines 236–345) contains a second, like-for-like study. In it every vendor ran the same STT, LLM and TTS (Deepgram, GPT OSS 120B on Groq, Cartesia). The medians bunched at 2.12–2.70 s, Synthesia came in at 2.20 s, and Anam's paired advantage over Synthesia was "not established". In the first study competitors ran "their defaults", so the 1.24 s vs 1.82–2.10 s gap there mostly measures pipeline choice, not the avatar. The chapter cites only the flattering study, and its table says "none published" for Synthesia latency even though a figure exists in a source already in hand. Report both studies.
2. **The cost inference contradicts the chapter itself.** "The commercial live vendors are not using 14B video diffusion per stream" (13:152) sits three paragraphs after LemonSlice-2 is described as a 20B real-time video model run per stream (13:70). The chapter's own derived $0.13/stream-min for LiveAct on 2×H100 falls inside Anam's $0.11–0.16 price band, and Tavus's $0.26–0.35 sits between LiveAct and FlashTalk. The arithmetic only rules something out for Simli, and price is not cost anyway. Rewrite it as "Simli's price is incompatible with multi-GPU diffusion per stream; Anam's and Tavus's are not."
3. **The Tavus 3DGS classification rests on an ambiguous phrase.** The saved Tavus docs say only "built on a Gaussian diffusion model" (`docs-tavus-io-sections-models`:14). That is ordinary ML vocabulary for Gaussian-noise diffusion, not 3D Gaussian Splatting. The 3DGS detail comes from a BusinessWire release seen only in search snippets (dossier: "Single-source"). This one phrase now carries a technical family (13:68), a "Chapter 07 prediction arriving" conclusion (13:168), and a Ch10 sentence (10:84). Reclassify Tavus as "undisclosed (possibly 3DGS)", and present Simli as the only self-described splat vendor.
4. **The reference design "mirrors what the vendors appear to do" (13:154–160) fails on the chapter's own evidence.** Every vendor that disclosed its technology (Anam, Simli, Tavus, LemonSlice) uses one-shot generation from a photo, not templates. The only "match" is HeyGen LiveAvatar, whose technology the chapter's own table marks "undisclosed". No vendor is shown to generate template footage with its offline model (step 2). Drop the mirroring claim, or label it a hypothesis based on LiveAvatar's two-minute footage requirement.
5. **Ch10 and Ch14 now contradict Ch13.** In the same Use Case 3, Ch10 still says "Pure diffusion methods … cannot hit real-time latency" (10:95), right next to the new LiveAvatar/FlashTalk recommendation. Ch14 still says diffusion "cannot run in real-time" (14:15) and predicts a photo-to-real-time-3DGS product "within 18 months" (14:74), which Simli already claims to sell. Ch10's latency note recasts the original 500 ms "input to face animation" target as a face-stage target, while Ch13:88 calls the same target a "sub-500 ms turn".

**Overall recommendation:** the chapter is not ready to come out of draft. The vendor-claim labelling is applied well on the surface; on that discipline the chapter does better than most market reviews. The *inferences* drawn from vendor claims are not held to the same standard, though. Three of the four closing conclusions (gap collapsed, 3DGS arriving through vendors, the reference design) each rest on one ambiguous or single-source datum. Fix the five items above and soften the taxonomies before calling it audited.

## Pass 1: claim by claim

**C1.** "Every product in this chapter is one of two shapes." / "There are three regimes" of identity creation (13:13, 13:19).
**OVERSTATED.** The identity regimes are not exhaustive:
- Synthesia Style Avatars, made from a text prompt, are a fourth regime: a synthetic identity from text (commercial dossier, Express-3 section).
- Tavus is a hybrid: a zero-shot preview first, then background tuning (dossier, Tavus).
- HeyGen LiveAvatar's two-minute requirement fits none of the three regimes cleanly.

The "two shapes" also omit broadcast streaming (HeyGen Avatar Realtime API, 24/7 Twitch), which is neither offline nor conversational. **Fix:** "the products surveyed fall mostly into…" and add the text-prompt regime.

**C2.** "Two families of face model sit underneath." (13:25)
**OVERSTATED.** Putting 3DGS renderers in the same "whole-frame generator" family as DiTs is a taxonomic fudge, and several approaches fall outside both families:
- A FLAME- or motion-driven splat head is a rendered head, not a generated frame.
- Motion-plus-warping models (Ditto, LivePortrait-derived pipelines, and probably Anam Cara-3's "motion-to-face renderer") belong to neither family.
- Rigged 3D CG (Soul Machines, UneeQ on NVIDIA ACE/MetaHuman) belongs to neither.

**Fix:** three or four families, with warping and CG rigs named.

**C3.** "In 2025–2026 the commercial leaders moved decisively from the first family to the second" (13:25).
**OVERSTATED.**
- "Moved from" needs evidence of what the prior engines were. None is cited; Avatar III's architecture is undisclosed.
- HeyGen still sells Avatar III ("unlimited on paid plans").
- HeyGen's live product needs two minutes of footage and no 4K "due to latency limitations". The chapter's own reference design (13:160) treats that as template-like.
- "Decisively" holds for the offline flagships only.

**Fix:** "the offline flagships of HeyGen, Synthesia and D-ID now describe diffusion or DiT renderers; their live products are mostly undisclosed."

**C4.** The Avatar V summary (13:40–48), prefaced "All of the following is HeyGen's own description".
**SOLID** on labelling, with two gaps:
- The chapter does not note that HeyGen still runs **24 sampling steps** *after* "two-phase distillation" (tech report line 531). That is unusual for DMD, where students are typically 1–4 steps. It also undercuts the later equivalence with 4-step LiveAvatar.
- The evaluation table omits OmniHuman 1.5 (7.53 / 0.732, in the dossier) and the 22.2% "Turing test" figure from 3 annotators × 18 pairs, which is a tiny n worth showing.

**Fix:** add the 24-step note and the omitted comparator.

**C5.** "Note that the generated Sync-C exceeds ground truth, which says more about the metric than about realism." (13:50)
**SOLID.** It is good scepticism, and Seedance and Veo also exceed ground truth. It should carry through to Ch06, which still leans on Sync-C elsewhere. **Fix:** cross-reference it.

**C6.** "The architecture confirms a pattern … the commercial leader is not doing anything categorically different from InfiniteTalk or LiveAvatar" (13:52).
**CIRCULAR.**
- "Confirms" treats a vendor self-description as confirmation of the review's prior framing.
- "Not categorically different" is unfalsifiable at that level of abstraction. By the same logic LiveAvatar is not categorically different from Sora.
- The listed differences are real architectural ones: whole-clip Sparse Reference Attention, a motion stream, an identity image engine, a super-resolution cascade, GRPO/DPO.
- Calling HeyGen "the commercial leader" is unsourced; no share data is cited.

**Fix:** "shares the same broad recipe as…" and drop "confirms" and "leader".

**C7.** "Synthesia … Express-Render … roughly 8 minutes of compute per minute of output (vendor claim)" (13:56).
**SOLID** as labelled. Note the omission, though: Synthesia 3.0 (October 2025) shipped "personal avatars from a single image", which undercuts 13:23's "Synthesia's studio-grade custom avatars historically did [fine-tune]". **Fix:** add it.

**C8.** "D-ID is also the only major Western vendor found to offer a self-hosted deployment" (13:58), and "Of the Western vendors, only D-ID sells a self-hosted product" (13:90).
**OVERSTATED.**
- The dossier lists three on-prem cases, including Avaturn AVTR-1 "now open source" (`avaturn-live`:4–9).
- Hedra prices "Dedicated serving, model training, and GPU execution … per engagement" (`hedra-com-pricing`:1846).
- LemonSlice offers a "self-managed pipeline" option (`lemonslice-com`:34). It is ambiguous, but it was not checked.
- The dossier explicitly says "That does not prove they have none". 13:58 keeps "found"; 13:90, Ch10:80 and Ch11:111 drop it.
- D-ID's self-hosted licence also "includes streaming minutes", so it is metered just like bitHuman, which alone is singled out for metering.
- The underlying source is single-source (D-ID's own page), and the convention requires a label.

**Fix:** "the only explicit self-hosted offer found (vendor page); Hedra quotes dedicated deployments per engagement; Avaturn released a model as open source."

**C9.** "Every major offline vendor now also sells a live product" (13:64).
**OVERSTATED.** Mirage, profiled in the same section, has "No real-time product, API, on-prem option" (dossier). Hedra's Live Avatars are "secondary sources only; hedra.com/live-avatars returned 404." **Fix:** "HeyGen, Synthesia and D-ID now also sell…"

**C10.** "The category's pioneer did not make the transition: Soul Machines went into receivership" (13:64).
**OVERSTATED (narrative).** Soul Machines was a real-time company from the start, so there was no transition to miss. The receivership facts are solid (two sources). The causal framing (technology shift leads to failure) is unsupported: the founders left by mid-2024 and staff were cut (dossier [53]). **Fix:** state the facts; drop "did not make the transition".

**C11.** "The vendors' disclosures … fall into three technical families" (13:64–70).
**OVERSTATED / taxonomy presented as exhaustive.** Of the nine rows in the table, only four map to a family by disclosure:
- Anam: Cara-3, not the current Cara-4.1. 13:66 itself says Cara-4.1 is "diffusion-based", yet the table assigns Cara-4.1 to "motion + renderer".
- Simli.
- LemonSlice.
- Tavus: ambiguous (fix 3).

The other rows do not fit:
- D-ID is "diffusion", which is none of the three.
- Synthesia's "family" cell is a model name ("Express-3").
- HeyGen and Beyond Presence are undisclosed.
- bitHuman is "on-device renderer".
- Griffin's assignment to "large real-time video transformers" is the author's guess; no parameter count is disclosed.

**Fix:** "the few disclosures that exist suggest three approaches"; correct Anam's row.

**C12.** "Tavus describes Phoenix-4 … 'built on a Gaussian diffusion model' … Generated motion driving 3D Gaussian splats" (13:68).
**OVERSTATED.** See top fix 3. The quoted phrase does not say splats. **Fix:** move Tavus out of the 3DGS family or flag it as single-snippet.

**C13.** "A real-time render path through 3DGS is exactly what Chapter 10 recommended for custom builds; these vendors sell it as a service." (13:68)
**OVERSTATED.** Ch10's recipe is one hour of multi-view studio capture, FLAME rigging and Audio2Face. Simli's is a single photo with its own speech-to-motion model. "Exactly" turns a shared primitive into a shared design. The same move recurs in Ch10:84 ("of this Gaussian-splat kind"). **Fix:** "uses the same rendering primitive."

**C14.** "It shows that nobody in the market is near the sub-500 ms turn that Chapter 10 originally set" (13:88).
**OVERSTATED.**
- The benchmark covers four vendors, run by one of them, on default pipelines.
- "Nobody in the market" generalizes to the vendors the benchmark excluded, such as D-ID, which claims <0.5 s per turn, and Tavus Griffin (0.43 s per press).
- This sentence also contradicts Ch10's new note (10:82), which says the 500 ms target was for the face stage.
- Missed corroboration: LemonSlice's own site gives "2.04s end to end" (`lemonslice-com`:82), which independently matches Anam's 2.10 s for LemonSlice. That is the closest thing to a two-source latency figure in the chapter, and it goes unused.

**Fix:** "none of the four measured vendors"; reconcile with Ch10; cite LemonSlice's self-reported 2.04 s.

**C15.** The Anam benchmark is described as "the right *kind* of measurement" with medians of 1.24/1.82/1.86/2.10 s (13:88).
**UNDERSTATED / selective.** See top fix 1. The shared-pipeline study (2.12/2.20/2.46/2.58/2.70 s) is the stronger result for the chapter's own thesis, "latency is mostly not the face model", and it is omitted. LemonSlice's counter-claim, "fastest from p75 through p99, ahead of Tavus Phoenix-4 and Anam Cara-3" (`lemonslice-com`:83), is also omitted; that is competing vendor benchmarks reported on one side only. **Fix:** report both Anam studies and the LemonSlice counter-claim.

**C16.** "Buyers with data-residency requirements are pushed toward D-ID, the Chinese vendors, or the open stacks" (13:90).
**OVERSTATED.**
- No on-prem evidence for any Chinese vendor was gathered; the duix dossier has no private-deployment findings, and Duix cloud is a cloud API.
- For a Western buyer, a PRC vendor works against data residency.
- Data residency usually means regional hosting, not on-prem. That question (for example, EU regions for Synthesia) was never researched.

**Fix:** delete "the Chinese vendors" or source it; separate residency from on-prem.

**C17.** "No commercial vendor publicly states that its product is built on MuseTalk, LivePortrait, Wan or any other open model. Whether open components sit inside the closed products is unknown." (13:92)
**OVERSTATED (internally inconsistent).** Nine lines later the chapter identifies DINet inside Duix-Avatar, a commercial vendor's product. Avaturn open-sourced its own model. Hedra describes "open core". **Fix:** "Western vendors do not state…; the one closed product reverse-engineered (Duix-Avatar) was found to use an open 2023 model."

**C18.** "Community reverse-engineering … identifies the face engine as DINet … a second community extraction ships the same files and weights [43] … rests on one decompile plus corroboration." (13:101)
**CIRCULAR.** [43] is not independent corroboration. [42] gets its weights from [43]: "Model weights (`dinet_v1_20240131.pth` …) are the publicly released downloads from HeyGem-Linux-Python-Hack" (`…oaifaye-heygem12…`:14). The [43] README never mentions DINet. The actually useful evidence is not argued: the weight filename `dinet_v1_20240131.pth`, if it is Silicon Intelligence's own name, is vendor-originated. Meanwhile the bullet's lead, "The face engine is an older lip-sync model", states the conclusion as fact. The hardware-tier table (13:127) and Ch10 inherit that without a hedge. "Older" is also loaded: the checkpoint is dated 2024-01-31, a vendor-retrained DINetV1. **Fix:** "one decompile ([42]) of binaries extracted by [43]; the weight file is named `dinet_v1`"; put the hedge in the bullet lead.

**C19.** "The licences contradict each other … treat the most restrictive of the three as binding" (13:104).
**SOFT.** The three quotations check out (README:288; LICENSE:24; model licence 2.2). Three nuances are missing:
- The model licence names a specific version, "Duix.Avatar:0.0.7_sdk_slim".
- It "asserts no rights over your use of the output".
- It binds the user to PRC law (2.3).

Ch10:97 compresses all of this to "its model licence is non-commercial", which loses the contradiction the chapter thinks matters. The advice itself is sound. **Fix:** add the version scope, the output carve-out and the PRC-law clause; make Ch10 say "contradictory licences, the strictest non-commercial".

**C20.** "Duix … the largest Chinese player by its own account" (Ch11:113); "32.2% share … (vendor claim, via prospectus)" (13:96).
**SOFT.** 13:96 is labelled correctly. Ch11 turns "share of the digital-human *agent* market per CIC" into "largest Chinese player". That is a scope shift on a prospectus statistic commissioned for an IPO. "Falling customer count" and "net losses in most of that period" could not be located in the saved 36Kr text by grep. The key figures may sit in images, so verify them or cite the HKEX proof directly. **Fix:** Ch11 should say "claims 32.2% of China's digital-human agent market (CIC, in its IPO prospectus)."

**C21.** "Licensing is not the blocker; compute is." (13:138)
**OVERSTATED (slogan contradicted by the chapter).** The same chapter documents:
- three contradictory Duix licences;
- TalkVerse non-commercial;
- an OpenRAIL-M VAE in FlashHead;
- LiteAvatar's unspecified weights licence.

The oss dossier adds HunyuanVideo-Avatar, whose licence *excludes the EU, UK and South Korea*. That is a hard blocker for European buyers, and the chapter omits it entirely. Nobody addressed training-data provenance or likeness and consent risk. Compute is also not the blocker for the template tier the chapter itself recommends. **Fix:** "for the Wan-based generator tier, licences are permissive; compute is the constraint."

**C22.** "Most open avatar models released since mid-2025 are built on Alibaba's Wan" (13:134); "Two strong non-Wan alternatives are … LongCat … and Kandinsky S2V" (13:136).
**SOFT.**
- "Most" depends on the dossier's selection; Tight's star-gated cohort is mostly Wan, which fits.
- "Two" non-Wan alternatives omits HunyuanVideo-Avatar (Tencent, May 2025, open weights) and LTX-2.3 DubIt, both in the oss dossier.
- HuMo (ByteDance, Apache) is listed in the oss dossier but not checked here for whether it is Wan-based. If it is not, it is a third omission.

A Chinese-ecosystem reader will notice that Tencent's open avatar model is missing. **Fix:** list them and say "among the alternatives".

**C23.** Tight benchmark table and "cold offline generation costs roughly $3.5 … to $21.5 per output minute" (13:138–152).
**OVERSTATED.** Tight's timed interval "includes container startup, model loading, preprocessing … decoding" (`tight-benchmark-report`:50) for a **3.63 s** clip. Extrapolating that per minute multiplies fixed overhead by about 16×. Tight warns that "a warmed streaming service would have different latency economics" (line 81). The chapter concedes the point at 13:148, then publishes the dollar figure anyway. The table also drops a measured row:
- **SoulX-FlashTalk** (331.93 s cold) is missing, along with its warm chunk time of about 3.75 s; FlashHead's warm chunk is about 0.19 s.
- Those warm figures are the only near-warm data Tight provides, and they undercut "no official open pipeline ran faster than playback".

Other limits go unstated: one seed, one AI-generated portrait, one male English voice; and Tight's own conflict-of-interest status is not established. **Fix:** drop the per-minute dollar figures for cold runs, or show them as an upper bound; add FlashTalk and the warm chunk times.

**C24.** "The commercial live vendors are not using 14B video diffusion per stream." (13:152)
**OVERSTATED (self-contradicting).** See top fix 2. The price-equals-cost assumption is unflagged. Reserved fleets cost a fraction of Modal's serverless list price, and VC-funded vendors price below cost. **Fix:** as in top fix 2.

**C25.** "The research-to-product gap has collapsed on the generator side. HeyGen's Avatar V and the open LiveAvatar are the same kind of system … separated mainly by data, preference tuning and serving scale." (13:166)
**CIRCULAR / OVERSTATED.**
- No head-to-head quality measurement of Avatar V against any open model exists in the evidence; Tight did not test Avatar V, and HeyGen did not test open models.
- "Separated mainly by" is a claim about what accounts for a gap that was never measured.
- The chapter itself says identity-from-clip is HeyGen's key differentiator and that "the gap that remains is in identity creation". That *is* a generator-side capability, since Sparse Reference Attention lives inside the DiT.
- **Name collision:** "LiveAvatar" means HeyGen's live product at 13:38, 13:74 and 13:160, and Alibaba Quark's open model at 13:52, 13:143, 13:150 and 13:166. A reader of 13:166 can reasonably think "HeyGen's Avatar V and [HeyGen's] LiveAvatar". Disambiguate throughout ("Quark LiveAvatar").

**Fix:** "the architectural recipe has converged; whether quality has is unmeasured."

**C26.** The reference design "mirrors what the vendors appear to do … essentially the split between HeyGen's offline Avatar V and its separately priced LiveAvatar" (13:154–160).
**CIRCULAR.** See top fix 4. The vendor behaviour is inferred from the design's logic, then cited as support for the design. There is also an unaddressed product problem: the offline (1080p DiT) and live (MuseTalk 256-px crop) modes will not look like the same person at the same quality. **Fix:** present it as the author's proposal, and flag the cross-mode consistency risk.

### Cross-chapter claims rated

**X1 (Ch10:82, latency note).** "The 500 ms target above is for the face stage."
**OVERSTATED (retcon).** The context paragraph (10:70) still reads "latency from input to face animation should be under 500 ms". That is a turn target, and Ch13:88 reads it that way too. The original 3DGS recommendation claimed "~100–200 ms *including LLM inference*", which has now been silently edited to "face-stage". **Fix:** amend 10:70 openly: "Originally set as a turn target; no measured product meets it; we now treat it as the face-stage budget."

**X2 (Ch10:80).** "Buying is the default…"
**SOFT.** The review recommends buying while reporting:
- Soul Machines' receivership;
- the bitHuman SDK archived and paywalled in October 2026;
- Tavus pricing "contested over time".

Vendor-continuity and lock-in risk is not mentioned. **Fix:** add vendor-failure and price-change risk as a buy-side pitfall.

**X3 (Ch10:117, InfiniteTalk for dubbing).** "Built for exactly this task … expect minutes of datacentre-GPU time per minute of video."
**OVERSTATED.**
- Ch13:148 says no measured speed exists for InfiniteTalk, so "minutes per minute" is unsupported.
- Tight's comparable 14B cold runs were about 49–205 s per second, which is an hour-scale order of magnitude, not minutes.
- The one-minute drift caveat quoted is for *image-to-video* mode, not the dubbing (video-to-video) mode the use case needs.
- InfiniteTalk re-synthesizes head motion and posture, which conflicts with Use Case 4's own premise of preserving "the speaker's original head motion and expressions" (10:106).

**Fix:** state that the speed is unmeasured, scope the drift caveat to I2V mode, and flag the performance-alteration trade-off.

**X4 (Ch06:179, gap update).** Distilled Wan models "now combine all five on multi-GPU datacentre hardware, by their authors' figures."
**SOFT.** The hedge is present. However, "high-quality" for the *streaming* mode was never independently assessed, since Tight tested the offline/FP8 paths. LiveAvatar's 1.21 s to first frame is throughput-real-time, not latency-real-time. **Fix:** "real-time throughput", and note that streaming-mode quality is untested.

**X5 (Ch06:187).** "Half- and upper-body presenter generation with gesture is now routine in open weights."
**OVERSTATED.** The independent evidence is one observed gesture from one model on one clip; the rest are author claims. "Routine" is a market-adoption word. **Fix:** "is now offered by several open models (author claims; one independent observation)."

**X6 (Ch11:109).** "HeyGen leads offline avatar video; … Avatar V … is a distilled video diffusion transformer that builds an identity from a 15-second recording."
**OVERSTATED.** "Leads" has no source; Synthesia has the disclosed $4B valuation. The architecture is stated as fact, with Ch13's "HeyGen's own description" hedge dropped. **Fix:** cite a basis for "leads" or drop it; add "per HeyGen's technical report".

**X7 (Ch11:120).** "The newer one, which most 2024–2026 entrants use, is self-serve per-minute pricing."
**SOFT.** "Most" is uncounted. Synthesia's interactive product is Enterprise-only, D-ID's API prices could not be read, and LiveAvatar's prices returned 404. **Fix:** "many".

## Pass 2: unflagged assumptions

1. **Price tracks cost.** The 13:152 inference treats per-minute list prices as evidence of per-stream compute. It ignores subsidy, reserved-capacity discounts against Modal serverless list prices, batching and multi-tenancy. A VC-backed vendor at $0.005/min could be losing money.
2. **Vendor self-descriptions name architectures accurately.** "Gaussian diffusion", "diffusion-based", "world model" and "20B" are marketing copy. The chapter labels the *numbers* as vendor claims but treats architecture *words* as disclosures, and builds the family taxonomy and the 3DGS conclusion on them.
3. **HeyGen LiveAvatar is template-based.** It is never stated, but the reference design's "mirrors" depends on it. The only evidence is the two-minute footage requirement and the no-4K note, which would equally fit a per-identity fine-tune.
4. **Absence of evidence means absence.** "Only D-ID", "nobody in the market", "no vendor states", "none publishes a multilingual lip-sync evaluation" all come from a single day of fetching (2026-11-04), with several pages failing (403s from BusinessWire, a 404 on LiveAvatar pricing, a JS-only page for D-ID API pricing). The dossier carries the caveat; the chapter mostly does not.
5. **The Tight benchmark is representative and independent.** It used one AI-generated portrait, one male English voice, one 3.63 s clip, one seed and cold runs, and its star-gated cohort excluded InfiniteTalk by release date. Tight Studio's own commercial position is not examined, yet it is called "the one independent" benchmark and the costs are built on it.
6. **Turn latency is the user-relevant quality axis.** The chapter's evaluation frame for live products is almost entirely latency plus price. Visual quality, lip-sync accuracy outside English, identity consistency over a session, and barge-in behaviour are not compared across vendors, so the "families" are never linked to outcomes.
7. **One GitHub issue generalizes.** "Barge-in, not frame rate, is the hard part of a live avatar" (13:116) is drawn from LiveTalking issue #510. It may well be true, but it is asserted as a field-level law from one user report.

## Pass 3: structural critique

**Motivated reasoning toward the review's prior architecture.** The chapter reads the commercial world through the lens the earlier chapters built: Ch07's 3DGS thesis, Ch10's 3DGS recipe and Ch14's 3DGS prediction. The evidence that 3DGS has "arrived through vendors" is one clear self-description (Simli) and one ambiguous phrase (Tavus), yet it becomes a headline conclusion (13:168) and a Ch10 endorsement. Likewise, "the research-to-product gap has collapsed" vindicates the open-source build path the chapter goes on to design, but there is no quality comparison behind it. The pattern is that confirmations of the review's priors are promoted to conclusions, while disconfirmations get no follow-through:
- LemonSlice's 20B per-stream model;
- Anam's own like-for-like study showing the avatar barely matters to turn latency;
- Ditto as an open motion-plus-warping counterpart to Anam's family, missing from the open-stack tiers.

**Selection effects.** The commercial survey is effectively Western startups plus one Chinese company:
- None of Tencent, Baidu, iFlytek, SenseTime, ByteDance (OmniHuman) or Xiaoice's commercial digital-human products is surveyed.
- The Chinese section is Duix plus Alibaba's open repositories, and then generalizes: "In this ecosystem 'open source' frequently means…".
- Two cases do not make an ecosystem pattern. A Chinese-ecosystem practitioner would object first that the largest commercial deployments (livestream-commerce digital humans on Douyin and Taobao) are absent, while a pre-IPO firm's prospectus share figure stands in for the market.

The Anam benchmark is also the only end-to-end source, and the chapter picks the study within it that ranks vendors rather than the one that controls for the pipeline.

**Where a hostile vendor engineer pushes back.** "You classified us from a marketing sentence. Your cost arithmetic uses serverless retail prices for a fleet we reserve at a third of that, and your 'not 14B per stream' contradicts a competitor you list as 20B per stream. Your 'nobody under 500 ms' excludes our own figure." For Tavus specifically: "'Gaussian diffusion' does not mean splats."

**Where an academic pushes back.** "'Same kind of system' is unfalsifiable. Show a matched evaluation. Your only independent benchmark is n=1 with a synthetic portrait, and you turned cold-start wall-clock times into dollars per minute after admitting they are cold."

**Internal inconsistencies:**
- **Ch10 vs Ch13 on the 500 ms target.** It is a "turn" target at Ch13:88, a "face stage" target at Ch10:82, and "input to face animation" at Ch10:70.
- **Ch10 within Use Case 3.** "Pure diffusion methods … cannot hit real-time latency" (10:95) is now adjacent to recommending LiveAvatar and FlashTalk for real time (10:86).
- **Ch10 Use Case 3's "lower budget: SadTalker"** survives beside the new MuseTalk/LiveTalking stack, which is cheaper, real-time and commercially licensed.
- **Ch14 vs Ch13.** Ch14 claim 4 (diffusion cannot run in real time) and prediction 5 (photo-to-real-time-3DGS product within 18 months, "probably from the Arc2Avatar lineage") are both overtaken by Ch13's evidence (distilled real-time DiTs; Simli). Ch13:168 cites Ch14's forecast as being fulfilled while Ch14 still frames it as future.
- **Ch13 internal.** "Whether open components sit inside the closed products is unknown" (13:92) contradicts the DINet identification (13:101). Anam's row puts Cara-4.1 in "motion + renderer" while the text calls it diffusion. "LiveAvatar" names two unrelated systems.
- **Ch11 vs Ch13.** Ch11 drops hedges that Ch13 keeps: "leads", "largest Chinese player", the Avatar V architecture as fact, and "only" for self-hosting.

**Asymmetric scepticism.** MuseTalk is called "commercially cleanest", yet its README requires compliance with the licences of Whisper, the ft-mse VAE, DWPose and S3FD, and says its test data is non-commercial. The chapter applies exactly this dependency caveat to FlashHead (the OpenRAIL-M VAE) but not to MuseTalk. bitHuman is singled out for metered self-hosting; D-ID's self-hosted licence also bundles streaming minutes.

## Final verdict

The chapter's descriptive layer (who sells what, at what list price, with which disclosed parts) is mostly well sourced and honestly labelled. Its analytic layer is where it fails its own convention.

Each of these rests on one ambiguous or vendor-only datum and is stated without a hedge:
- the family taxonomy;
- "only D-ID";
- "nobody near 500 ms";
- "not using 14B per stream";
- "3DGS arriving";
- "gap collapsed";
- the reference design "mirrors what the vendors appear to do".

Two of them contradict data printed in the same chapter (LemonSlice 20B; the DINet finding), and one omits the stronger half of its own source (the Anam shared-pipeline study).

Fix the five top items, disambiguate "LiveAvatar", reconcile Ch10 and Ch14, and recast the closing conclusions as hypotheses with named tests. Until then the chapter should stay marked draft and pre-audit.

I wrote no files. Everything above is from read-only inspection of the repository at e634645.