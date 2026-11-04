---
status: draft
last-verified: 2026-11-04
owner: duix-realtime research agent (saved verbatim by the main session; the harness blocked the subagent's own Write)
scope: Duix (Guiji / Silicon Intelligence) and the open-source / Chinese-ecosystem real-time digital-human stacks around it
---

# Duix and Chinese-ecosystem real-time digital-human stacks

Saved sources live in `docs/research/sources/text/<slug>.txt`. GitHub API snapshots are in `docs/research/agents/duix-realtime/gh/`. Star counts and last-push dates are as of 2026-11-04.

Labels: **Confirmed** (two or more independent sources agree), **Single-source**, **Contested** (sources disagree), **Vendor** (project's or company's own material), **Independent** (third-party test, decompile or user report).

The sibling agent `agents/oss-avatar/` covers LiveAvatar, SoulX-FlashTalk and StreamAvatar in depth.

Failed fetches (in `sources/log.jsonl`): bbtnews 403, Duix-Reface 404, Ultralight README 404, DeepWiki 429, OpenAvatarChat README_en 404.

## Headline findings

- **Duix-Avatar (formerly HeyGem) is neither per-identity trained nor fully open.**
  - The Electron client is open. The face, ASR and TTS services are Docker images containing Cython `.so` binaries [6][7][8].
  - Community Ghidra decompilation identifies the face engine as DINetV1 [7]: WeNet conformer audio features (256-d, 25 fps), SCRFD + PFLD landmarks, a 256×256 crop, optional GFPGAN ("chaofen", super-resolution) and landmark-mask paste-back. Weight files: `dinet_v1_20240131.pth` and `wenetmodel.pt`.
  - A clone is the user's reference video plus a zero-shot Fish-Speech voice prompt. No training takes place.
  - Label: Single-source for the architecture, corroborated by a second extraction that ships the same `.so` files and weights [8].
- **Duix licensing is Contested.**
  - README [1]: "global free commercial use" except firms with more than 100k users or more than US$10M annual revenue.
  - `LICENSE` [3]: more than 1,000 MAU requires a commercial licence granted at Duix's discretion. Also requires "Built with DUIX.COM", a "DUIX.COM" prefix on derived model names, and a perpetual case-study licence to Duix.
  - Model licence [4] ("Duix.Avatar:0.0.7_sdk_slim"): non-commercial only. Commercial use needs written authorisation, natural persons are not eligible, military use is banned, PRC law governs, disputes go to the licensor's local court, contact James@toolwiz.com.
- **Duix-Mobile is a CPU-only on-device player for per-identity 2D avatars.**
  - Maintainer: "pure CPU" inference using ncnn + ONNX [15].
  - Base model trained on studio green-screen plus web-collected video; public avatars are fine-tuned on 1–2 minutes [15].
  - Training code is closed [15]. Custom avatars are made by Duix from 15 s – 2 min of video [11].
  - Latency is Contested: "<120 ms on Snapdragon 8 Gen 2" in the README [11], "<1.5 s" in the repo description [5b], and a minimum 1 s of audio per push segment in SDK 4.0.1 [12].
- **Duix cloud** is server-rendered and streamed over WebRTC (Android SDK `player.connect(conversationId)` with an `onVideoTrack` callback) [17].
  - Vendor claim: 200 ms TTFB, 1080p [20][21].
  - Pricing: Free; $29/month for 150 min; $59/month for 300 min with 3 custom avatars; $4,999/month for 60,000 min with 50 custom avatars [21].
  - duix-skills (July 2026): portrait photo → live conversation link in about 20 min to 2 h; person video + audio → MP4 [22].
- **Company:** Nanjing Silicon Intelligence Technology Group (南京硅基智能), founded 2017 by Sima Huapeng [23][25].
  - HKEX Application Proof 2025-10-31 (CMBI and DBS) [25]; refiled 2026-05-21 [26].
  - Revenue RMB 531M / 655M / 789M for 2023–25 [23], and 223M in 2022 [25].
  - Net losses RMB 111M, 95.9M and 112M for 2022–24, and 8.29M in H1 2025 [24][25]. Cumulative net loss about RMB 233M for 2023–25; adjusted net profit positive in 2025 [23].
  - Gross margin fell from 45.8% to 31.6% (2023 to H1 2025). Direct sales are more than 96% of revenue [24]. Customers fell from 1,009 to 431 (2023–25); the largest customer brought RMB 325M in 2025 [23].
  - Claimed 32.2% share of China's digital-human agent market (CIC data) and more than 100k deployed agents (Vendor, via prospectus) [23][24]. DUIX ONE multimodal API launched in 2024 [23].
  - Repos moved from GuijiAI to duixcom: HeyGem.ai → Duix.Heygem → Duix-Avatar, and duix.ai → Duix-Mobile. GitHub API redirects confirm both [5][5b].

## Duix-Avatar

- **Function** [1]: offline video generation and voice clone, on Windows (WSL2 Docker) or Ubuntu 22.04. Three services: `guiji2025/fun-asr` (FunASR), `guiji2025/fish-speech-ziming` (Fish-Speech TTS) and `guiji2025/duix.avatar` (f2f/gen-video). APIs: `:18180/v1/invoke` (TTS) and `:8383/easy/submit` (video). The README states "non-real-time" and points to duix.com for interaction. 8 script languages. Vendor table: open-source lip-sync is "usable"; the paid API is "stunning and higher definition".
- **Hardware** [1][6][9][10]: reference i5-13400F, 32 GB RAM, RTX 4070, more than 100 GB disk; NVIDIA GPU mandatory. First image pull about 70 GB; images total 60–100 GB. Separate compose file for RTX 50-series / CUDA 12.8. Linux AppImage client. Olares one-click app. Community Podman guide recommends at least 8 GB VRAM.
- **Activity** [5][6]: 16,219 stars, 2,764 forks. Created 2024-12-24. Last push 2026-04-21 (README only). Last release v1.0.6 on 2025-09-28. 410 of 512 issues open. Maintenance mode.
- **Known issues** [6]: `model/addModel` SQLite3 bind error and socket hang-up (many duplicates); f2f restart loops with "no NVIDIA driver" (#47, #158, #187), one user advises driver ≤ 550 / CUDA ≤ 12.4 (#394); jobs stuck at 5% or 20% (#58, #226, #471); RTX 50 cloned-voice buzz (#435); `h264_nvenc` missing (#533); T4 fails to start (#447); requests for a remote client/server split (#589) and for source code (#243, "fake open source").
- **Independent ecosystem** [7][8]: HeyGem12, a clean-room Python 3.12 reimplementation (created October 2026, 86 stars), claims frame-aligned parity with the original on 23 paired clips and says the weights are "personal / non-commercial only". HeyGem-Linux-Python-Hack: 505 stars.

## Duix-Mobile

- **Platforms:** Android (armeabi-v7a / arm64-v8a, Android 10+, Snapdragon 8 Gen 2-class CPU, 8 GB RAM, 800 MB free, 1 GB storage) and iOS. OpenGL ES rendering; transparency supported [12][13].
- **Input:** 16 kHz mono PCM streaming with barge-in since 2025-07-17. Ships 4 public avatars [11].
- **Unexplained:** iOS v1.2.3 "support for 128 models" [13].
- **Licence:** duix.com Community License. More than 1,000 MAU requires a licence; "Powered by Duix.com" required [14].
- **Activity** [5b][15]: 8,308 stars. Created 2024-05-16. Last push 2026-08-05 (README). Release v2.0.1 on 2025-10-13. 56 of 84 issues open.
- **Issues** [15]: "not real open source, just advertising" (#28, #43); Android 9 crash (#37); missing `libscrfdncnn.so` (#10); broken public models (#26); watermark complaints (#23).
- **Duix-Reface** is linked as open source in the README [11] but returns 404.

## Duix cloud

- **API surface:** REST endpoints for sessions, concurrency and avatar creation, plus H5, Android and iOS SDKs [16]. SDK v0.3.0 added streaming-audio driving; v0.3.2 added camera input [18].
- **Billing:** per conversation minute; all plans include API access [19][21].
- **Architecture:** undisclosed.

## LiveTalking (lipku/LiveTalking, formerly metahuman-stream)

- **Face models:** code tree `avatars/` has only `wav2lip`, `musetalk` and `ultralight` [29]; the README still lists ER-NeRF [28]. The commercial edition adds "wav2lipls" [28]. Wav2Lip and MuseTalk need only per-avatar video preparation; Ultralight-Digital-Human (anliyuan, 2.7k stars) needs per-person training.
- **Vendor FPS** [28]:

  | Model | GPU | FPS |
  |---|---|---|
  | wav2lip256 | RTX 3060 | 60 |
  | wav2lip256 | RTX 3080 Ti | 120 |
  | MuseTalk | RTX 3080 Ti | 42 |
  | MuseTalk | RTX 3090 | 45 |
  | MuseTalk | RTX 4090 | 72 |

  Real-time requires `inferfps` and `finalfps` ≥ 25. Idle concurrency is CPU-bound; speaking concurrency is GPU-bound.
- **Independent user reports** [29]: about 3 s barge-in lag because WebRTC buffers and in-flight inference cannot be flushed (#510); three-stream stutter on a 4090 (#516); MuseTalk mouth still moving after audio ends (#366).
- **Composition:** `/human` (echo or LLM chat) → TTS plugin (EdgeTTS, GPT-SoVITS, CosyVoice, Tencent) → audio features → lip-sync → WebRTC, RTMP or virtual camera. ASR is external.
- **Licence:** Apache-2.0, plus a request for a watermark on Bilibili/Douyin videos.
- **Activity:** 10,260 stars. Last push 2026-10-20. Releases v2.0 (2026-03-31) to v2.0.4 (2026-06-20).

## OpenAvatarChat (HumanAIGC-Engineering, Alibaba)

- **Pipeline:** gradio-webrtc + Silero VAD + SenseVoice + LLM (or Qwen-Omni end-to-end) + CosyVoice + avatar handler [30].
- **Avatars:** LiteAvatar, LAM, MuseTalk and SoulX-FlashHead (added in v0.6.0, 2026-04-17). v0.6.0 also added a front-end split (OpenAvatarChat-WebUI), duplex barge-in, and a beta OpenClaw agent mode.
- **Latency:** "average response 2.2 s" [30][31] (Vendor).
- **Licence and activity:** Apache-2.0. 3,848 stars. Last push 2026-07-31 [32].

## LiteAvatar (HumanAIGC/lite-avatar)

- **Model:** Paraformer features → mouth parameters → light 2D generator. Vendor claims 30 fps on CPU only, "mobile-deployable" [33].
- **Per-identity, closed:** training will not be released; custom avatars are a paid Alibaba Cloud Bailian service (#3, #24) [34].
- **Licence:** code MIT; weights licence unspecified (#27).
- **Activity:** 487 stars. Last push 2025-06-30 (dormant).

## LAM + LAM_Audio2Expression (Alibaba Tongyi Lab)

- **Model:** one-shot 3D Gaussian head (SIGGRAPH 2025). Reconstruction 1.4 s; render 562.9 FPS on A100 and 110+ FPS on a Xiaomi 14 (Vendor) [35].
- **Driver:** A2E predicts ARKit blendshapes from audio [36]. WebGL renderer, exports to OpenAvatarChat.
- **Licence and activity:** Apache-2.0. LAM 1,091 stars (last push 2026-06-10); A2E 231 stars (last push 2025-10-24).

## Linly-Talker and Linly-Talker-Stream

- **Linly-Talker** [37]: SadTalker, Wav2Lip(v2), ER-NeRF or MuseTalk faces; Whisper or FunASR; multiple LLMs and TTS engines. MIT, 3,478 stars, last push 2026-02-10.
- **Linly-Talker-Stream** [38]: WebRTC full-duplex version referencing LiveTalking's real-time design. Apache-2.0, 151 stars, last push 2026-09-05. Early stage: demo video TODO, server-side VAD on the roadmap.

## Fay (xszyou/Fay)

- **Role:** orchestrator only — LLM agents, ASR and TTS, MCP tools, memory, barge-in and multi-user sessions [39].
- **Face back-ends:** fay-ue5 (MetaHuman with fixed-animation, MetaHuman SDK or OVRLipSync lip-sync) [40]. Docs reportedly list LiveTalking, Duix and Unity connectors (Feishu page, JS-only, unsaved).
- **Licence:** GitHub reports GPL-3.0; the README says "商用免责" (commercial-use disclaimer).
- **Activity:** 13,607 stars. Last push 2026-09-21.

## awesome-digital-human-live2d (wan-h)

Live2D characters; runs on under 2 cores / 2 GB [41]. Pluggable through Dify, FastGPT, Coze or OpenAI-compatible APIs. MIT. 2,437 stars. Last push 2026-05-18.

## Ditto (antgroup)

- **Model:** motion-space DiT + LivePortrait-style warping generator; one-shot. ACM MM 2025 [42][43].
- **Speed:** every module below RTF 1 on a single A100 [44]. Offline RTF 0.635 at 10 steps, versus MuseTalk 2.248 in the same table [44]. Tested with TensorRT 8.6.1 [42].
- **Licence and activity:** Apache-2.0; training code released 2025-11-12. 929 stars. Last push 2025-11-12.

## MuseTalk 1.5 (Tencent Music Lyra Lab)

- **Model:** latent inpainting on a 256×256 face region, "30fps+ on V100". v1.5 released 2025-03-28 with training code [45].
- **Licence:** code MIT; weights usable for any purpose, including commercial.
- **Real-time adoption:** used by LiveTalking, OpenAvatarChat and Linly-Talker (Confirmed real-time on desktop GPUs).
- **Activity:** 6,871 stars. Last push 2025-09-26.

## SoulX-FlashTalk and SoulX-FlashHead (Soul AI Lab)

- **FlashTalk (14B)** [46][47]: claims 0.87 s start-up and 32 FPS. Real-time only on 8×H800. Single GPU needs more than 64 GB VRAM, or 40 GB with offload. Apache-2.0. 1,561 stars. Last push 2026-07-30.
- **FlashHead (1.3B)** [48]: Lite model 96 FPS on one RTX 4090, or 3 concurrent real-time streams. Pro model 10.8 FPS on one 4090, real-time on 2× RTX 5090. Apache-2.0. 1,176 stars. Last push 2026-05-28. Integrated into OpenAvatarChat.

## Big-tech real-time releases (brief)

- **Alibaba-Quark LiveAvatar** [49]: Wan2.2-S2V-14B + LoRA. 45 FPS on multiple H800s; FP8 fits 48 GB GPUs. ECCV 2026. Apache-2.0, 2,504 stars.
- **ByteDance:** X-Streamer (real-time on 2×A100) [50] and FlowAct-R1 (480p at 25 fps, TTFF about 1.5 s) [51]. Papers only.
- **Tencent:** StreamAvatar (CVPR 2026) is a paper plus project page [52]. No open real-time Tencent release found besides MuseTalk.
- **OpenTalking:** reported in one blog post [53]; repo not located.

## Comparison table

| Project | Face model | Real-time? | Hardware | Clone input | Licence | Stars | Last push |
|---|---|---|---|---|---|---|---|
| Duix-Avatar | DINetV1 + WeNet, 256 px (decompiled) | No | NVIDIA GPU (RTX 4070), ~100 GB disk | Short video, no training | Contested: 1k MAU / 100k users / model non-commercial | 16,219 | 2026-04-21 |
| Duix-Mobile | Undisclosed 2D per-identity, ncnn/ONNX | Yes (<120 ms claim, contested) | CPU, Snapdragon 8 Gen 2, 8 GB | 15 s – 2 min, Duix-trained (paid) | Duix Community (1k MAU) | 8,308 | 2026-08-05 |
| Duix cloud | Undisclosed, WebRTC | Yes (200 ms TTFB claim) | Cloud | Video or single photo | SaaS, $29–$4,999/mo | n/a | n/a |
| LiveTalking | Wav2Lip-256 / MuseTalk / Ultralight | Yes | RTX 3060+ (Wav2Lip), 3080 Ti+ (MuseTalk) | Short video | Apache-2.0 (+ watermark request) | 10,260 | 2026-10-20 |
| OpenAvatarChat | LiteAvatar / LAM / MuseTalk / FlashHead | Yes (2.2 s claim) | CPU to RTX 4090 | Gallery / photo / video | Apache-2.0 | 3,848 | 2026-07-31 |
| LiteAvatar | 2D mouth-param generator | Yes (30 fps CPU claim) | CPU | Per-identity, closed, paid | MIT / weights unspecified | 487 | 2025-06-30 |
| LAM + A2E | 3D Gaussian + ARKit blendshapes | Yes (110 fps phone claim) | WebGL client | Single image | Apache-2.0 | 1,091 / 231 | 2026-06-10 |
| Linly-Talker (+Stream) | SadTalker / Wav2Lip / ER-NeRF / MuseTalk | Near-RT / duplex | GPU | Image or video | MIT / Apache-2.0 | 3,478 / 151 | 2026-02 / 2026-09 |
| Fay | None (orchestrator) | n/a | Any | n/a | GPL-3.0 | 13,607 | 2026-09-21 |
| awesome-dh-live2d | Live2D | Yes | 2 cores / 2 GB | Live2D model | MIT | 2,437 | 2026-05-18 |
| Ditto | Motion DiT + warping | Yes on A100 | A100 + TensorRT | Single image | Apache-2.0 | 929 | 2025-11-12 |
| MuseTalk 1.5 | Latent inpainting, 256 px | Yes | V100+ | Short video | MIT, commercial OK | 6,871 | 2025-09-26 |
| SoulX-FlashHead | 1.3B diffusion | Yes (4090 Lite) | RTX 4090/5090 | Single image | Apache-2.0 | 1,176 | 2026-05-28 |
| SoulX-FlashTalk | 14B diffusion | 8×H800 only | Datacentre | Single image | Apache-2.0 | 1,561 | 2026-07-30 |
| LiveAvatar | Wan2.2-S2V-14B + LoRA | Multi-H800 | Datacentre | Single image | Apache-2.0 | 2,504 | 2026-08-24 |

## Implications for the review

Ch10 "Real-time AI assistant with face" can use three tiers:

1. **CPU/mobile per-identity 2D players.** Duix-Mobile and LiteAvatar. Identity creation is closed and sold.
2. **GPU inpainting lip-sync on a looping reference video.** LiveTalking with Wav2Lip or MuseTalk; Duix-Avatar for offline use. Open, and commercially clean with MuseTalk.
3. **One-shot diffusion streaming.** FlashHead on consumer GPUs; FlashTalk and LiveAvatar need datacentre multi-GPU.

"Open source" in this ecosystem often means an open client or SDK with closed weights or training.

No independent latency benchmarks were found for any of these stacks; every latency and FPS figure is vendor-reported, except user reports in GitHub issues.

## Open questions / could not verify

- **Duix-Mobile:** face architecture, resolution and fps undisclosed; "128 models" unexplained.
- **Latency:** no independent tests for Duix-Mobile, Duix cloud or OpenAvatarChat. Duix-Mobile's <120 ms vs <1.5 s conflict is unresolved.
- **DINet identification:** rests on one decompile; never confirmed by Duix.
- **Duix licence:** no statement reconciles the three documents. The licensor entity is unclear ("Our Company", toolwiz.com email).
- **Duix cloud:** model undisclosed, including what powers photo-to-avatar in duix-skills.
- **Duix-Reface:** returns 404.
- **OpenAvatarChat hardware figures:** DeepWiki returned 429, so these remain unsaved snippets.
- **Fay connector list:** Feishu page is JS-only and unsaved.
- **Ultralight README:** fetch returned 404.
- **Business press:** bbtnews 403. Full HKEX prospectus not parsed; only the cover page is saved.
- **Big-tech affiliations:** ByteDance/Tencent attributions for X-Streamer, FlowAct-R1 and StreamAvatar come from search snippets only.
- **"10-second clip" for Duix-Avatar:** appears only in third-party posts.

## Sources

Slugs are in `docs/research/sources/text/`; `gh/` means `docs/research/agents/duix-realtime/gh/`.

- [1] raw.githubusercontent.com/duixcom/Duix-Avatar/main/README.md → `raw-githubusercontent-com-duixcom-duix-avatar-main-readme-md` (+ `-readme-zh-md`; older page copy `github-com-duixcom-duix-avatar`)
- [3] …/Duix-Avatar/main/LICENSE → `duix-avatar-LICENSE`
- [4] …/Duix-Avatar/main/Duix.Avatar model community Licensing Agreement.pdf → `duix-avatar-model-community-licence-pdf`
- [5] `gh/duixcom-Duix-Avatar.json`, `gh/GuijiAI-HeyGem.ai.json`, `gh/duixcom-Duix.Heygem.json`, `gh/duixcom-Duix-Avatar-releases.json`
- [5b] `gh/duixcom-Duix-Mobile.json`, `gh/GuijiAI-duix.ai.json`, `gh/duixcom-Duix-Mobile-releases.json`
- [6] `gh/duixcom-Duix-Avatar-issues-top-comments.json`, `gh/duixcom-Duix-Avatar-issue-{243,10,394}.json`
- [7] raw…/oaifaye/HeyGem12/main/README.md → `raw-githubusercontent-com-oaifaye-heygem12-main-readme-md`; `gh/oaifaye-HeyGem12.json`
- [8] raw…/Holasyb918/HeyGem-Linux-Python-Hack/main/README.md → `raw-githubusercontent-com-holasyb918-heygem-linux-python-hack-main-readme-md`
- [9] docs.olares.com/use-cases/duix-avatar.html → `docs-olares-com-use-cases-duix-avatar-html`
- [10] jishuzhan.net/article/1994199649645821954 → `jishuzhan-net-article-1994199649645821954`
- [11] raw…/duixcom/Duix-Mobile/main/README.md → `raw-githubusercontent-com-duixcom-duix-mobile-main-readme-md` (+ zh)
- [12] …/duix-android/dh_aigc_android/README.md → `raw-githubusercontent-com-duixcom-duix-mobile-main-duix-android-dh-aigc-android-readme-md` (+ zh)
- [13] …/duix-ios/GJLocalDigitalDemo/README.md → `raw-githubusercontent-com-duixcom-duix-mobile-main-duix-ios-gjlocaldigitaldemo-readme-md`
- [14] …/Duix-Mobile/main/LICENSE → `duix-mobile-LICENSE`
- [15] `gh/duixcom-Duix-Mobile-issues-top-comments.json`, `gh/duixcom-Duix-Mobile-issue-{2,4,19,28,63}.json`
- [16] docs.duix.com/llms.txt → `docs-duix-com-llms-txt`
- [17] docs.duix.com/sdks/android/quickstart.md → `docs-duix-com-sdks-android-quickstart-md`
- [18] docs.duix.com/sdks/versions.md → `docs-duix-com-sdks-versions-md`
- [19] docs.duix.com/documentation/introduction.md → `docs-duix-com-documentation-introduction-md`
- [20] duix.com → `duix-com`
- [21] duix.com/pricing → `duix-com-pricing`
- [22] raw…/duixcom/duix-skills/main/README.md → `raw-githubusercontent-com-duixcom-duix-skills-main-readme-md`; `docs-duix-com-documentation-duix-avatar-conversation-md`
- [23] 36kr.com/p/3825797690614017 → `36kr-com-p-3825797690614017` (Huxiu copy: `huxiu-com-article-4861640-html`)
- [24] eu.36kr.com/en/p/3559611691072647 → `eu-36kr-com-en-p-3559611691072647`
- [25] itiger.com/news/1160799526 → `itiger-com-news-1160799526`
- [26] hkexnews sehk26052101556.pdf → `www1-hkexnews-hk-app-sehk-2026-108560-a133153-sehk26052101556-pdf`
- [28] raw…/lipku/LiveTalking/main/README.md → `raw-githubusercontent-com-lipku-livetalking-main-readme-md` (+ `-readme-en-md`)
- [29] `gh/lipku-LiveTalking.json`, `-tree.json`, `-issues-top-comments.json`, `-issue-510.json`, `-releases.json`; `gh/anliyuan-Ultralight-Digital-Human.json`
- [30] raw…/HumanAIGC-Engineering/OpenAvatarChat/main/README.md → `raw-githubusercontent-com-humanaigc-engineering-openavatarchat-main-readme-md`
- [31] humanaigc-engineering.github.io/OpenAvatarChat → `humanaigc-engineering-github-io-openavatarchat`
- [32] `gh/HumanAIGC-Engineering-OpenAvatarChat.json`, `-releases.json`, `gh/HumanAIGC-Engineering-OpenAvatarChat-WebUI.json`
- [33] raw…/HumanAIGC/lite-avatar/main/README.md → `raw-githubusercontent-com-humanaigc-lite-avatar-main-readme-md`
- [34] `gh/HumanAIGC-lite-avatar.json`, `-issues-top-comments.json`, `-issue-{3,21,24,27}.json`
- [35] raw…/aigc3d/LAM/README.md → `aigc3d-lam-readme`; `gh/aigc3d-LAM.json`
- [36] raw…/aigc3d/LAM_Audio2Expression/main/README.md → `raw-githubusercontent-com-aigc3d-lam-audio2expression-main-readme-md`
- [37] raw…/Kedreamix/Linly-Talker/main/README.md → `raw-githubusercontent-com-kedreamix-linly-talker-main-readme-md`
- [38] raw…/Kedreamix/Linly-Talker-Stream/main/README.md → `raw-githubusercontent-com-kedreamix-linly-talker-stream-main-readme-md`; `gh/Kedreamix-Linly-Talker-Stream.json`
- [39] raw…/xszyou/Fay/main/README.md → `raw-githubusercontent-com-xszyou-fay-main-readme-md`; `gh/xszyou-Fay.json`
- [40] raw…/py-syy/fay-ue5/main/README.md → `raw-githubusercontent-com-py-syy-fay-ue5-main-readme-md`
- [41] raw…/wan-h/awesome-digital-human-live2d/main/README.md → `raw-githubusercontent-com-wan-h-awesome-digital-human-live2d-main-readme-md`
- [42] raw…/antgroup/ditto-talkinghead/main/README.md → `raw-githubusercontent-com-antgroup-ditto-talkinghead-main-readme-md`
- [43] arxiv.org/abs/2411.19509 → `arxiv-org-abs-2411-19509`
- [44] arxiv.org/html/2411.19509v1 → `arxiv-org-html-2411-19509v1`
- [45] raw…/TMElyralab/MuseTalk/main/README.md → `raw-githubusercontent-com-tmelyralab-musetalk-main-readme-md`
- [46] raw…/Soul-AILab/SoulX-FlashTalk/main/README.md → `raw-githubusercontent-com-soul-ailab-soulx-flashtalk-main-readme-md`
- [47] arxiv.org/abs/2512.23379 → `arxiv-org-abs-2512-23379`
- [48] raw…/Soul-AILab/SoulX-FlashHead/main/README.md → `raw-githubusercontent-com-soul-ailab-soulx-flashhead-main-readme-md`
- [49] raw…/Alibaba-Quark/LiveAvatar/main/README.md → `raw-githubusercontent-com-alibaba-quark-liveavatar-main-readme-md`; `gh/Alibaba-Quark-LiveAvatar.json`
- [50] arxiv.org/abs/2509.21574 → `arxiv-org-abs-2509-21574`
- [51] arxiv.org/abs/2601.10103 → `arxiv-org-abs-2601-10103`
- [52] arxiv.org/abs/2512.22065 → `arxiv-org-abs-2512-22065`
- [53] 80aj.com/2026/05/24/digital-human-gap-opentalking → `80aj-com-2026-05-24-digital-human-gap-opentalking`
