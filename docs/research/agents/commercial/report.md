
---
status: draft
last-verified: 2026-11-04
owner: commercial-vendors research agent (extracted verbatim from its hand-back by the main session; harness blocked its Write) (for Ch11 "Enterprise and Digital Human Market")
scope: HeyGen latest avatar models plus commercial competitors. Excludes open-source Chinese real-time stacks, Duix, and research papers already in Ch06.
---

# Commercial talking-head and digital-human vendors: dossier (as of 2026-11-04)

## How to read this
- `[N]` points to the Sources list. Each source is saved at `docs/research/sources/text/<slug>.txt`, with the raw copy and card alongside. All were fetched on 2026-11-04.
- Evidence labels:
  - **Confirmed**: two or more independent sources agree.
  - **Single-source**: only the vendor, or only one outlet.
  - **Contested**: sources disagree; both sides are given.
- Vendor numbers are marked **(vendor claim)**. A benchmark one vendor runs against its competitors is still a vendor claim.

## Headline findings
1. **"HeyGen v5" means Avatar V**, HeyGen's fifth-generation avatar engine. The technical report and blog are dated **2026-04-08** [1][2][3]. The "Announcing Avatar V" post appears in the release feed around **2026-05-04** [4]. The Avatar V API arrived in May 2026 at **$0.05 per second** [5]. The public API is **v3**: `POST /v3/videos` with `engine` set to `avatar_iii`, `avatar_iv` or `avatar_v` [6]. No "v5 API" exists. Confirmed.
2. **Avatar V is the most detailed technical disclosure by any commercial avatar vendor.** It is a diffusion transformer (DiT) trained with flow matching. It conditions on the reference video through Sparse Reference Attention. It has a motion-representation stream and an identity-aware super-resolution refiner. Training has five stages: text-to-video pretraining, audio-to-video pretraining, "personality" fine-tuning, CFG and DMD distillation (more than 10x faster), and RLHF using GRPO and DPO. It is served on 5,000+ GPUs with 8-GPU Ulysses sequence parallelism, 24 sampling steps and 6.4 s chunks [1][2]. Single-source (the vendor's report).
3. **The offline leaders have all moved to diffusion or DiT renderers.**
   - Synthesia Express-2 (2025-09-04) uses Express-Animate (audio to motion), Express-Eval (a CLIP-like selector) and Express-Render (a DiT distilled to 2 steps, about 8 minutes of compute per minute of 1080p30) [16]. Express-3 followed on 2026-07-15 [18].
   - D-ID V4 is "diffusion-based" [26].
   - Mirage (formerly Captions) is a foundation video model [43][44].
4. **Every major offline vendor now ships real-time streaming.**
   - HeyGen LiveAvatar (Oct 2025) [4][10].
   - Synthesia Interactive Avatar API (2026-07-15, Enterprise, LiveKit plugin, bring your own LLM, STT and TTS) [20].
   - D-ID V4 Visual Agents [26].
   - DeepBrain AI STUDIOS real-time agents (2026-04-28) [71].
5. **The real-time architectures fall into three families** (vendor disclosures):
   - Audio-to-motion (flow matching) plus a separate renderer: Anam Cara-3, about 70 ms time-to-first-frame on an H200 [50].
   - Diffusion-generated motion driving **3D Gaussian Splatting**: Tavus Phoenix-4 [33], and Simli, which builds Gaussian splats on real geometry from one photo [46].
   - Large real-time video DiTs: LemonSlice-2 (20B parameters, 20 fps) [70], and Tavus Griffin (full-duplex video-to-video, preview since 2026-10-01) [35].
6. **Latency claims are not comparable.**
   - Render-only figures: Simli about 150 ms [46], Tavus 134 ms [31], Beyond Presence under 100 ms [63], D-ID self-hosted under 200 ms [30].
   - End-to-end is 1–2 s. Anam's own benchmark (60 raters, 4,703 turns, 2026-10-16) gives medians of Anam 1.24 s, HeyGen LiveAvatar 1.82 s, Tavus Phoenix-4.5 1.86 s and LemonSlice 2.10 s [15]. This is vendor-run, so a vendor claim.
   - Beyond Presence contradicts itself: "<100 ms" on the homepage [63] against "250 ms speech-to-video, 1 s end-to-end" in the docs [64]. Contested.
7. **Soul Machines went into receivership in February 2026, not 2025.** KPMG receivers were appointed on 2026-02-05 [52]. The founders had left by mid-2024 [53]. AppDirect announced the acquisition on 2026-09-28, terms undisclosed [54][55][56]. Confirmed.
8. **On-prem is rare.** I found three cases:
   - D-ID self-hosted Expressive Avatars: your own cloud or data centre, annual licence, sold through the AWS and Azure marketplaces [30].
   - bitHuman on-device rendering, including CPU-only, though still metered [59][61].
   - Avaturn AVTR-1, described as open-sourced [72].

   I found no on-prem evidence for HeyGen, Synthesia, Tavus, Anam, Simli, Beyond Presence or LemonSlice. That does not prove they have none.
9. **No vendor publicly says it builds on MuseTalk, LivePortrait or similar.** HeyGen cites Wan, CogVideoX and HunyuanVideo only as related work, and it uses its own text-to-video pretrain [1]. Hedra describes its approach as "open core" base models [38].

## HeyGen

| Engine | Date | Input | Notes |
|---|---|---|---|
| Avatar III | earlier | video twin, or photo pipeline | API calls it the "photo-to-video pipeline, 4K" [6]. Unlimited on paid plans [4]. |
| Avatar IV | May 2025 (community post 2025-05-01 per snippet; launch coverage 2025-05-06/07) | one photo plus script or audio, or a video look | "diffusion-inspired audio-to-expression engine" [8]. Default API engine [6]. 16 credits/min (photo look), 31 credits/min (video look) [7]. |
| **Avatar V** | report and blog 2026-04-08 [2][3]; feed post 2026-05-04 [4]; API May 2026 [5] | 15 s phone or webcam recording [3][13]; voice clone from about 10 s of audio [2] | 48 credits/min [7]; API $0.05/s [5]; opt-in per look [6]; "Custom Motion" text direction added May 2026 [5]. |
| LiveAvatar | Oct 2025 [4] | at least 2 min of continuous 1080p footage in 3 parts; earlier footage cannot be reused [10] | WebRTC. Separate account and credits [11]. |
| Avatar Realtime API (Broadcast) | mid-2026 [4] | existing avatar | Live streaming agent shown on a 24/7 Twitch stream. Single-source. |

**Avatar V technology** [1][2] (Single-source, not peer reviewed):
- **Backbone:** HeyGen's own text-to-video and image-to-video DiT, adapted to audio-to-video with audio cross-attention, then fine-tuned on same-identity, different-scene pairs.
- **Identity:** Sparse Reference Attention gives every layer the full reference-video tokens. HeyGen says cost is "almost linear" in reference length, allowing "minutes-long reference footage". The 15 s product minimum is a floor.
- **Talking style:** a motion representation used both as a training objective and as conditioning.
- **Pipeline:**
  - An Identity-Preserving Image Engine sets up the scene.
  - The base DiT renders at low resolution, and an identity-aware super-resolution refiner on the same backbone upscales to 1080p.
  - An LLM-based TTS engine feeds the motion encoder.
- **Inference:**
  - Chunked autoregressive generation: 41 latent frames = 161 frames at 25 fps ≈ 6.4 s per chunk, with a prefix bridge and a global appearance anchor.
  - 24 steps with a stochastic Euler sampler.
  - Reference tokens are KV-cached.
  - Ulysses sequence parallelism across 8 GPUs with NVSHMEM, plus a custom compiler.
  - Runs on 5,000+ GPUs.
- **Data:** 100M+ clips curated from 50M raw videos.
- **Evaluation** (36 matched cases, HeyGen's own benchmark):

  | System | Sync-C | Face Sim |
  |---|---|---|
  | Avatar V | 8.97 | 0.840 |
  | Seedance 2.0 | 8.86 | 0.823 |
  | Kling O3 Pro | 5.16 | 0.838 |
  | Veo 3.1 | 8.05 | 0.714 |
  | OmniHuman 1.5 | 7.53 | 0.732 |
  | Ground truth | 7.93 | 0.861 |

  Avatar V wins 68.9–85.7% of pairwise human comparisons. In an "Avatar Turing test", annotators mistook its output for real video 22.2% of the time (3 annotators × 18 pairs). All **(vendor claim)**. Third parties [13][14] repeat these numbers without measuring them.
- **Long-form:** HeyGen claims 30 minutes of continuous video in a single pass on Avatar III, IV and V **(vendor claim)** [4].

**LiveAvatar:**
- Full mode is 2 credits/min and Lite mode (bring your own LLM and voice) is 1 credit/min [10].
- No 4K output "due to latency limitations" [10].
- In September 2026 HeyGen published MIT-licensed demos wiring OpenAI's GPT-Live-1 to LiveAvatar [4].
- Anam's competitor-run benchmark measured 1.82 s end-to-end [15].
- The $99/month Essential plan figure comes only from third parties; the LiveAvatar pricing URL returned 404.

**Pricing shape:** credit plans, in which Avatar IV and V are "premium" and Avatar III is unlimited [4][7]. The v3 API is pay-as-you-go [6].
**On-prem:** none found. **Last verified:** October 2026 [3][4].

## Synthesia
- **Express-1:** a custom "Studio Express-1" avatar is a $1,000/year add-on and takes up to 10 days [23].
- **Express-2** (2025-09-04) [16][17]. Confirmed.
  - **Express-Animate:** audio-to-gesture foundation model.
  - **Express-Eval:** CLIP-like model that picks the best of N motion candidates.
  - **Express-Render:** DiT producing 1080p30 of arbitrary length, distilled to 2 steps.
  - About 8 minutes of compute per minute of video **(vendor claim)**. A "Turbo" version was promised [16].
- **Synthesia 3.0** (October 2025): Video Agents that hold real-time conversations, and personal avatars from a single image [21][22].
- **Express-3** (2026-07-15):
  - More script-aligned gestures and "up to 2x faster" generation **(vendor claim)**.
  - Staged rollout, starting with stock avatars.
  - Also powers stylised Style Avatars made from a prompt [18][19].
  - No architecture disclosed.
- **Interactive Avatar API** (2026-07-15, Enterprise only) [20]:
  - Ships as the LiveKit plugin `livekit-plugins-synthesia`. You bring your own LLM and STT; TTS is optional.
  - A hosted LLM + TTS + avatar pipeline was promised for 2026-10-01; I found no confirmation.
  - No latency figure published.
- **Pricing:**
  - Free tier: 10 min/month. Paid tiers add about 12 or 60 min/month, plus an unlimited Enterprise tier.
  - 3, 5 or unlimited personal avatars by tier.
  - API: 360 min/year included [23].
- **Funding:** $200M Series E at about $4B, led by GV, 2026-01-26 [24][25]. Confirmed.
- **On-prem:** none found. **Last verified:** 2026-10-20.

## D-ID
- **V4 Expressive Visual Agents** (2026-03-16/17) [26][27]:
  - "Built on a new diffusion-based model and trained on performances captured from real actors."
  - Under 0.5 s per conversational turn and output up to 4K **(vendor claim)**. The Jerusalem Post repeats this from D-ID's own benchmark tests.
  - Handles both real-time agents and long-form scripted video. Optional camera-based sentiment awareness; inline UI elements.
  - Available on all plans, from $5.90/month.
- **Scale (vendor claims):** 1,500 enterprise customers, 800k visual agents, 300M avatar videos. ARR up 250% after acquiring simpleshow in September 2025 [26].
- **Self-hosted Expressive Avatars** [30]. Single-source, and the clearest on-prem offer I found.
  - Runs in your own cloud or private network; "nothing is sent to D-ID".
  - Renders in under 200 ms **(vendor claim)**.
  - Annual licence that includes streaming minutes, sold through the AWS and Azure marketplaces, with forward-deployed engineers.
- **Pricing:**
  - Minutes plans, with usage rounded up to 15 s. API usage draws on the same balance [29].
  - The API pricing page is JS-only, so I could not read its figures.
- Anam publishes a competitor critique of V4 [28].

## Tavus
- **Phoenix (rendering):**
  - Phoenix-4 launched February 2026. The docs say it is "built on a Gaussian diffusion model" [33].
  - The press release (seen only in search snippets; BusinessWire returned 403) says denoised motion coefficients drive a 3D Gaussian Splatting renderer, trained on thousands of hours of conversation.
  - Phoenix-4.5 is current. It works zero-shot from one image, with fuller training from video [32][34].
  - Gaussian diffusion: Confirmed (docs plus press). The 3DGS detail: Single-source.
- **Raven (perception):** Raven-1 (February 2026) is the default. Raven-2 adds camera and screen timelines [33].
- **Sparrow (turn-taking):** Sparrow-1 (January 2026); Sparrow-2 is current [31][32].
- **Griffin** (2026-10-01) [35]:
  - A full-duplex video-to-video "Human Interaction Model". Only Griffin-Lite is out, as a research preview for testers.
  - VideoFDB generation score 3.83 against a 3.92 human reference.
  - 48% of 54 participants thought they were talking to a person.
  - Press reports 0.43 s delay on an H100 at 720p, and a voice clone from about 10 s.
  - All **(vendor claim)**, from Tavus's own study, not replicated.
- **Latency** (Contested):
  - "134 ms from audio to video" **(vendor claim)** [31]; Raven under 300 ms [32].
  - Anam's competitor-run benchmark: 1.86 s end-to-end [15].
  - Press: "sub-600 ms" end-to-end (snippet only).
- **Replica input:**
  - A photo or a video. A zero-shot preview is ready in about a minute from a photo, or a few minutes from video, then tunes in the background. Non-human faces are not supported [34].
  - The "2 minutes of video" figure often quoted is not in the docs I saved.
- **Pricing** (read via WebFetch) [36][37]. Contested over time.
  - Current tiers: Free 20 min; Starter $22 (60 min); Builder $59 (175 min, $0.35/min overage); Growth $397 (1,300 min, $0.31/min); Business $975 (4,000 min, $0.26/min); Enterprise custom.
  - Consumer PALs plans: $0, $20, $50.
  - An older version showed Starter $59 for 100 min and Growth $397 for 1,250 min.
- **On-prem:** none found; Enterprise offers white-labelling and SLAs. **Last verified:** 2026-10-01.

## Hedra
- **Character-3** (2025-03-06 per secondary sources): marketed as an "omnimodal" model.
- **Live Avatars** (about July 2025, LiveKit, about $0.05/min, "sub-100 ms"): secondary sources only, unverified.
- **Omnia** (2026-02-05): a "world model" base over vision, text and audio, offered to partners for further training under an "open core" approach [38]. One guide calls it the "more advanced model for character dialogue in dynamic environments with camera control" [41].
- **Pivot:**
  - By October 2026 the site leads with model training, inference and infrastructure. Character-3 and Studio are still listed [41].
  - Recent posts include optimising Krea 3 on AMD MI355X (2026-11-02) [39].
  - Pricing is per output, "avatar & lip-sync from 2.5¢/second" [40].
- **On-prem:** dedicated serving and training priced per engagement [40]. **Last verified:** 2026-11-02.

## Mirage (formerly Captions)
- **Mirage model** (2025-03-12): a foundation model for UGC-style talking video. It generates the face, upper body and background from audio, video or script [43].
- **Rebrand** (September 2025): Captions became Mirage, positioned as a research lab. It had raised $100M+ at a $500M valuation. Mirage Studio launched in June 2025 [44]. Confirmed.
- **Avatar X** (2026-07-28): a digital twin from 10 s of footage **(vendor claim, single outlet)** [45]. The same outlet mentions a $75M round led by General Catalyst.
- Offline only. No real-time product, API, on-prem option or architecture found.

## Simli
- Real-time only. $0.009/min self-serve, down to $0.005 at volume, with 50 free min/month [46][47].
- Builds "a full 3D avatar out of Gaussian splats on real geometry" from one photo. Speech-to-motion animation.
- About 150 ms audio-to-video **(vendor claim)**. Streams at 1366×768 [46].
- The 2025 "Trinity" model name is no longer used on the site.
- Integrations: LiveKit and Pipecat [47]. No on-prem found.

## Anam
- **Models** [48][49]:
  - Cara-3: 720×480, landscape only.
  - Cara-4: diffusion model, 25 fps.
  - **Cara-4.1 Express** (current): 1152×768 or 768×1152, with "Director Notes" for setting the performance style in text.
- **Cara-3 architecture** [50]:
  - A flow-matching audio-to-motion model, then a separate motion-to-face renderer on a reference image. Any face from one photo, with no retraining.
  - About 70 ms to first frame on an H200 **(vendor claim)**.
  - Anam open-sourced the backbone of its data pipeline.
- **Latency:** 1.24 s median reply and 1.42 s median connection, from Anam's own benchmark [15].
- **Pricing:** $0.16 down to $0.11/min self-serve; volume from $0.04/min; 30 free min/month; unlimited custom avatars [51].
- **On-prem:** none found.

## Beyond Presence
- **Genesis 2.0:** 1080p real-time model [63]. Genesis 1.0 ran at 1080p and 35 fps [65].
- **Latency** (Contested): "<100 ms" on the homepage [63]; "250 ms speech-to-video, 1 s end-to-end" in the docs [64]; about 1.2 s end-to-end for Managed Agents [65].
- **Pricing:** Speech-to-Video 50 credits/min; Managed Agents 100 credits/min; free 40 min; paid plans from $49 [65].
- **Company:** founded 2024 in Munich by the Presize team (acquired by Meta); $3.1M pre-seed [65].
- Cloud, LiveKit and Pipecat. No on-prem found.

## bitHuman
- **Models:** Essence 2 (photoreal person from one portrait) and Expression 2 (animates any character from one portrait) [59][61].
- **Where it runs:** on the device — CPU-only Linux, Windows, Apple platforms (Swift), Android (Kotlin), or a browser tab via WebGPU. Also a cloud REST API, LiveKit and Pipecat [59].
- **Status flags:**
  - The GitHub SDK was archived on 2026-10-08 and moved to GitLab [60].
  - From 2026-10-12 the SDK requires the Creator plan or higher.
  - Self-hosted rendering is still metered at 2 credits/min of active session [61].
- The LiveKit plugin defaults to `essence`; `expression` adds dynamic emotional responses [62].

## Akool
- Cloud Streaming Avatar product [66]. Pricing gives small streaming allowances of 5–15 min [68].
- At CES 2026, Qualcomm demoed "AKOOL Live Camera" running across edge and cloud [67].
- No model name, latency figure, architecture or on-prem option found. Evidence is thin.

## Soul Machines
- **Founders out** by mid-2024, with staff cut and Bartok the largest shareholder (NZ Herald, 2024-07-28) [53].
- **Receivership:** KPMG receivers were appointed on **2026-02-05** (NBR, 2026-02-09) [52].
- **Acquisition:** AppDirect announced it on **2026-09-28**, terms undisclosed. Soul Machines continues as a standalone unit, and its avatars are slated for Devs.ai [54][55]. Confirmed.
- One brief says Soul Machines' contract lets it assign customer deals and keeps ownership of custom avatars [56].

## UneeQ
- UneeQ 2.0 launched January 2025. A December 2025 "record growth" release [57]. Now positioned as AI roleplay training and coaching [58].
- Used NVIDIA ACE and Audio2Face in 2024 (search results). No 2026 news found.

## Other 2025–2026 entrants
- **LemonSlice:** YC-backed, $10.5M seed (2025-12-23) [69]. LemonSlice-2 is a 20B-parameter "Character World Model" that animates any character, non-humans included, at 20 fps from one photo. Claims 471 ms p99 **(vendor claim)** [70]. Anam measured 2.10 s end-to-end [15].
- **DeepBrain AI STUDIOS:** real-time enterprise avatar agents (2026-04-28), working with any LLM, 150+ languages [71].
- **Avaturn Live AVTR-1:** a real-time full-face generation model described as "now open source" [72]. Single-source; hand to the open-source agent.

## Comparison table
| Vendor | Mode | Custom input | Latency claim | Pricing | API | Disclosed tech | On-prem | Last verified |
|---|---|---|---|---|---|---|---|---|
| HeyGen Avatar V | offline | 15 s video [3] | n/a | 48 cr/min; API $0.05/s [5][7] | v3 [6] | DiT + flow matching, Sparse Ref Attn, DMD, RLHF [1] | no | 2026-10 |
| HeyGen Avatar IV | offline | 1 photo or video look [8] | n/a | 16/31 cr/min [7] | yes (default) | "diffusion-inspired audio-to-expression" [8] | no | 2026-10 |
| HeyGen LiveAvatar | real-time | ≥2 min footage [10] | 1.82 s e2e (Anam-run) [15] | 1–2 cr/min [10] | yes [12] | none | no | 2026-10 |
| Synthesia Express-2/3 | offline | photo or video [21] | ~8 min compute per 1 min video (E-2) [16] | seats + minutes; API 360 min/yr [23] | yes | Animate + Eval + 2-step DiT [16] | no | 2026-10 |
| Synthesia Interactive | real-time | stock / personal / Style | none | Enterprise [20] | LiveKit plugin | Express-3 | no | 2026-07 |
| D-ID V4 | both | photo/video | <0.5 s turn [26]; <200 ms render [30] | from $5.90 [26] | yes | diffusion, actor-trained [26] | **yes** [30] | 2026-03 |
| Tavus Phoenix-4.5 / Griffin | real-time | photo or video [34] | 134 ms render [31]; 1.86 s e2e [15] | $22–975 + $0.26–0.35/min [36] | yes | Gaussian diffusion → 3DGS [33]; Griffin full-duplex [35] | no | 2026-10 |
| Hedra | offline (+ live) | photo | sub-100 ms (secondary) | from 2.5¢/s [40] | yes | Character-3; Omnia [38] | per engagement | 2026-11 |
| Mirage | offline | 10 s video [45] | n/a | app subscription | not found | foundation model [43] | no | 2026-07 |
| Simli | real-time | 1 photo | ~150 ms [46] | $0.009→$0.005/min | yes | Gaussian splats [46] | no | 2026-11 |
| Anam Cara-4.1 | real-time | 1 photo | 1.24 s e2e (own benchmark) [15] | $0.16→$0.11, $0.04 vol [51] | yes | flow-matching A2M + renderer [50] | no | 2026-10 |
| Beyond Presence Genesis 2.0 | real-time | photo/video | <100 ms vs 250 ms [63][64] | 50/100 cr/min, from $49 [65] | yes | undisclosed | no | 2026 |
| bitHuman Essence 2 / Expression 2 | real-time | 1 portrait | <100–200 ms (press) | 2 cr/min even self-hosted [61] | yes + SDKs | runs on CPU [59] | **on-device (metered)** | 2026-10 |
| LemonSlice-2 | real-time | 1 photo | 471 ms p99 [70] | not checked | yes | 20B DiT, 20 fps | no | 2026-09 |
| Akool | both | photo/video | none | 5–15 min streaming [68] | yes | none | no | 2026-01 |
| DeepBrain AI STUDIOS | both | n/a | none | enterprise | yes | none | not stated | 2026-04 |
| Soul Machines | real-time 3D | n/a | n/a | n/a | n/a | n/a | n/a | receivership Feb 2026 → AppDirect Sep 2026 |
| UneeQ | real-time roleplay | n/a | n/a | enterprise | n/a | NVIDIA ACE (2024) | n/a | 2025-12 |

## Open questions / could not verify
- **Avatar V public launch date:** 2026-04-08 (schema date) against about 2026-05-04 (feed). Aggregators also give 04-15 and 04-22. Possibly the April date is research and early access, and May is general availability plus the API.
- **Synthesia** hosted interactive pipeline (promised 2026-10-01) and Video Agents general availability: not confirmed.
- **Synthesia Express-3 architecture:** not disclosed.
- **D-ID API per-minute pricing:** the page is JS-only, and the WebFetch fallback returned only navigation.
- **Tavus BusinessWire releases** (Sparrow-1, Phoenix-4, $40M round) and MarkTechPost all returned 403. Those facts rest on search snippets plus the docs.
- **Hedra Live Avatars:** secondary sources only; hedra.com/live-avatars returned 404.
- **LiveAvatar plan prices:** /pricing returned 404.
- **Production use of open-source components** by any vendor: unknown.
- **Independent cross-vendor latency benchmark:** none found. Anam's is vendor-run, and the Griffin study is self-run.
- **Mirage Avatar X:** single outlet.
- **Avaturn AVTR-1:** licence not checked.
- **On-prem** for HeyGen, Synthesia, Tavus, Anam, Simli and Beyond Presence: none found.

## Sources (URL — slug)
1. https://dynamic.heygen.ai/www/Paper%20Links/avatarv_tech_report.pdf — heygen-avatarv-tech-report
2. https://www.heygen.com/research/avatar-v-model — heygen-research-avatar-v
3. https://www.heygen.com/blog/announcing-avatar-v — heygen-com-blog-announcing-avatar-v
4. https://releasebot.io/updates/heygen — releasebot-io-updates-heygen
5. https://www.heygen.com/blog/heygen-may-2026-release — heygen-com-blog-heygen-may-2026-release
6. https://developers.heygen.com/models — developers-heygen-com-models
7. https://help.heygen.com/en/articles/15125761-heygen-credit-based-pricing-plans-explained — help-heygen-com-en-articles-15125761-heygen-credit-based-pricing-plans-explained
8. https://help.heygen.com/en/articles/11269603-new-feature-alert-heygen-avatar-iv-is-here — help-heygen-com-en-articles-11269603-new-feature-alert-heygen-avatar-iv-is-here
9. https://community.heygen.com/public/resources/introducing-avatar-iv-create-talking-avatars-from-a-single-photo — community-heygen-com-public-resources-introducing-avatar-iv-create-talking-avatars-from-a-
10. https://help.heygen.com/en/articles/10035615-how-to-get-started-with-liveavatar — help-heygen-com-en-articles-10035615-how-to-get-started-with-liveavatar
11. https://www.liveavatar.com/heygen-vs-liveavatar — liveavatar-com-heygen-vs-liveavatar
12. https://docs.liveavatar.com/ — docs-liveavatar-com
13. https://theplanettools.ai/blog/heygen-avatar-v-tested-hands-on-review-2026 — theplanettools-ai-blog-heygen-avatar-v-tested-hands-on-review-2026
14. https://www.creativeainews.com/blog/heygen-avatar-v-identity-benchmark-analysis/ — creativeainews-com-blog-heygen-avatar-v-identity-benchmark-analysis
15. https://anam.ai/tools/latency-benchmark — anam-ai-tools-latency-benchmark
16. https://synthesiaresearch.github.io/express-video — synthesiaresearch-github-io-express-video
17. https://www.synthesia.io/post/express-2-is-synthesias-next-chapter-for-full-body-expressive-ai-avatars — synthesia-io-post-express-2-is-synthesias-next-chapter-for-full-body-expressive-ai-avatars
18. https://www.synthesia.io/post/synthesia-launches-new-ai-assistant-for-faster-video-creation-and-express-3-avatar-model — synthesia-io-post-synthesia-launches-new-ai-assistant-for-faster-video-creation-and-expres
19. https://www.synthesia.io/updates/express-3 — synthesia-io-updates-express-3
20. https://www.synthesia.io/post/interactive-avatar-api-real-time-avatars — synthesia-io-post-interactive-avatar-api-real-time-avatars
21. https://www.synthesia.io/post/synthesia-3-0-the-next-era-of-video — synthesia-io-post-synthesia-3-0-the-next-era-of-video
22. https://the-decoder.com/synthesia-rolls-out-version-3-0-of-its-video-avatar-platform/ — the-decoder-com-synthesia-rolls-out-version-3-0-of-its-video-avatar-platform
23. https://www.synthesia.io/pricing — synthesia-io-pricing
24. https://builtin.com/articles/synthesia-raises-200m-series-e-20260126 — builtin-com-articles-synthesia-raises-200m-series-e-20260126
25. https://www.eweek.com/news/synthesia-january-2026-funding/ — eweek-com-news-synthesia-january-2026-funding
26. https://elearningindustry.com/press-releases/d-id-launches-v4-expressive-visual-agents-for-real-time-ai-interaction — elearningindustry-com-press-releases-d-id-launches-v4-expressive-visual-agents-for-real-ti
27. https://jpost.com/business-and-innovation/tech-and-start-ups/article-890082 — jpost-com-business-and-innovation-tech-and-start-ups-article-890082
28. https://anam.ai/blog/d-id-v4-expressive-visual-agents-what-it-means — anam-ai-blog-d-id-v4-expressive-visual-agents-what-it-means
29. https://www.d-id.com/pricing/ — d-id-com-pricing (API page: d-id-com-pricing-api, empty)
30. https://www.d-id.com/self-hosting-realtime-avatars/ — d-id-com-self-hosting-realtime-avatars
31. https://tavus.io/demo — tavus-io-demo
32. https://www.tavus.io/research — tavus-io-research
33. https://docs.tavus.io/sections/models — docs-tavus-io-sections-models
34. https://docs.tavus.io/sections/replica/overview — docs-tavus-io-sections-replica-overview
35. https://www.morningstar.com/news/business-wire/20261001092598/tavus-introduces-griffin-the-first-face-to-face-human-interaction-model-unlocking-the-future-of-conversational-ai — morningstar-com-news-business-wire-20261001092598-tavus-introduces-griffin-the-first-face-
36. https://www.tavus.io/pricing — tavus-io-pricing (figures read via WebFetch)
37. https://usagepricing.com/blueprint/tavus — usagepricing-com-blueprint-tavus
38. https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model — hedra-com-blog-hedra-omnia-frontier-ai-video-model
39. https://www.hedra.com/blog — hedra-com-blog
40. https://www.hedra.com/pricing — hedra-com-pricing
41. https://magichour.ai/blog/guide-to-hedra-ai — magichour-ai-blog-guide-to-hedra-ai
42. https://tomsguide.com/ai/ai-image-video/hedra-lets-you-give-ai-characters-a-voice-this-new-model-is-a-huge-step-up — tomsguide-com-ai-ai-image-video-hedra-lets-you-give-ai-characters-a-voice-this-new-model-i (poor extraction)
43. https://captions.ai/blog/mirage-worlds-first-foundation-model-for-ugc-video — captions-ai-blog-mirage-worlds-first-foundation-model-for-ugc-video
44. https://techcrunch.com/2025/09/04/captions-rebrands-as-mirage-expands-beyond-creator-tools-to-ai-video-research/ — techcrunch-com-2025-09-04-captions-rebrands-as-mirage-expands-beyond-creator-tools-to-ai-v
45. https://runtimewire.com/article/mirage-avatar-x-ai-twin-launch — runtimewire-com-article-mirage-avatar-x-ai-twin-launch
46. https://www.simli.com/ — simli-com
47. https://www.simli.com/pricing — simli-com-pricing; https://docs.simli.com/ — docs-simli-com
48. https://anam.ai/docs/introduction/models.md — anam-ai-docs-introduction-models-md
49. https://anam.ai/research — anam-ai-research
50. https://anam.ai/blog/cara-3-interactive-avatars — anam-ai-blog-cara-3-interactive-avatars
51. https://www.anam.ai/pricing — anam-ai-pricing
52. https://www.nbr.co.nz/tech/soul-machines-in-receivership — nbr-co-nz-tech-soul-machines-in-receivership
53. https://www.nzherald.co.nz/business/founders-out-new-investor-in-at-slimmed-down-soul-machines/FNVWHTJTUFEWZP65B2CAWNMPUU/ — nzherald-co-nz-business-founders-out-new-investor-in-at-slimmed-down-soul-machines-fnvwhtj
54. https://siliconangle.com/2026/09/28/appdirect-acquires-interactive-ai-avatar-firm-soul-machines-for-advisors-and-businesses/ — siliconangle-com-2026-09-28-appdirect-acquires-interactive-ai-avatar-firm-soul-machines-fo
55. https://www.channeldive.com/news/appdirect-adds-ai-avatars-to-its-technology-commerce-platform/831694/ — channeldive-com-news-appdirect-adds-ai-avatars-to-its-technology-commerce-platform-831694
56. https://www.beri.net/tag/contract%20assignment — beri-net-tag-contract-20assignment
57. https://www.digitalhumans.com/blog/uneeq-announces-record-global-growth-as-digital-humans-redefine-the-future-of-ai — digitalhumans-com-blog-uneeq-announces-record-global-growth-as-digital-humans-redefine-the
58. https://www.digitalhumans.com/ — digitalhumans-com
59. https://www.bithuman.ai/ — bithuman-ai
60. https://github.com/bithuman-product/bithuman-sdk-public — github-com-bithuman-product-bithuman-sdk-public
61. https://docs.pipecat.ai/api-reference/server/services/video/bithuman.md — docs-pipecat-ai-api-reference-server-services-video-bithuman-md
62. https://docs.livekit.io/agents/models/avatar/plugins/bithuman.md — docs-livekit-io-agents-models-avatar-plugins-bithuman-md
63. https://www.beyondpresence.ai/ — beyondpresence-ai
64. https://docs.bey.dev/ — docs-bey-dev
65. https://makerstack.co/reviews/beyond-presence-review/ — makerstack-co-reviews-beyond-presence-review
66. https://akool.com/enterprise/streaming-avatar — akool-com-enterprise-streaming-avatar
67. https://akool.com/blog-posts/real-time-ai-avatars-at-ces-2026-qualcomm-powered-by-akool-live-camera — akool-com-blog-posts-real-time-ai-avatars-at-ces-2026-qualcomm-powered-by-akool-live-camer
68. https://akool.com/pricing — akool-com-pricing
69. https://siliconangle.com/2025/12/23/lemon-slice-launches-10-5m-seed-round-scale-real-time-interactive-ai-avatars/ — siliconangle-com-2025-12-23-lemon-slice-launches-10-5m-seed-round-scale-real-time-interact
70. https://lemonslice.com/ — lemonslice-com
71. https://b2b-asianews.com/globe-newswire/69117/detail/ — b2b-asianews-com-globe-newswire-69117-detail
72. https://avaturn.live/ — avaturn-live

**Also saved:** heygen-com-pricing, heygen-com-api-pricing (no prices extracted), heygen-com-blog-announcing-the-avatar-iv-api, tavus-io-blog, tavus-io-blog-conversational-ai-pricing, docs-hedra-com, soulmachines-com, anam-ai-compare.

**Failed fetches** (logged in log.jsonl):
- 403: theresanaiforthat Avatar V; BusinessWire Tavus ×3; sifted; computerweekly; marktechpost; letsdatascience; betanews; producthunt Avaturn; techleap.
- 404: developers.heygen.com/avatar-realtime; liveavatar.com/pricing; hedra.com/live-avatars; anam.ai/avatar-benchmark; docs.d-id.com pricing.