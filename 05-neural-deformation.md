# Chapter 05 — Neural Image Deformation: LivePortrait and the Implicit-Keypoint Lineage

## A Different Philosophy Entirely

The previous three chapters have traced three communities that all share a certain architectural assumption: that animating a face means defining a parametric representation of it (Live2D parameters, ARKit blendshapes, FLAME coefficients), driving those parameters over time, and rendering the result. The parameters differ. The rendering differs. But the pattern is the same: the face has *structure*, the structure is *named*, and animation is the process of changing the names.

This chapter covers a tradition that does not share that assumption. In the neural-deformation paradigm, animating a face means *warping a source image* toward a *driving motion* without ever committing to an underlying parametric face model. There is no rig. There is no named parameter set. There is no 3D mesh or blendshape vector at the API boundary. The system takes two inputs — a source portrait and a driving signal (another video, another image, or a live webcam feed) — and produces an output that makes the source look like it is doing what the driver is doing. What happens in between is a learned warp field applied to the source's pixels, optionally conditioned by a small set of learned implicit features that the system has discovered for itself. The "face model" is whatever the neural network internalized during training, and it is not directly inspectable or editable.

This approach has a long pedigree in the face animation literature, but it became practically important with the First Order Motion Model (Siarohin et al., NeurIPS 2019), reached production viability with LivePortrait (Guo et al., 2024), and is currently one of the most actively used face animation methods in the real world — more widely deployed, in raw user count, than either Live2D or any FLAME-based system. It is the method you use when you want to animate *any* face without rigging anything, when you want to turn a photograph into a performance without a 3D reconstruction pass, and when you want real-time portrait animation that works on whatever source image you feed it without preprocessing.

This chapter walks through the paradigm, the core methods, the quality and speed tradeoffs, the operations it supports and doesn't, and the specific role it plays in the larger landscape. The thesis is that neural deformation is not a lesser alternative to parametric animation — it is a parallel solution to a subtly different problem, and understanding the difference is important for knowing when to reach for which.

## The Source–Driver Split

The defining pattern of neural-deformation methods is the separation of the *source* and the *driver*. The source is the image you want animated: a photograph of a person, an illustration, a frame from a film, a generated image from a diffusion model — any 2D image containing a face. The driver is the thing that tells the source what to do: another video whose motion you want to transfer, another image whose expression you want to copy, or a live webcam feed that drives the source in real time. The system's job is to produce an output that preserves the *appearance* of the source (the person in the photo, their skin, their hair, their clothes) while executing the *motion* of the driver (the turn of the head, the opening of the mouth, the blink of the eye).

The source–driver distinction is the key architectural commitment and distinguishes this family from others. In a Live2D pipeline the source (the character illustration) is a pre-rigged asset, and the driver (the live tracking data) speaks a named parameter language that the rig expects. In a FLAME pipeline the source (the person's geometry) is represented as a FLAME parameter vector, and the driver (also a FLAME vector, perhaps extracted from another face) speaks the same parametric language. In neural deformation the source is raw pixels with *no parametric representation at all*, and the driver is raw pixels or raw keypoint positions — the system has to discover, on the fly and for each new source, how to warp those specific pixels to match that specific motion.

This makes the system's job harder in one specific sense — it cannot assume any parametric representation of the source — and easier in another — it does not depend on having a rigged asset or a successful 3DMM fit. The second property is why the approach matters for real applications. Any image you can find or generate becomes animatable without preprocessing, and the method is robust across source types (photos, illustrations, stylized renders, anime, animals, cartoon characters) that would fail or behave oddly in a FLAME pipeline.

## First Order Motion Model: The Ancestor

The paradigm's direct ancestor is the First Order Motion Model (FOMM) by Siarohin et al., published at NeurIPS 2019 [1]. FOMM frames the task as learning a *motion field* between the source and the driver that tells each source pixel where to move. The core architecture has three components:

1. A **keypoint detector** trained in a self-supervised fashion to find a small set of keypoints (typically ten) on both source and driver images. The keypoints are not labeled with semantic meaning — there is no "this is the left eye corner" — they are just the points that the network discovers during training as being informative for motion description. Because they are learned rather than hand-authored, they are called *implicit keypoints*.

2. A **dense motion network** that takes the source and driver keypoints, along with their first-order approximations (Jacobians of local affine transformations around each keypoint), and produces a dense optical flow field defined at every pixel of the source.

3. A **generator network** that warps the source pixels according to the dense motion field and fills in any gaps using learned inpainting, producing the final output image.

The FOMM architecture's key insight is that a small set of implicit keypoints plus local first-order motion information is sufficient to describe the complex non-rigid deformation of a face for animation purposes. You do not need a 3D reconstruction, a named parameter set, or a full FACS/blendshape vocabulary — ten learned keypoints plus local linear motion around each is enough. The training is fully self-supervised: given a video of someone's face, train the system to predict any frame from any other frame of the same video using the keypoint-based motion representation, and the keypoints and motion description will emerge as the representation that makes this task possible.

FOMM established the basic pattern, but it had limitations that kept it from being production-ready: the output quality degraded on strong head rotations, the inpainting was visible on occluded regions, the frame rate was around 10-15 FPS on GPU, and the training data was limited. It became an influential research prototype and a baseline that every subsequent method compared against.

## LivePortrait: The Production Implementation

LivePortrait (Guo et al., 2024) [2] is the FOMM lineage's current flagship and the method that moved implicit-keypoint animation from research prototype to production tool. Developed by the Kwai VGI (Visual Generation and Interaction) team and released with public code and weights under MIT license, LivePortrait is fast enough for real-time use, robust enough to handle diverse source images including anime and animals, and accessible enough that it has been packaged into ComfyUI nodes, standalone applications, Python libraries, and consumer-facing products [3].

The LivePortrait architecture has four neural modules:

**Appearance Extractor (𝓕).** Takes a source image and produces a 3D appearance feature volume — essentially a learned voxelized representation of the person's visual content that can be queried and warped. Running this module once per source (as long as you are animating the same photo repeatedly) is sufficient; the appearance features are reused for every output frame.

**Motion Extractor (𝓜).** Takes an image (source or driver) and produces a structured motion representation consisting of: K canonical implicit keypoints in 3D, a head rotation matrix, per-keypoint expression deltas, a global translation vector, a global scale factor, and explicit eye-open and lip-open scalars. The structured output is the key advance over FOMM, which only had keypoints — LivePortrait decomposes the motion into rotation, expression, translation, and scale components, each of which can be manipulated or retargeted independently.

**Warping Module (𝓦).** Takes the source appearance features and the motion representation and produces warped appearance features that match the target motion state. The warping is implemented as a neural network rather than a hand-coded warp operator, which allows it to handle occlusions and disocclusions that pure warp fields cannot.

**Decoder (𝓖).** Takes the warped appearance features and produces the final output RGB image. This is where the learned inpainting happens — when the warp exposes regions that were not visible in the source (e.g., the back of a head rotated into view), the decoder has to invent plausible content.

The motion representation is explicit enough to support *slider-based editing*: you can adjust the rotation matrix, the expression deltas, or the eye/lip scalars directly, without supplying a driver video. The community has explored this aggressively. The PowerHouseMan ComfyUI-AdvancedLivePortrait plugin reverse-engineered the relationship between the motion tensor and user-facing sliders like "smile," "blink," "eyebrow," "aaa/eee/woo" (vowel-shape mouth presets), "pupil_x," and "pupil_y," and exposed them as ComfyUI nodes. The slider mechanism is not trained into the model — it is a post-hoc mapping from hand-tuned tensor offsets to perceptual slider positions — but it works well enough that LivePortrait with sliders is now a practical tool for generating animated portraits via parametric control, without a driver video at all.

**Speed.** LivePortrait runs at 12.8 ms per frame on an RTX 4090 in PyTorch, and under 10 ms per frame with TensorRT optimization (FasterLivePortrait). This is well within real-time: a 30 FPS tracking loop has 33 ms per frame, a 60 FPS loop has 16.7 ms per frame, and LivePortrait fits both. On mid-range GPUs (RTX 3070, 3080) it still achieves 20-30 FPS for 512² output. On mobile, the story is different — LivePortrait in its standard form is too heavy for phones — but follow-up work (MobilePortrait, discussed below) specifically targets mobile-class hardware.

**Training data.** LivePortrait was trained on 69 million mixed image-video frames spanning diverse face types, including a fine-tuning pass on animal faces (cats, dogs, pandas). The diversity of training data matters because it determines what the system can animate: LivePortrait handles photographs robustly, handles stylized portraits (anime, illustrations) well enough to be useful in practice, and handles animal faces because it was specifically trained to. A method trained only on FFHQ-style photographs would fail on illustrations; LivePortrait does not.

**License.** LivePortrait is MIT-licensed, with MIT-licensed weights published on HuggingFace. The PowerHouseMan ExpressionEditor ComfyUI plugin is also MIT-licensed. Downstream tools built on LivePortrait have proliferated rapidly because the licensing is unambiguous and the code is clean.

## Variants and Descendants

LivePortrait has spawned a family of related methods in 2024 and 2025, each targeting a specific constraint the base method does not address.

**FasterLivePortrait** [4] is an optimized reimplementation of LivePortrait using ONNX and TensorRT for faster inference. On an RTX 3090, FasterLivePortrait achieves 30+ FPS including pre- and post-processing (face detection, cropping, paste-back), not just the model inference. This is the version you actually run for production real-time webcam use. The `python run.py --src_image portrait.jpg --dri_video 0 --cfg configs/trt_infer.yaml --realtime` command turns the system into a live webcam-driven portrait animator in one line. The output appears in a window; piping to OBS for streaming requires a virtual camera wrapper (`v4l2loopback` on Linux, OBS Virtual Camera on Windows, plus `ffmpeg` to bridge). FasterLivePortrait is MIT-licensed and the weights are hosted on HuggingFace at `warmshao/FasterLivePortrait`.

**MobilePortrait** (CVPR 2025) [5] targets mobile deployment with a lightweight U-Net architecture and a mixed explicit-implicit keypoint representation. At the 16 GFLOP configuration (compared to 200-629 GFLOPs for LivePortrait-class models — specifically, the paper quotes 200 GFLOPs for MCNet, 610 for Real3D, and 629 for FaceV2V), MobilePortrait runs at approximately 63 FPS on an iPhone 14 Pro (~15.8 ms per frame) and approximately 39 FPS on an iPhone 12. At lighter GFLOP budgets (4-7 GFLOPs), the paper reports well above 100 FPS on modern iPhones. The practical significance is that real-time neural portrait animation on phones is now feasible at multiple quality-versus-efficiency operating points, which matters for any application that needs to run on phones without a cloud backend.

**X-Portrait** (Xie et al., SIGGRAPH 2024) [6] extends the portrait animation paradigm by building on a pretrained diffusion backbone (Stable Diffusion) with ControlNet-style motion conditioning, rather than using a pure warp-and-decode pipeline. The authors (from ByteDance) use this to achieve better handling of large head rotations and unusual expressions than FOMM or LivePortrait can manage, at the cost of speed — X-Portrait is not real-time. The paper addresses the specific failure mode where warp-based methods produce visible artifacts on extreme cases and represents the diffusion-native branch of the lineage.

**Follow-Your-Emoji** (SIGGRAPH Asia 2024) [7] introduces expression-aware landmark conditioning: instead of transferring motion from a full driver video, it takes target facial landmarks describing an expression as an explicit motion signal and animates the source to match. This is closer to the parametric paradigm — the user specifies a target expression via landmarks, and the system produces it on the source — while still using a diffusion-based generator and no 3DMM.

**MegActor** (arXiv 2405.20851, May 2024) [8] addresses long-range temporal consistency: when animating a source for many frames, earlier methods drift and lose stability over time. MegActor is a conditional diffusion model that adds a Temporal Layer (initialized from AnimateDiff) in a stage-2 training pass to improve multi-second consistency. MegActor-Σ (arXiv 2408.14975) extends the approach to a Diffusion Transformer backbone. Both are research-level, not production.

**Thin-Plate Spline Motion Model (TPSMM)** (CVPR 2022) [9] predates LivePortrait and uses a different motion parameterization (thin-plate splines rather than local affine) but sits in the same paradigm. Community-maintained ONNX ports exist (e.g. instant-high's reenactment fork), and the method is worth knowing as a lightweight fallback when LivePortrait is not available. Anecdotal reports suggest it handles illustrated/anime sources somewhat more gracefully than LivePortrait for certain inputs, though the official repo does not specifically document this capability.

**PersonaLive (the wrapper)** [10] — note that this name is unfortunately overloaded with a separate CVPR 2026 research paper discussed below; they are unrelated projects. The wrapper by `neosun100` on GitHub is a LivePortrait-based tool that adds a local web UI (SvelteKit + TailwindCSS), a FastAPI REST API, and an MCP (Model Context Protocol) server, making the animation engine scriptable from Claude Code or other LLM agents. It requires 12 GB+ VRAM. Its significance is practical rather than research: it represents the move toward treating LivePortrait as a general-purpose tool that agentic workflows can invoke.

**Viggle LIVE** [11] is a commercial SaaS that offers real-time webcam-driven character animation, reportedly based on a LivePortrait-style approach. It has a 1-2 second input-to-output latency, which makes it unsuitable for live VTubing (where sub-100 ms feedback is expected) but acceptable for recorded content creation. Its existence is worth noting as evidence of commercial interest in the paradigm, even though the specific product is not competitive for real-time use.

The pattern across these variants is that LivePortrait is the baseline and each variant optimizes a specific axis: FasterLivePortrait optimizes inference speed, MobilePortrait optimizes mobile hardware, X-Portrait optimizes extreme cases, Follow-Your-Emoji optimizes parametric control, MegActor optimizes temporal stability. No single variant dominates LivePortrait across all axes, and the base LivePortrait remains the right starting point for most applications.

## 2026 Developments: The Successor Generation

Through the first quarter of 2026 the LivePortrait lineage entered a second generation of successors, published at CVPR 2026 and on arXiv. Three papers are worth flagging specifically because they continue the paradigm while addressing limitations the 2024-2025 methods could not.

**IM-Animation** (arXiv:2602.07498, February 2026) [12] is architecturally the most direct descendant of LivePortrait. The title — "An Implicit Motion Representation for Identity-Preserving Portrait Animation" — captures the agenda: rather than the 21-keypoint structured motion tensor that LivePortrait uses, IM-Animation proposes a more compact implicit motion encoder plus a temporal retargeting module, with a three-stage training strategy designed to decouple identity and motion more cleanly than LivePortrait achieves. It is the current state of the art on the "implicit keypoint" axis of the taxonomy as of early 2026, and its contribution is specifically the cleaner identity-motion disentanglement that LivePortrait's sliders struggle to achieve in their post-hoc form.

**FG-Portrait** (arXiv:2603.23381, CVPR 2026) [13] moves the lineage toward 3D-aware animation. The "3D Flow Guided Editable Portrait Animation" title indicates the approach: the motion representation incorporates 3D optical flow guidance, giving the system better handling of large head rotations and enabling editability that pure 2D warp methods cannot support. The paper is in the CVPR 2026 proceedings, positioning it as the CVPR-sanctioned 2026 advance in this space.

**PersonaLive!** [14] — despite sharing a name with the unrelated LivePortrait wrapper discussed above, this is a distinct research paper titled "PersonaLive! Expressive Portrait Image Animation for Live Streaming" (arXiv:2512.11253, December 2025). It is a streamable diffusion framework for infinite-length portrait animation with explicit attention to the live-streaming use case: long-form temporal consistency (which the 2024-2025 diffusion methods lost over multi-minute clips), 12 GB VRAM budget, and approximately 2x speedup with TensorRT. Code and weights are on GitHub at `GVCLab/PersonaLive` and HuggingFace at `huaichang/PersonaLive`, with a project page at `personalive.app`. A CVPR 2026 acceptance claim circulates in secondary sources but could not be corroborated against the official CVPR 2026 program page in a verification pass on 2026-04-14 — treat the venue as arXiv-only until an official source confirms. Independent of venue, PersonaLive is the first method to credibly claim production-quality real-time diffusion-based portrait animation for streaming, closing a gap that LivePortrait-class warp methods had owned exclusively in 2024-2025.

**Durian** (arXiv:2509.04434, September 2025) [15] is slightly outside the 2026 window but is included here because it explicitly uses LivePortrait among its baselines when constructing a dual-reference-image portrait animation with attribute transfer. It is evidence that the LivePortrait paradigm is now a standard reference point in the broader portrait animation literature, and its cross-pollination with diffusion-based attribute transfer points toward the hybrid methods that 2026 papers like PersonaLive and FG-Portrait are developing at production quality.

**The shape of the 2026 lineage.** Taken together, the 2026 successors mark two shifts from the 2024-2025 state of the art: first, a move from pure warp-and-decode generators toward diffusion-backed generators that handle extreme cases, long-form consistency, and editability better (PersonaLive, FG-Portrait); and second, a move from LivePortrait's 21-keypoint explicit motion tensor toward more compact implicit motion representations that disentangle identity and motion more cleanly (IM-Animation). The base LivePortrait remains the right starting point for lightweight and latency-constrained applications, but for the high-quality end of the space, 2026 methods are the frontier.

## What the Paradigm Does Well

Neural deformation methods, and LivePortrait in particular, excel at several tasks that parametric methods either cannot do or do awkwardly.

**Source-agnostic animation.** The biggest single advantage is that no preprocessing, rigging, or reconstruction is required. Upload any image with a face, get animation. This is the property that makes the method usable in contexts where FLAME extraction would fail (anime illustrations, cartoon characters, animals), where rigging would be prohibitive (one-off content creation, low-volume applications), or where the speed from-image-to-animation matters more than ultimate quality.

**Real-time driving.** LivePortrait and its descendants run at 30-100 FPS on commodity hardware with output resolutions from 256² to 512². This is real-time by any reasonable definition and comfortably fits the VTubing and live-capture use cases.

**Handling of diverse input styles.** Because the training data included diverse image types, the methods work on photographs, illustrations, stylized portraits, and even non-human faces. This is a genuinely surprising empirical result — a system trained on the general problem of "warp a source to match a driver" generalizes better across styles than you would expect, because the underlying task (motion transfer) is more style-invariant than semantic face modeling.

**Direct appearance preservation.** Because the output is a warp of the source pixels, the appearance details are preserved exactly up to the warp: the specific skin tone, the specific texture, the specific hair style, the specific lighting of the source image all carry through to the output without being "regenerated" by a neural renderer. A diffusion-based method that conditions on a face embedding has to reconstruct the face visually, and the reconstruction will lose details; LivePortrait just warps, so the details stay. For applications that need to animate a *specific* image exactly, this fidelity matters.

**Simplicity of integration.** The system has a simple API: source image in, driver in, output image out. No rigging, no parameter estimation, no 3D fitting. Downstream applications integrate with a few function calls.

## What the Paradigm Does Poorly

Symmetric with its strengths, neural deformation methods have characteristic weaknesses that come from the same architectural commitments.

**No parametric representation at the API boundary.** Because there is no named parameter set, you cannot easily edit the output by saying "make this smile 30% stronger" without either using a driver image that has that smile or using a learned slider mapping (as PowerHouseMan's ComfyUI plugin does) which is empirical and brittle. Parametric editing is possible but it is a secondary capability rather than the primary API, and the sliders do not correspond to well-defined semantic axes the way ARKit blendshapes or FLAME components do.

**Identity does not transfer cleanly.** The method animates the source; it cannot produce a novel identity from a description. If you want a face that nobody has ever generated before, you need a generation pipeline that sits *before* LivePortrait (e.g., Stable Diffusion → image → LivePortrait for animation). The neural deformation layer is not doing generation, only animation.

**Quality degrades on extreme motion.** Large head rotations, extreme expressions, and occlusions (hand over face, hair swinging across face) are the characteristic failure modes. The learned inpainting handles moderate cases but fails on edge cases that were underrepresented in training data. This is improving with each generation of methods but remains a pattern.

**Output looks video-like, not puppet-like.** This is subjective but real: when a traditional VTuber compares LivePortrait output to a hand-rigged Live2D performance, they will identify the LivePortrait as different in a way that matters aesthetically. The difference is not precisely quality — LivePortrait's photorealism on a photograph is beyond what Live2D attempts — but the frame-to-frame variation, the rotation handling, and the micro-expression stability are different in ways that trained VTubers and traditional animators notice immediately. The LivePortrait output *is* real-time-warped video, and it looks like real-time-warped video.

**No 3D structure to compose with.** Because there is no 3D mesh, the system cannot integrate with 3D scene content (compositing a LivePortrait-animated character into a 3D VR environment, for example, or relighting based on 3D scene lights). Some variants (X-Portrait and others with explicit pose control) approximate this, but the core paradigm is 2D.

**Cannot generate from text or from an embedding.** The source has to be an image. If your application's input is a text description, or an abstract latent vector, you need a text-to-image or latent-to-image stage that produces the source, and LivePortrait takes it from there. The method is purely an animation layer.

## Locating Neural Deformation in the Taxonomy

Returning to the three-axis taxonomy one more time:

- **Dimensionality:** 2D. LivePortrait and its relatives operate in the image plane. The implicit keypoints are described as 3D (K × 3), and the motion extractor predicts a 3D rotation matrix, so there is some 3D structure internally, but the output is 2D image-plane pixels and the method cannot render novel views. Calling it 2.5D captures the internal structure more faithfully.
- **Explicitness:** Implicit. The implicit keypoints, the motion tensor, and the appearance features are all learned during training and are not interpretable as named parameters. The sliders that PowerHouseMan's plugin exposes are a post-hoc mapping discovered by the community, not part of the model's trained API.
- **Authoring origin:** Learned. Everything from the keypoint structure to the motion decomposition to the appearance encoding emerges from self-supervised training on video data.

This is the cleanest "implicit + learned" representation in the landscape. Where FLAME is statistical, Live2D is hand-authored, and ARKit is hand-authored, LivePortrait is fully learned from data. Its profile in the operations matrix:

| Operation | LivePortrait support |
|---|---|
| Extract from photo | Not applicable — there is no parametric representation to extract into |
| Render to image | Native — the method produces images |
| Edit by parameters | Weak — only through post-hoc slider mappings |
| Interpolate between instances | Via driving video interpolation, not parameter interpolation |
| Compose identity + expression | Via choosing source (identity) and driver (expression), yes |
| Real-time driving | Strong — 30-100 FPS on commodity hardware |

The method is *complementary* to parametric methods — it handles tasks that parametric methods cannot handle and vice versa — and both are useful in different situations.

## When to Reach for Neural Deformation

Given the strengths and weaknesses, neural deformation is the right choice when several conditions hold:

- **You have an image of the specific thing you want to animate.** If the input is a photograph, illustration, generated image, or any other source where the identity is fixed in the image itself.
- **You do not have a rig and will not build one.** If the cost of rigging (hand-authoring, 3DMM extraction, etc.) is prohibitive for your use case.
- **You need animation at image fidelity, not geometric fidelity.** If the appearance of the specific source matters more than the 3D correctness of the animation.
- **You need real-time or near-real-time with minimal setup.** If the goal is to ship animation output immediately without a multi-stage preprocessing pipeline.
- **You do not need novel-view synthesis or 3D scene compositing.** If the output is always front-facing within a small rotation range and stays as a 2D asset.

Conversely, neural deformation is the wrong choice when:

- **You need to generate a novel identity from scratch.** Use a diffusion-based generation pipeline (Arc2Face, RigFace, HeadStudio) that outputs an image, then optionally animate the image with LivePortrait.
- **You need tight parametric control over specific expressions.** Use a FLAME-based pipeline or an ARKit-driven parametric rig.
- **You need 3D compositing, novel views, or physical lighting.** Use a 3DGS avatar pipeline.
- **You need the absolute best aesthetic quality for a specific stylized character.** Use a hand-rigged Live2D model driven by ARKit tracking.
- **You are building a VTubing product for professional creators.** The aesthetic objections to LivePortrait output are real in this community and will cost you users.

## Implications for the Rest of the Landscape

Neural deformation's existence as a working paradigm has a few structural implications worth stating explicitly, because they inform the rest of this review.

**FLAME is not architecturally necessary for animation.** The fact that LivePortrait produces high-quality real-time face animation with no 3DMM, no FLAME, and no explicit face geometry anywhere in its pipeline is proof that the parametric paradigm is not the only way to solve the problem. Chapter 08 will return to this point when discussing whether to use FLAME internally in a diffusion pipeline — and the answer, based partly on LivePortrait's existence, is "only if you need the properties that FLAME specifically provides."

**The VTubing world is quietly bifurcating.** Professional VTubers with character brands are staying on hand-rigged Live2D and will continue to do so. Casual users who want to "stream as a photo" or "stream as a generated image" are drifting toward LivePortrait-based tools. The two populations rarely meet, and the tooling landscapes for each are diverging.

**Neural deformation is a composable building block.** Because the source-in, driver-in, output-out API is simple, LivePortrait fits naturally into larger pipelines. Generate an image with Stable Diffusion, animate it with LivePortrait. Extract a face from a video, stylize it with a diffusion model, re-animate the stylized result with LivePortrait. The composability is high, and the method is being used as a "final-stage animator" in many pipelines even when the upstream stages use entirely different representations.

**Implicit keypoints are the fifth major face representation.** Alongside Live2D parameters, ARKit blendshapes, MediaPipe landmarks, and FLAME coefficients, LivePortrait's implicit keypoint tensor is now one of the common representations that researchers and engineers need to know about. Unlike the others, it is not at the API boundary — the tensor is internal — but it is the representation that the tooling operates on, and anyone extending LivePortrait or building on its weights needs to understand it.

## Summary

Neural deformation methods — the FOMM lineage, with LivePortrait and its variants as the 2026 production implementation — solve the face animation problem by warping a source image to match a driving motion via learned implicit keypoints and a neural warp-plus-decode generator, without committing to any parametric face representation. The approach is fast (12.8 ms/frame on an RTX 4090), robust across image styles (photographs, illustrations, animals), trivially simple to integrate, and requires no rigging or preprocessing. It excels at "animate this specific image" tasks and fails at "generate a new identity" or "provide tight parametric control" tasks. It is philosophically complementary to the parametric paradigms of Live2D, ARKit, and FLAME rather than a replacement for them, and the right production architecture often uses both: a parametric pipeline for identity and generation, a neural deformation layer for final animation. The paradigm is also a useful reminder that FLAME and 3DMMs are not architecturally necessary for face animation — they are one successful solution among several, and the others are worth knowing about. The next chapter turns to audio-driven talking head methods, which sit at the intersection of the neural deformation paradigm and a separate tradition of audio-driven lip synchronization.

## References

[1] Siarohin, A., Lathuilière, S., Tulyakov, S., Ricci, E., Sebe, N. "First Order Motion Model for Image Animation." NeurIPS 2019. The paradigm ancestor.

[2] Guo, J. et al. "LivePortrait: Efficient Portrait Animation with Stitching and Retargeting Control." arXiv:2407.03168, 2024. Kwai VGI. Code at `github.com/KwaiVGI/LivePortrait`.

[3] LivePortrait project page. `liveportrait.github.io`. Demos, videos, and links to downstream tools.

[4] warmshao. "FasterLivePortrait." `github.com/warmshao/FasterLivePortrait`. ONNX/TensorRT-optimized version. MIT.

[5] "MobilePortrait: Real-Time One-Shot Neural Head Avatars on Mobile Devices." CVPR 2025. arXiv:2407.05712. Note: FPS figures depend heavily on the GFLOP configuration — the paper's headline claims span roughly 63 FPS on iPhone 14 Pro at 16 GFLOPs up to ~169 FPS at lighter (4-7 GFLOP) configurations.

[6] Xie, Y., Xu, H., Song, G., Wang, C., Shi, Y., Luo, L. "X-Portrait: Expressive Portrait Animation with Hierarchical Motion Attention." SIGGRAPH 2024. ByteDance. arXiv:2403.15931. Built on a pretrained diffusion backbone with ControlNet-style conditioning; not a pure warp-and-decode pipeline.

[7] "Follow-Your-Emoji: Fine-Controllable and Expressive Freestyle Portrait Animation." SIGGRAPH Asia 2024. arXiv:2406.01900.

[8] "MegActor: Harness the Power of Raw Video for Vivid Portrait Animation." Megvii, arXiv:2405.20851, May 2024. MegActor-Σ extension: arXiv:2408.14975.

[9] yoyo-nb. "Thin-Plate-Spline-Motion-Model." CVPR 2022. `github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model`.

[10] neosun100. "PersonaLive" (LivePortrait wrapper, unrelated to the research paper below). `github.com/neosun100/PersonaLive`.

[11] Viggle AI. "Viggle LIVE." `viggle.ai/viggle-live`.

[12] "IM-Animation: An Implicit Motion Representation for Identity-Preserving Portrait Animation." arXiv:2602.07498, February 2026. Compact implicit motion encoder with temporal retargeting module and three-stage training to decouple identity and motion.

[13] "FG-Portrait: 3D Flow Guided Editable Portrait Animation." CVPR 2026. arXiv:2603.23381. Extends portrait animation with 3D optical flow guidance for better large-rotation handling and editability.

[14] "PersonaLive! Expressive Portrait Image Animation for Live Streaming." arXiv:2512.11253, December 2025. Code: `github.com/GVCLab/PersonaLive`. Weights: `huggingface.co/huaichang/PersonaLive`. Project page: `personalive.app`. Streamable diffusion framework for infinite-length portrait animation, 12 GB VRAM, ~2x TensorRT speedup. CVPR 2026 acceptance claim circulates in secondary sources but was not corroborated against the official CVPR 2026 program page on 2026-04-14; treat venue as arXiv-only. **Distinct from the LivePortrait-wrapper project of the same name in reference [10].**

[16] "Motion Manipulation via Unsupervised Keypoint Positioning in Face Animation" (MMFA). arXiv:2603.04302, March 2026. Face animation method representing the face via unsupervised 3D keypoints to enable arbitrary pose rotation/translation and motion-attribute editing. The authors acknowledge that expression deformation is coupled with facial scaling in their design, which limits accurate isolated expression manipulation. No code reported in the evidence. Conceptually in the implicit-keypoint / FOMM lineage despite not citing First-Order or LivePortrait directly in available excerpts.

[17] "Let Your Image Move with Your Motion! — Implicit Multi-Object Multi-Motion Transfer" (FlexiMMT). arXiv:2603.01000. Code: `github.com/Ethan-Li123/FlexiMMT` — repository self-identifies as "[CVPR 2026]" but the official CVPR 2026 program was not independently checked on 2026-04-14. Introduces Motion-Decoupled Mask Attention (per-object attention constraint) and Differentiated Mask Propagation (propagates derived object masks across frames) for compositional video generation. Not face-specific, but relevant to the motion-transfer family as a multi-object generalization.

[15] "Durian: Dual Reference Image-Guided Portrait Animation with Attribute Transfer." arXiv:2509.04434, September 2025. Uses LivePortrait among baselines; bridges portrait animation and image attribute transfer methods.

See also `portrait-to-live2d/docs/research/2026-04-05-liveportrait-deep-dive.md` for the detailed architectural analysis of LivePortrait's motion tensor and the PowerHouseMan slider reverse-engineering, and `portrait-to-live2d/docs/research/2026-04-03-realtime-portrait-animation-vtubing.md` for the comparative survey of real-time portrait animation methods that feeds into this chapter's LivePortrait-versus-parametric framing.
