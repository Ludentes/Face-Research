# Face Research — A 2026 Landscape Review

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A thesis-style review and curated index of the face representation, animation, and generation landscape as it stands in early 2026. Covers 2D rigged systems (Live2D), landmark/blendshape capture (MediaPipe, ARKit), 3D morphable models (FLAME), neural image deformation (LivePortrait and heirs), audio-driven talking heads, 3D Gaussian Splatting avatars, and diffusion-based parametric generation — and the bridges between them.

The field is fragmented across non-overlapping research communities. A researcher or product builder encountering it in 2026 has to assemble their worldview from the Live2D anime-rigging scene, the academic 3DMM lineage, the VFX/games pipeline anchored on ARKit, the diffusion-native image-editing community, and the fast-moving 3DGS avatar research front. Each community knows its own tooling deeply and the others shallowly or not at all. This project produces a single document that a researcher or engineer can read end-to-end to understand what exists, how the pieces relate, what is production-ready versus research-only, and — given a concrete use case — which stack to reach for and why.

## Contents

- [The Review](#the-review) — 13 chapters, read linearly or as standalone references
- [Curated Links](#curated-links) — papers, repos, and tools grouped by world
- [How to Cite](#how-to-cite)
- [Contributing](#contributing)
- [License](#license)

## The Review

| # | Chapter | One-line Summary |
|---|---|---|
| 00 | [Introduction](00-introduction.md) | The three worlds (2D rigged, 3D parametric, neural implicit) and the bridges between them |
| 01 | [Taxonomy](01-taxonomy.md) | A three-axis classification (dimensionality × explicitness × origin) for ~20 face representations |
| 02 | [The Live2D World](02-live2d-world.md) | 2D rigged animation in production — moc3 format, CartoonAlive, Textoon, Inochi2D |
| 03 | [MediaPipe & ARKit](03-mediapipe-arkit-world.md) | Landmark and blendshape capture as the lingua franca of production face pipelines |
| 04 | [The FLAME World](04-flame-3dmm-world.md) | 3D morphable models, DECA/EMOCA/SMIRK extractors, FLAME in diffusion |
| 05 | [Neural Image Deformation](05-neural-deformation.md) | LivePortrait and the implicit-keypoint lineage, plus 2026 successors (IM-Animation, FG-Portrait, PersonaLive, Durian) |
| 06 | [Talking Heads](06-talking-heads.md) | Audio-driven face synthesis 2024–2026 (EMO, Hallo, MuseTalk, FLOAT, NVIDIA Audio2Face, FantasyTalking2, UniTalking, DyStream) |
| 07 | [3DGS Avatars](07-3dgs-avatars.md) | The real-time photorealism track — GaussianAvatars, SplattingAvatar, 3D Gaussian Blendshapes, Arc2Avatar |
| 08 | [Diffusion-Based Parametric Generation](08-diffusion-parametric.md) | Arc2Face, RigFace, MorphFace, Concept Sliders, h-space direction finding |
| 09 | [Bridges and Conversions](09-bridges-and-conversions.md) | Explicit conversions between representations — cost, quality, and common pipelines |
| 10 | [Decision Trees by Use Case](10-decision-trees.md) | Given a concrete application, which stack to pick |
| 11 | [Market, Community, and Tooling Reality](11-market-and-community.md) | VTubing economics, enterprise digital humans, tool popularity rankings |
| 12 | [Conclusions and 12–24 Month Horizon](12-conclusions.md) | Open problems and where the field is going |

## Curated Links

A curated index of the most important artifacts referenced in the review, grouped by world. Each entry is linked to the chapter that discusses it in depth.

### Live2D World

- [Live2D Cubism](https://www.live2d.com/) — commercial rigging and runtime, dominant in VTubing. See [Ch02](02-live2d-world.md).
- [Inochi2D](https://inochi2d.com/) — open-source alternative, minority adoption. See [Ch02](02-live2d-world.md).
- [VTube Studio](https://denchisoft.com/) — dominant production runtime for Live2D VTubers. See [Ch02](02-live2d-world.md), [Ch11](11-market-and-community.md).
- [CartoonAlive](https://arxiv.org/abs/2505.12847) — automated portrait-to-Live2D rigging from a single image. See [Ch02](02-live2d-world.md).
- [Textoon](https://arxiv.org/abs/2504.00627) — text-conditioned Live2D character generation. See [Ch02](02-live2d-world.md).

### MediaPipe & ARKit

- [ARKit Face Tracking](https://developer.apple.com/documentation/arkit/arfaceanchor/blendshapelocation) — 52 blendshapes, production lingua franca. See [Ch03](03-mediapipe-arkit-world.md).
- [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker) — 468 landmarks + ARKit-compatible blendshape head. See [Ch03](03-mediapipe-arkit-world.md).
- [OpenSeeFace](https://github.com/emilianavt/OpenSeeFace) — open-source webcam face tracker used in VTube Studio. See [Ch03](03-mediapipe-arkit-world.md).
- [Live Link Face](https://apps.apple.com/us/app/live-link-face/id1495370836) — Epic's iPhone ARKit bridge for Unreal Engine. See [Ch03](03-mediapipe-arkit-world.md).
- [NVIDIA Audio2Face](https://developer.nvidia.com/blog/nvidia-open-sources-audio2face-animation-model/) — audio-to-ARKit-blendshape, open-sourced September 2025. See [Ch03](03-mediapipe-arkit-world.md), [Ch06](06-talking-heads.md).

### FLAME & 3D Morphable Models

- [FLAME](https://flame.is.tue.mpg.de/) — MPI-IS statistical head model, 5023 vertices, 300-d shape + 100-d expression PCA. See [Ch04](04-flame-3dmm-world.md).
- [DECA](https://github.com/yfeng95/DECA) — single-image FLAME parameter regression with detail displacement. See [Ch04](04-flame-3dmm-world.md).
- [EMOCA](https://github.com/radekd91/emoca) — emotion-aware FLAME fitting. See [Ch04](04-flame-3dmm-world.md).
- [SMIRK](https://github.com/georgeretsi/smirk) — self-supervised FLAME extractor with production-grade quality. See [Ch04](04-flame-3dmm-world.md).

### Neural Image Deformation

- [LivePortrait](https://github.com/KwaiVGI/LivePortrait) — Kuaishou's implicit-keypoint portrait animator, the reference point for 2024–2025 neural warp. See [Ch05](05-neural-deformation.md).
- [FasterLivePortrait](https://github.com/warmshao/FasterLivePortrait) — community-optimized LivePortrait with TensorRT acceleration. See [Ch05](05-neural-deformation.md).
- [First Order Motion Model](https://github.com/AliaksandrSiarohin/first-order-model) — the lineage ancestor (NeurIPS 2019). See [Ch05](05-neural-deformation.md).
- [Thin-Plate Spline Motion Model](https://github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model) — TPSMM (CVPR 2022), still used in some anime-rig pipelines. See [Ch05](05-neural-deformation.md).
- [X-Portrait](https://github.com/bytedance/X-Portrait) — ByteDance's diffusion-native portrait animator (SIGGRAPH 2024). See [Ch05](05-neural-deformation.md).
- [Follow-Your-Emoji](https://follow-your-emoji.github.io/) — expression-driven portrait animation (SIGGRAPH Asia 2024). See [Ch05](05-neural-deformation.md).
- [MegActor](https://arxiv.org/abs/2405.20851) — audio- and video-driven portrait diffusion. See [Ch05](05-neural-deformation.md).
- [IM-Animation](https://arxiv.org/abs/2602.07498) — 2026 successor to LivePortrait in the implicit-motion lineage. See [Ch05](05-neural-deformation.md).
- [FG-Portrait](https://arxiv.org/abs/2603.23381) — CVPR 2026, 3D flow guided portrait animation. See [Ch05](05-neural-deformation.md).
- [Durian](https://arxiv.org/abs/2509.04434) — diffusion-bridge portrait animation with LivePortrait baseline. See [Ch05](05-neural-deformation.md).

### Talking Heads

- [SadTalker](https://github.com/OpenTalker/SadTalker) — the dominant real-time accessible audio-driven head. See [Ch06](06-talking-heads.md).
- [MuseTalk](https://github.com/TMElyralab/MuseTalk) — latent-space inpainting in SD 1.5 VAE, dominant for region-only dubbing. See [Ch06](06-talking-heads.md).
- [Hallo](https://github.com/fudan-generative-vision/hallo) / [Hallo2](https://github.com/fudan-generative-vision/hallo2) — hierarchical audio-driven portrait diffusion. See [Ch06](06-talking-heads.md).
- [Hallo4](https://arxiv.org/abs/2505.23525) — DPO-based DiT portrait diffusion. See [Ch06](06-talking-heads.md).
- [EMO](https://humanaigc.github.io/emote-portrait-alive/) — Alibaba's expressive portrait audio-to-video (ECCV 2024, weights not released). See [Ch06](06-talking-heads.md).
- [FLOAT](https://deepbrainai-research.github.io/float/) — flow-matching audio-driven generation. See [Ch06](06-talking-heads.md).
- [FantasyTalking2](https://arxiv.org/abs/2508.11255) — AAAI 2026, first RLHF for talking heads (TLPO + Talking-Critic + 410K preference dataset). See [Ch06](06-talking-heads.md).
- [PersonaLive](https://arxiv.org/abs/2512.11253) — CVPR 2026, streamable diffusion for live streaming portrait animation. See [Ch06](06-talking-heads.md).
- [UniTalking](https://arxiv.org/abs/2603.01418) — joint audio+video diffusion with Multi-Modal Transformer Blocks. See [Ch06](06-talking-heads.md).
- [DyStream](https://arxiv.org/abs/2512.24408) — streaming dyadic flow matching, 34 ms/frame, <100 ms latency. See [Ch06](06-talking-heads.md).
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) — legacy lip-sync dubbing, still deployed. See [Ch06](06-talking-heads.md).

### 3DGS Avatars

- [3D Gaussian Splatting (SIGGRAPH 2023)](https://arxiv.org/abs/2308.04079) — Kerbl et al., the foundational paper. See [Ch07](07-3dgs-avatars.md).
- [GaussianAvatars](https://github.com/ShenhanQian/GaussianAvatars) — CVPR 2024 Highlight, FLAME-rigged 3DGS, the template. See [Ch07](07-3dgs-avatars.md).
- [SplattingAvatar](https://github.com/initialneil/SplattingAvatar) — CVPR 2024, mesh-embedded Gaussians, 300+ FPS desktop / 30 FPS iPhone 13. See [Ch07](07-3dgs-avatars.md).
- [3D Gaussian Blendshapes](https://gapszju.github.io/GaussianBlendshape/) — SIGGRAPH 2024, explicit blendshape offsets, 370 FPS. See [Ch07](07-3dgs-avatars.md).
- [FlashAvatar](https://ustc3dv.github.io/FlashAvatar/) — CVPR 2024, fast monocular reconstruction + 300 FPS rendering. See [Ch07](07-3dgs-avatars.md).
- [Gaussian Head Avatar](https://github.com/YuelangX/Gaussian-Head-Avatar) — CVPR 2024, ultra-high-fidelity dynamic Gaussians. See [Ch07](07-3dgs-avatars.md).
- [PSAvatar](https://arxiv.org/abs/2401.12900) — near-contemporary FLAME + 3DGS method. See [Ch07](07-3dgs-avatars.md).
- [HeadStudio](https://github.com/ZhenglinZhou/HeadStudio) — ECCV 2024, text-to-3DGS with F-SDS. See [Ch07](07-3dgs-avatars.md).
- [AniGS](https://arxiv.org/abs/2412.02684) — CVPR 2025, single-image animatable Gaussian avatar. See [Ch07](07-3dgs-avatars.md).
- [Arc2Avatar](https://github.com/dimgerogiannis/Arc2Avatar) — CVPR 2025, single-image FLAME-rigged 3DGS via Arc2Face synthetic views. See [Ch07](07-3dgs-avatars.md).

### Diffusion-Based Parametric Generation

- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion) — the canonical open-source diffusion backbone. See [Ch08](08-diffusion-parametric.md).
- [Flux](https://github.com/black-forest-labs/flux) — the 2024–2025 quality leader for open-weights text-to-image. See [Ch08](08-diffusion-parametric.md).
- [ControlNet](https://github.com/lllyasviel/ControlNet) — Zhang et al., ICCV 2023, structured image conditioning. See [Ch08](08-diffusion-parametric.md).
- [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter) — Ye et al., image-prompt adapter for identity/style conditioning. See [Ch08](08-diffusion-parametric.md).
- [Concept Sliders](https://github.com/rohitgandikota/sliders) — Gandikota et al., ECCV 2024, LoRA-based semantic direction control. See [Ch08](08-diffusion-parametric.md).
- [Asyrp](https://github.com/kwonminki/Asyrp_official) — Kwon et al., ICLR 2023, h-space direction finding in diffusion. See [Ch08](08-diffusion-parametric.md).
- [Arc2Face](https://github.com/foivospar/Arc2Face) — Papantoniou et al., ECCV 2024 Oral, ArcFace-conditioned face diffusion. See [Ch08](08-diffusion-parametric.md).
- [Arc2Face + Expression Adapter](https://arxiv.org/abs/2510.04706) — ICCVW 2025, FLAME blendshape cross-attention on top of Arc2Face. See [Ch08](08-diffusion-parametric.md).
- [RigFace](https://github.com/weimengting/RigFace) — Wei et al., arXiv:2502.02465, full SD 1.5 fine-tune with dedicated identity UNet. See [Ch08](08-diffusion-parametric.md).
- [MorphFace](https://arxiv.org/abs/2504.00430) — CVPR 2025, 3DMM-guided diffusion with temporal context blending. See [Ch08](08-diffusion-parametric.md).
- [InstantID](https://github.com/InstantID/InstantID) — identity-preserving generation in seconds. See [Ch08](08-diffusion-parametric.md).
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) — node-based diffusion workflow runtime, dominant for power users. See [Ch11](11-market-and-community.md).

### Proprietary / Enterprise

- [Apple ARKit](https://developer.apple.com/augmented-reality/arkit/) — the reference implementation of 52-blendshape face tracking. See [Ch03](03-mediapipe-arkit-world.md).
- [Meta Codec Avatars](https://research.facebook.com/publications/authentic-volumetric-avatars-from-a-phone-scan/) — photorealistic research avatars, proprietary capture rig. See [Ch07](07-3dgs-avatars.md).
- [NVIDIA Omniverse + ACE](https://www.nvidia.com/en-us/ai/digital-humans/) — enterprise digital-human stack. See [Ch11](11-market-and-community.md).

## How to Cite

If you reference this review in academic work:

```bibtex
@misc{face-research-2026,
  title        = {Face Research: A 2026 Landscape Review},
  author       = {Ludentes},
  year         = {2026},
  howpublished = {\url{https://github.com/Ludentes/Face-Research}},
  note         = {Thesis-style review of face representation, animation, and generation}
}
```

## Contributing

This is a living document. If you spot a factual error, an outdated claim, or a paper that should be in scope, open an issue or a PR. Specific things that would help:

- **Corrections** with a source link — especially for venue/year/FPS claims, where factual drift is common.
- **New 2026 papers** in any of the seven worlds — the review's 2026 coverage is strongest in Chapters 05 and 06 and thinnest in Chapter 08 (diffusion parametric).
- **Production war stories** — "we tried X for use case Y and it failed because Z" is exactly the kind of context a paper-only review cannot capture.

Please keep PRs focused on one chapter at a time. Cite sources inline, and use absolute dates (`2026-04-13`) rather than relative ones (`last month`).

## License

The text of this review is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You may share and adapt the material with attribution. See [LICENSE](LICENSE) for the full text.

Papers, code repositories, and tools linked from this review remain under their own respective licenses.
