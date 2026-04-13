# Chapter 06 — Talking Heads: Audio-Driven Face Synthesis 2024-2026

## A Parallel Lineage with Its Own Logic

The face animation methods discussed so far have all taken visual driving signals — a video, a tracked webcam, a set of blendshape coefficients, a FLAME parameter vector. This chapter covers a different tradition: methods that take *audio* as the primary driving signal and synthesize face animation that matches the audio's speech content and emotional prosody. These are the *talking head* methods, and they serve a specific and commercially important set of applications: dubbing, text-to-speech avatars, virtual newsreaders, language learning videos, and the growing class of AI assistants and digital humans that need to produce speech with a face attached.

The talking-head tradition has its own history, its own canonical benchmarks, and its own failure modes, and it overlaps with but is not identical to the face animation methods in the preceding chapters. Understanding the overlap requires a quick architectural observation. A talking-head method can be factored into two stages: an *audio-to-motion* stage that converts speech into some intermediate face motion representation, and a *motion-to-image* stage that renders the motion into video frames. The motion-to-image stage is essentially the same problem we have been discussing — neural deformation, 3DMM-based rendering, 3DGS avatars, or diffusion — and a talking-head system typically uses one of these methods as its image synthesizer. The audio-to-motion stage is the distinctive contribution: it is the part that maps a speech waveform or a phoneme stream or a text prompt into the motion parameters that the image synthesizer consumes.

Different talking-head systems make different choices at both stages. Some use FLAME-based rendering with an audio-to-FLAME mapping. Some use implicit-keypoint warp rendering (LivePortrait-style) with an audio-to-keypoint mapping. Some use diffusion-based rendering with an audio-to-latent mapping. Some use 3DGS avatars with an audio-to-blendshape mapping. The taxonomy that the preceding chapters established is still operative — the motion representations are still the same five or six options — and the audio-to-motion mapping is a separate trained module that is specific to each method. This chapter walks through the state of the art as of early 2026, evaluates the systems by their speed and quality tradeoffs, and places them within the larger landscape.

## The Task Definition

A talking-head method takes two things as input: a reference image of a face (the identity to animate) and an audio track of speech (the content to sync to). It produces a video of the reference face speaking the audio. The quality criteria are:

**Lip sync accuracy.** The mouth shapes in the output must match the phonemes in the audio at the correct times. This is the most important single criterion — a face whose mouth moves incorrectly is immediately obvious and unacceptable for production use. Lip sync is typically measured via Sync-D (Wav2Lip's sync score, which compares audio features to mouth region features via a pretrained discriminator) or via LSE-D and LSE-C (Lip-Sync Error, distance and confidence).

**Identity preservation.** The face in the output must remain recognizable as the same person as the reference image. This is measured via identity cosine similarity in an ArcFace embedding space or by human identity ranking tests.

**Naturalness and motion fidelity.** The face should produce not just correct mouth movements but also the accompanying natural motion: subtle head bobbing, eye movements, eyebrow engagement, and other secondary signals that real speakers produce. A face that has perfect lip sync but a frozen head looks robotic in a way that users find uncomfortable.

**Temporal consistency.** The output must be stable over time without flicker, jitter, or identity drift. A single frame that looks good is not the task; a multi-minute video that looks consistently good is the task, and this is where many methods fail.

**Speed.** For many applications, offline synthesis is fine — a dubbing pipeline can take as long as it needs to. For live applications (AI assistants, virtual agents) the speed constraint tightens to real-time or near-real-time, and the set of viable methods shrinks dramatically.

**Emotional expressivity.** Higher-quality methods aim to capture not just the phoneme content of the audio but also its emotional prosody — happy speech should produce a happy face, angry speech should produce an angry face. This is measured by emotion classifier agreement or by human emotion ranking.

Quality on all six criteria has improved substantially between 2020 (when Wav2Lip and MakeItTalk were the dominant methods) and 2026 (when FLOAT, MuseTalk, and audio-driven 3DGS methods are the frontier). The most important single advance has been the move from deterministic regression-based methods to stochastic generative methods — first GAN-based, then diffusion-based, then flow-matching-based — which has allowed talking-head systems to produce expressive, natural output rather than the frozen regression-mean faces that earlier methods produced.

## The 2020-2023 Era: Regression-Based Methods

The dominant talking-head methods through roughly 2023 were regression-based: a neural network mapped audio features directly to face parameters (landmarks, blendshapes, or image pixels) with a standard supervised loss. The regression approach worked for lip sync because the mapping from phonemes to mouth shapes is relatively deterministic — the /aa/ sound always requires an open mouth, the /m/ sound always requires closed lips — but it failed on the expressive and natural-motion criteria because a regression model trained with MSE or similar loss collapses to the mean of the training distribution. The mean face for any given audio clip has a frozen head, minimal eyebrow motion, and no emotional expressivity, because any specific motion would increase MSE relative to the average over many training examples.

**Wav2Lip** (Prajwal et al., 2020) [1] was the canonical regression-based method and is still widely deployed. It uses a GAN-based architecture with a sync discriminator that penalizes outputs whose audio and mouth region are out of sync. Wav2Lip produces accurate lip sync on a reference video of the person speaking, but its outputs have characteristic frozen heads, flat affect, and visible artifacts around the mouth region where the method has inpainted new mouth shapes. Wav2Lip's quality is "good enough" for many dubbing applications and has been used commercially for years, but it represents the ceiling of the regression paradigm.

**MakeItTalk** (Zhou et al., 2020) [2] improved on Wav2Lip by factoring the output into content (phonemes) and style (speaker-specific motion patterns), with separate streams for each. This addressed some of the "frozen head" problem by learning speaker-specific head motion patterns that could be applied on top of the lip sync. Still regression-based, still subject to mean-collapse in the stochastic components of motion.

**SadTalker** (Zhang et al., CVPR 2023) [3] is a transitional method that moves toward generative modeling for head motion while keeping regression for lip sync. It uses an audio-to-3DMM-coefficient mapping followed by a neural renderer that produces the final video. SadTalker has the notable property of being real-time on consumer GPUs, runs out-of-the-box on a wide range of hardware, and produced outputs that are noticeably more natural than Wav2Lip's despite using a simpler architecture. It is the pragmatic choice for real-time talking-head applications that can accept moderate quality and is still widely deployed as of 2026.

## The Diffusion Era: Expressive Talking Heads

Starting around 2023, talking-head methods moved toward generative modeling — first with GANs (EAMM, PC-AVS), then with diffusion models. The diffusion approach addressed the mean-collapse problem by sampling from a distribution of plausible motions rather than regressing to the mean, producing outputs that were both accurate in lip sync and natural in head motion and expression.

**DiffTalk** (CVPR 2023) [4] was one of the first diffusion-based talking-head methods. It frames the task as audio-conditioned latent diffusion (built on the Stable Diffusion lineage), conditioning on a reference portrait image plus facial landmarks as the driving signal, rather than going through an explicit 3DMM or FLAME intermediate. The quality gains over regression methods were substantial — human evaluators consistently rated DiffTalk outputs as more natural and more expressive — but the inference speed was poor (diffusion sampling at ten or more denoising steps is expensive) and real-time use was not feasible.

**EMO** (Emote Portrait Alive) (Tian, Wang, Zhang, Bo — Alibaba Institute for Intelligent Computing, ECCV 2024) [5] produced some of the most impressive talking-head demo videos of the era. It uses a video-diffusion backbone that generates full video frames directly from audio and a reference image, without an explicit intermediate motion representation. The output quality is the state of the art as of 2024-2025: natural head motion, emotional expressivity driven by audio prosody, and strong identity preservation. The cost is speed — EMO is firmly offline, with generation taking multiple seconds per second of output on high-end hardware. **EMO's code and weights have not been released** — the `HumanAIGC/EMO` repository contains only paper links and BibTeX, not an implementation. The full pipeline is owned by Alibaba and is not currently reproducible from public sources.

**Hallo** (2024) [6] is a diffusion-based method with public code that aims to reproduce EMO-level quality in an open framework. It uses a ReferenceNet-style architecture (a second UNet that processes the reference image and injects features into the main denoiser) to preserve identity, and conditions on audio features at multiple timesteps. Hallo's quality is good but still below EMO's on expressivity benchmarks, and it is similarly offline-only.

**EchoMimic** (2024) [7] extends the diffusion paradigm by taking either audio or face landmarks as driving input. This dual-conditioning lets the system work in a hybrid mode where the audio drives the mouth and the landmarks drive the head pose, which produces results that some evaluators prefer to pure-audio driving.

**V-Express** and **Loopy** (2024) are additional diffusion-based methods with incremental improvements on the core pipeline. They represent the active research frontier and are worth knowing but not individually transformative.

The pattern across the diffusion-based methods is: excellent quality, slow inference, offline use only. For the class of applications that can afford 5-30 seconds per second of output — dubbing, content creation, video production, pre-recorded virtual avatar presentations — these methods are the state of the art. For real-time applications they remain infeasible.

## The Flow-Matching Era: Speed With Quality

The most recent shift in talking-head methods is the move from diffusion toward flow matching — a closely related generative modeling paradigm that supports faster sampling without sacrificing quality. Flow matching methods sample in 1 to 4 denoising steps rather than 10 to 50, which brings the method into or near real-time speed.

**FLOAT** (Ki et al., ICCV 2025) [8] is the most important 2025 talking-head paper and represents the current frontier for real-time audio-driven face animation. FLOAT uses flow matching in motion latent space rather than pixel space, which is substantially more efficient — the model generates a sequence of motion latent vectors, and a separate decoder produces frames from those latents. This decoupling means that the expensive flow-matching step operates on a low-dimensional motion representation (compact) rather than on high-dimensional pixel sequences (expensive), and the decoder can be a lightweight network trained separately.

FLOAT's specific contributions:

- **Motion latent flow matching** — the generative stage operates in a learned motion latent space derived from video data. This is the key efficiency gain.
- **Audio-conditional motion generation** — audio features drive the flow matching process, producing motion latents that match the speech prosody and phoneme content.
- **Competitive quality with substantially faster inference** than diffusion methods. FLOAT runs faster than the diffusion-based SOTA of 2024 while achieving comparable quality metrics.
- **Public code and weights** at `github.com/deepbrainai-research/float`.

FLOAT is the paper I would point to as "what the field looks like now" for talking-head methods. It represents the successful move from pure diffusion to flow matching, which will probably continue across the field through 2026 and 2027.

**READ** (Real-time and Efficient Asynchronous Diffusion for Audio-driven Talking Head, 2025) [9] is another recent method aimed at real-time speed. It runs at approximately 25 FPS at 512² resolution on a consumer GPU, which is real-time. The quality is slightly below FLOAT's but the speed-quality tradeoff is in a useful zone for applications that need true real-time operation.

**MuseTalk** (TMElyralab, 2024) [10] is a different approach: it targets real-time lip sync specifically, not full face animation. It generates only the mouth region as an overlay on a reference video frame, using *latent space inpainting* in the Stable Diffusion 1.5 VAE latent space — a latent-diffusion-style pipeline, rather than a full pixel-space diffusion. On a V100 GPU with face regions cropped to 256×256, MuseTalk achieves 30+ FPS, making it real-time on consumer hardware. The quality is limited to the mouth region — head motion, eyebrow motion, and emotion are taken from the reference video, not generated — but for applications that only need lip sync (dubbing a recorded video with new audio) MuseTalk is one of the fastest production-quality options.

**OmniTalker** (2024) [11] adds text input as an alternative driving signal: instead of a pre-recorded audio track, you provide text, a TTS synthesizer, and a reference image, and the system produces the talking-head video at 25 FPS. This is close to an end-to-end "text-to-talking-face-video" pipeline with public code, which matters because most downstream applications are starting from text rather than from audio.

## 3DGS-Based Talking Heads

A parallel line of work uses 3D Gaussian Splatting avatars as the image synthesizer, with audio as the driving signal. This approach leverages the real-time rendering speed of 3DGS (100-370 FPS) to produce talking heads at far higher frame rates than diffusion-based methods can achieve.

**TalkingGaussian** and **GaussianTalker** (2024) [12] use 3DGS avatars with deformation primitives and train audio-to-deformation mappings. GaussianTalker (cvlab-kaist) achieves approximately 120 FPS, produces real-time-grade visual quality, and can be driven by live microphone input. The cost is the same as for any per-person 3DGS avatar: you need multi-view video of the target person to build the avatar in the first place, which blocks the zero-shot-identity use case.

**GeneFace** is related in goal but architecturally distinct — it is a NeRF-based talking-head method rather than a 3DGS one, and it predates most of the 3DGS-based work. It is included here for context but belongs to the NeRF lineage that 3DGS has largely displaced for real-time rendering.

The 3DGS-based talking heads are the right choice when you have a specific target identity you can capture from video, and you need live talking-head synthesis at broadcast quality. Example applications: a virtual newsreader built from a professionally recorded reference session, a virtual assistant with a fixed avatar that ships with a pre-recorded identity pack, or a VTuber-adjacent real-time speech-driven character. They are not the right choice for zero-shot applications where the target face is a photograph you have never seen before.

## NVIDIA Audio2Face and the Proprietary Ecosystem

**NVIDIA Audio2Face** (originally part of NVIDIA Omniverse, open-sourced on September 24, 2025) [14] is a production-grade audio-to-blendshape pipeline that has been deployed commercially for several years inside Omniverse. It takes audio input and produces a stream of ARKit-compatible blendshape values that can drive a MetaHuman, a Unity character, or any rig that accepts ARKit. NVIDIA's September 2025 open-source release included the SDK, Maya and Unreal Engine 5 plugins, the training framework (v1.0), a regression model (v2.2) and a diffusion model (v3.0), and the companion Audio2Emotion model. NVIDIA's NIM service wraps Audio2Face to output ARKit blendshapes directly.

Audio2Face is architecturally conservative: it predicts explicit blendshape coefficients rather than generating images or videos directly, and the downstream rendering is someone else's problem. This makes it a *building block* rather than a *complete system* — you still need a rig and a renderer — but it also makes it the right tool for integrating audio-driven face animation into an existing production pipeline that already has a rig and a renderer.

For a pipeline that already targets ARKit blendshapes (any Live2D VTuber rig, any MetaHuman character, any VRM avatar), NVIDIA Audio2Face is the simplest path to audio-driven animation: feed the audio in, receive the blendshape stream, drive the existing rig. No additional tooling required. This is why Audio2Face has become the de facto standard audio-to-face component for many production pipelines as of 2026.

## Comparison Table

A summary of the most relevant methods as of early 2026:

| Method | Year | Input | Rendering | Speed | Quality | Code | Use case |
|---|---|---|---|---|---|---|---|
| Wav2Lip | 2020 | audio + video | GAN | real-time | moderate lip sync, frozen head | public | legacy dubbing |
| SadTalker | 2023 | audio + image | neural renderer (3DMM) | real-time | natural, limited expression | public | accessible pipeline |
| DiffTalk | CVPR 2023 | audio + image + landmarks | latent diffusion | offline | good expressivity | public | research |
| EMO | ECCV 2024 | audio + image | video diffusion | offline (seconds/frame) | SOTA natural | not released | — |
| Hallo | 2024 | audio + image | diffusion | offline | approaching EMO | public | open EMO alternative |
| EchoMimic | 2024 | audio + landmarks + image | diffusion | offline | high control | public | hybrid driving |
| FLOAT | 2025 | audio + image | flow matching in motion latent | faster than diffusion | near-SOTA | public | current frontier |
| READ | 2025 | audio + image | async diffusion | real-time (~25 FPS) | good | paper | real-time |
| MuseTalk | 2024 | audio + video | latent-space inpainting (SD 1.5 VAE) | real-time (30+ FPS at 256²) | mouth-only | public | lip sync only |
| OmniTalker | 2024 | text + image | pipeline with TTS | near-real-time (25 FPS) | good | public | text-driven |
| TalkingGaussian | 2024 | audio | 3DGS avatar | 100+ FPS | high, per-identity | partial | captured-identity |
| NVIDIA Audio2Face | 2019+, OSS Sept 2025 | audio | ARKit blendshape output only | real-time | production-grade parameters | open | rig integration |

The table makes several patterns visible. Quality has gone up steadily from 2020 through 2025, with the biggest single jump at the move to diffusion-based generation. Speed has gotten better with flow matching and with VAE-based region methods, though the pure diffusion branch remains offline. The proliferation of methods is real but not chaotic — most methods can be classified cleanly into "offline diffusion," "real-time flow matching," "real-time region-only," "real-time 3DGS-based," and "production blendshape component."

## 2026 Developments

Through the first quarter of 2026, the talking-head field saw a clear set of extensions to the 2024-2025 state of the art. Five papers are worth flagging specifically because they address limitations that the earlier methods left open.

**Hallo4** (arXiv:2505.23525, May 2025) [15] extended the Hallo/Hallo3 DiT-based lineage with direct preference optimization (DPO) and temporal motion condition modulation. Hallo4 is technically late 2025 rather than 2026, but it is the bridge between the pure-diffusion Hallo3 generation and the 2026 preference-aligned methods below; without Hallo4, the 2026 work that builds on preference-based alignment would have less context.

**FantasyTalking2** (arXiv:2508.11255, AAAI 2026) [16] is the most architecturally important 2026 talking-head paper and represents the first serious RLHF pipeline applied to talking heads. Its contribution has three parts: (1) **Talking-Critic**, a multimodal reward model trained to score talking-head outputs on alignment with human preferences; (2) **Talking-NSQ**, a 410,000-pair human preference dataset covering lip-sync, motion naturalness, and visual quality dimensions; and (3) **TLPO** (Timestep-Layer adaptive Preference Optimization), a framework that decouples the competing preference dimensions into per-dimension expert modules with a timestep-and-layer-adaptive fusion schedule. The significance is that TLPO solves the "mean-collapse on expressivity" problem not through architectural change but through post-training alignment — the generation model still produces motion, but the model is fine-tuned against explicit rewards for naturalness, sync, and fidelity simultaneously, so it can escape the MSE-collapsed mean that earlier methods defaulted to. Code is public at `github.com/Fantasy-AMAP/fantasy-talking2` under the Fantasy-AMAP (Alibaba AMAP / Fantasy) umbrella, and the paper is in the AAAI 2026 proceedings.

**UniTalking** (arXiv:2603.01418, March 2026) [17] takes a different direction: instead of animating a reference face with given audio, UniTalking is an end-to-end diffusion transformer that **jointly generates speech and video** from text input. The key architectural commitment is Multi-Modal Transformer Blocks that share self-attention across audio and video latent tokens, and the training alternates among multiple tasks (Text-to-Audio-Video, Text-Video-to-Audio, Text-Image-to-Audio-Video, Text-Reference-to-Audio-Video) to improve joint consistency. Reported metrics include Sync-C = 4.87 and Sync-D = 8.05, improving on the Universe-1 baseline and approaching Sora2-class joint A/V generators in the paper's evaluations. UniTalking extends OmniTalker's text-driven TTS-then-video cascade into a truly joint audio-video generation pipeline. The arXiv preprint is verified; a CVPR 2026 acceptance claim circulates in secondary sources but is not confirmed in the available evidence, so the venue should be treated as arXiv-only until further confirmation.

**DyStream** (arXiv:2512.24408, v1 December 2025, v2 February 2026) [18] addresses the streaming-latency frontier. It is a streaming dyadic talking-head generator — notable because it models two-person (speaker + listener) conversations explicitly, not just the solo-speaker setup that the 2024-2025 methods assumed. The architecture combines an autoencoder that decomposes a reference image into static appearance and identity-agnostic motion features with an audio-to-motion generator and an autoregressive causal self-attention plus flow-matching head. The reported figures are approximately 34 ms per frame, under 100 ms end-to-end latency, and SOTA lip-sync quality on HDTF (Sync-C 8.13 offline, 7.61 online). DyStream is the first method to credibly deliver streaming-compatible dyadic flow-matching talking heads at broadcast-quality lip sync, and it is the direct follow-up to FLOAT on the autoregressive/streaming axis. No venue confirmation beyond the arXiv preprint is available.

**Emotion-editing extensions.** Two 2026 papers push specifically on emotional control, which the 2024-2025 methods handle only as a side-effect of audio prosody. **EditEmoTalk** (arXiv:2601.10000, January 2026) [19] provides speech-driven 3D facial animation with continuous expression editing, built on FLAME parameters — the FLAME-adjacent counterpart of the 2D methods discussed in this chapter. **Cross-Modal Emotion Transfer for Emotion Editing in Talking Face Video** (arXiv:2604.07786, April 2026) [20] enables emotion editing of existing talking-face videos by transferring emotional content across modalities. Together these two papers represent the beginning of a line of work that decouples emotional expression from the audio input entirely, which has been an open problem throughout the 2023-2025 period.

**The shape of the 2026 lineage.** The 2026 talking-head papers do not represent a single dominant architecture shift — they represent differentiated advances on multiple axes: preference alignment (FantasyTalking2), joint A/V generation (UniTalking), streaming dyadic support (DyStream), and explicit emotion editing (EditEmoTalk, Cross-Modal Emotion Transfer). The field is becoming less monolithic and more specialized, with each new method addressing a specific limitation of the 2024-2025 baseline rather than attempting to be the next general-purpose SOTA.

## What Still Does Not Exist

Several gaps in the talking-head landscape are worth flagging explicitly.

**Real-time, zero-shot, full-face, high-quality, open-source.** No method combines all five. FLOAT is close but not fully real-time at broadcast resolution. READ is real-time but slightly lower quality. MuseTalk is real-time and open-source but only animates the mouth region. The full combination would be a significant commercial product; the closest publicly available approximation as of early 2026 is FLOAT running at moderate speed on good hardware.

**Emotional control separate from audio prosody.** Current methods mostly take emotional expression from the audio itself — happy audio produces happy face. Independent control over emotional expression (audio-neutral + explicit emotion parameter) is not well supported in any publicly available method. The few methods that attempt this (V-Express, some research prototypes) are not mature.

**Cross-language prosody generalization.** Methods trained on English often produce wrong mouth shapes or unnatural motion for other languages, especially tonal languages or languages with phoneme sets that do not appear in the training data. This limits the practical reach of open-source methods for non-English applications.

**Long-form temporal consistency.** Most methods are benchmarked on clips of 5-10 seconds. For multi-minute videos, identity drift, expression drift, and stylistic drift become visible problems. Fixing this requires either very large temporal context windows (expensive) or clever memory mechanisms (active research).

**Full-body talking head.** Almost all current methods animate only the head (face and neck). Full-body motion that includes gesture matching the speech — the kind of motion a news anchor or a presenter naturally produces — is handled by a separate tradition (audio-to-gesture generation) and has not been unified with talking-head face synthesis in a single production-quality system. The combined problem remains open.

## Where Talking Heads Fit in the Landscape

Talking-head methods are a specialized application of the face animation machinery we have been discussing, distinguished by their audio input rather than by any fundamental architectural innovation. Their motion representations are the same as in non-audio-driven methods (blendshapes, FLAME, implicit keypoints, 3DGS deformations). Their image synthesizers are the same (warp-and-decode, FLAME + neural renderer, 3DGS rendering, diffusion). The audio-to-motion mapping is the distinctive component.

The practical implication is that product builders should think of talking-head synthesis as a *feature* of a larger face animation pipeline rather than as a separate technology stack. If you are building a FLAME-based avatar pipeline, you add audio-to-FLAME mapping to support talking-head use cases. If you are building a Live2D-based VTubing pipeline, you add audio-to-blendshape mapping (via NVIDIA Audio2Face or similar). If you are building a neural deformation pipeline, you use one of the diffusion- or flow-matching-based methods that connect audio to motion tensors.

This view avoids the common mistake of treating talking-head synthesis as monolithic. A pipeline that starts with "use FLOAT for talking head" is often constrained in ways the builder does not initially realize — FLOAT is specifically a flow-matching-based motion-latent method with its own image synthesizer, and integrating it with an existing rig pipeline means replacing the rig with FLOAT's internal representation or running two parallel image pipelines. A pipeline that starts with "use audio-to-blendshape and plug it into the existing rig" is cleaner, more composable, and usually the right architectural choice unless the existing rig pipeline is specifically unsuited to the task.

## Summary

Talking-head synthesis — animating a reference face to match an audio track of speech — has evolved from regression-based methods (Wav2Lip, MakeItTalk, SadTalker) through diffusion-based methods (EMO, Hallo, EchoMimic) to flow-matching methods (FLOAT) over the period 2020-2025. Quality has improved dramatically with each generation, with the move to generative modeling (from regression) being the biggest single jump because it ends the mean-collapse problem that kept early methods frozen and robotic. Speed lags quality — the highest-quality methods (EMO, Hallo) are offline; the real-time methods (MuseTalk, READ, SadTalker, NVIDIA Audio2Face) are lower-quality; FLOAT sits in between. A parallel 3DGS-based branch achieves real-time broadcast quality at the cost of per-identity capture. The field is best understood as a specialized application of the face animation representations and rendering methods from the other chapters, with audio-to-motion mapping as the distinctive added component. Product integration usually works best when the talking-head functionality is added as a feature of an existing face animation pipeline (via audio-to-blendshape for rigged systems, audio-to-motion-latent for LivePortrait-style systems) rather than adopted as a standalone stack.

The next chapter turns to 3D Gaussian Splatting avatars — the real-time photorealism track that underlies the 3DGS-based talking heads discussed above and serves a broader role as the production path for real-time high-quality face rendering.

## References

[1] Prajwal, K. R. et al. "A Lip Sync Expert Is All You Need for Speech to Lip Generation In the Wild." ACM MM 2020. `github.com/Rudrabha/Wav2Lip`.

[2] Zhou, Y. et al. "MakeItTalk: Speaker-Aware Talking-Head Animation." SIGGRAPH Asia 2020.

[3] Zhang, W. et al. "SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation." CVPR 2023. `sadtalker.ai`.

[4] Shen, S. et al. "DiffTalk: Crafting Diffusion Models for Generalized Audio-Driven Portraits Animation." CVPR 2023. arXiv:2301.03786. `github.com/sstzal/DiffTalk`. Latent diffusion with reference image + facial landmark conditioning; does not use FLAME.

[5] Tian, L., Wang, Q., Zhang, B., Bo, L. "EMO: Emote Portrait Alive — Generating Expressive Portrait Videos with Audio2Video Diffusion Model under Weak Conditions." ECCV 2024. arXiv:2402.17485. Alibaba Institute for Intelligent Computing. The `HumanAIGC/EMO` repository hosts the paper and project page but does not release code or weights.

[6] "Hallo: Hierarchical Audio-Driven Visual Synthesis for Portrait Image Animation." 2024. arXiv:2406.08801. Open-source diffusion-based talking-head method built on SD 1.5 with ReferenceNet-style identity injection.

[7] "EchoMimic: Lifelike Audio-Driven Portrait Animations through Editable Landmark Conditioning." Ant Group (Alipay Terminal Technology Department), AAAI 2025. arXiv:2407.08136. `github.com/antgroup/echomimic`. Supports audio-only, landmark-only, or combined driving.

[8] Ki, T., Min, D., Chae, G. "FLOAT: Generative Motion Latent Flow Matching for Audio-driven Talking Portrait." ICCV 2025. arXiv:2412.01064, December 2024. KAIST and DeepBrain AI. `github.com/deepbrainai-research/float` — inference code and checkpoints released February 2025.

[9] Wang et al. "READ: Real-time and Efficient Asynchronous Diffusion for Audio-driven Talking Head Generation." arXiv:2508.03457, 2025. Real-time diffusion goal; specific FPS/resolution claims should be verified against the paper body before quoting.

[10] TMElyralab. "MuseTalk: Real-Time High Quality Lip Synchronization with Latent Space Inpainting." 2024. arXiv:2410.10122. `github.com/TMElyralab/MuseTalk`. Latent-diffusion-style (SD 1.5 VAE latent space inpainting), not a pure VAE.

[11] "OmniTalker: Real-Time Text-Driven Talking Head Generation with In-Context Audio-Visual Style Replication." NeurIPS 2025. arXiv:2504.02433. `humanaigc.github.io/omnitalker/`. Dual-branch diffusion transformer jointly generating speech and video at 25 FPS.

[12] "GaussianTalker: Real-Time High-Fidelity Talking Head Synthesis with Audio-Driven 3D Gaussian Splatting." arXiv:2404.14037, CVLab-KAIST. `cvlab-kaist.github.io/GaussianTalker/`. Approximately 120 FPS. TalkingGaussian is a separate related method in the same family.

[13] GeneFace — NeRF-based audio-driven talking-head method. Included here for historical context; it predates and is architecturally distinct from the 3DGS-based methods that replaced NeRF for this task.

[14] NVIDIA. "NVIDIA Open-Sources Audio2Face Animation Model." NVIDIA Developer Blog, September 24, 2025. `developer.nvidia.com/blog/nvidia-open-sources-audio2face-animation-model/`. Released: SDK, Maya/UE5 plugins, training framework v1.0, regression model v2.2, diffusion model v3.0, Audio2Emotion. NVIDIA NIM service wraps Audio2Face with ARKit blendshape output.

[15] "Hallo4: High-Fidelity Dynamic Portrait Animation via Direct Preference Optimization." arXiv:2505.23525, May 2025. DiT-based portrait diffusion with DPO and temporal motion condition modulation; bridge to 2026 preference-aligned methods.

[16] Wang, M., Wang, Q., Jiang, F., Xu, M. "FantasyTalking2: Timestep-Layer Adaptive Preference Optimization for Audio-Driven Portrait Animation." AAAI 2026. arXiv:2508.11255. Code: `github.com/Fantasy-AMAP/fantasy-talking2`. First RLHF pipeline for talking heads: Talking-Critic reward model, Talking-NSQ 410K preference dataset, TLPO preference-optimization framework.

[17] "UniTalking: A Unified Audio-Video Framework for Talking Portrait Generation." arXiv:2603.01418, March 2026. Multi-Modal Transformer Blocks with shared self-attention across audio and video latent tokens; joint audio-video generation via multi-task training. Venue: arXiv preprint; a CVPR 2026 acceptance claim exists in secondary sources but is not substantiated in verified evidence.

[18] "DyStream: Streaming Dyadic Talking Heads Generation via Flow Matching-based Autoregressive Model." arXiv:2512.24408, v1 Dec 2025, v2 Feb 2026. Project page: `robinwitch.github.io/DyStream-Page/`. Streaming dyadic (two-person) talking heads at ~34 ms per frame, under 100 ms end-to-end latency, SOTA lip-sync on HDTF. Direct autoregressive/streaming follow-up to FLOAT.

[19] "EditEmoTalk: Controllable Speech-Driven 3D Facial Animation with Continuous Expression Editing." arXiv:2601.10000, January 2026. FLAME-parameter-based speech-driven animation with explicit emotion editing axis.

[20] "Cross-Modal Emotion Transfer for Emotion Editing in Talking Face Video." arXiv:2604.07786, April 2026. Decouples emotional expression from audio input by transferring emotional content across modalities for post-hoc emotion editing.

See also `vamp-interface/docs/research/2026-04-12-3dmm-flame-diffusion-vtuber-realtime.md` for the underlying research that this chapter draws on for the talking-head section, especially the comparison tables for fastest production-grade methods.
