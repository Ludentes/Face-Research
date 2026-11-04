# Chapter 13 — The Avatar Product World

## Why a Product Chapter

Chapter 06 surveyed audio-driven talking heads as *methods*: papers with architectures, benchmarks and released weights. A buyer who searches for "AI avatar" in 2026 meets something else entirely — HeyGen, Synthesia, Tavus, Duix — and those are not methods but *products*: a voice, a language model, a face model, a video transport and a billing meter, stitched together and sold by the minute. Like the game-engine pipelines of Chapter 12, they are best understood as assemblies, and the interesting questions are about which component fills each stage, what the vendor discloses about it, and what it costs to run.

This chapter covers that world as of November 2026. It has four parts. The first describes the anatomy that all avatar products share. The second surveys the commercial vendors, split into offline presenter video and live conversational avatars. The third covers Duix and the Chinese open-source stacks, where "open source" means something narrower than the phrase suggests. The fourth asks whether a team could build an equivalent product on open weights — in practice, on Alibaba's Wan video models — and what it would cost.

**Evidence conventions.** Almost every performance figure in this market comes from the vendor that sells the product. The chapter labels such figures as *vendor claims* and reserves unqualified statements for facts confirmed by at least two independent sources. Where vendors benchmark their competitors, that is still a vendor claim. The underlying research — three dossiers and roughly 240 saved source pages, all fetched on 2026-11-04 — is archived under `docs/research/agents/` and `docs/research/sources/`; each reference below names the saved copy.

## Anatomy of an Avatar Product

Every product in this chapter is one of two shapes.

**Offline presenter video.** A script goes to a text-to-speech engine (often with a cloned voice), the audio drives a face model against a stored identity, and the result is rendered to a video file. Latency is measured in minutes and nobody minds. This is the original HeyGen and Synthesia business: training videos, marketing clips, localized product demos.

**Live conversational avatar.** Voice-activity detection and speech recognition turn the user's speech into text, a language model writes a reply, text-to-speech voices it, and the face model renders frames that are streamed back over WebRTC. Every stage adds delay, and the stages must overlap (streaming ASR, streaming LLM tokens, chunked TTS, chunked rendering) for the conversation to feel live.

**How an identity is created** separates the products more sharply than any architecture choice. There are three regimes:

- *Single photo, zero-shot.* The face model generalizes from one image. HeyGen Avatar IV, Simli, Anam, LemonSlice and the open Wan-based models of Chapter 06 work this way.
- *Short reference clip, no training.* The user records seconds to minutes of video, and the product reuses that footage directly — either as conditioning for a generator (HeyGen Avatar V reads the whole clip [1]) or as a template whose mouth region is re-synthesized (Duix-Avatar, LiveTalking).
- *Per-identity fine-tune.* A base model is adapted to the person, usually by the vendor as a paid service. Duix-Mobile and Alibaba's LiteAvatar work this way, and Synthesia's studio-grade custom avatars historically did [14].

**Two families of face model** sit underneath. *Template re-lip-sync* models (Wav2Lip, DINet, MuseTalk) keep a recorded video of the person and repaint only the mouth region to match new audio; they are cheap and fast but the body, head motion and expression are whatever the template contained. *Whole-frame generators* (diffusion or flow-matching transformers, and the 3D Gaussian Splatting renderers of Chapter 07) synthesize the entire frame, so head motion, gesture and expression follow the audio — at a much higher compute cost. In 2025–2026 the commercial leaders moved decisively from the first family to the second, while most open real-time stacks still ship the first.

## Offline Presenter Video

### HeyGen and Avatar V

What users call "HeyGen v5" is **Avatar V**, HeyGen's fifth-generation avatar engine. HeyGen published its technical report and research page on 2026-04-08 [1][2][3]; the product announcement appears in HeyGen's release feed around 2026-05-04 [4], and the Avatar V API arrived in the May 2026 release at $0.05 per second of output [5]. There is no "v5 API": HeyGen's public API is v3, and a single `engine` field selects `avatar_iii`, `avatar_iv` or `avatar_v` per request, with Avatar IV the default [6].

| Engine | Released | Identity input | Notes |
|---|---|---|---|
| Avatar III | earlier | video twin | unlimited on paid plans [4] |
| Avatar IV | May 2025 | one photo, or a video "look" | "diffusion-inspired audio-to-expression engine" [8]; 16 credits/min (photo) or 31 (video look) [7] |
| Avatar V | report 2026-04-08; API May 2026 | 15-second phone or webcam recording [3] | 48 credits/min [7]; API $0.05/s [5] |
| LiveAvatar | October 2025 | at least 2 minutes of footage [9] | real-time WebRTC product; see *Live Conversational Avatars* |

The Avatar V technical report [1] is the most detailed architectural disclosure any commercial avatar vendor has made, and it is worth summarizing because it shows where the commercial frontier sits relative to the open models of Chapter 06. All of the following is HeyGen's own description and has not been independently reproduced:

- **Backbone.** HeyGen's own text-to-video and image-to-video diffusion transformer, trained with flow matching, then adapted to audio-to-video with audio cross-attention. Wan, CogVideoX and HunyuanVideo appear only as related work; the backbone is in-house.
- **Identity from the whole clip.** *Sparse Reference Attention* exposes every layer to the tokens of the full reference video rather than one frame, at a cost HeyGen describes as almost linear in reference length. This is why the product asks for a 15-second recording instead of a photo: the clip carries talking style, not just appearance.
- **A separate motion stream.** A motion representation, used both as a training target and as conditioning, carries the person's talking style.
- **Cascade.** An identity-preserving image engine sets up the scene, the base model renders at low resolution, and an identity-aware super-resolution refiner on the same backbone upscales to 1080p.
- **Training in five stages:** text-to-video pretraining, audio-to-video pretraining, "personality" fine-tuning, CFG and DMD distillation (more than 10× faster), and preference tuning with GRPO and DPO.
- **Serving.** Chunked autoregressive generation in 6.4-second chunks (161 frames at 25 fps) with 24 sampling steps, cached reference tokens, and 8-GPU sequence parallelism, on a fleet HeyGen puts at more than 5,000 GPUs.
- **Data.** More than 100 million clips curated from 50 million raw videos.

HeyGen's evaluation on 36 matched cases reports Sync-C 8.97 and face similarity 0.840 for Avatar V, against 8.86 / 0.823 for Seedance 2.0, 5.16 / 0.838 for Kling O3 Pro and 8.05 / 0.714 for Veo 3.1, with a ground-truth reference of 7.93 / 0.861 [1]. These are vendor numbers on a vendor-chosen test set; third-party write-ups repeat them without re-measuring. Note that the generated Sync-C exceeds ground truth, which says more about the metric than about realism. HeyGen also claims single-pass generation of up to 30 minutes on Avatar III, IV and V [4] (vendor claim).

The architecture confirms a pattern visible across the open literature: the commercial leader is not doing anything categorically different from InfiniteTalk or LiveAvatar (Chapter 06) — a distilled, chunked, audio-conditioned video diffusion transformer — but it does it with a private pretrained backbone, far more curated data, preference tuning, and a large serving fleet.

### Synthesia, D-ID, Mirage, Hedra

**Synthesia** disclosed the architecture of Express-2 (2025-09-04) on a research page [11]: *Express-Animate*, an audio-to-gesture model; *Express-Eval*, a CLIP-like model that picks the best of several motion candidates; and *Express-Render*, a diffusion transformer distilled to two steps that produces 1080p30 video of arbitrary length at roughly 8 minutes of compute per minute of output (vendor claim). Express-3 followed on 2026-07-15 with more script-aligned gestures and "up to 2× faster" generation, without an architecture disclosure [12]. The same day Synthesia launched an Enterprise-only Interactive Avatar API, shipped as a LiveKit plugin in which the customer brings the language model and speech recognition [13]. Synthesia raised $200M at a roughly $4B valuation in January 2026 [15].

**D-ID** launched V4 "Expressive Visual Agents" in March 2026, described as "built on a new diffusion-based model and trained on performances captured from real actors", serving both live agents and scripted video, with a vendor-claimed turn latency under 0.5 seconds [16]. D-ID is also the only major Western vendor found to offer a **self-hosted** deployment: real-time avatars running in the customer's own cloud or network, sold as an annual licence through the AWS and Azure marketplaces, with a vendor-claimed render time under 200 ms [17].

**Mirage** (Captions until its September 2025 rebrand) positions itself as a research lab built around a foundation model for UGC-style talking video that generates face, upper body and background from audio or script [25][26]. **Hedra** moved from its Character-3 creator product (March 2025) to Omnia (February 2026), a base model offered to partners for further training [23], and by late 2026 leads its site with model-training and inference infrastructure, pricing avatar and lip-sync output from 2.5¢ per second [24].

## Live Conversational Avatars

Every major offline vendor now also sells a live product — HeyGen LiveAvatar, Synthesia's Interactive Avatar API, D-ID V4 — alongside companies built for real time from the start: Tavus, Anam, Simli, Beyond Presence, bitHuman and LemonSlice. The category's pioneer did not make the transition: Soul Machines went into receivership in February 2026 and was acquired by AppDirect in September [37][38]. The vendors' disclosures, where they exist, fall into three technical families.

**Motion model plus renderer.** A small model predicts motion from audio and a separate renderer animates a reference image. Anam's Cara-3 is the clearest disclosure: a flow-matching audio-to-motion model followed by a motion-to-face renderer, any face from one photo, about 70 ms to first frame on an H200 (vendor claim) [29]. Anam's current model, Cara-4.1, is diffusion-based and outputs 1152×768 [31].

**Generated motion driving 3D Gaussian splats.** This is the Chapter 07 representation arriving in commercial products. Tavus describes Phoenix-4 (February 2026) as "built on a Gaussian diffusion model" [18], and Simli says it builds "a full 3D avatar out of Gaussian splats on real geometry" from one photo, at about 150 ms audio-to-video (vendor claim) [27]. A real-time render path through 3DGS is exactly what Chapter 10 recommended for custom builds; these vendors sell it as a service.

**Large real-time video transformers.** LemonSlice-2 is a 20-billion-parameter model that animates any character, non-human included, at 20 fps from one photo [36]. Tavus's Griffin (research preview from 2026-10-01) goes further: a single full-duplex video-to-video model that listens and renders at once rather than chaining ASR, LLM, TTS and face. In Tavus's own study, 48% of 54 participants judged it to be a person [20] (vendor claim, not replicated).

| Vendor / product | Family | Identity input | Latency claim | Price shape | On-prem |
|---|---|---|---|---|---|
| HeyGen LiveAvatar | undisclosed | ≥2 min footage [9] | — | 1–2 credits/min [9] | no |
| Synthesia Interactive API | Express-3 | stock or personal avatar | none published | Enterprise only [13] | no |
| D-ID V4 | diffusion | photo or video | <0.5 s per turn [16] | from $5.90/mo [16] | **yes** [17] |
| Tavus Phoenix-4.5 | Gaussian diffusion | photo or video [19] | 134 ms render [22] | $22–$975/mo + $0.26–0.35/min [21] | no |
| Anam Cara-4.1 | motion + renderer | one photo | ~70 ms first frame (Cara-3) [29] | $0.16→$0.11/min [30] | no |
| Simli | Gaussian splats | one photo | ~150 ms [27] | $0.009→$0.005/min [28] | no |
| Beyond Presence Genesis 2.0 | undisclosed | photo or video | <100 ms vs 250 ms (contested) [32][33] | credits, from $49/mo | no |
| bitHuman Essence 2 | on-device renderer | one portrait | — | 2 credits/min even self-hosted [35] | on-device, metered |
| LemonSlice-2 | 20B video DiT | one photo | 471 ms p99 [36] | — | no |

### Why Latency Claims Do Not Compare

The numbers in the table above measure different things. "134 ms" or "150 ms" is the face renderer's own delay from audio to video. What a user experiences is the full turn: end of their speech, detection, transcription, language-model reply, speech synthesis, rendering, network. That is typically one to two seconds. Beyond Presence illustrates the gap within a single vendor: its homepage advertises under 100 ms [32], its documentation states 250 ms speech-to-video and about one second end-to-end [33].

The only cross-vendor end-to-end measurement found was run by Anam itself (60 raters, 4,703 conversational turns, published 2026-10-16). It reports median reply latencies of 1.24 s for Anam, 1.82 s for HeyGen LiveAvatar, 1.86 s for Tavus Phoenix-4.5 and 2.10 s for LemonSlice [10]. It is a competitor-run benchmark and should be read as such, but it is the right *kind* of measurement, and it shows that nobody in the market is near the sub-500 ms turn that Chapter 10 originally set as the target for a real-time assistant.

**On-premise deployment is rare.** Of the Western vendors, only D-ID sells a self-hosted product [17]; bitHuman renders on the device (including CPU-only Linux, phones and the browser) but still meters self-hosted sessions [34][35]. No on-premise evidence was found for HeyGen, Synthesia, Tavus, Anam, Simli, Beyond Presence or LemonSlice. Buyers with data-residency requirements are pushed toward D-ID, the Chinese vendors, or the open stacks below.

**What vendors do not say.** No commercial vendor publicly states that its product is built on MuseTalk, LivePortrait, Wan or any other open model. Whether open components sit inside the closed products is unknown.

## Duix and the Chinese Digital-Human Ecosystem

**The company.** Duix is the international brand of Nanjing Silicon Intelligence Technology (南京硅基智能), founded in 2017. It filed for a Hong Kong listing in October 2025 and refiled in May 2026 [48][49]. The prospectus coverage reports revenue of RMB 531M, 655M and 789M for 2023–2025, with net losses in most of that period and a falling customer count, and claims a 32.2% share of China's digital-human agent market based on CIC data (vendor claim, via prospectus) [48]. Its open-source repositories were moved from the GuijiAI GitHub organization to `duixcom` and renamed along the way: HeyGem.ai became Duix-Avatar, and duix.ai became Duix-Mobile.

**Duix-Avatar (formerly HeyGem)** is the project most people mean by "Duix". It is an *offline* video generator with voice cloning — its own README calls it non-real-time and sends interactive users to the paid cloud [39]. It has about 16,200 GitHub stars but has been in maintenance mode since its last release in September 2025. Three facts matter:

- *Only the client is open.* The open repository is an Electron desktop app. The face, speech-recognition (FunASR) and speech-synthesis (Fish-Speech) services ship as Docker images of 60–100 GB containing compiled modules [39]; "fake open source" is a recurring complaint in the issue tracker [50].
- *The face engine is an older lip-sync model.* Community reverse-engineering of the compiled modules identifies the face engine as DINet, a 2023 lip-sync model, working on a 256-pixel face crop with optional GFPGAN restoration [42]; a second community extraction ships the same files and weights [43]. Duix has never confirmed this, so it rests on one decompile plus corroboration.
- *A "clone" involves no training.* It is the user's reference video, re-lip-synced, plus a zero-shot voice prompt [42]. This is the template re-lip-sync family, not a generator.

**The licences contradict each other.** The README offers "global free commercial use" except for firms above 100,000 users or US$10M annual revenue [39]. The repository LICENSE requires a commercial licence, granted at Duix's discretion, above 1,000 monthly active users, plus attribution and naming conditions [40]. The bundled model licence permits non-commercial use only and requires written authorization for any commercial use [41]. A team considering Duix-Avatar for a product should treat the most restrictive of the three as binding until Duix says otherwise in writing.

**Duix-Mobile** is an on-device SDK for Android and iOS that plays a per-identity 2D avatar on the CPU; the maintainer describes inference as "pure CPU" [45]. Each avatar is a base model fine-tuned on one to two minutes of video, the training code is closed, and custom avatars are a paid service from Duix [44][45]. Its latency is stated inconsistently — under 120 ms on a Snapdragon 8 Gen 2 in the README, under 1.5 s in the repository description [44].

**Duix cloud** is a server-rendered avatar API streamed over WebRTC [47], priced per conversation minute from $29/month for 150 minutes to $4,999/month for 60,000 minutes, with a vendor-claimed 200 ms time to first byte [46]. A July 2026 "duix-skills" package builds a conversational avatar from a single portrait [73]. The model behind it is undisclosed.

**The pattern generalizes.** Alibaba's LiteAvatar follows the same shape as Duix-Mobile: a 2D mouth-parameter model that runs at a vendor-claimed 30 fps on CPU, MIT-licensed code, an unspecified weights licence, and closed training with custom avatars sold through Alibaba Cloud [54]. In this ecosystem "open source" frequently means *open client or SDK, closed weights or closed training*, and the identity-creation step is where the business model lives.

## Open Real-Time Stacks

A second tier of genuinely open projects assembles the live-avatar pipeline from open parts. None of them publishes independent latency measurements; every figure below is from the project's own README or from user reports in its issue tracker.

**LiveTalking** (formerly metahuman-stream; Apache-2.0, about 10,300 stars, active through October 2026) is the de facto open engine [51]. Its current code ships three face back-ends — Wav2Lip-256, MuseTalk and Ultralight-Digital-Human — all template re-lip-sync models over a prepared video of the person (the README still advertises ER-NeRF, which is no longer in the code tree [52]). Its own figures give Wav2Lip 60 fps on an RTX 3060 and MuseTalk 72 fps on an RTX 4090 [51]. Users report about three seconds of lag when interrupting the avatar, because buffered WebRTC frames and in-flight inference cannot be flushed [52] — a reminder that barge-in, not frame rate, is the hard part of a live avatar.

**OpenAvatarChat** (Alibaba, Apache-2.0, about 3,800 stars) is the cleanest modular design: Silero VAD, SenseVoice ASR, any LLM or Qwen-Omni end-to-end, CosyVoice TTS, and a choice of four avatar back-ends — LiteAvatar (CPU 2D), LAM (a single-image 3D Gaussian head rendered in WebGL [55]), MuseTalk, and SoulX-FlashHead [53]. It reports an average response time of 2.2 s (vendor claim) [53], consistent with the commercial end-to-end figures above.

**Others.** Linly-Talker and its 2026 streaming successor Linly-Talker-Stream (small, early) follow LiveTalking's design [71]. Fay is an orchestrator only — agents, ASR, TTS, memory — that plugs into LiveTalking, Duix or an Unreal MetaHuman for the face [72]. For stylized characters, the Live2D path of Chapter 02 remains the cheapest live avatar of all.

The open stacks sort into three hardware tiers, which is the useful way to choose between them:

| Tier | Face model | Hardware | Identity creation | Examples |
|---|---|---|---|---|
| CPU / mobile 2D player | per-identity 2D model | phone or CPU | closed, paid | Duix-Mobile, LiteAvatar |
| GPU template re-lip-sync | Wav2Lip, MuseTalk, DINet | one consumer GPU | your own video, no training | LiveTalking, Duix-Avatar (offline) |
| One-shot streaming generator | distilled video DiT | consumer GPU (head only) to multi-GPU datacentre | one photo | SoulX-FlashHead, LiveAvatar, SoulX-FlashTalk |

MuseTalk 1.5 is the commercially cleanest choice in the middle tier: MIT code with weights usable commercially [56].

## Building One on Open Weights: The Wan Question

Most open avatar models released since mid-2025 are built on Alibaba's **Wan** video models (Chapter 06 covers them as methods). The question here is the product one: could a team build a HeyGen- or Duix-like service on them?

**What is open.** Every open Wan checkpoint is Apache-2.0: Wan 2.1, Wan 2.2, Wan2.2-S2V (Alibaba's own audio-to-video model), Wan2.2-Animate and Wan-Animate-2 [61]. The later flagship versions — Wan 2.5, 2.6, 2.7 and 3.0 — are available only through Alibaba's API (Wan 2.6 reference-to-video at roughly $0.09–0.10 per second at 720p [62]), and Alibaba's end-to-end real-time interactive model, Wan-Streamer, is a paper without released weights [63]. The open foundation therefore stops at the 2.2 generation. Most Wan-derived avatar models carry permissive licences — InfiniteTalk, MultiTalk, OmniAvatar, EchoMimicV3, LiveAvatar and SoulX-FlashTalk are Apache-2.0, StableAvatar is MIT — but not all: Snap's TalkVerse is non-commercial, and SoulX-FlashHead Lite bundles a VAE under OpenRAIL-M. Two strong non-Wan alternatives are Meituan's LongCat-Video-Avatar (MIT) [74] and Kandinsky S2V (MIT) [75].

**Licensing is not the blocker; compute is.** The one independent cross-model benchmark — Tight Studio's August 2026 run on a single portrait and a 3.6-second English clip, with pinned runners [64][65] — found that no official open pipeline ran faster than playback on a cold job:

| Model | GPU | Seconds of compute per output second | Notes |
|---|---|---|---|
| Wan2.2-S2V | 1×H200 | 204.6 | slowest; restrained motion |
| LiveAvatar (offline mode) | 1×H200 | 48.8 | sharpest identity among the large models |
| EchoMimicV3-Flash | 1×L40S | ≈70 | best value; used 33.7 GB against a claimed 12 GB |
| LongCat-Video-Avatar 1.5 | 1×H200 | ≈65 | most expressive, added gestures; exaggerated mouth shapes |
| SoulX-FlashHead Lite | — | fast once compiled | 5.8 GB; softer identity, weaker mouth |

These are cold-start figures that include model loading and compilation, so they overstate the steady-state cost of a warm server. No measured speed on a named GPU was found for InfiniteTalk, the most-used long-form model, with or without the 4-step distillation LoRA its README supports [66].

**Real time exists, at a hardware floor.** Distilling 14B Wan models into causal few-step students (Self-Forcing / DMD style) produced the first open streaming avatar generators, all with author-reported figures only: LiveAvatar at 45 fps on 5×H800 with 1.21 s to first frame [59], SoulX-FlashTalk at 32 fps on 8×H800 [58], and SoulX-LiveAct at 20 fps on 2×H100 [60]. On a single consumer GPU only the 1.3B models qualify: SoulX-FlashHead Lite claims 96 fps on an RTX 4090 at 512² head-only [57], visibly softer than the large models in Tight's comparison. A known failure mode of these distilled students is collapse toward static motion [70].

**Cost per output minute.** From the Tight measurements and public GPU list prices [69], cold offline generation costs roughly $3.5 (EchoMimicV3-Flash) to $21.5 (Wan2.2-S2V) per output minute. Real-time streaming on the large distilled models works out — by arithmetic on author throughput and list prices, not by measurement — at roughly $0.13 (LiveAct on 2×H100) to $0.53 (FlashTalk on 8×H100) per stream-minute, and about a cent for FlashHead Lite sharing one GPU across three streams. Hosted InfiniteTalk ranges from $1.80–3.60 per minute (WaveSpeed) to $12–24 (fal) [67][68]. For comparison, Simli sells live avatar minutes at under a cent and Anam at 11–16 cents [28][30]: the commercial live vendors are not using 14B video diffusion per stream.

**A reference design.** The economics point to a hybrid that mirrors what the vendors appear to do:

1. Use a Wan-based generator (InfiniteTalk, Wan2.2-S2V or LiveAvatar in offline mode; LongCat as the expressive non-Wan option) for high-quality *offline* presenter video, where minutes of GPU time per clip are acceptable.
2. Use the same generator once per identity to produce template footage — idle loops, listening poses, gestures.
3. For the *live* mode, run a cheap real-time model over those templates: MuseTalk-class re-lip-sync on one consumer GPU, or a one-shot streaming head model like FlashHead where a single photo must suffice.

This gives generator quality where latency does not matter and template economics where it does — essentially the split between HeyGen's offline Avatar V and its separately priced LiveAvatar.

**Risks.** Alibaba stopped releasing flagship Wan weights after 2.2, so a product built today stays on that backbone unless another lab releases a successor. No independent test of long-form drift beyond one minute exists for any open model, and no independent verification of any real-time figure. Lip-sync quality outside English and Chinese is untested.

## What the Product World Tells the Rest of the Review

**The research-to-product gap has collapsed on the generator side.** HeyGen's Avatar V and the open LiveAvatar are the same kind of system — a distilled, chunked, audio-conditioned video diffusion transformer — separated mainly by data, preference tuning and serving scale. The gap that remains is in identity creation, voice, and the engineering of a live turn.

**Chapter 07's 3DGS prediction is arriving through vendors.** Tavus and Simli both describe Gaussian-splat renderers driven by generated motion — the "3DGS as the default real-time rendering target" direction that Chapter 14 forecasts — but as closed services, not as the open FLAME-rigged pipelines the research literature describes.

**Latency needs a shared definition.** The field reports render latency and calls it response latency. A review, a buyer or a benchmark should ask for end-to-end turn latency under barge-in, measured by someone other than the seller.

**"Open source" needs reading closely.** Open client, closed weights; open weights, closed training; open code, unspecified weights licence; three contradictory licence documents in one repository. The licence and the identity-creation path matter more than the star count.

## Open Questions

- Which open components, if any, run inside the commercial products.
- An independent, cross-vendor, end-to-end latency benchmark under interruption.
- Measured warm-server speed and cost for InfiniteTalk and the distilled Wan models on named GPUs.
- Long-form drift beyond one minute for any open model, measured independently.
- What model powers Duix cloud and duix-skills, and whether the DINet identification of Duix-Avatar is correct.
- Whether Synthesia's promised hosted interactive pipeline (announced for 2026-10-01) shipped.

## References

All sources were retrieved on 2026-11-04. The saved copy of each is in `docs/research/sources/text/<slug>.txt`; GitHub API snapshots are in `docs/research/agents/duix-realtime/gh/`. The full dossiers are `docs/research/agents/commercial/report.md`, `docs/research/agents/duix-realtime/report.md` and `docs/research/agents/oss-avatar/report.md`.

[1] HeyGen. "Avatar V Technical Report." `dynamic.heygen.ai/www/Paper%20Links/avatarv_tech_report.pdf`. Saved: `heygen-avatarv-tech-report`.

[2] HeyGen. "Avatar V model" (research page). `heygen.com/research/avatar-v-model`. Saved: `heygen-research-avatar-v`.

[3] HeyGen. "Announcing Avatar V." `heygen.com/blog/announcing-avatar-v`. Saved: `heygen-com-blog-announcing-avatar-v`.

[4] Releasebot. HeyGen release feed. `releasebot.io/updates/heygen`. Saved: `releasebot-io-updates-heygen`.

[5] HeyGen. "HeyGen May 2026 release." `heygen.com/blog/heygen-may-2026-release`. Saved: `heygen-com-blog-heygen-may-2026-release`.

[6] HeyGen. API models documentation. `developers.heygen.com/models`. Saved: `developers-heygen-com-models`.

[7] HeyGen Help. "HeyGen credit-based pricing plans explained." Saved: `help-heygen-com-en-articles-15125761-heygen-credit-based-pricing-plans-explained`.

[8] HeyGen Help. "New feature alert: HeyGen Avatar IV is here." Saved: `help-heygen-com-en-articles-11269603-new-feature-alert-heygen-avatar-iv-is-here`.

[9] HeyGen Help. "How to get started with LiveAvatar." Saved: `help-heygen-com-en-articles-10035615-how-to-get-started-with-liveavatar`.

[10] Anam. "Latency benchmark." `anam.ai/tools/latency-benchmark`. Saved: `anam-ai-tools-latency-benchmark`.

[11] Synthesia Research. "Express" video models. `synthesiaresearch.github.io/express-video`. Saved: `synthesiaresearch-github-io-express-video`.

[12] Synthesia. Express-3 launch post. Saved: `synthesia-io-post-synthesia-launches-new-ai-assistant-for-faster-video-creation-and-expres`.

[13] Synthesia. "Interactive Avatar API: real-time avatars." Saved: `synthesia-io-post-interactive-avatar-api-real-time-avatars`.

[14] Synthesia. Pricing. `synthesia.io/pricing`. Saved: `synthesia-io-pricing`.

[15] Built In. "Synthesia raises $200M Series E." Saved: `builtin-com-articles-synthesia-raises-200m-series-e-20260126`.

[16] eLearning Industry (D-ID press release). "D-ID launches V4 Expressive Visual Agents." Saved: `elearningindustry-com-press-releases-d-id-launches-v4-expressive-visual-agents-for-real-ti`.

[17] D-ID. "Self-hosted Expressive Avatars." `d-id.com/self-hosting-realtime-avatars/`. Saved: `d-id-com-self-hosting-realtime-avatars`.

[18] Tavus. Models documentation. `docs.tavus.io/sections/models`. Saved: `docs-tavus-io-sections-models`.

[19] Tavus. Replica overview. `docs.tavus.io/sections/replica/overview`. Saved: `docs-tavus-io-sections-replica-overview`.

[20] Business Wire via Morningstar. "Tavus introduces Griffin." Saved: `morningstar-com-news-business-wire-20261001092598-tavus-introduces-griffin-the-first-face-`.

[21] Tavus. Pricing. `tavus.io/pricing`. Saved: `tavus-io-pricing`.

[22] Tavus. Demo page. `tavus.io/demo`. Saved: `tavus-io-demo`.

[23] Hedra. "Hedra Omnia." Saved: `hedra-com-blog-hedra-omnia-frontier-ai-video-model`.

[24] Hedra. Pricing. `hedra.com/pricing`. Saved: `hedra-com-pricing`.

[25] Captions. "Mirage: world's first foundation model for UGC video." Saved: `captions-ai-blog-mirage-worlds-first-foundation-model-for-ugc-video`.

[26] TechCrunch. "Captions rebrands as Mirage." 2025-09-04. Saved: `techcrunch-com-2025-09-04-captions-rebrands-as-mirage-expands-beyond-creator-tools-to-ai-v`.

[27] Simli. Homepage. `simli.com`. Saved: `simli-com`.

[28] Simli. Pricing. `simli.com/pricing`. Saved: `simli-com-pricing`.

[29] Anam. "Cara-3 interactive avatars." Saved: `anam-ai-blog-cara-3-interactive-avatars`.

[30] Anam. Pricing. `anam.ai/pricing`. Saved: `anam-ai-pricing`.

[31] Anam. Models documentation. Saved: `anam-ai-docs-introduction-models-md`.

[32] Beyond Presence. Homepage. `beyondpresence.ai`. Saved: `beyondpresence-ai`.

[33] Beyond Presence. Documentation. `docs.bey.dev`. Saved: `docs-bey-dev`.

[34] bitHuman. Homepage. `bithuman.ai`. Saved: `bithuman-ai`.

[35] Pipecat. bitHuman video service documentation. Saved: `docs-pipecat-ai-api-reference-server-services-video-bithuman-md`.

[36] LemonSlice. Homepage. `lemonslice.com`. Saved: `lemonslice-com`.

[37] NBR. "Soul Machines in receivership." Saved: `nbr-co-nz-tech-soul-machines-in-receivership`.

[38] SiliconANGLE. "AppDirect acquires interactive AI avatar firm Soul Machines." 2026-09-28. Saved: `siliconangle-com-2026-09-28-appdirect-acquires-interactive-ai-avatar-firm-soul-machines-fo`.

[39] Duix. Duix-Avatar README. `github.com/duixcom/Duix-Avatar`. Saved: `raw-githubusercontent-com-duixcom-duix-avatar-main-readme-md`.

[40] Duix. Duix-Avatar LICENSE. Saved: `duix-avatar-LICENSE`.

[41] Duix. "Duix.Avatar model community Licensing Agreement" (PDF). Saved: `duix-avatar-model-community-licence-pdf`.

[42] oaifaye. HeyGem12 README (clean-room reimplementation and decompile notes). `github.com/oaifaye/HeyGem12`. Saved: `raw-githubusercontent-com-oaifaye-heygem12-main-readme-md`.

[43] Holasyb918. HeyGem-Linux-Python-Hack README. Saved: `raw-githubusercontent-com-holasyb918-heygem-linux-python-hack-main-readme-md`.

[44] Duix. Duix-Mobile README. `github.com/duixcom/Duix-Mobile`. Saved: `raw-githubusercontent-com-duixcom-duix-mobile-main-readme-md`.

[45] Duix-Mobile issue tracker (maintainer replies). Saved: `gh/duixcom-Duix-Mobile-issue-4.json` and related issue snapshots.

[46] Duix. Pricing. `duix.com/pricing`. Saved: `duix-com-pricing`.

[47] Duix. Android SDK quickstart. `docs.duix.com/sdks/android/quickstart.md`. Saved: `docs-duix-com-sdks-android-quickstart-md`.

[48] 36Kr. Silicon Intelligence prospectus coverage. `36kr.com/p/3825797690614017`. Saved: `36kr-com-p-3825797690614017`.

[49] HKEXnews. Silicon Intelligence application proof, May 2026 (cover). Saved: `www1-hkexnews-hk-app-sehk-2026-108560-a133153-sehk26052101556-pdf`.

[50] Duix-Avatar issue tracker. Saved: `gh/duixcom-Duix-Avatar-issues-top-comments.json`, `gh/duixcom-Duix-Avatar-issue-243.json`.

[51] lipku. LiveTalking README. `github.com/lipku/LiveTalking`. Saved: `raw-githubusercontent-com-lipku-livetalking-main-readme-md`.

[52] LiveTalking repository tree and issue #510. Saved: `gh/lipku-LiveTalking-tree.json`, `gh/lipku-LiveTalking-issue-510.json`.

[53] HumanAIGC-Engineering. OpenAvatarChat README. Saved: `raw-githubusercontent-com-humanaigc-engineering-openavatarchat-main-readme-md`.

[54] HumanAIGC. LiteAvatar README and issues. Saved: `raw-githubusercontent-com-humanaigc-lite-avatar-main-readme-md`, `gh/HumanAIGC-lite-avatar-issue-27.json`.

[55] aigc3d. LAM README. Saved: `aigc3d-lam-readme`.

[56] TMElyralab. MuseTalk README. Saved: `raw-githubusercontent-com-tmelyralab-musetalk-main-readme-md`.

[57] Soul AI Lab. SoulX-FlashHead README. Saved: `gh-soulx-flashhead-readme`.

[58] Soul AI Lab. SoulX-FlashTalk README. Saved: `gh-soulx-flashtalk-readme`.

[59] Alibaba Quark. LiveAvatar README. Saved: `gh-liveavatar-readme`.

[60] Soul AI Lab. SoulX-LiveAct README. Saved: `gh-soulx-liveact-readme`.

[61] Hugging Face. Wan-AI organization model list. Saved: `hf-api-wan-ai-models-list`.

[62] Alibaba Cloud. Wan 2.6 reference-to-video pricing. Saved: `alibaba-wan26-r2v`.

[63] Wan team. "Wan-Streamer." arXiv 2606.25041. Saved: `arxiv-2606.25041-wan-streamer`.

[64] Tight Studio. "Open-source talking avatar benchmark" report. `github.com/tight-studio/open-source-talking-avatar-benchmark`. Saved: `tight-benchmark-report`.

[65] Tight Studio. "Open-source talking avatar models" (blog). Saved: `tight-studio-blog`.

[66] MeiGen-AI. InfiniteTalk README. Saved: `gh-infinitetalk-readme`.

[67] WaveSpeed. InfiniteTalk model page. Saved: `wavespeed-infinitetalk-model`.

[68] fal. InfiniteTalk model page. Saved: `fal-infinitalk`.

[69] Modal. GPU pricing. Saved: `modal-pricing`.

[70] "DynaForcing." arXiv 2608.17707. Saved: `arxiv-2608.17707-dynaforcing`.

[71] Kedreamix. Linly-Talker-Stream README. Saved: `raw-githubusercontent-com-kedreamix-linly-talker-stream-main-readme-md`.

[72] xszyou. Fay README. Saved: `raw-githubusercontent-com-xszyou-fay-main-readme-md`.

[73] Duix. duix-skills README. Saved: `raw-githubusercontent-com-duixcom-duix-skills-main-readme-md`.

[74] Meituan LongCat. "LongCat-Video-Avatar 1.5." arXiv 2605.26486. Saved: `arxiv-2605.26486-longcat-avatar-1.5`.

[75] Kandinsky Lab. Kandinsky S2V README. Saved: `gh-kandinsky-s2v-readme`.
