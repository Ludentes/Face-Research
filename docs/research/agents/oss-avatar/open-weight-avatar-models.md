---
status: draft dossier for Ch06 follow-up
last-verified: 2026-11-04
owner: oss-avatar research agent (extracted verbatim from its hand-back by the main session; harness blocked its Write)
scope: open-weight photo/clip + audio -> presenter video models, mid-2025 to 2026-11, not already in Ch06
---

# Open-weight alternatives to HeyGen-style avatar video (mid-2025 to November 2026)

## Summary

Since mid-2025 open-weight avatar video has turned into a crowded field of its own. Nearly all of it is built on video-diffusion transformers, and most of those are fine-tunes or LoRAs on **Alibaba Wan 2.1/2.2** (Apache-2.0). The few exceptions include LongCat-Video, Kandinsky 5 Video, HunyuanVideo and LTX-2. Three things changed relative to what Ch06 describes:

1. **Long-form and half/full-body generation became normal in open weights.** InfiniteTalk, StableAvatar, LongCat-Video-Avatar, LiveAvatar, SoulX-LiveAct and Kandinsky S2V all advertise minute-to-hour generation from one photo plus audio, with upper-body motion and gestures. The long-duration claims come only from the authors.
2. **Real-time streaming arrived through Self-Forcing / DMD causal distillation of 14B Wan models.** LiveAvatar, SoulX-FlashTalk and SoulX-LiveAct reach 20 to 45 FPS, but only on 2 to 8 H100/H200/H800 GPUs. On one consumer GPU, real time exists only for 1.3B models: SoulX-FlashHead Lite (96 FPS on an RTX 4090, 512²) and AvatarForcing (34 ms/frame). Both trade away visible quality.
3. **The one independent cross-model benchmark** (Tight Studio, Aug 2026 [1][2]) found that no official open pipeline ran faster than playback on a cold job. Wan2.2-S2V took 204.6 s of compute per output second. LiveAvatar was the sharpest, EchoMimicV3-Flash the best value on a 48 GB card, and LongCat-Video-Avatar 1.5 the most expressive.

Evidence labels: **Confirmed** means two or more independent sources (an author's paper and that author's own README count as one party for performance claims, but as two sources for release facts such as dates and licences). **Single-source** means one party only. **Contested** means sources disagree. GitHub stars, licences and push dates are from the GitHub API on 2026-11-04 [3].

## Comparison table

"s/s" means seconds of compute per second of output video. RT means real time.

| Model (org) | First open release | Input → output | Base / arch | Speed & GPU | Licence (code / weights) | Stars | Ch06 gaps closed |
|---|---|---|---|---|---|---|---|
| InfiniteTalk (Meituan/MeiGen) | 2025-08-19 | image/video + audio → face+head+body; "unlimited", I2V clean ~1 min | Wan2.1-I2V-14B, streaming chunks + context frames | 40 steps default; 4–8 with lightx2v/FusionX LoRA; low-VRAM mode; no measured s/s found | Apache-2.0 / Apache-2.0 | 8,302 | long-form (claimed), half-body |
| MultiTalk (MeiGen) | 2025-06-09 | image + 1–N audio → multi-person, ≤15 s | Wan2.1-I2V-14B, L-RoPE | 480p on 1×RTX 4090 (low-VRAM); 8 GB via Wan2GP | Apache-2.0 / Apache-2.0 | 3,029 | half-body, multi-person |
| Wan2.2-S2V-14B (Alibaba) | 2025-08-26 | image + audio (+pose, TTS) → 480p/720p | Wan2.2 14B | 204.6 s/s cold, H200, 58.7 GB [1]; ≥80 GB single GPU | Apache-2.0 / Apache-2.0 | 18,358 (Wan2.2) | half/full-body |
| OmniAvatar (ZJU/Alibaba) | 2025-06-24 | image + audio + text → full/half-body, 480p | Wan2.1-T2V-14B/1.3B + LoRA | 16 s/it on 1×A800, 36 GB; 8 GB at 22 s/it | Apache-2.0 / Apache-2.0 | 1,867 (inactive since 2025-08) | half-body |
| StableAvatar (Fudan/Microsoft) | 2025-08-11 | image + audio → "infinite", 512² / 480×832 | Wan2.1-Fun-1.3B + time-step-aware audio adapter | 30–50 steps (10 in ComfyUI) | MIT / MIT | 1,274 | long-form (claimed) |
| EchoMimicV3 / -Flash (Ant) | 2025-08-08 / 2026-01-22 | image + audio → head or half-body | Wan2.1-Fun-1.3B | Flash 8 steps, "12 GB"; measured 33.7 GB, 252 s for 3.6 s on L40S [1] | Apache-2.0 / Apache-2.0 | 1,115 | half-body |
| HunyuanVideo-Avatar (Tencent) | 2025-05-28 | image + audio (+emotion ref) → portrait/upper/full body, multi-character | HunyuanVideo MM-DiT | min 24 GB "very slow", 96 GB recommended; 10 GB via Wan2GP | Hunyuan Community (excl. EU/UK/KR; >100 M MAU needs a licence) | 2,204 | half/full-body |
| HuMo (ByteDance/Tsinghua) | 2025-09-10 | text + ref + audio → 480/720p, trained on 97 frames | 17B / 1.7B on Wan components | 1.7B: 480p in 8 min on a 32 GB GPU | Apache-2.0 / Apache-2.0 | 1,295 | half-body (short only) |
| LongCat-Video-Avatar 1.0/1.5 (Meituan) | 2025-12-16 / 2026-05-21 | image/text + audio (1–N) → 480/720p; continuation | LongCat-Video 13.6B (not Wan); v1.5 Whisper-L, DMD2 8 NFE, INT8 | 46.8 GB, 233 s for 3.6 s on H200 [1] | MIT / MIT | 9,342 | long-form (claimed), half-body + gestures |
| LiveAvatar (Alibaba Quark/USTC) | 2025-12-08 | image + audio → streaming, 10,000+ s | LoRA on Wan2.2-S2V; Self-Forcing DMD 4-step, TPP | 45 FPS RT on 5×H800, TTFF 1.21 s; 1×80 GB offline (48 GB FP8); 48.8 s/s cold on H200, 384×704 [1] | Apache-2.0 / Apache-2.0 | 2,504 | long-form, RT (datacenter) |
| SoulX-FlashTalk (Soul) | 2026-01-08 | image + audio → infinite streaming | 14B from InfiniteTalk/Wan2.1 | 32 FPS, 0.87 s start-up on 8×H800; >64 GB; warm chunk ≈3.75 s on H200 [1] | Apache-2.0 / Apache-2.0 | 1,561 | long-form, RT (datacenter) |
| SoulX-FlashHead (Soul) | 2026-02-12 | image + audio → head 512² streaming | 1.3B Wan2.1; Lite uses LTX VAE | Lite 96 FPS on 1×4090 (3 concurrent RT); Pro 10.8 FPS on 4090, RT on 2×5090; 5.8 GB measured [1] | Apache-2.0 code; DiT Apache, Lite VAE OpenRAIL-M | 1,176 | RT full-face on consumer GPU |
| SoulX-LiveAct (Soul) | 2026-03-16 | image + audio (+action/emotion edit) → hour-scale, 720×416 / 512² | Wan2.1-14B + 4B audio; Neighbor Forcing + ConvKV | 20 FPS RT on 2×H100/H200; 6 FPS on 1×5090 | HF Apache-2.0; no GitHub LICENSE | 1,229 | long-form (hour), RT |
| AvatarForcing (Kling AI Research) | 2026-03 | image + audio → 832×480 @25 | Wan2.1-T2V-1.3B, 1-step | 34 ms/frame (hardware unstated) | Apache-2.0 code; weights untagged | 84 | RT (small) |
| AptAvatar (Taobao Live) | code 2026-06-29, weights 2026-07 | image + audio → 720p long-form | 14B from InfiniteTalk/Wan, 2 NFE | "60×" (paper) | Apache-2.0 / Apache-2.0 | 235 | long-form (claimed) |
| Kandinsky S2V 1.0 (Kandinsky Lab) | 2026-10-13 | image + speech + text → whole figure, 25 fps SD/HD, 5 s chunks | Kandinsky 5 Video 2B/21B, π-Flow distilled | H100: Lite-distill 8.7 s/s; Pro-distill 41.5; Pro 189; Pro-HD 773; 46–57 GB | MIT / MIT | 17 | half/full-body, long-form (claimed) |
| TalkVerse-5B (Snap) | 2025-12-31 | image + audio → minute-long | Wan2.2-TI2V-5B | "10× cheaper than Wan-S2V", 4090 with offload | Snap Non-Commercial | 39 | long-form; non-commercial |

## Per-model sections

**InfiniteTalk.**
- arXiv 2508.14033 (2025-08-19). Code, weights, Gradio and ComfyUI were released the same day. Apache-2.0, with no claim on outputs [4][5][81]. **Confirmed.**
- Does "sparse-frame dubbing": it keeps reference keyframes and re-synthesises lips, head, posture and expression. Works in both V2V and I2V modes.
- Built on Wan2.1-I2V-14B-480P with chinese-wav2vec2. Context frames carry motion between chunks.
- Outputs 480/720p; default max is 40 s. The README admits I2V is "good up to 1 minute", after which colour shift appears, and that FusionX "exacerbates color shift over 1 minute and reduces ID preservation" [5]. **Single-source** (a self-critical admission).
- Speed tooling: TeaCache, INT8, multi-GPU, low-VRAM mode, and lightx2v (4-step) or FusionX (8-step) LoRAs [5]. LightX2V supports it [71]. **No measured s/s on a named GPU.**
- Hosted prices: WaveSpeed $0.03/s at 480p and $0.06/s at 720p, up to 10 min [74]; fal $0.20/s at 480p, doubled for 720p [75].
- AptAvatar's 720p table (from a competitor): Sync-C 7.17, FID 24.8 [34].
- It is the base for FlashTalk and AptAvatar.

**MultiTalk.** arXiv 2505.22647; weights 2025-06-09; NeurIPS 2025; Apache [6][7]. Multi-person conversation from multiple audio streams, with L-RoPE binding each stream to a person. 480p only in code (720p needs multiple GPUs), up to 15 s. Runs on one 4090 in low-VRAM mode, or 8 GB via Wan2GP. Supports 4–8-step LoRAs [7].

**Wan2.2-S2V-14B.**
- arXiv 2508.18621 and weights on 2025-08-26, Apache [8][9][63]. **Confirmed.**
- Image + audio, with optional pose and CosyVoice TTS. 480/720p. Needs ≥80 GB on a single GPU [9].
- Tight measured 780 s for a 3.8 s clip on an H200 (204.6 s/s), 58.7 GB, 512×896 at 16 fps. Identity and background held well, motion was restrained, and it was the slowest and costliest in the cohort [1][2]. **Confirmed.**

**OmniAvatar.** arXiv 2506.18866. 14B weights 2025-06-24, 1.3B 2025-07-02. Apache [10][11]. Full/semi-body audio-driven video with text control, pixel-wise multi-hierarchical audio embedding, and LoRA on Wan2.1-T2V. 480p only. On an A800: 16 s/it at 36 GB, 22 s/it at 8 GB; 25 steps recommended. Inactive since 2025-08.

**StableAvatar.** arXiv 2508.08248, MIT, NeurIPS 2026 per the README [12][13]. Claims "first end-to-end … infinite-length" video using a time-step-aware audio adapter, Audio Native Guidance and a sliding window. Released weights are Wan2.1-Fun-1.3B at 512² or 480×832; there is training code for 14B but no 14B weights.

**EchoMimicV3 / Flash.**
- arXiv 2507.03905, AAAI 2026, Apache. Code 2025-08-08; Flash 2026-01-22 [14][15]. A unified 1.3B model on Wan2.1-Fun.
- Claims 12 GB. Tight measured 33.7 GB at the official 768 config and 252 s for 3.6 s on an L40S, and called it the "strongest balance for deployment" [1]. VRAM is **Contested**.
- EchoMimicV2 (Nov 2024, half-body, Apache) is outside the window [58].

**HunyuanVideo-Avatar.**
- arXiv 2505.20156; released 2025-05-28 [16][17].
- MM-DiT with character-image injection, an Audio Emotion Module and a Face-Aware Audio Adapter. Multi-style and multi-character, portrait to full body.
- Hardware: 24 GB minimum ("very slow"), 96 GB recommended, or 10 GB via Wan2GP.
- **Licence:** the Hunyuan Community License excludes the EU, UK and South Korea, and services above 100 M MAU need permission [18].
- No 2026 Tencent open avatar successor found. HunyuanPortrait (SVD-based, video-driven) [79] is not audio-driven. Ch05 already mentions both briefly.

**HuMo.** arXiv 2509.08519. 17B weights 2025-09-10, 1.7B 2025-09-16. Apache [47][48]. Text + reference + audio. Trained on 97 frames, and the authors say longer clips degrade, so it is not long-form. 1.7B makes 480p in 8 min on a 32 GB GPU. It is ByteDance's open model; OmniHuman stays closed.

**LongCat-Video-Avatar 1.0 / 1.5.**
- v1.0 on 2025-12-16; v1.5 on 2026-05-21 (arXiv 2605.26486). MIT [19][20][21]. **Confirmed.**
- Built on LongCat-Video, a 13.6B continuation-pretrained DiT (arXiv 2510.22200) [83]. **Not Wan.**
- v1.5 adds Whisper-L-v3, RLHF, DMD2 8 NFE and INT8. The official example uses 2 GPUs. 480/720p.
- Authors' human evaluation (500+ cases): "competitive or superior" to HeyGen, OmniHuman 1.5 and Kling Avatar 2.0 [20]. **Single-source.**
- Tight: 46.8 GB, 233 s on one H200; "most expressive", added a hand gesture, but "mouth frames looked exaggerated" [1].
- AptAvatar table: lowest Sync-C (4.14) of the baselines [34].
- Lip sync is **Contested**; expressiveness is **Confirmed**. Most-liked avatar model on HF (887 likes) [77].

**LiveAvatar.**
- arXiv 2512.04677. Weights 2025-12-08, single-GPU code 2025-12-12, v1.1 (FP8, 48 GB) 2026-01-20. ECCV 2026 Spotlight. Apache [22][23][24].
- A LoRA on Wan2.2-S2V. Self-Forcing DMD, 4 steps, rolling sink frame, Timestep-forcing Pipeline Parallelism.
- 45 FPS with TTFF 1.21 s on 5×H800. Claims more than 10,000 s of stable generation. Introduces the GenBench long-form benchmark.
- Real time needs five 80 GB GPUs.
- Tight: fastest heavyweight cold job (181 s for 3.7 s on one H200, 384×704, 61.4 GB), "sharpest identity" [1]. Quality is **Confirmed**; the real-time figure is **Single-source**.

**SoulX-FlashTalk.**
- arXiv 2512.23379; weights 2026-01-08; Apache [25][26]. 14B, from InfiniteTalk.
- Self-correcting bidirectional distillation (bidirectional attention within chunks) plus retrospective self-correction.
- 32 FPS and 0.87 s start-up, real time only on ≥8×H800. Needs >64 GB (40 GB with offload). The 4-GPU version is still "coming soon".
- Tight: 120 s compile, then ~3.75 s per warm chunk; "stable face, clear mouth" [1]. AptAvatar: best baseline for sync (Sync-C 7.74) [34]. **Confirmed.**

**SoulX-FlashHead.**
- arXiv 2602.07449; released 2026-02-12 [27][28]. 1.3B Wan2.1-based, head only, with the VividHead dataset (782 h).
- Lite: 96 FPS on one 4090, or 3 concurrent RT streams. Pro: 10.8 FPS on a 4090, RT on 2×5090. **Single-source.**
- Tight measured 5.8 GB and 0.19 s per warm chunk, but found it "softer in identity, weaker mouth" [1]. Low VRAM is **Confirmed**; quality is **Contested**.
- Licence: DiT Apache, but Lite bundles the **LTX-0.9 VAE under OpenRAIL-M**. Pro is fully Apache [29].

**SoulX-LiveAct.**
- arXiv 2603.11746; released 2026-03-16 [30][31][32]. 18B: Wan2.1-14B plus 4B audio.
- Neighbor Forcing plus ConvKV memory gives constant-memory, hour-scale generation, with action and emotion editing.
- 20 FPS on 2×H100/H200 at 720×416 or 512², FP8. 6 FPS on one RTX 5090. **Single-source.**
- HF weights are Apache-2.0, but the GitHub repo has no LICENSE file.
- A community "self-hosted HeyGen alternative" webapp built on it exists (0 stars).

**AvatarForcing (Kling AI Research).** arXiv 2603.14331; code Apache; HF weights untagged [38][39]. One-step student on Wan2.1-T2V-1.3B with local-future window denoising and dual anchors. 832×480 at 25 fps, 34 ms/frame. Different from TaekyungKi's "Avatar Forcing" (CVPR 2026, real-time interactive head).

**AptAvatar (Taobao Live).** arXiv 2607.24013. Code 2026-06-29; weights on HF with an Apache LICENSE file [33][34][35]. 14B from InfiniteTalk, 2 NFE at 720p, Self-Generated History Replay, "60×" speedup. Its README has the only cross-model table (internal, 720p, self-interested) [34].

**Kandinsky S2V 1.0.** arXiv 2610.19290; MIT; repo one week old [36][37]. Built on Kandinsky 5.0 Video (2B Lite, 21B Pro) with Qwen2.5-Omni conditioning and three-scale visual memory. Animates the whole figure, 25 fps SD/HD, in 5 s chunks; English and Russian. Has the best-documented speed table, on one H100: Lite-distill 8.7 s/s (3.8 on 4 GPUs), Pro-distill 41.5, Pro 189, Pro-HD 773; 46–57 GB. Its own human evaluation claims ≥ the strongest open baseline and 2 commercial systems. **Single-source.**

**TalkVerse-5B (Snap).** arXiv 2512.14938. Released 2025-12-31 with the dataset (2.3 M clips, 6.3 kh). Wan2.2-TI2V-5B, minute-long, "10× cheaper than Wan-S2V". **Snap Non-Commercial** [49][50].

**Older or adjacent models:**
- **FantasyTalking**: 2504.04842, Apache, Wan2.1-I2V-14B-720P, 15.5 s/it at 40 GB on an A100 [51][52].
- **Sonic**: CVPR 2025, **CC BY-NC-SA 4.0, non-commercial** [53][54].
- **LatentSync 1.6**: 2025-06-11, 512², 18 GB, weights OpenRAIL++, lip-sync only (V2V) [55].
- **Ditto**: Jan 2025, Apache, real-time head [56][57].
- **VividAnimator**: half-body; no code [80].
- **Wan2.2-Animate / Wan-Animate-2 (2026-08-07)**: Apache, but **video-driven**. Base and 10-step Distilled weights released; the "Lite" real-time variant is not; 8×A800 for 720p [9][69].
- **LTX-2.3**: community talking-head LoRAs; the DubIt checkpoint was gated in Tight's test [77][1].

**Closed systems (calibration only):**
- **OmniHuman-1.5** (2508.19209): MLLM semantic plan plus MMDiT; closed [59].
- **KlingAvatar 2.0** (2512.13313): spatio-temporal cascade with LLM directors; closed [61].
- **Seedance 2.0**: one informal creator test ranked it top for lip sync [62].
- **MoCha** (Meta, 2503.23307): no weights found [60].
- **Wan 2.5–3.0**: API-only.

**Streaming research without weights:**
- **StreamAvatar** (2512.22065, CVPR 2026): project page only [40].
- **Omni-LiveAvatar** (2608.13602): LTX-2 student generating audio and video jointly, 21.99 FPS on one H200, 60 s consistent; "code and checkpoints not released yet" [43][44].
- **OmniMate** (2607.23023): no code [45].
- **Wan-Streamer v0.1** (2606.25041, Wan team): a single full-duplex transformer replacing the ASR+LLM+TTS+avatar cascade, ~200 ms model latency. No official code; only an unofficial replication exists [46].
- **TurboTalk** (2604.14580, one-step, "120×") [41] and **DynaForcing** (2608.17707, ACM MM 2026) [42]: DynaForcing shows that DMD students collapse toward static motion (Dyn-Deg 0.31 → 0.73 with the fix). Neither has code.

## Which Ch06 gaps are now closed

- **Long-form consistency.** Closed in author claims: InfiniteTalk (~1 min clean in I2V), StableAvatar, LiveAvatar (more than 10,000 s, plus GenBench), SoulX-LiveAct (hour-scale), FlashTalk, LongCat, AptAvatar, TalkVerse and Kandinsky. Still open in evidence: the only independent benchmark used 3.6 s and explicitly did not test drift [1].
- **Full-body talking head.** Closed for half/upper body: OmniAvatar, Wan-S2V, HunyuanVideo-Avatar, EchoMimicV3, LongCat (gesture independently observed [1]), Kandinsky and HuMo. Semantic gesture (OmniHuman-1.5 style) is closed-source only.
- **Real-time, zero-shot, full-face, open-source.** Closed on datacenter GPUs: LiveAvatar (5×H800), FlashTalk (8×H800) and LiveAct (2×H100), all Apache, 384–720p. On consumer hardware only with a quality cost: FlashHead Lite (4090, 512² head) and AvatarForcing.
- **Cross-language.** Still open. Encoders are chinese-wav2vec2 or Whisper-L; Kandinsky trains with English and Russian captions; no multilingual lip-sync evaluation exists.
- **Emotion separate from prosody.** Partly addressed by HunyuanVideo-Avatar (emotion reference image) and LiveAct (emotion editing).

## Can Wan be used to build a HeyGen/Duix-like product?

**Yes for offline HeyGen-style video, and yes for real-time Duix-style streaming, with a hardware floor.** Licensing is not the blocker: every open Wan checkpoint and most Wan avatar models are Apache-2.0. The constraints are GPU cost and latency. Real-time at 14B needs 2 to 8 H100-class GPUs per stream, and the 1.3B real-time models give up quality. Alibaba's newer Wan versions (2.5 to 3.0) are API-only, and Wan-Streamer is unreleased.

**Which Wan releases are open-weight.** Primary evidence is the HF `Wan-AI` and GitHub `Wan-Video` org listings, captured 2026-11-04 [63][3].

| Release | Date | Open weights? | Licence | Avatar relevance |
|---|---|---|---|---|
| Wan2.1 (T2V 1.3B/14B, I2V, FLF2V, VACE) | 2025-02 to 05 | Yes | Apache-2.0 | Base of most avatar models |
| Wan2.2 (A14B MoE, TI2V-5B) | 2025-07-28 | Yes | Apache-2.0 | TalkVerse |
| Wan2.2-S2V-14B | 2025-08-26 | Yes | Apache-2.0 | Alibaba's own audio→video; base of LiveAvatar |
| Wan2.2-Animate-14B | 2025-09-19 | Yes | Apache-2.0 | Video-driven |
| Wan-Dancer-14B | 2026-07 | Yes | Apache-2.0 | Music→dance |
| Wan-Animate-2 (Base + Distilled) | 2026-08-07 | Yes (Lite not released) | Apache-2.0 | Video-driven |
| Wan 2.5 / 2.6 / 2.7 / 3.0 | 2025-09 to 2026-08 | **No, API only** | none | wan2.6-r2v: $0.086–0.10/s at 720p, $0.143–0.15/s at 1080p [67] |
| Wan-Streamer v0.1 | arXiv 2026-06 | **No** | — | Real-time interactive [46] |

API-only status is **Confirmed** by the primary listing [63] plus independent write-ups [64][65][66]. A youart.ai claim of open 2.5 weights is contradicted. Alibaba's docs list wan3.0-video, wan2.7-* and wan2.2-animate-move/mix as API models [68].

**Wan-based avatar models and licences:**

| Model | Licence | Commercial use |
|---|---|---|
| InfiniteTalk | Apache-2.0 | Yes |
| MultiTalk | Apache-2.0 | Yes |
| OmniAvatar | Apache-2.0 | Yes |
| StableAvatar | MIT | Yes |
| FantasyTalking | Apache-2.0 | Yes |
| EchoMimicV3 | Apache-2.0 | Yes |
| HuMo | Apache-2.0 | Yes |
| LiveAvatar | Apache-2.0 | Yes |
| FlashTalk | Apache-2.0 | Yes |
| AptAvatar | Apache-2.0 | Yes |
| FlashHead | Pro fully Apache; Lite's VAE OpenRAIL-M | Yes, with OpenRAIL use restrictions on Lite |
| SoulX-LiveAct | HF weights Apache; no code LICENSE | Check the code licence |
| AvatarForcing | Code Apache; weights untagged | Unclear |
| TalkVerse-5B | Snap Non-Commercial | **No** |

Similar but not Wan-based: LongCat (MIT), Kandinsky S2V (MIT), HunyuanVideo-Avatar (territory-limited).

**Speed per second of output.** Labels: (M) independently measured, (A) author-reported, (D) derived by me.

| Model | Setting | GPU | s/s |
|---|---|---|---|
| Wan2.2-S2V | default | 1×H200 | 204.6 (M), cold [1] |
| LiveAvatar | 4-step DMD, FP8 | 1×H200 | 48.8 (M), cold [1] |
| LiveAvatar | 4-step, TPP | 5×H800 | 0.56 (A): 45 FPS for 25 fps output [22] |
| FlashTalk | 4-step | 1×H200 | ≈90 (M) cold incl. compile; ≈3.75 s per warm chunk [1] |
| FlashTalk | 4-step | 8×H800 | 0.78 (A): 32 FPS [25] |
| LiveAct | FP8 | 2×H100 | ≈1.0 (A): 20 FPS [31] |
| LiveAct | FP8, offload | 1×5090 | ≈4 (A): 6 FPS [31] |
| FlashHead Lite | distilled 1.3B | 1×4090 | 0.26 (A): 96 FPS [27]; 0.19 s per warm chunk (M) [1] |
| FlashHead Pro | distilled 1.3B | 1×4090 | 2.3 (A) [28] |
| AvatarForcing | 1-step | unstated | 0.85 (A) [38] |
| EchoMimicV3-Flash | 8-step | 1×L40S | ≈69 (M), cold [1] |
| OmniAvatar 14B | 25 steps | 1×A800 | ≈400 s per chunk (D from 16 s/it) [11] |
| FantasyTalking | — | 1×A100 | 15.5 s per step at 512², 81 frames (A) [52] |
| InfiniteTalk / MultiTalk | 40 steps → 4 with lightx2v LoRA | — | **not found**; LightX2V claims ~20–24× for Wan 4-step in general [72] |
| Kandinsky S2V (not Wan) | Lite-distill / Pro-distill / Pro | 1×H100 | 8.7 / 41.5 / 189 (A) [37] |

There are two distillation routes. The first is lightx2v/FusionX LoRAs (40–50 → 4–8 steps, no CFG), officially supported by InfiniteTalk and MultiTalk [5][7]. The second is causal Self-Forcing/DMD students (LiveAvatar, FlashTalk, LiveAct, AvatarForcing, AptAvatar), which is what enables streaming. Its known failure mode is motion collapse toward static output [42].

**Real-time Wan streaming:**

| Model | Hardware | Throughput / latency | Resolution |
|---|---|---|---|
| LiveAvatar | 5×H800 | 45 FPS, TTFF 1.21 s | ~384×704 |
| FlashTalk | 8×H800 | 32 FPS, 0.87 s start-up | ~416×720 |
| LiveAct | 2×H100/H200 | 20 FPS | 720×416 |
| FlashHead Lite | 1×4090 | 96 FPS (or 3 streams) | 512² head |
| FlashHead Pro | 2×5090 | ≥25 FPS | 512² head |
| AvatarForcing | not stated | 34 ms/frame | 832×480 |

Not released: Wan-Animate-2-Lite and Wan-Streamer (~200 ms model / ~550 ms total latency). No real-time figure has been independently verified.

**Serving cost per output minute.** The measured figures are cold-start, from Tight [1]. The derived figures are mine, using Modal list prices: H200 $4.54/h, H100 $3.95/h, L40S $1.95/h [76].

| Model | ≈ $ per output minute |
|---|---|
| Wan-S2V | ~$21.5 (M, cold) |
| LongCat 1.5 | ~$6.6 (M, cold) |
| LiveAvatar, offline | ~$5.1 (M, cold) |
| EchoMimicV3-Flash | ~$3.5 (M, cold) |
| FlashHead Lite | ~$3.3 (M, cold, mostly compile) |
| LiveAvatar, real-time on 5×H100 | ~$0.33 (D) |
| FlashTalk, real-time on 8×H100 | ~$0.53 (D) |
| LiveAct, real-time on 2×H100 | ~$0.13 (D) |
| FlashHead Lite, 3 streams per GPU (L40S as proxy) | ~$0.01 (D) |
| Kandinsky Lite-distilled | ~$0.57 (D) |
| Kandinsky Pro-distilled | ~$2.7 (D) |
| InfiniteTalk, hosted | WaveSpeed $1.8–3.6 [74]; fal $12–24 [75] |
| Wan 2.6 r2v API (closed) | ~$5.2–6.0 at 720p [67] |

Tight's always-on estimate is $2,843 per month per H100 [2].

**Verdict.**
- **Offline:** feasible on Apache weights. InfiniteTalk with lightx2v, or LiveAvatar offline; LongCat 1.5 (MIT, not Wan) is the expressive alternative. The warm, distilled InfiniteTalk cost is unmeasured.
- **Real-time:** LiveAvatar, FlashTalk or LiveAct, each tying up 2 to 8 H100-class GPUs per stream (about $0.13–0.53 per minute, derived). On consumer hardware, only FlashHead Lite (head-only, softer quality).
- **Risk:** Alibaba stopped open-sourcing flagship Wan models after 2.2. Products stay on the 2.1/2.2 backbone, and Alibaba's own real-time model is paper/API-only.

## Open questions / could not verify

- No measured InfiniteTalk or MultiTalk s/s on a named GPU. An anecdotal Reddit claim that LongCat takes about 4× as long as InfiniteTalk was not saved.
- No independent drift test longer than 1 minute for any model; no independent real-time FPS verification.
- Contested: LongCat 1.5 lip sync, and EchoMimicV3-Flash VRAM.
- Licence gaps: LiveAct code licence; AvatarForcing weights licence; Kandinsky Lite card not checked; the HunyuanVideo-Avatar HF API has no licence tag (I used the GitHub LICENSE).
- The Wan "digital human" API model was not found in the saved docs.
- Closed systems (Kling, Seedance, OmniHuman-1.5) were only touched; Seedance evidence is one informal test.
- MoCha weights: not exhaustively checked.
- Wan2GP [73] and Helios [78] READMEs were saved but not analysed.
- Tight is a small studio: transparent method and pinned runners, but one portrait, 3.6 s of English and no blind study.

## References

Saved slugs are under `docs/research/sources/text/<slug>.txt`; GitHub snapshots are under `docs/research/agents/oss-avatar/gh/`.

[1] tight-benchmark-report (https://github.com/tight-studio/open-source-talking-avatar-benchmark/blob/main/REPORT.md; also tight-benchmark-readme) · [2] tight-studio-blog (https://tight.studio/blog/open-source-talking-avatar-models/) · [3] gh/*.json, gh/search-repos-2026-11-04.txt · [4] arxiv-2508.14033-infinitetalk · [5] gh-infinitetalk-readme · [6] arxiv-2505.22647-multitalk · [7] gh-multitalk-readme · [8] arxiv-2508.18621-wan-s2v · [9] gh-wan22-readme · [10] arxiv-2506.18866-omniavatar · [11] gh-omniavatar-readme · [12] arxiv-2508.08248-stableavatar · [13] gh-stableavatar-readme · [14] arxiv-2507.03905-echomimicv3 · [15] gh-echomimicv3-readme · [16] arxiv-2505.20156-hunyuanvideo-avatar · [17] gh-hunyuanvideo-avatar-readme · [18] gh-hunyuanvideo-avatar-license · [19] gh-longcat-video-readme · [20] arxiv-2605.26486-longcat-avatar-1.5 · [21] hf-longcat-video-avatar-1.5 (v1: hf-longcat-video-avatar) · [22] arxiv-2512.04677-liveavatar · [23] gh-liveavatar-readme · [24] hf-quark-live-avatar · [25] arxiv-2512.23379-soulx-flashtalk (hf-soulx-flashtalk-readme) · [26] gh-soulx-flashtalk-readme · [27] arxiv-2602.07449-soulx-flashhead · [28] gh-soulx-flashhead-readme · [29] hf-soulx-flashhead-card · [30] arxiv-2603.11746-soulx-liveact · [31] gh-soulx-liveact-readme · [32] hf-api-soulx-liveact · [33] arxiv-2607.24013-aptavatar · [34] gh-aptavatar-readme · [35] hf-api-aptavatar, hf-aptavatar-license · [36] arxiv-2610.19290-kandinsky-s2v (hf-api-kandinsky-s2v-pro) · [37] gh-kandinsky-s2v-readme · [38] arxiv-2603.14331-avatarforcing · [39] gh-klingai-avatarforcing-readme, hf-avatarforcing (other paper: gh-taekyungki-avatarforcing-readme) · [40] arxiv-2512.22065-streamavatar · [41] arxiv-2604.14580-turbotalk · [42] arxiv-2608.17707-dynaforcing · [43] arxiv-2608.13602-omni-liveavatar · [44] gh-omni-liveavatar-readme · [45] arxiv-2607.23023-omnimate · [46] arxiv-2606.25041-wan-streamer · [47] arxiv-2509.08519-humo · [48] gh-humo-readme · [49] arxiv-2512.14938-talkverse · [50] gh-talkverse-readme · [51] arxiv-2504.04842-fantasytalking · [52] gh-fantasytalking-readme · [53] gh-sonic-readme · [54] gh-sonic-license (arxiv-2411.16331-sonic) · [55] gh-latentsync-readme · [56] arxiv-2411.19509-ditto · [57] gh-ditto-readme · [58] arxiv-2411.10061-echomimicv2 · [59] arxiv-2508.19209-omnihuman-1.5 · [60] arxiv-2503.23307-mocha · [61] arxiv-2512.13313-klingavatar2 · [62] curiousrefuge-lipsync · [63] hf-api-wan-ai-models-list (+ gh/Wan-Video-org-repos.json, gh/hf-Wan-AI-models.json) · [64] atlascloud-wan3-open-source · [65] fuser-open-video-licences · [66] wan27org-wan25-open-source · [67] alibaba-wan26-r2v · [68] alibaba-video-generation · [69] gh-wan-animate-2-readme · [70] gh-wan-dancer-readme · [71] gh-lightx2v-readme · [72] lightx2v-step-distill-doc · [73] gh-wan2gp-readme · [74] wavespeed-infinitetalk-model (wavespeed-infinitetalk-docs) · [75] fal-infinitalk · [76] modal-pricing · [77] hf-api-search-avatar-likes, hf-api-search-talk-likes · [78] gh-helios-readme · [79] arxiv-2503.18860-hunyuanportrait · [80] arxiv-2510.10269-vividanimator · [81] hf-api-meigen-ai-infinitetalk, hf-api-meigen-ai-meigen-multitalk, hf-api-omniavatar-omniavatar-14b, hf-api-francisring-stableavatar, hf-api-acvlab-fantasytalking, hf-api-badtobest-echomimicv3, hf-api-tencent-hunyuanvideo-avatar, hf-api-soul-ailab-soulx-flashtalk-14b, hf-api-soul-ailab-soulx-flashhead-1_3b, hf-api-quark-vision-live-avatar, hf-api-bytedance-research-humo, hf-api-lycui-avatarforcing, hf-api-meituan-longcat-longcat-video-avatar-1.5, hf-api-bytedance-latentsync-1.6 · [82] arxiv-2502.01061-omnihuman-1 · [83] arxiv-2510.22200-longcat-video