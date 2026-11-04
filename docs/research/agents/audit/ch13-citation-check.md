# Ch13 citation check (13-avatar-product-world.md, Ch06 [27]–[41], Ch11 [5]–[10], Ch10 numbers)

Checked 2026-11-04 against the saved copies in `docs/research/sources/text/` and `docs/research/agents/duix-realtime/gh/`. All 75 Ch13 saved copies exist and none is empty or truncated, so I fetched nothing live. **No new sources saved.**

## Summary

| Scope | FAITHFUL | GENEROUS | MISATTRIBUTED | OVERREACH | UNVERIFIABLE |
|---|---|---|---|---|---|
| Ch13 (75 refs, rated by the worst issue in each) | 46 | 10 | 10 | 3 | 6 |
| Ch06 [27]–[41] (15) | 11 | 1 | 1 | 0 | 2 |
| Ch11 [5]–[10] (6) | 5 | 0 | 1 | 0 | 0 |

The architecture, benchmark and price numbers hold up well. Every number in the HeyGen tech report, the Anam benchmark, the Tight benchmark, Modal prices, WaveSpeed/fal, Simli, Anam, Duix pricing, the 36Kr revenue figures and the LiveTalking fps table matches its source. The cost arithmetic reproduces: $21.5 and $3.5 per output minute, $0.13 and $0.53 per stream-minute. Most problems are **dates and secondary numbers cited to the wrong saved copy** (usually a README when the number is in the arXiv paper or the GitHub metadata JSON), plus three wording overreaches.

**Top fixes, in priority order**
1. **Tavus pricing [21]**: the saved `tavus-io-pricing` has no prices at all. $22–$975/mo and $0.26–0.35/min are only in `usagepricing-com-blueprint-tavus` (third-party). Cite that, and note the $22 Starter plan has no pay-as-you-go rate. The same $0.35 is mis-cited to HeyGen [5] in Ch11.
2. **Ch13:88, "nobody in the market is near the sub-500 ms turn"**: overreach. Anam's benchmark [10] measured four vendors, and D-ID claims sub-0.5 s turns [16]. Narrow it.
3. **Ch13:152, "the commercial live vendors are not using 14B video diffusion per stream"**: contradicted by the chapter's own LemonSlice row, a 20B real-time model [36]. Limit it to Simli and Anam.
4. **HeyGen dates (Ch13:31, table)**:
   - Only [2] carries "Apr 8, 2026". [3] says "Last Updated October 20th, 2026".
   - The release feed [4] lists Avatar V in "What's new at HeyGen: April 2026", dated **May 6, 2026**, not "around 2026-05-04".
   - "Avatar III unlimited on paid plans [4]" is out of date: current credit plans charge 7 credits/min (photo look) and 4 credits/min (video look) [7]. It is unlimited only on legacy plans.
   - Avatar IV "May 2025" has no source.
5. **Moved citations**:
   - Duix cloud's "200 ms TTFB" is in `duix-com`, not [46].
   - LiveAvatar's "1.21 s" is in `arxiv-2512.04677-liveavatar`, not [59].
   - FlashTalk's "32 fps" is in `arxiv-2512.23379-soulx-flashtalk`, not [58].
   - FlashHead's "512²" appears only in Tight [64], not [57].
   - LiteAvatar's closed training and Alibaba Cloud customization are in `gh/HumanAIGC-lite-avatar-issue-3.json` and `issue-24`, not issue-27.
   - LongCat's MIT licence is in `hf-api-meituan-longcat-longcat-video-avatar-1.5` (or `gh-longcat-video-readme`), not [74].
   - Duix-Mobile's "<1.5 s" is the GitHub repo description (`gh/duixcom-Duix-Mobile.json`), not the README [44].
6. **Unsupported details**:
   - Griffin's "54 participants" [20] is not in the source.
   - Anam Cara-4.1 "is diffusion-based" [31] is not in the docs.
   - Fay "plugs into LiveTalking, Duix or an Unreal MetaHuman" [72] is not in the README, and the dossier itself says the connector list is unsaved.
   - bitHuman "CPU-only Linux" [34] is not in the source.
   - The phrase "fake open source" in quotation marks [50] does not appear in the saved issues.

## Per-citation review: Chapter 13

### HeyGen

- **13:31 [1][2][3], "published its technical report and research page on 2026-04-08".** Actual: [2] has "Apr 8, 2026". The tech report has no date, and [3] says "Last Updated October 20th, 2026". **GENEROUS.** Rewrite: "HeyGen's research page dates the technical report 2026-04-08 [2]; the report itself is [1]."
- **13:31 [4], "product announcement … around 2026-05-04".** Actual: the release feed entry "What's new at HeyGen: April 2026" (date parsed from source: May 6, 2026) says "Avatar V is here". **OVERREACH (wrong date).** Rewrite: "HeyGen's April 2026 roundup (published 2026-05-06) announces Avatar V as launched in April [4]."
- **13:31 [5], "$0.05 per second".** Actual: "Avatar V API… at five cents per second". **FAITHFUL.**
- **13:31 [6], v3 API, `engine` field, Avatar IV default.** Actual: "selected per request through the engine field on POST /v3/videos. New integrations should default to Avatar IV". **FAITHFUL.**
- **13:35 table, Avatar III "video twin" and "unlimited on paid plans [4]".** Actual: [4] says Avatar III is unlimited for paid users "with your personal photo or video avatars". But [7] says credit plans charge "Avatar III Photo Look 1 minute = 7 credits; Video Look = 4 credits", and that Avatar III is "free and unlimited on legacy plans". [6] describes Avatar III as "Photo-to-video pipeline. 4K." **OVERREACH (out of date, identity input too narrow).** Rewrite: "photo or video look | 7 / 4 credits/min on credit plans; unlimited on legacy plans [7]".
- **13:36 [8][7], Avatar IV.** The quotation "diffusion-inspired audio-to-expression engine" and 16 / 31 credits/min are **FAITHFUL**. "May 2025" is **UNVERIFIABLE** (no date in [8], nothing in [4]): cite a source or drop it.
- **13:37 [3][7][5], Avatar V row.** Actual: 48 credits/min ✓. [3] says "You need a phone"; "webcam" does not appear. **GENEROUS (minor).** Rewrite: "15-second phone recording [3]".
- **13:38 [9], LiveAvatar "at least 2 minutes of footage".** Actual: "Minimum of 2 minutes". 1 and 2 credits/min ✓. **FAITHFUL.** The "October 2025" date comes from [4] ("HeyGen releases an October 2025 update with LiveAvatar"); add [4].
- **13:42–48 [1], tech report architecture.** All verified:
  - Sparse Reference Attention: "scales almost linearly".
  - Motion stream ✓; cascade with image engine, base DiT and SR refiner on the same backbone ✓.
  - Five stages ✓; ">10× acceleration" ✓.
  - "161 pixel frames at 25 fps, approximately 6.4 seconds" ✓; "24 steps" ✓; "Ulysses Sequence Parallelism across 8 GPUs" ✓.
  - "HELIOS manages more than 5,000 GPUs" ✓; "100M+ clips from 50M raw videos" ✓.
  - Wan, CogVideoX and HunyuanVideo appear only in related work ✓.

  "In-house" is an inference from the T2V pretraining stage; the report never says it, but the inference is reasonable. **FAITHFUL.**
- **13:50 [1], evaluation numbers.** Table 1 on "36 matched test cases" matches exactly: Avatar V 8.97 / 0.840, Seedance 2.0 8.86 / 0.823, Kling O3 Pro 5.16 / 0.838, Veo 3.1 8.05 / 0.714, ground truth 7.93 / 0.861. **FAITHFUL.** The report also compares OmniHuman 1.5, which the text omits; that is acceptable.
- **13:50 [4], 30 minutes in a single pass on Avatar III, IV and V.** Actual: "single 30-minute AI talking video in one pass… available now on Avatar III, IV, and V". Labelled as a vendor claim. **FAITHFUL.**

### Synthesia, D-ID, Mirage, Hedra

- **13:56 [11], Express-2 architecture.** Actual: Express-Animate, Express-Eval ("CLIP-like"), Express-Render (a DiT distilled to "just two diffusion steps"), "one minute of video at 1080p and 30fps… in around 8 minutes". **FAITHFUL.** The date 2025-09-04 is not in [11]; it is in the uncited `synthesia-io-post-express-2-is-synthesias-next-chapter-for-full-body-expressive-ai-avatars` ("September 4, 2025"). **MISATTRIBUTED (date only).** Add that source.
- **13:56 [12], Express-3 on 2026-07-15, "up to 2× faster".** Actual: "July 15, 2026… can generate up to 2x faster". **FAITHFUL.**
- **13:56 [13], Enterprise-only, LiveKit plugin, customer brings the LLM and ASR.** Actual: "launches today for Enterprise customers… Synthesia layers the avatar on top via LiveKit… livekit-plugins-synthesia". **FAITHFUL.** The 2026-10-01 hosted pipeline (13:181) is also in [13] ✓.
- **13:23 [14], Synthesia studio avatars as a per-identity fine-tune that "historically did".** Actual: "Studio Express-1 avatar is a paid add-on ($1000/year)… can take up to 10 days to process." Nothing in the source says "fine-tune", and the product is current, not historical. **GENEROUS.** Rewrite: "Synthesia's Studio avatars are a paid add-on that takes up to 10 days to process [14], which suggests per-identity training."
- **13:56 [15], $200M at about $4B in January 2026.** Actual: "Jan 26, 2026… $200 million Series E… valuing the company at about $4 billion". **FAITHFUL.**
- **13:58 [16], D-ID V4.** Actual: "March 16, 2026… Built on a new diffusion-based model and trained on performances captured from real actors… (sub-0.5-second) conversational turns"; "starting from as little as $5.90 a month". **FAITHFUL.**
- **13:58 [17], D-ID self-hosted.** Actual: "renders in under 200ms"; "Transactable on Azure & AWS"; "An annual platform license". **FAITHFUL.**
- **13:60 [25][26], Mirage.** Actual: "rebranding to Mirage… AI research lab" (TechCrunch, September 4, 2025); "full facial and upper-body motion… background environments". **FAITHFUL.**
- **13:60 [23], Hedra.** Actual: "unified base model… partners can specialize through post-training". **FAITHFUL** on substance. The dates "Character-3 (March 2025)" and "Omnia (February 2026)" are **UNVERIFIABLE**: neither appears in [23] or [24].
- **13:60 [24], Hedra pricing.** Actual: "Avatar & lip-sync from 2.5¢ / second"; the page title is "API, Infrastructure, and Studio". **FAITHFUL.**

### Live vendors

- **13:64 [37][38], Soul Machines.** Actual: KPMG receivers "appointed… on February 5" (NBR, 9 Feb 2026); AppDirect acquisition on September 28, 2026. **FAITHFUL.**
- **13:66 [29], Anam Cara-3.** Actual: "A diffusion transformer takes audio… core algorithm behind audio-to-motion is flow matching… motion-to-face… ~70ms TTFF… on an H200". **FAITHFUL.**
- **13:66 [31], "Cara-4.1, is diffusion-based and outputs 1152×768".** The resolution is ✓ ("1152x768"). "Diffusion-based" does not appear anywhere in the docs. The table's "motion + renderer" family for Cara-4.1 is carried over from the Cara-3 disclosure. **UNVERIFIABLE.** Rewrite: "Anam's current model, Cara-4.1 Express, outputs 1152×768 [31]; its architecture is not separately disclosed." Label the table family "motion + renderer (Cara-3 disclosure)".
- **13:68 [18], Tavus "built on a Gaussian diffusion model".** The quotation is ✓. "(February 2026)" for Phoenix-4 appears in no saved copy. **UNVERIFIABLE (date).**
- **13:68 [27], Simli.** Actual: "From a single photo we build a full 3D avatar out of Gaussian splats on real geometry"; "about 150 ms". **FAITHFUL.**
- **13:70 [36], "LemonSlice-2 … 20-billion-parameter … 20 fps from one photo".** Actual: "LemonSlice-2.1 — 20B parameter model that animates any character at 20 fps from just 1 photo". The site now leads with "CWM-1". **GENEROUS (wrong version name).** Rewrite as "LemonSlice-2.1", and mention CWM-1 as the current model.
- **13:70 [20], Griffin.** Actual: "full-duplex, video-to-video"; "48% of participants believed they were speaking with a real person"; "Griffin-Lite… research preview". "**54 participants**" appears nowhere in the source. **UNVERIFIABLE (54).** Rewrite: "48% of participants in Tavus's own live study [20]", and drop 54 unless another source is saved.
- **13:76 [16][17], D-ID row.** **FAITHFUL.**
- **13:77 [19][22][21], Tavus row.**
  - [19]: "Train one from a photo or a video" ✓ **FAITHFUL**.
  - [22]: "Tavus PALs render at 134 ms from audio to video" ✓ **FAITHFUL**.
  - [21]: the saved pricing page has **no prices**. "Starter $22/mo… Business $975/mo" and "$0.35/min on Builder… $0.26/min on Business" are only in `usagepricing-com-blueprint-tavus`. **MISATTRIBUTED.** Recite to that copy as third-party, and note "Starter has no pay-as-you-go rate".
- **13:78 [30], Anam "$0.16→$0.11/min".** Actual: "then $0.16/min… $0.11/min, Lowest self-serve rate"; also "Volume pricing from $0.04/min". **FAITHFUL** for self-serve. Consider adding "volume from $0.04". This also affects "Anam at 11–16 cents" at 13:152.
- **13:79 [28], Simli "$0.009→$0.005/min".** Actual: Hobby $0.01, Pro $0.0095, Scale $0.009, Enterprise "as low as $0.005". **FAITHFUL** ("under a cent" holds from the Pro plan up).
- **13:80 [32][33], Beyond Presence.** Actual: "response time <100ms" [32]; "250 ms speech-to-video latency and 1-second end-to-end" [33]. **FAITHFUL.** "Credits, from $49/mo" has no citation; it is in `makerstack-co-reviews-beyond-presence-review` ("From $49/month… 50 credits per minute").
- **13:81 and 13:90 [34][35], bitHuman.**
  - [35]: "2 credits a minute on your own machine… one portrait" ✓ **FAITHFUL**.
  - [34]: shows iPhone, Android, Python and "A web page… One iframe" rendering. "CPU-only Linux" appears in neither copy. **OVERREACH.** Rewrite: "renders on the device (iOS, Android, or in-process via the Python SDK) [34][35]".
- **13:82 [36], "471 ms p99".** Actual: "471ms p99 latency"; also "471ms time-to-first-byte and 2.04s end to end". **FAITHFUL.** Adding LemonSlice's own 2.04 s end-to-end figure would strengthen *Why Latency Claims Do Not Compare*.
- **13:86 [32][33].** **FAITHFUL.**
- **13:88 [10], Anam benchmark.** Actual: "Sixty people… 4,703 measured turns, October 16, 2026"; medians 1.24 / 1.82 (HeyGen) / 1.86 (Tavus phoenix-4.5) / 2.10 (LemonSlice). **FAITHFUL.** The closing clause "nobody in the market is near the sub-500 ms turn" is an **OVERREACH**: only four vendors were measured, and D-ID claims under 0.5 s [16]. Rewrite: "…and none of the four measured products came near the sub-500 ms turn… (D-ID's sub-0.5 s claim [16] is unmeasured)."

### Duix and the Chinese stacks

- **13:96 [48][49], company facts.**
  - Founded 2017 ✓.
  - Revenue "5.31亿… 6.55亿… 7.89亿" ✓.
  - Customers "1009家降至2025年的431家" ✓.
  - Market share "市场份额高达32.2%", by 灼识咨询 (CIC) ranking on **2024** revenue ✓.
  - Losses: the source gives a cumulative net loss of about RMB 233M over 2023–2025, with 2025 adjusted profit positive but net profit not yet positive.
  - Filing dates: the source says the previous filing lapsed at the end of April and the refiling came about three weeks later (May 2026). "October 2025" is an inference from that lapse.
  - "International brand" is not in [48].

  **GENEROUS (minor).** Rewrite: "a cumulative net loss of about RMB 233M over 2023–2025"; "32.2% share by 2024 revenue (CIC data)"; "first filing (lapsed end of April 2026)".
- **13:96, repo moves and renames.** Supported only by `gh/GuijiAI-HeyGem.ai.json`, `gh/duixcom-Duix-Avatar.json` and similar, which are not cited. Add them.
- **13:98 [39], offline only and sends interactive users to the cloud.** Actual: "realizes digital human cloning and non-real-time video synthesis. If you want a digital human to support interaction, you can visit duix.com". **FAITHFUL.** The 16,219 stars and the v1.0.6 release (2025-09-28) come from `gh/duixcom-Duix-Avatar.json` and `-releases.json`, not the README; cite those.
- **13:100 [39], "Docker images of 60–100 GB containing compiled modules".** Actual: "download will consume about 70GB of traffic"; "Free space requirement: More than 100GB". "Compiled modules" is supported by [42] and [43] ("closed-source Cython .so binaries"), not [39]. **GENEROUS.** Rewrite: "a roughly 70 GB download needing 100 GB of disk [39], with compiled Cython modules [42]".
- **13:100 [50], "fake open source" in quotation marks.** Actual: issue 243 comments such as "结果代码是py加密成.so的" and "开源吹的镇天响", plus an issue asking for the Dockerfiles and source. The phrase itself appears in neither saved file. **GENEROUS.** Remove the quotation marks: "complaints that the 'open source' release ships encrypted .so modules recur in the issue tracker [50]."
- **13:101 [42][43], DINet identification.**
  - [42]: "recovered by decompiling the original .so modules with Ghidra"; "DINet input = crop[5:-5] (256×256)"; "(optional) GFPGAN restore" ✓.
  - [43] ships the .so files, and [42]'s weights (`dinet_v1_20240131.pth`) are "the publicly released downloads from HeyGem-Linux-Python-Hack", so the "corroboration" is the same weights, not an independent identification.

  **GENEROUS ([43]).** Rewrite: "…[42], using weights published by a second community extraction [43]."
- **13:101, "DINet, a 2023 lip-sync model".** No citation. Cite Ch06 or the DINet paper.
- **13:102 [42], "plus a zero-shot voice prompt".** [42] covers the face pipeline only. Voice cloning (Fish-Speech) is in [39]. **MISATTRIBUTED (voice half).** Cite [39] for the voice.
- **13:104 [39][40][41], three licences.** Actual:
  - [39]: "global free commercial use (enterprises with more than 100,000 users or annual revenue exceeding 10 million USD need to sign…)".
  - [40]: "greater than 1 thousand Monthly Active Users, you must request a commercial license… in its sole discretion", plus "Built with DUIX.COM" and naming conditions.
  - [41]: "license for Non-Commercial Purposes… Commercial Use… obtain written authorization".

  **FAITHFUL (all three).**
- **13:106 [44][45], Duix-Mobile.**
  - Issue 4: "纯cpu推理的" ✓.
  - Issue 19: "基础模型… 提供1~2分钟数据微调" ✓.
  - Issue 2: "暂时没有开源训练部分的计划" ✓.
  - README: "under 120ms (tested on Snapdragon® 8 Gen 2)" ✓; "For custom avatars, please contact us" (it never says "paid").
  - "<1.5 s latency" is in the GitHub repo description (`gh/duixcom-Duix-Mobile.json`), not the README.

  **[45] FAITHFUL / [44] MISATTRIBUTED (the 1.5 s figure).** "Paid service" is mildly GENEROUS.
- **13:108 [46][47], Duix cloud.** Actual: $29 / 150 minutes to $4,999 / 60,000 minutes ✓; the Android SDK "uses WebRTC under the hood" ✓. "200 ms TTFB" is not in [46]; it is in `duix-com` ("200ms TTFB latency"). **MISATTRIBUTED.** Cite `duix-com`.
- **13:108 [73], duix-skills.** Actual: "Upload a portrait → choose a voice → get a conversation webpage link". **FAITHFUL.** "July 2026" is **UNVERIFIABLE**: no date in the saved README.
- **13:110 [54], LiteAvatar.** Actual: "can run in 30fps on only CPU devices"; "mouth parameter prediction model"; issue 27 says the "code repository is MIT, but the model weights… doesn't specify a license". **FAITHFUL** for those claims. "Closed training with custom avatars sold through Alibaba Cloud" is in issue 3 ("暂时无法开源训练脚本… 后续会在阿里云百炼提供形象定制API") and issue 24 (Alibaba Cloud customization pricing link), neither of which is cited. **MISATTRIBUTED (partly).** Add issue-3 and issue-24 to [54].

### Open real-time stacks

- **13:116 [51], LiveTalking.** Actual: "wav2lip256 | RTX 3060 | 60", "musetalk | RTX 4090 | 72"; the open edition is "Apache 2.0… wav2lip / musetalk / ultralight 三款模型". **FAITHFUL.** The 10,260 stars and the 2026-10-20 push come from `gh/lipku-LiveTalking.json`; cite it.
- **13:116 [52], ER-NeRF missing from the tree.** The tree snapshot is top-level only (25 entries), so it cannot show that a model directory is absent. The better evidence is README line 203, which lists three open models while line 26 still lists ernerf. **GENEROUS.** Rewrite: "the README still lists ER-NeRF among supported models but its own comparison table lists only three for the open edition [51]."
- **13:116 [52], about three seconds to interrupt, "cannot be flushed".** Actual: issue 510, "响应最快3秒… 因为webrtc也存在缓冲区，数字人的推理还在进行". Later commenters report patches reaching "1.5秒内" and "500ms 内". **GENEROUS.** Rewrite: "…cannot be flushed without patching; users report patches bringing it to 0.5–1.5 s [52]."
- **13:118 [53][55], OpenAvatarChat.** Actual: "平均响应时间仅 2.2 秒"; SenseVoice, CosyVoice, silero-vad, Qwen-Omni; LiteAvatar, LAM, MuseTalk, FlashHead ✓. [55]: "One-shot Animatable Gaussian Head", "WebGL-Render" ✓. **FAITHFUL.** Cite the stars (3,848) to `gh/HumanAIGC-Engineering-OpenAvatarChat.json`.
- **13:120 [71], Linly-Talker-Stream.** Actual: "2026.02… references LiveTalking for real-time communication design"; 151 stars in the gh JSON. **FAITHFUL.**
- **13:120 [72], Fay plugs into LiveTalking, Duix or MetaHuman.** The README lists features only ("自由匹配数字人模型…ASR、TTS"). None of those three back-ends is named, and `agents/duix-realtime/duix-and-realtime-stacks.md:117` says the connector list is on an unsaved Feishu page. **OVERREACH.** Rewrite: "Fay is an orchestrator only (agents, ASR, TTS, memory) that drives an external face model [72]; GPL-3.0." Name back-ends only from a saved source.
- **13:130 [56], MuseTalk.** Actual: "code… MIT License… no limitation for… commercial usage. model: available for any purpose, even commercially." **FAITHFUL.** Caveat worth adding: dependencies (whisper, dwpose, S3FD) carry their own licences.

### Wan and the economics

- **13:136 [61], every open Wan checkpoint is Apache-2.0.** All 27 Wan-AI repos are tagged license:apache-2.0, including Wan2.2-S2V-14B, Wan2.2-Animate-14B and Wan2.2-Animate-2-14B. **FAITHFUL.**
- **13:136 [62], Wan 2.6 r2v at 720p.** Actual: "0.086012 Per second" and "0.1 Per second". **FAITHFUL.**
- **13:136 [63], Wan-Streamer "a paper without released weights".** The abstract page describes the model but cannot show that weights are absent. **UNVERIFIABLE (absence claim).** Rewrite: "…no weights were found as of 2026-11-04."
- **13:136, uncited: "Wan 2.5, 2.6, 2.7 and 3.0 … only through Alibaba's API".** Saved support exists in `atlascloud-wan3-open-source` ("Not open source, not open weights") and `wan27org-wan25-open-source`. Cite them.
- **13:136, uncited licence list.**
  - InfiniteTalk, MultiTalk, EchoMimicV3 and LiveAvatar: "Apache 2.0" in their gh READMEs.
  - OmniAvatar: `hf-api-omniavatar-omniavatar-14b`.
  - SoulX-FlashTalk: `gh/Soul-AILab-SoulX-FlashTalk.json`.
  - StableAvatar MIT: `hf-api-francisring-stableavatar`.
  - TalkVerse non-commercial: `gh-talkverse-readme` / `arxiv-2512.14938-talkverse`.
  - FlashHead Lite VAE under OpenRAIL-M: `hf-soulx-flashhead-card` ("you MUST preserve the license of VAE_LTX as Open-RAIL-M").

  Cite these or point to the Ch06 references.
- **13:136 [74], LongCat-Video-Avatar MIT.** The arXiv abstract copy shows no licence text; MIT is in `hf-api-meituan-longcat-longcat-video-avatar-1.5` ("license":"mit") and `gh-longcat-video-readme`. **MISATTRIBUTED (minor).**
- **13:136 [75], Kandinsky S2V MIT.** Actual: "The code in this repository is MIT… The published weights carry their own licence, stated on each model card." **GENEROUS.** Rewrite: "Kandinsky S2V (MIT code; weights under their own model-card licence)".
- **13:138–146 [64][65], Tight table.**
  - Wan2.2-S2V 204.64× ✓; LiveAvatar 48.77× ✓.
  - EchoMimicV3-Flash 251.94 s, and LongCat 233.08 s, over the "3.63-second narration" give about 70× and about 65× ✓.
  - FlashHead Lite 5,763 MiB ✓.
  - Qualitative notes: "sharpest identity", "hand gesture absent from the reference image… mouth frames looked exaggerated", "softer in identity, and weaker in mouth movement" ✓.
  - August 2026 and "pinned versions" ✓.

  **FAITHFUL.** Two notes:
  - "Used 33.7 GB against a claimed 12 GB": the 12 GB claim comes from the uncited `gh-echomimicv3-readme` ("12G VRAM… GradioUI" from a community contributor). Tight explicitly says "The project advertises lower-memory modes, so this is observed usage for our settings". **GENEROUS.** Rewrite: "33.7 GB in the official 768-area configuration (the project advertises a 12 GB mode)".
  - SoulX-FlashTalk (331.93 s, about 91×) is left out of the table without saying so.
- **13:148 [66], InfiniteTalk 4-step LoRA.** Actual: "Run with FusioniX or Lightx2v (Require only 4~8 steps)". **FAITHFUL.**
- **13:150 [59], LiveAvatar "45 fps on 5×H800 with 1.21 s to first frame".** The README has "45 FPS on multi-card H800" and "no need for 5×H800". "1.21 s" is only in `arxiv-2512.04677-liveavatar` ("45 FPS with a TTFF of 1.21 s on 5 H800 GPUs"). **MISATTRIBUTED.** Add the arXiv copy to [59].
- **13:150 [58], SoulX-FlashTalk "32 fps on 8×H800".** The README has "Real-time inference speed can only be supported on 8xH800". "32 FPS" is only in `arxiv-2512.23379-soulx-flashtalk`. **MISATTRIBUTED (partly).** Add the arXiv copy to [58].
- **13:150 [60], SoulX-LiveAct.** Actual: "20 FPS using only two H100/H200 GPUs". **FAITHFUL.**
- **13:150 [57], FlashHead Lite "96 fps on an RTX 4090 at 512² head-only".** "96 FPS… on single RTX4090" ✓. "512²" is not in [57]; it is Tight's measured output (512 x 512) [64]. **MISATTRIBUTED (minor).**
- **13:150 [70], DynaForcing.** Actual: "dynamic collapse, where the student model converges to a near-static optimum". **FAITHFUL.**
- **13:152 [69] with [64], cost arithmetic.**
  - Wan: $1.3692 / 3.81 s × 60 = $21.5 ✓.
  - EchoMimic: $0.2120 / 3.63 s × 60 = $3.5 ✓.
  - LiveAct: 2 × H100 $0.001097/s × 60 = $0.13 ✓.
  - FlashTalk: 8 × H100 = $0.53 ✓. This uses H100 prices for the authors' H800 figure, which is fine but worth stating.
  - FlashHead "about a cent" works only on an L40S ($0.000542/s × 60 / 3 = $0.011). On an L4 it is $0.004. The three-stream figure is an RTX 4090 claim.

  **FAITHFUL.** Name the GPU used for the FlashHead figure.
- **13:152 [67][68], hosted InfiniteTalk.** Actual: WaveSpeed "$0.03 per second… HD (720p) $0.06 per second"; fal "$0.2 per second. For 720p price will be doubled". So $1.80–3.60/min and $12–24/min ✓. **FAITHFUL.**
- **13:152, uncited inference "the commercial live vendors are not using 14B video diffusion per stream".** This contradicts LemonSlice-2.1 (a 20B real-time model [36]). **OVERREACH.** Rewrite: "Simli and Anam are evidently not running 14B video diffusion per stream."

### Other uncited sentences in Ch13

- 13:21, the list of single-photo products: supported by [27], [29] and the LemonSlice copy ("Upload a photo"); add the citations.
- 13:50, "third-party write-ups repeat them without re-measuring": cite the saved `theplanettools-ai-blog-heygen-avatar-v-tested-hands-on-review-2026` or soften the wording.
- 13:92, "No commercial vendor publicly states…": acceptable as a research-absence claim, but say "found".

## Per-citation review: Chapter 06 [27]–[41]

| Ref | Claim checked | Saved evidence | Rating |
|---|---|---|---|
| [27] | Wan 2.1 and 2.2 are Apache-2.0 | 27 repos tagged license:apache-2.0 | FAITHFUL |
| [28] | MultiTalk: 2025-06, ≤15 s, Wan2.1-I2V-14B, Apache | "June 9, 2025… weights"; "up to 15 seconds"; Wan2.1-I2V-14B-480P; "Apache 2.0" | FAITHFUL |
| [29] | InfiniteTalk: 2025-08, "unlimited", clean for about a minute | "August 19, 2025"; "Supports unlimited video duration"; "good results from a single image for up to 1 minute. Beyond 1 minute, color shifts" | FAITHFUL |
| [30] | Wan2.2-S2V: 2025-08, 480p/720p, Apache | "Aug 26, 2025"; "480P and 720P" | FAITHFUL |
| [31] | OmniAvatar: 2025-06, 480p, LoRA, Apache | "June 24-th, 2025"; "480p only for now"; "Our LoRA". The Apache licence is only in uncited `hf-api-omniavatar-omniavatar-14b` | UNVERIFIABLE (licence); add that copy |
| [32] | StableAvatar: Wan2.1-Fun 1.3B, MIT, 2025-08 | Base ✓. MIT only in uncited `hf-api-francisring-stableavatar`; the August date is not in the saved README | UNVERIFIABLE (licence, date) |
| [33] | EchoMimicV3: Wan2.1-Fun 1.3B, Flash 2026-01, Apache | "Wan2.1-Fun-V1.1-1.3B-InP"; "[2026.01.22]… Flash"; "Apache 2.0" | FAITHFUL |
| [34] | LongCat: 13.6B, MIT, 2025-12 and 2026-05, parity claim with HeyGen and OmniHuman | "13.6B"; "Dec 16, 2025"; "May 21, 2026"; "MIT License"; "competitive or superior… (e.g., HeyGen, OmniHuman 1.5, Kling Avatar 2.0)" | FAITHFUL |
| [35] | LiveAvatar: 45 fps on 5×H800, 10,000+ s, Apache | arXiv: "45 FPS with a TTFF of 1.21 s on 5 H800 GPUs"; README "10,000+ second" | FAITHFUL |
| [36] | FlashTalk: 32 fps on 8×H800 | arXiv "32 FPS"; README "8xH800". The Apache licence is only in `gh/Soul-AILab-SoulX-FlashTalk.json` | FAITHFUL |
| [37] | FlashHead: 96 fps on a 4090, head-only 512², Lite VAE OpenRAIL-M | 96 fps ✓. 512² appears only in Tight. OpenRAIL-M appears only in uncited `hf-soulx-flashhead-card` | MISATTRIBUTED (minor); cite [41] and the HF card |
| [38] | LiveAct: 20 fps on 2×H100 | "20 FPS using only two H100/H200". The licence is in `hf-api-soulx-liveact` | FAITHFUL |
| [39] | Kandinsky S2V: 2026-10, 5 s chunks, Kandinsky 5 Video base, MIT | "13 Oct 2026"; "5-second chunks"; "starts from the Kandinsky 5.0 Video foundation models"; but "weights carry their own licence" | GENEROUS (MIT covers code only) |
| [40] | Distilled students collapse toward static motion | "dynamic collapse… near-static optimum" | FAITHFUL |
| [41] | Tight benchmark; LongCat adds a hand gesture | "a hand gesture absent from the reference image" | FAITHFUL |

**Uncited claims in the Ch06 update notes**
- "Their audio encoders are Chinese wav2vec2 or Whisper variants" is uncited and **GENEROUS**: Kandinsky S2V draws audio from Qwen2.5-Omni, and TalkVerse uses wav2vec2-large-xlsr-53-english. Kandinsky's README also points to "other languages" examples (examples, not an evaluation). Rewrite: "mostly Chinese wav2vec2, Whisper or Qwen-Omni encoders; none publishes a multilingual lip-sync evaluation."
- "Alibaba's own later Wan versions (2.5 to 3.0, API-only)": cite `atlascloud-wan3-open-source`.
- "Semantically planned gesture, as in the closed OmniHuman 1.5": uncited.

## Chapter 11 [5]–[10]

- **[5], HeyGen bullet.**
  - Avatar V as a distilled DiT and the $0.05/s API price are ✓.
  - "15-second recording" is not in the three [5] copies (the tech report says "short reference video"). It is in Ch13 [3].
  - "LiveAvatar (October 2025)" is not in the [5] copies; it is in the release feed.
  - **MISATTRIBUTED (partly).** Add `heygen-com-blog-announcing-avatar-v` and `releasebot-io-updates-heygen`.
- **[5] in *Where the money flows*, "live avatar minutes from under $0.01 to about $0.35".** $0.35 is Tavus's Builder overage (`usagepricing-com-blueprint-tavus`) and $0.009 is Simli (`simli-com-pricing`); neither is in [5]. **MISATTRIBUTED.** Cite those copies.
- **[6] Synthesia, [7] D-ID, [9][10] Soul Machines.** **FAITHFUL**, as in Ch13.
- **[8] Duix.** "Largest Chinese player by its own account" matches #1 by 2024 revenue per CIC in the prospectus coverage. **FAITHFUL.**
- **Uncited:**
  - The bullet listing real-time vendors with prices "from under a cent (Simli) to tens of cents": cite Simli, Anam and Tavus pricing.
  - "UneeQ has repositioned around AI roleplay training": cite the saved `digitalhumans-com` ("UneeQ | AI roleplay training and coaching").

## Chapter 10 Use Cases 3 and 4 (numbers only)

- "1.2–2.1 s median across four commercial products": [10] gives 1.24–2.10 ✓.
- "OpenAvatarChat: 2.2 s average": ✓ [53].
- "LiveAvatar, SoulX-FlashTalk need 2–8 datacentre GPUs per stream": 5×H800 and 8×H800; LiveAct needs 2 ✓.
- "MuseTalk's weights allow commercial use": ✓ [56].
- "Hosted versions cost roughly $1.80–24 per output minute": ✓ [67][68].
- InfiniteTalk "clean for about a minute in image-to-video mode": ✓ [29].
- "Duix-Avatar … model licence is non-commercial": ✓ [41].
- "Duix-Mobile's on-device avatars must be trained by the vendor as a paid service": the README says "contact us"; training is closed (issue 2). "Paid" is mildly GENEROUS.
- "Only D-ID among the Western vendors sells a self-hosted version": should keep "found", as Ch13 does.

## Final verdict

**Fit to publish once the fixes are made.** The numbers that carry the argument are faithful to their sources at the stated scope:
- the Avatar V architecture and metrics
- the Anam end-to-end medians
- the Tight cold-start figures
- the cost arithmetic
- the Duix licences and revenue
- the vendor prices other than Tavus

The required changes, none of which alters the chapter's conclusions:
1. Recite Tavus prices to the saved third-party copy, and fix the Ch11 $0.35 citation.
2. Narrow the two overreaching sentences (13:88 and 13:152).
3. Correct the HeyGen dates and the Avatar III pricing.
4. Move six numbers to the saved copies that actually contain them: 200 ms, 1.21 s, 32 fps, 512², the LiteAvatar training claims, and LongCat MIT.
5. Remove or source the unsupported details: 54 participants, Cara-4.1 "diffusion-based", the Fay back-ends, bitHuman CPU-only Linux, the "fake open source" quotation marks, and the Phoenix-4, Omnia, Character-3, Avatar IV and duix-skills dates.

No new sources were saved, and I wrote nothing outside this report.
