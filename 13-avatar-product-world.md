# Chapter 13 — The Avatar Product World

## Why a Product Chapter

Chapter 06 surveyed audio-driven talking heads as *methods*: papers with architectures, benchmarks and released weights. A buyer who searches for "AI avatar" in 2026 meets something else entirely — HeyGen, Synthesia, Tavus, Duix — and those are not methods but *products*: a voice, a language model, a face model, a video transport and a billing meter, stitched together and sold by the minute. Like the game-engine pipelines of Chapter 12, they are best understood as assemblies, and the interesting questions are about which component fills each stage, what the vendor discloses about it, and what it costs to run.

This chapter covers that world as of November 2026. It has four parts. The first describes the anatomy most avatar products share. The second surveys the commercial vendors, split into offline presenter video and live conversational avatars. The third covers Duix and the Chinese open-source stacks around it. The fourth asks whether a team could build an equivalent product on open weights — in practice, on Alibaba's Wan video models — and what it would cost.

**Evidence conventions.** Almost every performance figure in this market comes from the vendor that sells the product. The chapter labels such figures as *vendor claims* and reserves unqualified statements for facts confirmed by at least two independent sources. Where vendors benchmark their competitors, that is still a vendor claim. Architecture words in marketing copy ("diffusion-based", "world model") are treated as claims too, not as disclosures. Statements that something does not exist ("no vendor offers…") mean *not found* in a survey run on a single day, 2026-11-04, during which several vendor pages could not be fetched. The underlying research — three dossiers, roughly 240 saved source pages, and the adversarial review and citation check this chapter went through — is archived under `docs/research/`; each reference below names the saved copy.

**Scope.** The commercial survey covers the Western vendors and one Chinese company, Duix. It does not cover the large Chinese commercial digital-human businesses of Tencent, Baidu, iFlytek, SenseTime or ByteDance, nor the livestream-commerce avatars on Douyin and Taobao, which are probably the largest deployments by volume. Statements about "the Chinese ecosystem" below are about the open-source projects examined, not that market.

## Anatomy of an Avatar Product

Most products in this chapter take one of two shapes.

**Offline presenter video.** A script goes to a text-to-speech engine (often with a cloned voice), the audio drives a face model against a stored identity, and the result is rendered to a video file. Latency is measured in minutes and nobody minds. This is the original HeyGen and Synthesia business: training videos, marketing clips, localized product demos.

**Live conversational avatar.** Voice-activity detection and speech recognition turn the user's speech into text, a language model writes a reply, text-to-speech voices it, and the face model renders frames that are streamed back over WebRTC. Every stage adds delay, and the stages must overlap (streaming ASR, streaming LLM tokens, chunked TTS, chunked rendering) for the conversation to feel live. A third, smaller shape sits between the two: one-way live broadcast, such as HeyGen's streaming API demonstrated on a 24-hour Twitch stream [4].

**How an identity is created** separates the products more sharply than any architecture choice. The main regimes are:

- *Single photo, zero-shot.* The face model generalizes from one image. HeyGen Avatar IV [8], Simli [27], Anam [29], LemonSlice [36] and the open Wan-based models of Chapter 06 work this way, and Synthesia added single-image personal avatars in October 2025 [77].
- *Short reference clip, no training.* The user records seconds to minutes of video, and the product reuses that footage directly — either as conditioning for a generator (HeyGen Avatar V reads the whole clip [1]) or as a template whose mouth region is re-synthesized (Duix-Avatar, LiveTalking).
- *Per-identity fine-tune.* A base model is adapted to the person, usually by the vendor. Duix-Mobile and Alibaba's LiteAvatar work this way. Synthesia's studio avatars, a paid add-on that takes up to 10 days to process [14], suggest per-identity training.
- *Synthetic identity.* No real person at all: Synthesia's Style Avatars are created from a text prompt [12].

Some products mix regimes; Tavus, for example, offers a zero-shot preview from a photo and then tunes the replica in the background [19].

**Families of face model.** Four kinds of face model sit underneath, and a product may combine them:

- *Template re-lip-sync* (Wav2Lip, DINet, MuseTalk) keeps a recorded video of the person and repaints only the mouth region to match new audio. Cheap and fast, but body, head motion and expression are whatever the template contained.
- *Motion plus warping or rendering* predicts motion from audio and animates a reference image with a separate renderer — the LivePortrait lineage of Chapter 05, Ditto, and Anam's disclosed Cara-3 design [29].
- *Whole-frame generators* — diffusion or flow-matching video transformers — synthesize the entire frame, so head motion, gesture and expression follow the audio, at a much higher compute cost.
- *Rendered 3D heads* — 3D Gaussian splats (Chapter 07) or rigged CG such as MetaHuman (Chapter 12) — are driven by generated motion and rendered.

The offline flagships of HeyGen, Synthesia and D-ID now describe diffusion or diffusion-transformer renderers [1][11][16]; what their earlier engines used is not disclosed, and HeyGen still sells its older Avatar III. Most live products do not disclose their face model at all. Most open real-time stacks ship template re-lip-sync.

## Offline Presenter Video

### HeyGen and Avatar V

What users call "HeyGen v5" is **Avatar V**, HeyGen's fifth-generation avatar engine. HeyGen's research page dates the technical report to 2026-04-08 [2][1]. HeyGen's April 2026 roundup, published 2026-05-06, announces Avatar V as launched [4], and the Avatar V API arrived in the May 2026 release at $0.05 per second of output [5]. There is no "v5 API": HeyGen's public API is v3, and a single `engine` field selects `avatar_iii`, `avatar_iv` or `avatar_v` per request, with Avatar IV the default for new integrations [6].

| Engine | Released | Identity input | Notes |
|---|---|---|---|
| Avatar III | before Avatar IV | photo or video look [6] | 7 / 4 credits/min (photo / video look) on credit plans; unlimited on legacy plans [7] |
| Avatar IV | before Avatar V | one photo, or a video look | "diffusion-inspired audio-to-expression engine" [8]; 16 credits/min (photo) or 31 (video look) [7] |
| Avatar V | report 2026-04-08; API May 2026 | 15-second phone recording [3] | 48 credits/min [7]; API $0.05/s [5] |
| HeyGen LiveAvatar | October 2025 [4] | at least 2 minutes of footage [9] | real-time WebRTC product; see *Live Conversational Avatars* |

The Avatar V technical report [1] is the most detailed architectural disclosure any commercial avatar vendor has made. All of the following is HeyGen's own description and has not been independently reproduced:

- **Backbone.** HeyGen's text-to-video and image-to-video diffusion transformer, trained with flow matching, then adapted to audio-to-video with audio cross-attention. Wan, CogVideoX and HunyuanVideo appear only as related work, and the report describes its own text-to-video pretraining stage, so the backbone appears to be in-house.
- **Identity from the whole clip.** *Sparse Reference Attention* exposes every layer to the tokens of the full reference video rather than one frame, at a cost HeyGen says scales almost linearly with reference length. This is why the product asks for a 15-second recording instead of a photo: the clip carries talking style, not just appearance.
- **A separate motion stream.** A motion representation, used both as a training target and as conditioning, carries the person's talking style.
- **Cascade.** An identity-preserving image engine sets up the scene, the base model renders at low resolution, and an identity-aware super-resolution refiner on the same backbone upscales to 1080p.
- **Training in five stages:** text-to-video pretraining, audio-to-video pretraining, "personality" fine-tuning, CFG and DMD distillation (more than 10× faster), and preference tuning with GRPO and DPO.
- **Serving.** Chunked autoregressive generation in 6.4-second chunks (161 frames at 25 fps), cached reference tokens, and 8-GPU sequence parallelism, on a fleet HeyGen puts at more than 5,000 GPUs. Notably, sampling still takes 24 steps after distillation — far more than the 1–4-step students of the open streaming models discussed below — which places Avatar V firmly on the offline side.
- **Data.** More than 100 million clips curated from 50 million raw videos.

HeyGen's evaluation on 36 matched cases reports Sync-C 8.97 and face similarity 0.840 for Avatar V, against 8.86 / 0.823 for Seedance 2.0, 5.16 / 0.838 for Kling O3 Pro, 8.05 / 0.714 for Veo 3.1 and 7.53 / 0.732 for OmniHuman 1.5, with a ground-truth reference of 7.93 / 0.861 [1]. In an "Avatar Turing test", three annotators each judging 18 pairs mistook Avatar V for real footage 22.2% of the time [1] — a small sample. These are vendor numbers on a vendor-chosen test set; third-party write-ups repeat them without re-measuring [86]. Note that several generated systems exceed ground truth on Sync-C, which says more about the metric than about realism; the same caution applies to the Sync-C comparisons in Chapter 06. HeyGen also claims single-pass generation of up to 30 minutes on Avatar III, IV and V [4] (vendor claim).

The disclosure shows that HeyGen's flagship follows the same broad recipe as the open long-form models of Chapter 06 such as InfiniteTalk and Quark's LiveAvatar — a distilled, chunked, audio-conditioned video diffusion transformer. The differences it describes are also substantive: whole-clip reference attention, a dedicated motion stream, an identity-preserving cascade, preference tuning, a private backbone, far more curated data, and a large serving fleet. No matched quality comparison between Avatar V and any open model exists.

### Synthesia, D-ID, Mirage, Hedra

**Synthesia** disclosed the architecture of Express-2 (announced 2025-09-04 [76]) on a research page [11]: *Express-Animate*, an audio-to-gesture model; *Express-Eval*, a CLIP-like model that picks the best of several motion candidates; and *Express-Render*, a diffusion transformer distilled to two steps that produces 1080p30 video of arbitrary length at roughly 8 minutes of compute per minute of output (vendor claim). Express-3 followed on 2026-07-15 with more script-aligned gestures and "up to 2× faster" generation, without an architecture disclosure [12]. The same day Synthesia launched an Enterprise-only Interactive Avatar API, shipped as a LiveKit plugin in which the customer brings the language model and speech recognition [13]. Synthesia raised $200M at a roughly $4B valuation in January 2026 [15].

**D-ID** launched V4 "Expressive Visual Agents" in March 2026, described as "built on a new diffusion-based model and trained on performances captured from real actors", serving both live agents and scripted video, with a vendor-claimed turn latency under 0.5 seconds [16]. D-ID also advertises a **self-hosted** deployment: real-time avatars running in the customer's own cloud or network, sold as an annual licence that includes streaming minutes, through the AWS and Azure marketplaces, with a vendor-claimed render time under 200 ms [17]. It is the only explicit self-hosted product offer found among the major Western vendors (single source: D-ID's own page).

**Mirage** (Captions until its September 2025 rebrand) positions itself as a research lab built around a foundation model for UGC-style talking video that generates face, upper body and background from audio or script [25][26]; no live product was found. **Hedra**'s current base model, Omnia, is offered to partners for further training [23], and by late 2026 Hedra leads its site with model-training and inference infrastructure, pricing avatar and lip-sync output from 2.5¢ per second and quoting dedicated deployments per engagement [24].

## Live Conversational Avatars

HeyGen (LiveAvatar), Synthesia (Interactive Avatar API) and D-ID (V4) now sell live products alongside their offline video, competing with companies built for real time from the start: Tavus, Anam, Simli, Beyond Presence, bitHuman and LemonSlice. Soul Machines, an early pioneer of real-time digital humans, went into receivership in February 2026 and was acquired by AppDirect in September [37][38].

Few live vendors disclose their face model. The disclosures that exist suggest three approaches; the taxonomy is ours, built from a handful of vendor descriptions, and most products cannot yet be placed in it.

**Motion model plus renderer.** Anam's Cara-3 is the clearest disclosure: a flow-matching audio-to-motion model followed by a motion-to-face renderer, any face from one photo, about 70 ms to first frame on an H200 (vendor claim) [29]. Anam's current model, Cara-4.1 Express, outputs 1152×768 [31]; its architecture is not separately disclosed.

**Generated motion driving 3D Gaussian splats.** Simli says it builds "a full 3D avatar out of Gaussian splats on real geometry" from one photo, at about 150 ms audio-to-video (vendor claim) [27]. This uses the same rendering primitive as the custom 3DGS build Chapter 10 describes, though from a single photo rather than a studio capture. Tavus describes Phoenix only as "built on a Gaussian diffusion model" [18] — wording that is standard for any Gaussian-noise diffusion model; a press release seen only in search snippets during the research describes a 3DGS renderer, but that could not be verified, so Tavus's renderer is treated here as undisclosed.

**Large real-time video transformers.** LemonSlice describes LemonSlice-2.1 as a 20-billion-parameter model that animates any character, non-human included, at 20 fps from one photo; its site now leads with a newer model, CWM-1 [36]. Tavus's Griffin (research preview from 2026-10-01) goes further: a single full-duplex video-to-video model that listens and renders at once rather than chaining ASR, LLM, TTS and face. In Tavus's own live study, 48% of participants believed they were speaking with a real person [20] (vendor claim, not replicated).

| Vendor / product | Disclosed approach | Identity input | Latency figures | Price shape | Self-hosted |
|---|---|---|---|---|---|
| HeyGen LiveAvatar | undisclosed | ≥2 min footage [9] | 1.82 s / 2.58 s e2e median (Anam-run) [10] | 1–2 credits/min [9] | not found |
| Synthesia Interactive API | Express-3 | stock or personal avatar | 2.20 s e2e median, shared pipeline (Anam-run) [10] | Enterprise only [13] | not found |
| D-ID V4 | "diffusion-based" | photo or video | <0.5 s per turn (vendor) [16] | from $5.90/mo [16] | **yes**, licensed with streaming minutes [17] |
| Tavus Phoenix-4.5 | undisclosed ("Gaussian diffusion") [18] | photo or video [19] | 134 ms render (vendor) [22]; 1.86 s / 2.46 s e2e median (Anam-run) [10] | $22–$975/mo + $0.26–0.35/min overage (third-party summary) [79] | not found |
| Anam Cara-4.1 | motion + renderer (Cara-3 disclosure) [29] | one photo | ~70 ms first frame (Cara-3, vendor) [29]; 1.24 s / 2.12 s e2e median (own benchmark) [10] | $0.16→$0.11/min self-serve, volume from $0.04 [30] | not found |
| Simli | Gaussian splats [27] | one photo | ~150 ms (vendor) [27] | $0.009→$0.005/min [28] | not found |
| Beyond Presence Genesis 2.0 | undisclosed | photo or video | <100 ms vs 250 ms (contested, vendor) [32][33] | credits, from $49/mo [80] | not found |
| bitHuman Essence 2 | on-device renderer | one portrait | — | 2 credits/min even on your own machine [35] | on-device, metered [34][35] |
| LemonSlice-2.1 | 20B video model [36] | one photo | 471 ms p99 to first byte, 2.04 s e2e (vendor) [36]; 2.10 s / 2.70 s e2e median (Anam-run) [10] | — | not found |

### Why Latency Claims Do Not Compare

The figures in the table measure different things. "134 ms" or "150 ms" is the face renderer's own delay from audio to video. What a user experiences is the full turn: end of their speech, detection, transcription, language-model reply, speech synthesis, rendering, network. That is typically one to three seconds. Beyond Presence illustrates the gap within a single vendor: its homepage advertises under 100 ms [32], its documentation states 250 ms speech-to-video and about one second end-to-end [33].

The only cross-vendor end-to-end measurement found was published by Anam itself on 2026-10-16, and it contains two studies [10]. In the first (60 raters, 4,703 measured turns), each vendor ran its own default speech, language and voice pipeline, and median reply latencies were 1.24 s for Anam, 1.82 s for HeyGen LiveAvatar, 1.86 s for Tavus Phoenix-4.5 and 2.10 s for LemonSlice. In the second, every vendor ran the *same* pipeline (Deepgram Nova-3 speech recognition, GPT OSS 120B on Groq, Cartesia Sonic-3.6), and the medians bunched together: Anam 2.12 s, Synthesia 2.20 s, Tavus 2.46 s, HeyGen 2.58 s, LemonSlice 2.70 s, with Anam's advantage over Synthesia not statistically established. LemonSlice's self-reported 2.04 s end-to-end figure [36] agrees with the 2.10 s Anam measured for it in the first study — the closest thing to a two-source latency number in this market — while LemonSlice in turn claims to be the fastest from the 75th through 99th percentile, ahead of Tavus and Anam [36].

Read together, the two studies suggest that the difference between vendors' default stacks — their choice of speech recognizer, language model and voice — accounts for much of the spread in turn latency, and the face model for less. None of the measured products came near a 500 ms turn; D-ID claims sub-0.5-second turns [16] but was not measured. The benchmark is competitor-run and should be read as such, but it is the right *kind* of measurement: end-to-end, many turns, and — in its second study — with the pipeline held constant.

**Self-hosting and data residency.** Of the major Western vendors, only D-ID advertises a self-hosted product [17]; bitHuman renders on the device (iOS, Android, or in-process through its Python SDK) but still meters those sessions [34][35]; Hedra quotes dedicated deployments per engagement [24]; and Avaturn has released its real-time model as open source [78]. No self-hosting offer was found for HeyGen, Synthesia, Tavus, Anam, Simli, Beyond Presence or LemonSlice. Regional hosting, which is what most data-residency requirements actually ask for, was not researched. Buyers who need the model on their own hardware are pushed toward D-ID or the open stacks below.

**What vendors do not say.** No Western vendor was found stating that its product is built on MuseTalk, LivePortrait, Wan or another open model. The one closed product whose internals have been reverse-engineered — Duix-Avatar, below — was reported to use an open 2023 research model. Whether open components sit inside the Western products is unknown.

## Duix and the Chinese Digital-Human Ecosystem

**The company.** Duix is a brand of Nanjing Silicon Intelligence Technology (南京硅基智能), founded in 2017. It submitted a Hong Kong listing application on 2025-10-31 [81]; that filing lapsed at the end of April 2026 and was refiled in May 2026 [48][49]. The prospectus coverage reports revenue of RMB 531M, 655M and 789M for 2023–2025, a cumulative net loss of about RMB 233M over those years, a customer count that fell from 1,009 to 431, and a 32.2% share of China's digital-human agent market by 2024 revenue according to CIC data commissioned for the prospectus (vendor claim) [48]. Its open-source repositories moved from the GuijiAI GitHub organization to `duixcom` and were renamed: HeyGem.ai became Duix-Avatar, and duix.ai became Duix-Mobile [82].

**Duix-Avatar (formerly HeyGem)** is the project most people mean by "Duix". It is an *offline* video generator with voice cloning — its own README describes "non-real-time video synthesis" and sends interactive users to the paid cloud [39]. It has about 16,200 GitHub stars but has seen no release since September 2025 [82]. Three facts matter:

- *Only the client is open.* The open repository is an Electron desktop app. The face, speech-recognition (FunASR) and speech-synthesis (Fish-Speech) services ship as Docker images — a roughly 70 GB download needing more than 100 GB of disk [39] — containing compiled Cython modules [42][43]. Complaints that the "open source" release ships encrypted binaries recur in the issue tracker [50].
- *The face engine is reportedly DINet.* A community decompilation of those compiled modules [42] — of binaries and weights published by a second community extraction [43] — reports that the face engine is DINet, a lip-sync model published at AAAI 2023 [85], working on a 256-pixel face crop with optional GFPGAN restoration. The weight file's name, `dinet_v1_20240131.pth`, points the same way. Duix has never confirmed this; it rests on one decompile.
- *A "clone" involves no training.* It is the user's reference video, re-lip-synced [42], plus a zero-shot voice prompt for Fish-Speech [39]. This is the template re-lip-sync family, not a generator.

**The licences contradict each other.** The README offers "global free commercial use" except for firms above 100,000 users or US$10M annual revenue [39]. The repository LICENSE requires a commercial licence, granted at Duix's sole discretion, above 1,000 monthly active users, plus attribution and naming conditions [40]. The bundled model licence, which names a specific model version ("Duix.Avatar:0.0.7_sdk_slim"), permits non-commercial use only, requires written authorization for any commercial use, asserts no rights over the generated output, and is governed by PRC law [41]. A team considering Duix-Avatar for a product should treat the most restrictive of the three as binding until Duix says otherwise in writing.

**Duix-Mobile** is an on-device SDK for Android and iOS that plays a per-identity 2D avatar on the CPU; the maintainer describes inference as "pure CPU" [45]. Each avatar is a base model fine-tuned on one to two minutes of video, the training code is not open, and custom avatars are made by Duix on request [44][45]. Its latency is stated inconsistently: under 120 ms on a Snapdragon 8 Gen 2 in the README [44], under 1.5 s in the repository description [82].

**Duix cloud** is a server-rendered avatar API streamed over WebRTC [47], priced per conversation minute from $29/month for 150 minutes to $4,999/month for 60,000 minutes [46], with a vendor-claimed 200 ms time to first byte [83]. A newer "duix-skills" package builds a conversational avatar web page from a single portrait [73]. The model behind it is undisclosed.

**A recurring pattern.** Alibaba's LiteAvatar has the same shape as Duix-Mobile: a 2D mouth-parameter model that runs at a vendor-claimed 30 fps on CPU, MIT-licensed code with an unspecified weights licence, training scripts that will not be released, and custom avatars offered through Alibaba Cloud [54]. In both projects examined here, "open source" means *open client or SDK, closed weights or closed training*, and the identity-creation step is where the business model lives. Whether this holds across the wider Chinese market was not researched.

## Open Real-Time Stacks

A second tier of genuinely open projects assembles the live-avatar pipeline from open parts. None publishes independent latency measurements; every figure below is from the project's own README or from user reports in its issue tracker.

**LiveTalking** (formerly metahuman-stream; Apache-2.0, about 10,300 stars, active through October 2026 [82]) is the most-starred open engine [51]. Its open edition lists three face back-ends — Wav2Lip-256, MuseTalk and Ultralight-Digital-Human — all template re-lip-sync models over a prepared video of the person, although an older part of the README still lists ER-NeRF [51]. Its own figures give Wav2Lip 60 fps on an RTX 3060 and MuseTalk 72 fps on an RTX 4090 [51]. One user reported about three seconds of lag when interrupting the avatar, because buffered WebRTC frames and in-flight inference were not flushed; later commenters report patches bringing it to 0.5–1.5 s [52]. Interruption handling, not frame rate, is where that thread shows the engineering effort going.

**OpenAvatarChat** (Alibaba, Apache-2.0, about 3,800 stars [82]) is the cleanest modular design: Silero VAD, SenseVoice ASR, any LLM or Qwen-Omni end-to-end, CosyVoice TTS, and a choice of four avatar back-ends — LiteAvatar (CPU 2D), LAM (a single-image 3D Gaussian head rendered in WebGL [55]), MuseTalk, and SoulX-FlashHead [53]. It reports an average response time of 2.2 s (vendor claim) [53], consistent with the commercial end-to-end figures above.

**Others.** Linly-Talker and its 2026 streaming successor Linly-Talker-Stream (small, early) follow LiveTalking's design [71]. Fay is an orchestrator only — agents, ASR, TTS, memory — that drives an external face model [72]. For stylized characters, the Live2D path of Chapter 02 remains the cheapest live avatar of all.

The open options sort into three hardware tiers, which is the useful way to choose between them:

| Tier | Face model | Hardware | Identity creation | Examples |
|---|---|---|---|---|
| CPU / mobile 2D player | per-identity 2D model | phone or CPU | closed, vendor-made | Duix-Mobile, LiteAvatar |
| GPU template re-lip-sync | Wav2Lip, MuseTalk, DINet (reported) | one consumer GPU | your own video, no training | LiveTalking, Duix-Avatar (offline) |
| One-shot streaming generator | distilled video DiT | consumer GPU (head only) to multi-GPU datacentre | one photo | SoulX-FlashHead, Quark LiveAvatar, SoulX-FlashTalk |

MuseTalk 1.5 is the commercially cleanest choice in the middle tier: MIT code with weights usable commercially [56], though its dependencies (Whisper, the VAE, DWPose, S3FD) carry their own licences, which a product team must check as well.

## Building One on Open Weights: The Wan Question

Most open avatar models released since mid-2025 are built on Alibaba's **Wan** video models (Chapter 06 covers them as methods). The question here is the product one: could a team build a HeyGen- or Duix-like service on them?

**What is open.** Every open Wan checkpoint is Apache-2.0: Wan 2.1, Wan 2.2, Wan2.2-S2V (Alibaba's own audio-to-video model), Wan2.2-Animate and Wan-Animate-2 [61]. The later flagship versions — Wan 2.5, 2.6, 2.7 and 3.0 — are available only through Alibaba's API [87] (Wan 2.6 reference-to-video costs roughly $0.09–0.10 per second at 720p [62]), and no weights were found for Alibaba's end-to-end real-time interactive model, Wan-Streamer [63]. The open foundation therefore stops at the 2.2 generation. Most Wan-derived avatar models carry permissive licences — InfiniteTalk, MultiTalk, OmniAvatar, EchoMimicV3, Quark LiveAvatar and SoulX-FlashTalk are Apache-2.0 and StableAvatar is MIT (Chapter 06, *Open-Weight Presenter Models*, has the per-model sources) — but not all: Snap's TalkVerse is non-commercial, and SoulX-FlashHead Lite bundles a VAE under OpenRAIL-M [57]. Among the non-Wan alternatives, Meituan's LongCat-Video-Avatar is MIT [89]; Kandinsky S2V's code is MIT while its weights carry their own model-card licences [75]; and Tencent's HunyuanVideo-Avatar is licensed for use everywhere except the European Union, the United Kingdom and South Korea [88] — a hard stop for European products.

**For the Wan generator tier, licences are mostly permissive and compute is the constraint.** The one independent cross-model benchmark found — Tight Studio's August 2026 run of the official pipelines with pinned versions [64][65] — found that no pipeline generated faster than playback on a cold job. Its limits matter: one AI-generated portrait, one English voice, one 3.63-second clip, one seed, and timings that include container start-up, model loading and compilation.

| Model | GPU | Seconds of compute per output second (cold) | Notes |
|---|---|---|---|
| Wan2.2-S2V | 1×H200 | 204.6 | slowest; restrained motion |
| SoulX-FlashTalk | 1×H200 | ≈91 | warm chunks about 3.75 s each after compilation |
| EchoMimicV3-Flash | 1×L40S | ≈70 | best value; 33.7 GB in the official configuration (the project advertises a 12 GB mode) |
| LongCat-Video-Avatar 1.5 | 1×H200 | ≈65 | most expressive, added a hand gesture; exaggerated mouth shapes (its authors claim parity with HeyGen and OmniHuman 1.5 [74]) |
| Quark LiveAvatar (offline mode) | 1×H200 | 48.8 | sharpest identity among the large models |
| SoulX-FlashHead Lite | — | first chunk 155.7 s (compilation), then about 0.19 s per chunk | 5.8 GB; softer identity, weaker mouth |

Because these are cold runs of a few seconds of output, they overstate the steady-state cost of a warm server by an unknown but probably large factor. No measured speed on a named GPU was found for InfiniteTalk, the most-used long-form model, with or without the 4-step distillation LoRA its README supports [66].

**Real time exists, at a hardware floor.** Distilling 14B Wan models into causal few-step students (Self-Forcing / DMD style) produced the first open streaming avatar generators, all with author-reported figures only: Quark LiveAvatar at 45 fps on 5×H800 with 1.21 s to first frame [59], SoulX-FlashTalk at 32 fps on 8×H800 [58], and SoulX-LiveAct at 20 fps on 2×H100 [60]. These are throughput figures; time to first frame is still over a second. On a single consumer GPU only the 1.3B models qualify: SoulX-FlashHead Lite claims 96 fps on an RTX 4090 [57], producing 512×512 head-only video that Tight found visibly softer than the large models [64]. A known failure mode of these distilled students is collapse toward static motion [70].

**What it costs.** Tight's cold runs translate, at public GPU list prices [69], into roughly $3.5 (EchoMimicV3-Flash) to $21.5 (Wan2.2-S2V) per output minute — an upper bound, since they include start-up and compilation. Real-time streaming on the large distilled models works out — by arithmetic on author throughput and on-demand H100 list prices, not by measurement — at roughly $0.13 (LiveAct on 2×H100) to $0.53 (FlashTalk on 8×H100, standing in for the authors' H800s) per stream-minute, and about a cent for FlashHead Lite if three streams share an L40S-class GPU. Hosted InfiniteTalk ranges from $1.80–3.60 per minute (WaveSpeed) to $12–24 (fal) [67][68]. Vendor prices for comparison: Simli sells live minutes at under a cent [28], Anam at $0.11–0.16 self-serve [30], Tavus overage at $0.26–0.35 [79]. Prices are not costs — vendors reserve capacity below list price and may price below cost — but Simli's price is hard to reconcile with multi-GPU diffusion per stream, while Anam's and Tavus's prices are not; and LemonSlice says it runs a 20B model per stream [36].

**A possible design.** The following is this review's proposal, not a description of any vendor's system:

1. Use a Wan-based generator (InfiniteTalk, Wan2.2-S2V or Quark LiveAvatar in offline mode; LongCat as the expressive non-Wan option) for high-quality *offline* presenter video, where minutes or more of GPU time per clip are acceptable.
2. Use the same generator once per identity to produce template footage — idle loops, listening poses, gestures.
3. For the *live* mode, run a cheap real-time model over those templates: MuseTalk-class re-lip-sync on one consumer GPU, or a one-shot streaming head model like FlashHead where a single photo must suffice.

This puts generator quality where latency does not matter and template economics where it does. HeyGen's split between offline Avatar V and a separately priced LiveAvatar that needs two minutes of footage is consistent with something like it, but HeyGen does not disclose how LiveAvatar works. The design has a known product risk: a 1080p generated offline video and a 256-pixel re-lip-synced live stream will not look like the same person at the same quality, and users will notice the switch.

**Risks.** Alibaba stopped releasing flagship Wan weights after 2.2, so a product built today stays on that backbone unless another lab releases a successor. No independent test of long-form drift beyond one minute exists for any open model, and no independent verification of any real-time figure. Lip-sync quality outside English and Chinese is untested. Consent and likeness rights for cloned identities, and the provenance of the models' training data, were outside this survey's scope but are live legal questions for any avatar product.

## What the Product World Tells the Rest of the Review

**The architectural recipe has converged; whether quality has is unmeasured.** HeyGen's disclosed Avatar V and the open Quark LiveAvatar and InfiniteTalk are the same broad kind of system — a distilled, chunked, audio-conditioned video diffusion transformer. HeyGen's disclosure also lists real differences, and no matched comparison of commercial and open output exists. A shared benchmark that includes both would settle it.

**3DGS has reached at least one commercial product.** Simli describes a Gaussian-splat avatar built from one photo [27] — the "photo-to-real-time-3DGS-avatar" product that Chapter 14 predicts, if its description is accurate. Tavus's wording is ambiguous. Neither vendor uses the open FLAME-rigged pipelines the research literature describes, as far as either discloses.

**Latency needs a shared definition.** The field reports render latency and calls it response latency. Anam's shared-pipeline study suggests the face model is a minor part of turn latency. A buyer or a benchmark should ask for end-to-end turn latency under interruption, measured by someone other than the seller, with the speech and language pipeline held constant.

**"Open source" needs reading closely.** Open client, closed weights; open weights, closed training; open code, unspecified weights licence; three contradictory licence documents in one repository; a licence that excludes Europe. The licence and the identity-creation path matter more than the star count.

## Open Questions

- Which open components, if any, run inside the Western commercial products.
- An independent, cross-vendor, end-to-end latency benchmark under interruption, and a quality comparison of commercial and open output on matched inputs.
- Measured warm-server speed and cost for InfiniteTalk and the distilled Wan models on named GPUs.
- Long-form drift beyond one minute for any open model, measured independently.
- What model powers Duix cloud and duix-skills, and whether the DINet identification of Duix-Avatar is correct.
- The large Chinese commercial digital-human vendors and livestream-commerce deployments, which this chapter does not cover.
- Regional hosting and data-residency options for the cloud vendors.
- Whether Synthesia's hosted interactive pipeline, announced for 2026-10-01 [13], shipped.

## References

All sources were retrieved on 2026-11-04. The saved copy of each is in `docs/research/sources/text/<slug>.txt`; GitHub API snapshots are in `docs/research/agents/duix-realtime/gh/`. The full dossiers are `docs/research/agents/commercial/report.md`, `docs/research/agents/duix-realtime/report.md` and `docs/research/agents/oss-avatar/report.md`; the audit of this chapter is in `docs/research/agents/audit/`.

[1] HeyGen. "Avatar V Technical Report." `dynamic.heygen.ai/www/Paper%20Links/avatarv_tech_report.pdf`. Saved: `heygen-avatarv-tech-report`.

[2] HeyGen. "Avatar V model" (research page, dated 2026-04-08). `heygen.com/research/avatar-v-model`. Saved: `heygen-research-avatar-v`.

[3] HeyGen. "Announcing Avatar V." `heygen.com/blog/announcing-avatar-v`. Saved: `heygen-com-blog-announcing-avatar-v`.

[4] Releasebot. HeyGen release feed. `releasebot.io/updates/heygen`. Saved: `releasebot-io-updates-heygen`.

[5] HeyGen. "HeyGen May 2026 release." `heygen.com/blog/heygen-may-2026-release`. Saved: `heygen-com-blog-heygen-may-2026-release`.

[6] HeyGen. API models documentation. `developers.heygen.com/models`. Saved: `developers-heygen-com-models`.

[7] HeyGen Help. "HeyGen credit-based pricing plans explained." Saved: `help-heygen-com-en-articles-15125761-heygen-credit-based-pricing-plans-explained`.

[8] HeyGen Help. "New feature alert: HeyGen Avatar IV is here." Saved: `help-heygen-com-en-articles-11269603-new-feature-alert-heygen-avatar-iv-is-here`.

[9] HeyGen Help. "How to get started with LiveAvatar." Saved: `help-heygen-com-en-articles-10035615-how-to-get-started-with-liveavatar`.

[10] Anam. "Latency benchmark" (two studies, 2026-10-16). `anam.ai/tools/latency-benchmark`. Saved: `anam-ai-tools-latency-benchmark`.

[11] Synthesia Research. "Express" video models. `synthesiaresearch.github.io/express-video`. Saved: `synthesiaresearch-github-io-express-video`.

[12] Synthesia. Express-3 launch post (2026-07-15). Saved: `synthesia-io-post-synthesia-launches-new-ai-assistant-for-faster-video-creation-and-expres`.

[13] Synthesia. "Interactive Avatar API: real-time avatars." Saved: `synthesia-io-post-interactive-avatar-api-real-time-avatars`.

[14] Synthesia. Pricing. `synthesia.io/pricing`. Saved: `synthesia-io-pricing`.

[15] Built In. "Synthesia raises $200M Series E." Saved: `builtin-com-articles-synthesia-raises-200m-series-e-20260126`.

[16] eLearning Industry (D-ID press release). "D-ID launches V4 Expressive Visual Agents." Saved: `elearningindustry-com-press-releases-d-id-launches-v4-expressive-visual-agents-for-real-ti`.

[17] D-ID. "Self-hosted Expressive Avatars." `d-id.com/self-hosting-realtime-avatars/`. Saved: `d-id-com-self-hosting-realtime-avatars`.

[18] Tavus. Models documentation. `docs.tavus.io/sections/models`. Saved: `docs-tavus-io-sections-models`.

[19] Tavus. Replica overview. `docs.tavus.io/sections/replica/overview`. Saved: `docs-tavus-io-sections-replica-overview`.

[20] Business Wire via Morningstar. "Tavus introduces Griffin." Saved: `morningstar-com-news-business-wire-20261001092598-tavus-introduces-griffin-the-first-face-`.

[21] Reference removed during audit: the saved Tavus pricing page (`tavus-io-pricing`) contains no prices; see [79].

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

[45] Duix-Mobile issue tracker (maintainer replies in issues 2, 4, 19). Saved: `gh/duixcom-Duix-Mobile-issue-4.json` and related issue snapshots.

[46] Duix. Pricing. `duix.com/pricing`. Saved: `duix-com-pricing`.

[47] Duix. Android SDK quickstart. `docs.duix.com/sdks/android/quickstart.md`. Saved: `docs-duix-com-sdks-android-quickstart-md`.

[48] 36Kr. Silicon Intelligence prospectus coverage. `36kr.com/p/3825797690614017`. Saved: `36kr-com-p-3825797690614017`.

[49] HKEXnews. Silicon Intelligence application proof, May 2026 (cover). Saved: `www1-hkexnews-hk-app-sehk-2026-108560-a133153-sehk26052101556-pdf`.

[50] Duix-Avatar issue tracker. Saved: `gh/duixcom-Duix-Avatar-issues-top-comments.json`, `gh/duixcom-Duix-Avatar-issue-243.json`.

[51] lipku. LiveTalking README. `github.com/lipku/LiveTalking`. Saved: `raw-githubusercontent-com-lipku-livetalking-main-readme-md`.

[52] LiveTalking issue #510. Saved: `gh/lipku-LiveTalking-issue-510.json`.

[53] HumanAIGC-Engineering. OpenAvatarChat README. Saved: `raw-githubusercontent-com-humanaigc-engineering-openavatarchat-main-readme-md`.

[54] HumanAIGC. LiteAvatar README and issues 3, 24 and 27. Saved: `raw-githubusercontent-com-humanaigc-lite-avatar-main-readme-md`, `gh/HumanAIGC-lite-avatar-issue-3.json`, `gh/HumanAIGC-lite-avatar-issue-24.json`, `gh/HumanAIGC-lite-avatar-issue-27.json`.

[55] aigc3d. LAM README. Saved: `aigc3d-lam-readme`.

[56] TMElyralab. MuseTalk README. Saved: `raw-githubusercontent-com-tmelyralab-musetalk-main-readme-md`.

[57] Soul AI Lab. SoulX-FlashHead README and Hugging Face model card. Saved: `gh-soulx-flashhead-readme`, `hf-soulx-flashhead-card`.

[58] Soul AI Lab. SoulX-FlashTalk README and paper (arXiv 2512.23379). Saved: `gh-soulx-flashtalk-readme`, `arxiv-2512.23379-soulx-flashtalk`.

[59] Alibaba Quark. LiveAvatar README and paper (arXiv 2512.04677). Saved: `gh-liveavatar-readme`, `arxiv-2512.04677-liveavatar`.

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

[76] Synthesia. "Express-2 is Synthesia's next chapter for full-body expressive AI avatars" (2025-09-04). Saved: `synthesia-io-post-express-2-is-synthesias-next-chapter-for-full-body-expressive-ai-avatars`.

[77] Synthesia. "Synthesia 3.0: the next era of video." Saved: `synthesia-io-post-synthesia-3-0-the-next-era-of-video`.

[78] Avaturn Live. Homepage (AVTR-1 open-source announcement). `avaturn.live`. Saved: `avaturn-live`.

[79] UsagePricing. "Tavus pricing blueprint" (third-party summary of Tavus plans). Saved: `usagepricing-com-blueprint-tavus`.

[80] MakerStack. "Beyond Presence review." Saved: `makerstack-co-reviews-beyond-presence-review`.

[81] Tiger Brokers news. Silicon Intelligence files for Hong Kong IPO (2025-10-31). Saved: `itiger-com-news-1160799526`.

[82] GitHub API snapshots: repository metadata, renames and releases for Duix-Avatar, Duix-Mobile, LiveTalking and OpenAvatarChat. Saved: `gh/duixcom-Duix-Avatar.json`, `gh/GuijiAI-HeyGem.ai.json`, `gh/duixcom-Duix-Mobile.json`, `gh/GuijiAI-duix.ai.json`, `gh/duixcom-Duix-Avatar-releases.json`, `gh/lipku-LiveTalking.json`, `gh/HumanAIGC-Engineering-OpenAvatarChat.json`.

[83] Duix. Homepage. `duix.com`. Saved: `duix-com`.

[84] Reference removed during audit.

[85] Zhang, Z. et al. "DINet: Deformation Inpainting Network for Realistic Face Visually Dubbing on High Resolution Video." AAAI 2023. arXiv 2303.03988. Saved: `arxiv-2303.03988-dinet`.

[86] The Planet Tools. "HeyGen Avatar V tested: hands-on review 2026." Saved: `theplanettools-ai-blog-heygen-avatar-v-tested-hands-on-review-2026`.

[87] Atlas Cloud. Wan 3.0 open-source status. Saved: `atlascloud-wan3-open-source`.

[88] Tencent. HunyuanVideo-Avatar LICENSE. Saved: `gh-hunyuanvideo-avatar-license`.

[89] Hugging Face. LongCat-Video-Avatar 1.5 model metadata (licence: MIT). Saved: `hf-api-meituan-longcat-longcat-video-avatar-1.5`.
