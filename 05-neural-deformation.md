# Chapter 05 — Neural Image Deformation: From LivePortrait to Distilled Streaming Diffusion

## A different philosophy entirely

The previous three chapters traced communities that all share a single architectural assumption: animating a face means defining a parametric representation of it (Live2D parameters, ARKit blendshapes, FLAME coefficients), driving those parameters over time, and rendering the result. The parameters differ. The rendering differs. The pattern is the same — the face has *structure*, the structure is *named*, and animation is the process of changing the names.

This chapter covers a tradition that does not share that assumption. In the neural-deformation paradigm, animating a face means *warping a source image* toward a *driving motion* without ever committing to an underlying parametric model. There is no rig, no named parameter set, no 3D mesh at the API boundary. The system takes two inputs — a source portrait and a driving signal (another video, another image, a live webcam, or, in the most recent generation, an implicit motion latent) — and produces an output that makes the source look like it is doing what the driver is doing. What happens in between is a learned warp field applied to the source, optionally conditioned by a small set of learned implicit features the system discovered for itself. The "face model" is whatever the network internalized during training, and it is not directly inspectable or editable.

The paradigm has a long pedigree, became practical with First Order Motion Model (Siarohin et al., NeurIPS 2019), reached production quality with LivePortrait (Guo et al., 2024), and split into three operating regimes during 2025–2026 — pure deformation, pure diffusion, and distilled streaming diffusion. By raw user count it is more widely deployed than either Live2D or any FLAME-based system. This chapter walks through the paradigm as it stands at mid-2026, with particular attention to the 2025–2026 developments that changed the architectural picture, and to the question this chapter is increasingly asked to answer: when, if ever, does neural deformation replace the parametric stack rather than complement it?

## The source–driver split

The defining pattern of these methods is the separation of *source* and *driver*. The source is the image you want animated: a photograph, an illustration, a frame from a film, a generated image from a diffusion model — any 2D image containing a face. The driver is the thing that tells the source what to do: another video whose motion you want to transfer, another image whose expression you want to copy, a live webcam feed, or — in the most recent generation — a low-dimensional implicit motion latent. The system's job is to produce an output that preserves the *appearance* of the source (the person in the photo, their skin, their hair, their clothes) while executing the *motion* of the driver.

This is the key architectural commitment, and it distinguishes the family from others. In a Live2D pipeline the source (the character illustration) is a pre-rigged asset, and the driver (live tracking data) speaks a named parameter language the rig expects. In a FLAME pipeline the source (a person's geometry) is a FLAME parameter vector, and the driver is the same. In neural deformation the source is raw pixels with *no parametric representation at all*, and the driver is raw pixels, raw keypoint positions, or a learned latent — the system has to discover, for each new source, how to warp those specific pixels to match that specific motion.

This makes the system's job harder in one specific sense — no parametric prior on the source — and easier in another — no dependence on a rigged asset or a successful 3DMM fit. The second property is why the paradigm matters in practice. Any image you can find or generate becomes animatable without preprocessing, and the methods are robust across source types (photos, illustrations, stylised renders, anime, animals, cartoons) that fail or behave oddly in a FLAME pipeline.

## First Order Motion Model: the ancestor

The paradigm's direct ancestor is the First Order Motion Model (FOMM), Siarohin et al., NeurIPS 2019 [1]. FOMM frames the task as learning a *motion field* between source and driver that tells each source pixel where to move. The architecture has three components:

A **keypoint detector**, trained self-supervised, finds a small set of keypoints (typically ten) on both source and driver. The keypoints are not labelled with semantic meaning — there is no "this is the left eye corner" — they are just the points the network discovers as informative for motion description. Because they are learned rather than hand-authored, they are called *implicit keypoints*.

A **dense motion network** takes the keypoints, along with their first-order approximations (Jacobians of local affine transformations around each keypoint), and produces a dense optical flow field at every source pixel.

A **generator network** warps the source pixels according to the dense motion field and fills in any gaps using learned inpainting, producing the final image.

The architectural insight is that a small set of implicit keypoints plus local first-order motion is sufficient to describe the complex non-rigid deformation of a face for animation purposes. You do not need 3D reconstruction, a named parameter set, or a FACS/blendshape vocabulary — ten learned keypoints plus local linear motion around each is enough. Training is fully self-supervised: given a video of someone's face, train the system to predict any frame from any other frame using the keypoint-based motion representation, and the keypoints and motion description emerge as the representation that makes this task possible.

FOMM established the pattern but had production-blocking limitations: output quality degraded on strong head rotations, the inpainting was visible on occluded regions, frame rate was 10–15 FPS on GPU, and training data was limited. It became an influential research prototype and a baseline every successor compared against.

## LivePortrait: the production implementation

LivePortrait (Guo et al., 2024) [2] is the FOMM lineage's flagship and the method that moved implicit-keypoint animation from research prototype to production tool. Developed by Kwai VGI and released with public code and weights under MIT licence, it is fast enough for real-time use, robust enough to handle diverse source images including anime and animals, and accessible enough to have been packaged into ComfyUI nodes, standalone applications, Python libraries, and consumer-facing products [3].

The architecture is best understood as two stages trained in sequence. The base generator (Stage 1) is a face vid2vid network closely related to FOMM but with a structured motion representation; the Stage 2 retargeting modules are small MLPs trained on top of the frozen Stage 1 to give the user fine, isolated control over individual motions.

The Stage 1 base has four neural modules:

The **Appearance Extractor (𝓕)** takes a source image and produces a 3D appearance feature volume — a learned voxelised representation of the person's visual content that can be queried and warped. Running this once per source is sufficient; the appearance features are reused for every output frame.

The **Motion Extractor (𝓜)**, a ConvNeXt-V2-Tiny backbone, takes an image (source or driver) and produces a structured motion representation: 21 canonical implicit keypoints in 3D, a head rotation matrix, per-keypoint expression deltas, a global translation vector, a global scale factor, and explicit eye-open and lip-open scalars. The structured output is the key advance over FOMM, which had only keypoints — LivePortrait decomposes motion into rotation, expression, translation, and scale components, each independently manipulable or retargetable.

The **Warping Module (𝓦)** takes the source appearance features and the motion representation and produces warped appearance features that match the target motion state. The warping is implemented as a neural network rather than a hand-coded warp operator, which lets it handle occlusions and disocclusions that pure flow fields cannot.

The **Decoder (𝓖)**, a SPADE-conditioned generator, takes the warped appearance features and produces the final RGB image. This is where the learned inpainting happens — when the warp exposes regions not visible in the source (e.g. the back of a head rotated into view), the decoder invents plausible content.

The Stage 1 loss zoo is what makes the warp clean enough to ship. Eight loss terms are jointly active: keypoint *equivariance* (the same keypoints should fall on the same physical points after a known image transform); a keypoint *prior* against degenerate collapse; head-pose supervision; a *deformation prior* keeping per-keypoint expression deltas bounded so that the network does not overload them with identity; a cascaded *perceptual* loss on global, face, and lip crops; three cascaded *GAN* discriminators on the same three crops; a *face-identity* loss against an ArcFace embedding; and a *landmark-guided Wing* loss on lip and eye corners. Each of these terms exists because, in ablations the paper reports, removing it produced a specific visible failure mode.

Stage 2 trains three small MLPs on top of the frozen Stage 1 to fix problems that Stage 1 cannot address from a single base model: a **stitching module** that hides the seam between the warped face crop and the surrounding image (so the face can be pasted back into a full portrait without a visible boundary), an **eyes retargeting MLP** that lets the user dial blink/wide-eye independently of the driver, and a **lip retargeting MLP** that does the same for mouth open/close. These modules turn LivePortrait into a model with a small number of partially exposed control axes, and they are what made the slider-based community workflows possible.

The motion representation is explicit enough to support slider-based editing without a driver. The community exploited this aggressively. The **PowerHouseMan ComfyUI-AdvancedLivePortrait** plugin reverse-engineered the relationship between the motion tensor and twelve user-facing sliders — `smile`, `blink`, `eyebrow`, `aaa`, `eee`, `woo`, `wink`, `pupil_x`, `pupil_y`, `rotate_pitch`, `rotate_yaw`, `rotate_roll` — exposed as ComfyUI nodes via a `calc_fe` function that applies hand-tuned offsets to specific keypoint indices of the motion tensor. There is no ARKit-52 mapping in the plugin: each of the twelve sliders is its own ad-hoc formula on a small set of keypoint indices, and an ARKit-52 → ALP mapping table (≈ 50 lines of code) is something a downstream user has to write themselves. The slider mechanism is not trained into the model — it is a post-hoc mapping from hand-tuned tensor offsets to perceptual slider positions — but it works well enough that LivePortrait with sliders is now a practical tool for parametric animation control without a driver video.

**Speed.** LivePortrait runs at 12.8 ms per frame on an RTX 4090 in PyTorch, and under 10 ms per frame with TensorRT optimisation (FasterLivePortrait). This is well inside real-time: a 30 FPS loop has 33 ms per frame, a 60 FPS loop has 16.7 ms per frame, and LivePortrait fits both. Mid-range GPUs (RTX 3070, 3080) achieve 20–30 FPS at 512² output. On phones the standard form is too heavy, but follow-up work (MobilePortrait) targets that hardware specifically.

**Training data.** LivePortrait was trained on 69 million mixed image-video frames spanning diverse face types, with a fine-tuning pass on animal faces. The diversity matters because it determines what the system can animate: photographs robustly, stylised portraits well enough to be useful in practice, animal faces by design. A model trained only on FFHQ-style photographs would fail on illustrations; LivePortrait does not.

**Licence.** LivePortrait is MIT, with MIT-licensed weights on HuggingFace. The PowerHouseMan ExpressionEditor plugin is also MIT. Downstream tools have proliferated rapidly because the licensing is unambiguous and the code is clean.

## X-NeMo: the diffusion-native cousin

X-NeMo (Liu et al., ICLR 2025) [12] takes the same source–driver setup and replaces the warp-and-decode generator with a fundamentally different recipe. Instead of a structured 21-keypoint motion tensor consumed by an explicit warp field, X-NeMo passes motion through a **1D motion bottleneck** — a low-dimensional implicit token sequence — that is *injected via cross-attention* into a diffusion U-Net's reference branch. The motion is no longer a spatial warp instruction; it is a learned semantic vector the denoiser conditions on.

Two specific innovations make this work at quality. The first is the bottleneck itself: by squeezing motion through a 1D representation rather than a structured 3D one, the encoder is forced to drop identity-correlated content and keep only what is needed to reproduce expression, pose, and gaze. Identity has nowhere to leak through. The second is **Reference Feature Masking** — during training, regions of the reference image's feature map are randomly masked, forcing the cross-attention path to recover the masked regions from the motion signal alone. This breaks the model's reliance on direct copy from reference and pushes it to learn cleaner identity–motion disentanglement. A dual GAN head, with separate discriminators for identity preservation and motion fidelity, completes the recipe.

The result is markedly better cross-identity reenactment than LivePortrait can deliver — driving a stranger's face with someone else's expression no longer leaks the driver's features into the output — but it comes at a cost. X-NeMo is a full diffusion forward pass per frame; on the order of 250 ms on an A100 in the paper's configuration. It is not real-time. What it contributes to the lineage is the recipe — the 1D motion bottleneck plus cross-attention injection — that the next generation of methods then make real-time through distillation. Code is publicly released.

## PersonaLive: the streaming-distilled hybrid

PersonaLive (Li et al., CVPR 2026) [10] is the method that most directly resolves the speed–quality tension between LivePortrait and X-NeMo. It is a streaming diffusion framework for infinite-length portrait animation, runs at roughly 15–20 FPS on a single 4090, fits in a 12 GB VRAM budget, and was designed end-to-end for live streaming with the chunk-boundary discontinuities of LivePortrait/X-Portrait/HunyuanPortrait explicitly addressed. Code and weights are public on GitHub (`GVCLab/PersonaLive`) and HuggingFace (`huaichang/PersonaLive`); the ~15 GB of weights download cleanly from the HuggingFace mirror. A CVPR 2026 acceptance is claimed by the authors.

The recipe is best read as a hybrid that takes specific architectural choices from both ancestors and a set of streaming-specific tricks of its own.

From X-NeMo it takes the 1D implicit motion latent and the cross-attention injection path, gaining the cleaner identity–motion separation that LivePortrait's spatial warp does not provide. From LivePortrait it takes the 21-keypoint 3D structured motion as a *parallel* condition channel, retaining LivePortrait's robust geometric backbone for pose, gaze, and large rotations. The hybrid (1D motion + LivePortrait 3D kp) injection is the first novel piece: each conditioning signal carries what it is best at, and the denoiser sees both.

The second piece is **4-step appearance distillation** with a StyleGAN2 adversarial loss. A 20-step diffusion teacher is distilled into a 4-step student under an adversarial objective rather than a per-step MSE; the discriminator is a frozen StyleGAN2, which provides a sharper, more identity-preserving target than reconstruction loss alone. The student runs CFG-free, which alone roughly halves per-step cost compared to standard guided diffusion.

The third piece is the **AR micro-chunk architecture with sliding training**. Rather than generating one long video at once (which any current method runs out of VRAM trying to do) or generating independent short clips and concatenating them (which produces visible chunk boundaries), PersonaLive generates 8-frame micro-chunks autoregressively, each conditioned on a sliding window of recent frames during training. This is the structural fix for the chunk-boundary problem that has dogged streaming-diffusion methods.

The fourth piece is the **Historical Keyframe Mechanism**. Beyond the sliding window, the model maintains a small bank of historical keyframes that are attended to during each new chunk's generation, which prevents long-form drift over many minutes (the failure mode that X-NeMo and HunyuanPortrait both exhibit past the one-minute mark).

The fifth piece is **Motion-Interpolated Initialisation**. A new chunk is initialised not from pure noise but from the prior chunk's last latent linearly interpolated toward the target motion's predicted endpoint, which collapses several inference steps' worth of work and removes the visible "jump" at chunk boundaries.

Each of these pieces is independently small. Stacked, they are what turns 250 ms/frame X-NeMo-class diffusion into 15–20 FPS streaming.

The architectural significance is that PersonaLive is the first method to credibly close the real-time gap between warp-based methods and diffusion-based methods. LivePortrait owned real-time exclusively in 2024–2025 because the diffusion alternatives could not catch up. PersonaLive removes that exclusivity at quality that, on the metrics the paper reports, exceeds LivePortrait on cross-identity reenactment and matches it on within-identity playback, while remaining usable on consumer hardware.

## Three regimes of real-time

The 2025–2026 generation makes the design space cleaner than it was, and it is worth stating the three regimes explicitly:

**Pure deformation** (LivePortrait, FasterLivePortrait, MobilePortrait). One feed-forward warp-and-decode pass per frame, no diffusion anywhere. Fastest (~10 ms/frame on a 4090), most efficient on memory, lowest quality ceiling. Fails on extreme rotations, occlusions, and OOD source images. Strengths and weaknesses both come from the absence of diffusion.

**Pure diffusion** (X-NeMo, X-Portrait, HunyuanPortrait, FG-Portrait). Full diffusion forward pass per frame, no distillation. Highest quality on extreme cases (large rotations, OOD identities, challenging expressions), best identity-motion disentanglement, but ~250 ms/frame at A100-class hardware. Suitable for offline rendering and animation but not for live capture.

**Distilled streaming diffusion** (PersonaLive). 4-step distilled diffusion + AR micro-chunks + sliding training + historical keyframes. Approaches LivePortrait's speed (~50–65 ms/frame on 4090) at much closer to X-NeMo's quality. The architectural innovation that makes diffusion-class quality affordable at near-real-time on consumer hardware.

The expectation that real-time would *require* abandoning diffusion entirely turns out to have been wrong. Real-time can be achieved either by avoiding diffusion (LivePortrait route) or by making diffusion fast enough through distillation and streaming-aware architecture (PersonaLive route). The right choice depends on what kinds of source images and driver motions you need to handle: easy cases are cheaper through deformation; hard cases need diffusion-grade machinery, and that machinery is now affordable.

## Other 2024–2026 variants

The lineage has spawned a wider family of methods, each targeting a specific constraint the base methods do not address.

**FasterLivePortrait** [4] is an ONNX/TensorRT-optimised reimplementation. On an RTX 3090 it achieves 30+ FPS including pre- and post-processing (face detection, cropping, paste-back), not just model inference. This is the version to run for production real-time webcam use. MIT-licensed; weights at `warmshao/FasterLivePortrait`.

**MobilePortrait** (CVPR 2025) [5] targets mobile deployment with a lightweight U-Net and a mixed explicit-implicit keypoint representation. At the 16 GFLOP configuration (vs. 200–629 GFLOPs for LivePortrait-class models) it runs at ~63 FPS on iPhone 14 Pro and ~39 FPS on iPhone 12; lighter (4–7 GFLOP) configurations exceed 100 FPS on modern iPhones. The practical significance is real-time neural portrait animation on phones without a cloud backend.

**X-Portrait** (Xie et al., SIGGRAPH 2024) [6] extends the paradigm with a Stable Diffusion backbone and ControlNet-style motion conditioning rather than warp-and-decode. Better large-rotation and unusual-expression handling than warp methods, but not real-time. Closely related architecturally to X-NeMo and HunyuanPortrait.

**Follow-Your-Emoji** (SIGGRAPH Asia 2024) [7] introduces expression-aware landmark conditioning. Instead of transferring motion from a full driver video, it takes target facial landmarks describing an expression as an explicit motion signal. Closer to the parametric paradigm in spirit while still using a diffusion-based generator.

**HunyuanPortrait** and **HunyuanVideo-Avatar** (Tencent, 2025) sit in the same diffusion-based portrait-animation slot as X-Portrait/X-NeMo, with comparable quality and speed characteristics. Not real-time without distillation.

**MegActor** (arXiv:2405.20851, May 2024) [8] addresses long-range temporal consistency by adding a Temporal Layer (initialised from AnimateDiff) in a stage-2 training pass. MegActor-Σ extends to a Diffusion Transformer backbone. Both research-level.

**Thin-Plate Spline Motion Model (TPSMM)** (CVPR 2022) [9] predates LivePortrait, uses thin-plate splines rather than local affine for the motion parameterisation, and sits in the same paradigm. Worth knowing as a lightweight fallback.

**FG-Portrait** (CVPR 2026) [13] is the closest published method to driving a portrait animator from FLAME/parameter vectors directly. It uses 3D flow from a parametric head model as learning-free motion correspondence, replacing the implicit motion latent entirely. **No public code as of fetch (2026-05-03)**, which gates adoption.

**IM-Animation** (arXiv:2602.07498, February 2026) [14] continues the implicit-motion thread with a more compact motion encoder and a temporal retargeting module under a three-stage training strategy, designed to disentangle identity and motion more cleanly than LivePortrait's post-hoc sliders allow. **No public code as of fetch.**

**Durian** (arXiv:2509.04434, September 2025) [15] uses LivePortrait among baselines for dual-reference portrait animation with attribute transfer. Evidence that the LivePortrait paradigm is now a standard reference point in the broader literature.

**FlashPortrait** (CVPR 2026) [27] is a long-form DiT-acceleration framework on top of Wan2.1, claiming 6× speedup over its Wan-Animate baseline through a Sliding-Window Adaptive Latent Prediction mechanism (Taylor-expansion-based latent forecasting that skips denoising steps) plus Normalized Facial Expression Blocks (matching distribution centers of diffusion latents and PD-FGC facial features to fight identity drift). The "6×" is relative to a baseline that itself takes ~38 minutes for a 20-second 480×832 video; FlashPortrait completes the same task in 720 seconds (~0.83 FPS render speed on H100-class hardware per the paper's Table 1). The contribution is real for offline long-form generation but does not approach real-time. Code at `github.com/Francis-Rings/FlashPortrait`.

**FantasyPortrait** (CVPR 2026) [28] is an Alibaba DiT-based animator with an Expression-Augmented Learning Strategy that trains implicit representations to capture identity-agnostic facial dynamics, with explicit support for multi-character animation in a single shot. The paper's reported inference time is ~4339 s for a 20-second video (per FlashPortrait's Table 1), placing it firmly in the offline-quality regime. Project: `fantasy-amap.github.io/fantasy-portrait/`.

**DeX-Portrait** (arXiv:2512.15524, December 2025) [29] disentangles pose (explicit global transformation) from expression (implicit latent) via a dual-branch conditioning mechanism in a diffusion model, with a progressive hybrid CFG for identity preservation. Targets the "expression-only or pose-only editing" regime that prior diffusion-based animators handle poorly.

**FactorPortrait** (arXiv:2512.11645, December 2025) [30] decomposes portrait control along expression × pose × viewpoint, in the same disentanglement-of-control thread as DeX-Portrait. December 2025 saw two papers in this slot in the same fortnight, suggesting the field has converged on disentangled-control as the next research front after the speed/quality tradeoff was resolved.

**RAIN** (Shu, Feng, Cao, Zha — arXiv:2412.19489, December 2024) [32] is the streaming-distilled-diffusion sibling to PersonaLive, with a different architectural recipe pointing at the same problem. RAIN fine-tunes an SD-Image-Variations backbone with AnimateDiff 1D temporal blocks, then expands the StreamDiffusion batching pattern: instead of one frame per noise level (StreamDiffusion's choice), it groups `K/p` consecutive frames at the *same* noise level (K=16, p=4 in the paper), with adjacent groups offset by T/p ≈ 250 timesteps, and runs a Temporal Adaptive Attention module *across noise levels* — a setting prior stream methods explicitly avoided. The result is 18 FPS at 512² on a single RTX 4090 with TensorRT and DWPose extraction included, driven by 21-point body keypoints + 68→26-point face landmark linear map. Two findings in the paper are independently interesting outside its specific architecture: (1) the strict-causal ablation fails catastrophically — visible jitter every 4 frames at the group boundary — establishing that *streaming* portrait animation needs **causal-at-the-stream-level but non-causal inside a sliding K-frame window**, not strict per-frame causality; (2) long-range identity drift is mitigated by a frozen reference identity frame fed back into the model, an architectural pattern that recurs in production LivePortrait deployments as "frame-0 calibration" (see operational notes below). RAIN does not displace PersonaLive — at comparable FPS, PersonaLive's distillation + AR micro-chunk recipe targets the same regime — but it is a cleaner formulation of the streaming-batch + cross-noise-attention trick, and a useful reference point when designing future stream-native diffusion animators.

**Streaming filter post-processing.** A separate question that becomes load-bearing as soon as a neural-deformation pipeline is deployed live: per-frame post-stylization filters flicker visibly. Per-frame arbitrary-style transfer methods (AdaIN, AdaAttN, StyTr², AnimeGANv3) applied frame-by-frame to a 30-FPS warp-and-decode output exhibit the same group-boundary jitter pathology RAIN reports. Two responses exist in the literature: flow-aware video stylizers that ingest a small lookahead window natively (ReReVST [33] / "Consistent Video Style Transfer via Compound Regularization," AAAI 2020; Shekhar et al., "Interactive Control over Temporal Consistency while Stylizing Video Streams," Computer Graphics Forum 2023), and wrap-style temporal-coherence passes (RAFT-based flow warp from prior stylized frame + EMA toward an anchor-frame-0 reference) that turn any per-frame filter into a streaming filter at ~5–8 ms additional cost on a 3080. The practical implication for production deployments: the filter slot in a live LivePortrait/PersonaLive pipeline is a *streaming pass*, not a per-frame pass, and must be designed accordingly from the start.

## Operational notes from production LP streaming

Several lessons surfaced from hands-on deployments of LivePortrait-class pipelines in live-streaming contexts during 2026 that did not have an obvious home in the academic literature but are load-bearing for production pipelines.

**The bridge introduces artifacts, not the renderer.** When a parametric driver (ARKit blendshapes from Live Link Face, MediaPipe blendshapes, or a custom landmark stream) is converted to LivePortrait's implicit motion representation through a learned bridge or student network, the *bridge* is responsible for most of the perceived quality difference between a video-driven and parameter-driven session. A production-quality LivePortrait running on a webcam (where the driver is a cropped face image consumed by the unmodified motion extractor) is consistently rated higher than the same renderer driven by ARKit→implicit-motion-latent through a learned bridge — even when the bridge has been distilled against the renderer's own teacher signal at ~10⁵-pair scale. The architectural recommendation is to *keep the parameter signal out of the renderer* and treat it as a measurement/control signal that drives renderer-native inputs (implicit keypoints, video frames) through whatever conversion the parameter source allows. This aligns with the GIF 2020 finding (Chapter 04) that direct FLAME-parameter conditioning of learned generators is unsatisfactory; the same logic extends to ARKit-parameter conditioning of LivePortrait-class generators.

**Production LP daemon recipe.** The setting combination that consistently produces shippable live output on FasterLivePortrait at 30 FPS with sub-200ms glass-to-OBS latency on consumer GPUs: `--crop_driver --pasteback --smooth_motion --scale_clamp 0.0`. `--smooth_motion` applies an OneEuroFilter to driver pitch/yaw/roll/translation/expression/scale and kills the small-amplitude jitter that makes raw-driver output read as "uncanny." `--scale_clamp 0.0` pins driver scale to the frame-0 source value and kills "head pumping" (audience-visible scale drift over a minute of streaming); looser settings (3%) were experimentally too loose. Relative rather than absolute motion mode for expression/rotation preserves driver freedom without the squinted-mouth artifact that absolute mode introduces. For non-FFHQ anchors (paintings, stylised illustrations), `--src_scale 3.0 --dri_scale 2.5` extends the warp's tolerance for off-distribution source images. These are not in the LivePortrait paper; they emerge from production deployment.

**The compositional-split pattern.** A practical observation for stylised anchors (paintings, illustrations, anime portraits): asking the warp network to render the entire anchor (face + clothing + background + non-anatomical extensions like horns, elf ears, long beards) is asking more than the warp network was trained to do — these structures are W's failure mode, not G's, and no amount of decoder retraining fixes them. The Live2D-VTubing pattern — animate only the face region richly, keep body/extensions as static sprite layers — applies cleanly: pre-compute a face-region mask with a segmentation network (BiRefNet, SAM2), run LivePortrait on the cropped face only, composite the animated face back over the anchor's static non-face pixels with edge feathering. Anatomical failures disappear because they are no longer asked of the renderer. Identity preservation improves because the anchor's actual painted/illustrated pixels carry through unchanged outside the face region. Trade: head-rotation envelope is bounded by where the static body can plausibly meet a moving head (acceptable for talking-head streaming, insufficient for headbanging). This is the production unlock for "be Pushkin/Vermeer/Repin" use cases that vanilla LP cannot deliver.

**Where the photoreal-prior lives in encoder-decoder warp networks.** A useful piece of architectural knowledge for anyone considering fine-tuning a LivePortrait-class generator for stylised output: the photoreal-skin bias that makes stylised anchors render "too photoreal" is concentrated in the decoder G's SPADE γ/β projection layers. Three converging arguments support this localisation: (1) Gatys et al. show stylisation is a channel-statistics property (Gram matrices over channel co-occurrence), which is exactly what SPADE's spatially-adaptive affine modulation injects; (2) the StyleGAN coarse-to-fine resolution-to-attribute map places texture/skin-detail in the fine layers, where the SPADE projections operate; (3) the CustomDiffusion finding that fine-tuning only K/V cross-attention projections (≈3% of params) is sufficient for full DreamBooth-style personalisation establishes a precedent for surgically small-parameter fine-tuning at the channel-statistics injection point — and SPADE γ/β are the architectural analog of cross-attention K/V in encoder-decoder GANs. The practical implication is that a stylised LivePortrait variant probably does not need a full retrain; a LoRA on G's SPADE γ/β projections, trained on a paired-synthetic corpus (same StyleGAN latent W rendered through FFHQ-StyleGAN2 and a style-head StyleGAN — MetFaces, Ukiyoe, the FFHQ-transfer-trained NeuralKuvshinov family, or DualStyleGAN's 10 heads — gives identity-preserved photo↔styled pairs at scale), should be sufficient. This research direction is open as of mid-2026; no public stylised LivePortrait variant exists.

## Audio-driven cousins

A separate but architecturally adjacent thread takes audio rather than video as the driver. The 2025–2026 papers worth knowing because they share machinery with the visual-driven family:

**Teller** (CVPR 2025) [16] is autoregressive rather than diffusion-based, with FMLG (Facial Motion Latent Generation) and ETM (Efficient Temporal Module) running at 25 FPS / 0.92 s per second of audio. Strict sub-second latency.

**Sonic** (CVPR 2025) [17] introduces a global audio perception module — replacing frame-local conditioning — for full-face emotion and head motion from audio rather than just lip-sync.

**Hallo2** (ICLR 2025) [18] addresses 4K resolution and hour-long audio-driven animation via multi-resolution patches and long-duration training.

**Hallo-Live** (arXiv:2604.23632, 2026) [19] generates joint audio + video output (not just video from audio) via Asynchronous dual-stream generation, Future-Expanding Attention, and a Human-centric Preference DMD distillation. 20.38 FPS / 0.94 s latency on 2× H200.

**RAP** (arXiv:2508.05115, 2026) [20] adds fine-grained audio control to a DiT-backbone animator with a hybrid attention scheme and a static-dynamic training-inference paradigm to control drift over long generations.

**JoyVASA** [31] is the cleanest published bridge between the audio-driven and video-driven threads — a diffusion-based audio-to-motion generator that emits LivePortrait's implicit-keypoint motion latents directly, allowing any LivePortrait-class generator to be driven by audio without changing the rendering stack. The decoupled facial representation (dynamic facial expressions separated from static 3D facial representation) generalises beyond human portraits to animals. JoyVASA is the audio-side counterpart to FasterLivePortrait — same underlying motion space, different driver. Code: `github.com/jdh-algo/JoyVASA`.

**TalkingMachines** (arXiv:2506.03099, 2025) [21] distils an 18 B I2V DiT into a sparse causal AR student via asymmetric knowledge distillation. The systems co-design — overlapping CUDA streams across model + audio + I/O — is independently interesting.

**AvatarSync** (arXiv:2509.12052, 2025) [22] picks AR over diffusion for the lip-sync core, with cross-lingual generalisation.

**OmniHuman** (ByteDance, 2025) [23] is the closed-source SOTA ceiling: a DiT trained on ~19,000 h of video under an omni-conditions weak-to-strong curriculum (text + audio + pose). Production model behind Dreamina. **No public code.**

**VASA-1** (Microsoft, NeurIPS 2024) [24] is a reference benchmark at up to 40 FPS audio-driven, but **no code or weights** were released.

The audio-driven and video-driven families are converging architecturally — both end up with diffusion or AR backbones consuming a learned motion/expression latent — and the engineering tricks (distillation, streaming chunks, history mechanisms) port between them. PersonaLive's recipe in particular is largely audio-agnostic; an audio-conditioned variant is a natural and likely-imminent direction.

## What the paradigm does well

Neural deformation methods, with the 2026 generation in particular, excel at several tasks that parametric methods cannot do or do awkwardly.

**Source-agnostic animation.** No preprocessing, rigging, or reconstruction is required. Upload any image with a face, get animation. This makes the method usable where FLAME extraction would fail (anime, cartoons, animals), where rigging would be prohibitive (one-off content, low-volume use), or where image-to-animation latency matters more than ultimate quality.

**Real-time driving on consumer hardware.** LivePortrait runs at 30–100 FPS on commodity GPUs. PersonaLive runs at 15–20 FPS on a 4090. Both fit live capture and VTubing. For any application that needs instant feedback, this is the reachable performance envelope.

**Diverse input styles.** Because training data spans photographs, illustrations, and stylised portraits, the methods generalise across input styles in a way that is genuinely surprising. The underlying task (motion transfer) turns out to be more style-invariant than semantic face modelling.

**Direct appearance preservation.** Because the output of a warp-based method is a deformation of the source pixels, appearance details — specific skin tone, specific texture, specific hair, specific lighting — carry through without being regenerated by a renderer. Diffusion methods that condition on a face embedding have to reconstruct visually, and reconstruction loses details. For "animate this *exact* image" tasks, the warp-based fidelity matters. PersonaLive partially recovers this through the StyleGAN2-distilled student, but the cleanest fidelity is still on the warp side.

**Simplicity of integration.** Source image in, driver in, output image out. No parameter estimation, no 3D fitting. Downstream applications integrate with a few function calls.

## What the paradigm does poorly

Symmetric weaknesses come from the same architectural commitments.

**No parametric representation at the API boundary.** Without a named parameter set, you cannot easily say "make this smile 30% stronger" without a driver image that has that smile or a learned slider mapping. Parametric editing is a secondary capability rather than the primary API, and the AdvancedLivePortrait sliders are twelve in number, not the 52 of ARKit; they cover smile, blink, eyebrow, three vowel mouth shapes, wink, gaze, and three head rotations. Roughly 20–25 of ARKit-52's channels can be expressed cleanly through the 12 ALP sliders; the rest (squint, sneer, jaw-side, the asymmetric eye and brow channels, dimple, lip-funnel, lip-roll, etc.) have no slider home and require either a different control mechanism or training.

**Identity does not transfer cleanly in pure-warp methods.** LivePortrait can leak identity from a same-identity driver and degrade on cross-identity drives. X-NeMo and PersonaLive substantially fix this through the 1D motion bottleneck and (for PersonaLive) Reference Feature Masking. The absence of explicit identity preservation in pure-warp methods is real and is one of the things the 2026 generation specifically addresses.

**Quality degrades on extreme motion in pure-warp methods.** Large head rotations, extreme expressions, and occlusions (hand over face, hair across face) are characteristic failure modes. Improving with each generation; PersonaLive handles them better than LivePortrait. Still a pattern.

**Output character.** Trained VTubers comparing LivePortrait to hand-rigged Live2D will identify the LivePortrait as different in a way that matters aesthetically. Frame-to-frame variation, rotation handling, and micro-expression stability differ in ways that trained eyes notice. Pure-warp output *is* real-time-warped video, and it looks like real-time-warped video. PersonaLive narrows this gap but does not close it.

**No 3D structure to compose with.** No 3D mesh means no compositing into 3D scenes, no relighting from scene lights, no novel views. Some variants approximate this; the core paradigm is 2D.

**Cannot generate from text or from an embedding.** The source has to be an image. A text description or an abstract latent vector requires a text-to-image stage (Flux, SDXL, Imagen) before the deformation method takes over. The animation layer is purely a layer.

## On bridging to ARKit blendshapes

Because this chapter is increasingly read as background for projects that need *both* the neural-deformation pipeline and an ARKit-compatible parametric API, it is worth stating the bridge problem explicitly.

The natural ARKit-52 → AdvancedLivePortrait bridge does not exist as a published artefact. Neither LivePortrait, the AdvancedLivePortrait plugin, IM-Animation, nor FG-Portrait ships an ARKit-52 mapping. The PowerHouseMan plugin's `calc_fe` function has twelve hand-tuned formulas, each touching a few keypoint indices of LivePortrait's 21-keypoint motion tensor. Mapping ARKit's 52 channels to those twelve sliders is a ~50-line table-and-arithmetic task — straightforward but bespoke. The mapping covers about 20–25 of the 52 ARKit channels with reasonable fidelity (the symmetric expression channels: smile, blink, brow lift, jaw open, the vowel mouth shapes, gaze direction, head pose). The remaining 25–30 channels (asymmetric variants, fine-grained channels like squint and sneer, lip-funnel, lip-roll, cheek puff, jaw-side) have no clean slider home and are either approximated through a least-squares fit to multiple sliders, simulated by composing slider over time, or handled by an entirely different mechanism (a LoRA slider trained directly on the diffusion generator that produced the source image, for instance).

The honest framing for projects that need ARKit-driven control of a neural-deformed portrait is that neural deformation is *complementary* to slider/LoRA-based parametric control, not a replacement. A useful production architecture combines them: the 12 ALP sliders cover the channels where they fit cleanly, image-side LoRAs or diffusion-internal interventions cover the remaining channels. The two paths fail in opposite directions — LoRA sliders fail "wrong-but-sharp" (classifier fooling, identity drift, over-edit), warp-based control fails "right-but-degraded" (correct geometry, softer texture) — and a combined system is more robust than either alone. A future chapter (Chapter 09) will return to the bridge question in the context of FLAME → ARKit → ALP composition.

## Locating neural deformation in the taxonomy

Returning to the three-axis taxonomy one more time:

- **Dimensionality:** 2D, with 2.5D internal structure. LivePortrait's implicit keypoints are 3D (21 × 3) and the motion extractor predicts a 3D rotation, but the output is image-plane pixels and the methods cannot render novel views. PersonaLive operates fully in 2D latent space.
- **Explicitness:** Implicit. The motion latents (1D in X-NeMo/PersonaLive, 21-keypoint 3D in LivePortrait) and appearance features are learned during training and not interpretable as named parameters. Twelve ALP sliders are a post-hoc mapping, not the model's trained API.
- **Authoring origin:** Learned. Everything from keypoint structure to motion decomposition to appearance encoding emerges from self-supervised training on video data.

This is the cleanest "implicit + learned" representation in the landscape. Where FLAME is statistical, Live2D is hand-authored, and ARKit is hand-authored, the neural-deformation lineage is fully learned. Its profile in the operations matrix:

| Operation | LivePortrait | PersonaLive |
|---|---|---|
| Extract from photo | N/A — no parametric repr | N/A — no parametric repr |
| Render to image | Native (warp + decode) | Native (4-step diffusion) |
| Edit by parameters | Weak — 12 ALP sliders | Weak — same 12 sliders apply via the LP-3D path |
| Interpolate between instances | Via driving video / motion latent | Via 1D motion latent (cleaner) |
| Compose identity + expression | Via source/driver split | Via source/driver split, cleaner disentangling |
| Real-time driving | Strong — 30–100 FPS | Strong — 15–20 FPS |
| Cross-identity reenactment | Weak — leaks driver identity | Strong — 1D bottleneck + RFM |
| Long-form temporal stability | Weak past ~30 s | Strong — historical keyframes + sliding training |

The methods are *complementary* to parametric methods — they handle tasks parametric methods cannot handle, and vice versa — and both are useful in different situations.

## When to reach for neural deformation

Given the strengths and weaknesses, the paradigm is right when several conditions hold:

- **You have an image of the specific thing you want to animate.** Photograph, illustration, generated image, anything 2D.
- **You do not have a rig and will not build one.**
- **You need animation at image fidelity, not geometric fidelity.**
- **You need real-time or near-real-time with minimal setup.**
- **You do not need novel-view synthesis or 3D scene compositing.**

Conversely, the paradigm is wrong when:

- **You need to generate a novel identity from scratch.** Use a diffusion-based generation pipeline (Arc2Face, Flux/SDXL with sliders), then optionally animate the result with LivePortrait or PersonaLive.
- **You need tight parametric control over channels outside the 12-slider ALP coverage.** Use a FLAME-based pipeline, ARKit-driven parametric rig, or LoRA sliders on the upstream generator.
- **You need 3D compositing, novel views, or physical lighting.** Use a 3DGS avatar pipeline.
- **You need the absolute best aesthetic quality for a stylised character.** Use a hand-rigged Live2D model driven by ARKit tracking.
- **You are building a VTubing product for professional creators.** The aesthetic objections to neural-deformed output remain real in this community, though PersonaLive's quality narrows the gap.

## Implications for the rest of the landscape

Neural deformation's existence as a working paradigm has structural implications worth stating explicitly.

**FLAME is not architecturally necessary for animation.** LivePortrait produces high-quality real-time animation with no 3DMM, no FLAME, no explicit face geometry. Chapter 08 returns to whether to use FLAME *internally* in a diffusion pipeline; the answer, partly because of LivePortrait's existence, is "only if you need the properties FLAME specifically provides".

**Real-time and diffusion are no longer mutually exclusive.** This is the 2026 update to the chapter's earlier framing. Through 2024–2025, real-time meant warp-and-decode; diffusion meant offline. PersonaLive falsifies that. The right architecture for a streaming-quality system is now distilled diffusion plus AR micro-chunks, not pure deformation. Pure deformation remains the right *cheap* path; distilled streaming diffusion is the new *quality* path; pure diffusion is the offline path.

**The VTubing world is bifurcating, with a third lane opening.** Professional VTubers with character brands stay on hand-rigged Live2D. Casual users drift toward LivePortrait-based tools. A new mid-tier — content creators who want diffusion-grade quality at near-real-time — is now serviceable by PersonaLive-class methods and was not before.

**Neural deformation is a composable building block.** Source-in, driver-in, output-out is a simple API. Generate an image with Flux, animate with LivePortrait. Extract a face from video, stylise with diffusion, re-animate the stylised result. Composability is high, and the methods are used as final-stage animators in many pipelines whose upstream stages use entirely different representations.

**Implicit motion latents are the fifth major face representation.** Alongside Live2D parameters, ARKit blendshapes, MediaPipe landmarks, and FLAME coefficients, the 21-keypoint LivePortrait motion tensor and the 1D X-NeMo/PersonaLive motion latent are now common representations researchers and engineers need to know about. Unlike the others, they are not at the API boundary — the latents are internal — but they are what the tooling operates on, and anyone extending these methods needs to understand them.

**Some recipes from the parametric side may be ports back.** For projects that use both parametric LoRA-slider control and neural deformation, several techniques developed on the slider side are not present in the LivePortrait loss zoo and may be worth contributing back: robustness training of the critic (PGD-adversarial inner loop), latent-space distilled critics that bypass the VAE decode in the training loop (a 10–100× speedup over decode-based losses), inference-time step gating (turning a slider on only over a controlled portion of the diffusion schedule), NMF/sparse atom bases over the motion-latent or blendshape space (interpretable composition), and inverse pair selection (Solver C — selecting training pairs that already maximally exhibit the target axis rather than synthesising them). These are all small additions and most have direct analogues in the LivePortrait/PersonaLive setup.

## Summary

Neural-deformation methods solve face animation by warping a source image to match a driving motion via learned implicit keypoints or motion latents and a neural warp-plus-decode or distilled-diffusion generator, without committing to any parametric face representation. The 2026 generation has split into three regimes: pure deformation (LivePortrait, ~10 ms/frame, lowest quality ceiling), pure diffusion (X-NeMo, X-Portrait, FG-Portrait, ~250 ms/frame, highest quality), and distilled streaming diffusion (PersonaLive, 15–20 FPS, near-best quality on consumer hardware). The expectation that real-time required abandoning diffusion has been falsified — real-time can now be reached either by avoiding diffusion or by making diffusion fast enough through distillation and streaming-aware architecture. The paradigm is fast, robust across image styles, trivially simple to integrate, and requires no rigging. It excels at "animate this specific image" tasks and fails at "generate a new identity" or "provide tight parametric control over arbitrary axes". Twelve ALP sliders cover roughly 20–25 of ARKit-52's channels cleanly; the rest require a complementary mechanism, typically image-side LoRA sliders or diffusion-internal interventions. The right production architecture combines both. The next chapter turns to audio-driven talking-head methods, which now share most of their machinery with the visual-driven family covered here.

## References

[1] Siarohin, A., Lathuilière, S., Tulyakov, S., Ricci, E., Sebe, N. "First Order Motion Model for Image Animation." NeurIPS 2019. The paradigm ancestor.

[2] Guo, J. et al. "LivePortrait: Efficient Portrait Animation with Stitching and Retargeting Control." arXiv:2407.03168, 2024. Kwai VGI. Code at `github.com/KwaiVGI/LivePortrait`.

[3] LivePortrait project page. `liveportrait.github.io`.

[4] warmshao. "FasterLivePortrait." `github.com/warmshao/FasterLivePortrait`. ONNX/TensorRT-optimised. MIT.

[5] "MobilePortrait: Real-Time One-Shot Neural Head Avatars on Mobile Devices." CVPR 2025. arXiv:2407.05712. FPS figures depend heavily on the GFLOP configuration — 63 FPS on iPhone 14 Pro at 16 GFLOPs up to ~169 FPS at 4–7 GFLOP configurations.

[6] Xie, Y., Xu, H., Song, G., Wang, C., Shi, Y., Luo, L. "X-Portrait: Expressive Portrait Animation with Hierarchical Motion Attention." SIGGRAPH 2024. ByteDance. arXiv:2403.15931.

[7] "Follow-Your-Emoji: Fine-Controllable and Expressive Freestyle Portrait Animation." SIGGRAPH Asia 2024. arXiv:2406.01900.

[8] "MegActor: Harness the Power of Raw Video for Vivid Portrait Animation." Megvii, arXiv:2405.20851, May 2024. MegActor-Σ extension: arXiv:2408.14975.

[9] yoyo-nb. "Thin-Plate-Spline-Motion-Model." CVPR 2022. `github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model`.

[10] Li et al. "PersonaLive: Expressive Portrait Image Animation for Live Streaming." CVPR 2026, arXiv:2512.11253. Code: `github.com/GVCLab/PersonaLive`. Weights: `huggingface.co/huaichang/PersonaLive`. Project page: `personalive.app`. Streamable diffusion framework for infinite-length portrait animation: hybrid (1D implicit motion + LivePortrait 3D kp) injection + 4-step appearance distillation with StyleGAN2 adversarial loss + AR micro-chunks with sliding training + Historical Keyframe Mechanism + Motion-Interpolated Initialisation. ~15 GB weights, 12 GB VRAM, ~2× TensorRT speedup. **Distinct from the unrelated `neosun100/PersonaLive` LivePortrait wrapper of the same name.**

[11] neosun100. "PersonaLive" (LivePortrait wrapper, unrelated to [10]). `github.com/neosun100/PersonaLive`. SvelteKit + TailwindCSS UI + FastAPI + MCP server.

[12] Liu et al. "X-NeMo: Expressive Neural Motion Reenactment via Disentangled Latent Attention." ICLR 2025, arXiv:2507.23143. ByteDance. 1D motion bottleneck + cross-attention injection + dual GAN head + Reference Feature Masking. Code released. The recipe PersonaLive borrows for the disentangled-motion path.

[13] "FG-Portrait: 3D Flow Guided Editable Portrait Animation." CVPR 2026, arXiv:2603.23381. 3D flow from parametric head model as learning-free motion correspondence; the closest published method to driving a portrait animator from FLAME / ARKit parameters directly. **No public code as of 2026-05-03.**

[14] "IM-Animation: An Implicit Motion Representation for Identity-Preserving Portrait Animation." arXiv:2602.07498, February 2026. Compact implicit motion encoder + temporal retargeting module + three-stage training. **No public code as of 2026-05-03.**

[15] "Durian: Dual Reference Image-Guided Portrait Animation with Attribute Transfer." arXiv:2509.04434, September 2025.

[16] Zhen et al. "Teller: Real-Time Streaming Audio-Driven Portrait Animation with Autoregressive Motion Generation." CVPR 2025, arXiv:2503.18429. AR rather than diffusion. FMLG + ETM. 25 FPS / 0.92 s per second of audio.

[17] "Sonic: Shifting Focus to Global Audio Perception in Portrait Animation." Tencent, CVPR 2025, arXiv:2411.16331.

[18] Cui et al. "Hallo2: Long-Duration and High-Resolution Audio-driven Portrait Image Animation." ICLR 2025, arXiv:2410.07718.

[19] Li et al. "Hallo-Live: Real-Time Joint Audio-Video Avatar Generation." arXiv:2604.23632, 2026. Asynchronous dual-stream + Future-Expanding Attention + Human-centric Preference DMD. 20.38 FPS / 0.94 s on 2× H200.

[20] Du et al. "RAP: Realistic Audio-Driven Portrait Animation with Hybrid Attention." arXiv:2508.05115, 2026. DiT backbone + hybrid attention + static-dynamic training-inference paradigm.

[21] Low & Wang. "TalkingMachines: Real-Time Audio-Driven Talking Head Avatars via Asymmetric Knowledge Distillation." arXiv:2506.03099, 2025. 18 B I2V DiT distilled to 2 diffusion steps; CUDA stream overlap.

[22] "AvatarSync: Cross-Lingual Autoregressive Lip-Sync." arXiv:2509.12052, 2025. AR over diffusion for lip-sync.

[23] Lin et al. "OmniHuman: Scaling Up One-Stage Multimodality Conditioned Human Animation." ByteDance, 2025, arXiv:2502.01061. DiT + omni-conditions weak-to-strong curriculum + ~19,000 h training video. Production model behind Dreamina. **No public code.**

[24] Microsoft. "VASA-1: Lifelike Audio-Driven Talking Faces Generated in Real Time." NeurIPS 2024. Up to 40 FPS audio-driven. **No code or weights released.**

[25] "Motion Manipulation via Unsupervised Keypoint Positioning in Face Animation" (MMFA). arXiv:2603.04302, March 2026. Unsupervised 3D keypoints for arbitrary pose rotation/translation and motion-attribute editing. Authors acknowledge expression deformation is coupled with facial scaling — limits accurate isolated expression manipulation. No code reported.

[26] "Let Your Image Move with Your Motion! — Implicit Multi-Object Multi-Motion Transfer" (FlexiMMT). arXiv:2603.01000, claimed CVPR 2026. Code: `github.com/Ethan-Li123/FlexiMMT`. Motion-Decoupled Mask Attention + Differentiated Mask Propagation. Not face-specific but relevant as a multi-object generalisation.

[27] Tu et al. "FlashPortrait: 6× Faster Infinite Portrait Animation with Adaptive Latent Prediction." CVPR 2026, arXiv:2512.16900. Fudan + MSRA + XJTU + Tencent + Tongyi Lab Alibaba. Wan2.1 14B DiT backbone + Sliding-Window Adaptive Latent Prediction (Taylor expansion over historical latent differences) + Normalized Facial Expression Block. 720 s per 20-second video on H100-class (~0.83 FPS). Code: `github.com/Francis-Rings/FlashPortrait`. Weights: `huggingface.co/FrancisRing/FlashPortrait`.

[28] Wang et al. "FantasyPortrait: Enhancing Multi-Character Portrait Animation with Expression-Augmented Diffusion Transformers." CVPR 2026, arXiv:2507.12956. Alibaba. DiT + Expression-Augmented Learning Strategy + multi-character support in a single generation. Project: `fantasy-amap.github.io/fantasy-portrait/`.

[29] "DeX-Portrait: Disentangled and Expressive Portrait Animation via Explicit and Latent Motion Representations." arXiv:2512.15524, December 2025. Pose as explicit global transformation, expression as implicit latent code, dual-branch diffusion conditioning, progressive hybrid CFG. Project: `syx132.github.io/DeX-Portrait/`.

[30] "FactorPortrait: Controllable Portrait Animation via Disentangled Expression, Pose, and Viewpoint." arXiv:2512.11645, December 2025. Three-axis disentanglement of portrait control. Companion to DeX-Portrait in the late-2025 disentangled-control wave.

[31] Cao et al. "JoyVASA: Portrait and Animal Image Animation with Diffusion-Based Audio-Driven Facial Dynamics and Head Motion Generation." JD Health AI / jdh-algo, late 2024 / 2025. Diffusion transformer over LivePortrait's implicit-keypoint motion space; the audio-side bridge that lets LivePortrait-class generators run from audio. Code: `github.com/jdh-algo/JoyVASA`.

[32] Shu, Z., Feng, R., Cao, Y., Zha, Z.-J. "RAIN: Real-time Animation of Infinite Video Stream." arXiv:2412.19489, December 2024. SD-Image-Variations + AnimateDiff temporal blocks + Temporal Adaptive Attention with K/p frame grouping at the same noise level + cross-noise-level attention. 18 FPS at 512² on RTX 4090 with TensorRT, DWPose-driven. Strict-causal ablation fails at group boundaries; reference identity frame mitigates long-range drift. Streaming-distilled-diffusion sibling of PersonaLive with a cleaner formulation of the streaming-batch trick.

[33] Wang, W., Yang, S., Xu, J., Liu, J. "Consistent Video Style Transfer via Compound Regularization" (ReReVST). AAAI 2020. Flow-aware video stylization with built-in temporal coherence; cited as the canonical pre-streaming-LP reference for streaming filter post-processing. Companion: Shekhar et al., "Interactive Control over Temporal Consistency while Stylizing Video Streams." Computer Graphics Forum, 2023 — explicitly streaming, framework-agnostic temporal-coherence wrap around per-frame stylizers.

See also `vamp-interface/docs/research/2026-05-03-liveportrait-x-nemo-analysis.md` for the architectural deep-dive on LivePortrait Stages 1–2 and X-NeMo's 1D bottleneck + cross-attention recipe, including a side-by-side loss-zoo comparison vs the slider-LoRA training stack; `vamp-interface/docs/research/2026-05-03-personalive-experiment-plan.md` for a four-phase verification plan (sanity → recipe grid → slider data factory → ARKit bridge); `vamp-interface/docs/research/2026-05-03-neural-deformation-synthesis.md` for the complementary-not-replacement decision relative to LoRA-slider blendshape control on Flux portraits; and `vamp-interface/docs/papers/README.md` for the local PDF archive (PersonaLive, X-NeMo, FG-Portrait, OmniHuman, Teller, Sonic, Hallo2, Hallo-Live, RAP, TalkingMachines, AvatarSync) with one-line "read this if you need to…" problem-indexed entries.
