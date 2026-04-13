# Chapter 01 — A Taxonomy of Face Representations

## Why Taxonomy First

Most of the confusion in this field reduces to people using the same word to mean different things, or using different words to mean the same thing. "Blendshape" is the worst offender — it variously refers to Apple's 52 ARKit parameters, FLAME's 100 PCA expression components, 3D Gaussian Blendshape Gaussian offsets, a handful of Live2D mouth parameters, or the generic linear-combination-of-target-shapes idea that goes back to 1970s computer animation. "Landmark," "keypoint," "anchor," "embedding," and "latent" are all similarly overloaded. Before the rest of this review can proceed, we need shared vocabulary.

This chapter establishes that vocabulary by organizing face representations along three axes — dimensionality, explicitness, and authoring origin — and placing every representation used later in the review within that three-axis space. The classification is not the only possible one, but it is the one that will make subsequent chapters coherent. The reader who finds this chapter pedantic can skim the summary table at the end; the reader who is confused about why the field is so hard should read carefully.

## Axis One: Dimensionality — 2D, 2.5D, 3D

The first axis is the straightforward question of how many spatial dimensions the representation commits to. It is not the most important axis but it is the most obvious and serves as a first cut.

**2D representations** model a face as a flat image or as structures living in image-plane coordinates. Live2D is the paradigmatic 2D representation: a face is a layered stack of illustrated sprites, each deformable by a 2D mesh, controlled by named parameters that move vertices within the image plane. MediaPipe's 2D landmark output (the `face_landmarks` variant that returns `(x, y)` pixel coordinates) is 2D. Warping-based neural methods that operate directly in pixel space without reconstructing an underlying 3D model — first-order motion models, many earlier talking-head methods — are 2D. StyleGAN's image output is 2D, though its internal latent spaces encode 3D-ish content.

2D representations have an important practical advantage: they commit to no 3D structure, and therefore they never suffer from 3D fitting failures, topology mismatches, or reconstruction errors. They have a symmetric disadvantage: they cannot synthesize novel views, they cannot compose with 3D scene content, and they cannot represent head rotations faithfully without cheating (Live2D fakes head rotation by layered 2D deformations that are plausible only for small angles).

**2.5D representations** are a slightly fuzzy category that I use for methods that compute depth or surface normals but do not commit to a full topology or explicit mesh. The MediaPipe Face Mesh with its 468 `(x, y, z)` landmarks is 2.5D — the z-coordinates are real and useful, but the landmarks form a fixed pre-defined triangulation rather than a morphable model. Depth-augmented warping methods like Face2Face (Thies et al., 2016, pre-FLAME) are 2.5D. Some portrait animation methods infer depth as an intermediate signal and use it to improve warping without ever forming an explicit 3D head.

The 2.5D category is worth naming because it contains some of the most practically useful representations in production. MediaPipe Face Mesh is 2.5D and is the workhorse of countless AR filter applications, Snapchat-style effects, and face tracking pipelines. The representation is strong enough to support useful applications without incurring the complexity of full 3D morphable modeling.

**3D representations** commit to a full three-dimensional model of the face surface, usually as a triangulated mesh with explicit vertices, or as a volumetric field, or as a point cloud, or as a cloud of learned 3D Gaussians. FLAME is 3D. BFM (Basel Face Model) is 3D. DECA, EMOCA, and SMIRK all output FLAME-shaped 3D meshes. GaussianAvatars and HeadStudio produce 3D Gaussian clouds. NeRF-based avatars produce volumetric radiance fields that are 3D though not mesh-based. The defining property is that the representation can in principle be rendered from an arbitrary viewpoint.

The 2D versus 3D distinction matters because it determines whether a method can handle the tasks that require novel-view synthesis: VR avatars, 3D scene compositing, arbitrary-angle rendering for games, or just animating a portrait through a large head rotation. For many applications — especially anime-style VTubing — the 2D limitation is acceptable because the content stays roughly front-facing. For other applications — 3D VR, spatial computing, large-angle rotation — it is not.

## Axis Two: Explicitness — Explicit, Implicit, Hybrid

The second axis cuts across dimensionality and is in many ways more important. It asks: does the representation explicitly encode face structure as named, interpretable parameters, or does it encode face structure implicitly in the weights of a neural network?

**Explicit representations** expose face structure as a vector of parameters with known semantic meaning. ARKit's 52 blendshapes are maximally explicit: each parameter has a name (`eyeBlinkLeft`, `mouthOpenY`, `jawForward`), a fixed range (`[0, 1]`), and a known effect on the face. Live2D parameters are explicit. FLAME's shape PCA is somewhat explicit (the components have *statistical* interpretability — PC1 is the largest variance mode in the training data — but not *semantic* interpretability; no one can tell you in advance what PC7 will do). FLAME's pose parameters are fully explicit (jaw rotation, neck rotation). FLAME's expression PCA is statistical but not semantic.

The key property of explicit representations is that they support *compositional editing*: if you want to change the expression without touching identity, you edit the expression parameters and leave the identity parameters alone. This is the promise that ARKit's blendshapes and FLAME's orthogonal PCA spaces deliver. You can sweep expression continuously, you can blend two expressions linearly, you can extract an expression from one face and apply it to another. The representation gives you an algebra.

**Implicit representations** encode face structure in neural network weights or activations. StyleGAN's W-space and W+ space are implicit: they are high-dimensional latent vectors that produce convincing faces through a trained generator, but the coordinates of W-space are not named, and editing in W-space requires discovering *directions* — learned vectors in W-space that correspond to semantic changes — rather than editing named parameters. Diffusion model bottleneck activations (the h-space of Haas et al., 2024) are implicit. LivePortrait's "implicit keypoints" are an unusual case: they are 3D points in space that exist for motion transfer, but their semantics are learned rather than authored, hence "implicit" in the method's own terminology.

The key property of implicit representations is that they can capture *fine-grained detail* that explicit parameterizations cannot. FLAME's 100-component expression PCA cannot represent a particular asymmetric smirk; a StyleGAN latent vector or a diffusion h-space activation can. The cost is interpretability: editing is done via learned directions, not by setting named sliders.

**Hybrid representations** combine explicit and implicit components. GaussianAvatars are a clean example: the motion is explicit (FLAME mesh deformations drive the positions of attached Gaussians), but the rendering content is implicit (the Gaussians themselves are learned color+opacity+scale blobs). RigFace is hybrid: input conditioning is explicit (FLAME expression coefficients, pose parameters, lighting SH coefficients) but the generation is implicit (the entire SD UNet). Arc2Face with its expression adapter is hybrid: identity is implicit (ArcFace embedding vector) and expression is explicit (FLAME blendshape coefficients via SMIRK). Most of the interesting recent research is hybrid — the pattern is to use explicit parameters for the axes you want to control and implicit representations for everything else.

The explicit/implicit axis is where the field's future is being fought. Pure explicit models (Live2D, FLAME mesh alone) cannot reach photorealism; pure implicit models (early GANs, raw diffusion) cannot reach fine-grained parametric control. Hybrid wins. The open question is *how* to combine the two, and that is the question Chapters 07 and 08 address at length.

## Axis Three: Authoring Origin — Hand-Authored, Statistical, Learned

The third axis asks where the representation's structure came from.

**Hand-authored representations** were designed by human engineers or artists. ARKit's 52 blendshapes are hand-authored — Apple engineers picked 52 face deformations that they judged semantically meaningful and bounded them to `[0, 1]`. Live2D parameters are hand-authored per-character by the rigger. VRM's standard expression set is hand-authored. Classic keyframe animation is hand-authored. The defining property is that the representation has *a priori semantic meaning* — somebody thought about what each parameter should mean and committed to it.

**Statistical representations** are derived from a dataset by a classical (non-deep-learning) statistical procedure. FLAME's shape PCA is statistical: the 300 components are principal components of 3,800 neutral 3D head scans, so the basis is optimal in a linear-algebra sense but not designed for semantic interpretability. BFM is statistical. Classical 3DMM shape bases are statistical. Statistical representations are orthogonal by construction, which is why they support compositional editing, but they are limited by the linear assumption — a linear PCA basis cannot capture nonlinear shape variation.

**Learned representations** are the output of deep neural network training on some objective. StyleGAN's W-space is learned: the structure of W-space emerges from adversarial training, not from any explicit design. Diffusion h-space is learned. The features in EMOCA's expression encoder are learned. LivePortrait's implicit keypoints are learned. Most modern representations fall here. They capture nonlinear variation well and are not restricted by linear-algebra assumptions, but their internal structure is opaque and has to be *discovered* after the fact via direction-finding methods.

The three origins correspond roughly to three eras: hand-authored is the animation-industry tradition from the 1970s through 2010s; statistical is the classical 3DMM tradition from Blanz and Vetter 1999 through FLAME 2017; learned is the deep-learning tradition from 2014 onward. In 2026 all three coexist in production, and the choice between them is mostly task-driven rather than era-driven. ARKit's hand-authored blendshapes remain the production standard precisely because their semantic legibility makes them easy to integrate into tooling — a designer can look at `jawOpen = 0.7` and know what will happen.

## Placing the Representations

With the three axes established, we can place the concrete representations the rest of the review will discuss. The following table gives the canonical entry for each:

| Representation | Dimensionality | Explicit/Implicit | Origin | Primary Use |
|---|---|---|---|---|
| Live2D parameters | 2D | Explicit | Hand-authored | Anime-style VTubing, indie creators |
| ARKit 52 blendshapes | 2.5D / 3D driving | Explicit | Hand-authored | Face capture, VTubing, AR |
| MediaPipe 468 landmarks | 2.5D | Explicit | Hand-authored | AR filters, tracking, face mesh |
| MediaPipe blendshapes | 3D driving | Explicit | Hand-authored (ARKit-aligned) | Landmark→blendshape solving |
| FLAME shape PCA (β, 300 dims) | 3D | Explicit-statistical | Statistical (PCA over 3D scans) | Identity parameterization in research |
| FLAME expression PCA (ψ, 100 dims) | 3D | Explicit-statistical | Statistical (PCA over 4D scans) | Expression parameterization in research |
| FLAME pose (jaw/neck/eye) | 3D | Explicit | Hand-authored | Pose control in FLAME-family models |
| BFM / Basel Face Model | 3D | Explicit-statistical | Statistical (older than FLAME) | Legacy 3DMM research |
| SMPL-X | 3D | Explicit-statistical | Statistical | Full-body model, FLAME is the face component |
| DECA/EMOCA/SMIRK output | 3D | Explicit (FLAME-shaped) | Statistical+learned encoder | Photo→FLAME parameter extraction |
| NeRF head avatar | 3D | Implicit | Learned | Photorealistic volumetric rendering (superseded by 3DGS) |
| 3D Gaussian Splatting head avatar | 3D | Hybrid (motion explicit, appearance implicit) | Learned | Real-time photorealistic rendering |
| 3D Gaussian Blendshapes | 3D | Hybrid | Learned, ARKit-compatible blending | Blendshape-driven photorealistic avatars |
| StyleGAN W / W+ space | 2D output, 3D-encoding | Implicit | Learned (adversarial) | GAN-based portrait generation and editing |
| Stable Diffusion text latent | 2D output | Implicit | Learned | Text-to-image, foundation for editing methods |
| Diffusion h-space | 2D output, hidden | Implicit | Learned | Direction-finding for semantic editing |
| ArcFace identity embedding (512-d) | — | Implicit | Learned (face recognition) | Identity encoding for generation |
| CLIP image embedding | — | Implicit | Learned (contrastive) | Style transfer, IP-Adapter conditioning |
| LivePortrait implicit keypoints | 3D | Implicit (despite the name) | Learned | Motion transfer, portrait animation |
| LoRA-based Concept Sliders | 2D output | Hybrid (sliders are explicit axes, mechanism is learned) | Learned | Compositional direction-finding in diffusion |

The table has one subtlety worth calling out: ARKit's blendshapes are *both* hand-authored and explicit, and they are also *production-standard*. No other representation in the table combines all three properties as cleanly. This is why Chapter 03 will argue that ARKit occupies a uniquely load-bearing position in the ecosystem, even though it is not the most powerful or the most photorealistic or the most flexible representation in any individual sense.

## Operations: What You Can Do With a Representation

A representation is only as useful as the operations it supports. The operations that matter for face animation and generation are:

1. **Extract** from a photo: given an image, recover the representation. DECA/EMOCA/SMIRK extract FLAME parameters; MediaPipe extracts landmarks and blendshapes; ArcFace extracts identity embeddings; there is no standard extractor from arbitrary photos into Live2D parameters (this is part of why Live2D rigging is hand-authored).

2. **Render** back to image: given the representation, produce a face image. Raw FLAME meshes render to gray mannequins; neural renderers (GaussianAvatars, diffusion models) render to photorealistic images; Live2D parameters render via the Cubism engine to stylized 2D frames.

3. **Edit** by modifying parameters: given the representation, change some aspect (expression, pose, identity, lighting) and render the edited version. Explicit representations natively support this; implicit representations support it via direction-finding.

4. **Interpolate** between two instances: given two representations, produce intermediate versions. Explicit representations support linear interpolation directly; implicit representations support it via their learned latent structure (though the interpolations may not be semantically meaningful).

5. **Compose** with other representations: given two representations of the same type, combine them (e.g., identity from one, expression from another). Orthogonally factored representations (Arc2Face + FLAME expression, FLAME shape + expression) support this cleanly; entangled representations do not.

6. **Drive in real time** by tracking input: given a live face-tracking stream (ARKit, MediaPipe, OpenSeeFace), produce a continuously updating rendered output. This is the VTubing loop, and the representations that support it well (Live2D, 3D Gaussian Blendshapes, LivePortrait) are the ones with fast rendering and a direct mapping from ARKit-style tracking data.

Different representations support these operations at very different levels of maturity. A full matrix of operation-by-representation support is one of the core deliverables of this review, and will appear in Chapter 10 as the substrate for the decision trees. A preview:

| Operation | Live2D | ARKit blend. | FLAME | 3DGS avatar | StyleGAN W | Diffusion+FLAME | LivePortrait |
|---|---|---|---|---|---|---|---|
| Extract from photo | — | — (real-time capture only) | strong | needs video | weak (inversion) | strong | n/a (motion only) |
| Render to image | native | — (driving signal only) | mannequin | photorealistic | photorealistic | photorealistic | photorealistic |
| Edit by parameters | strong | strong | strong | strong | via directions | strong | weak |
| Interpolate | strong | strong | strong | strong | strong | strong | n/a |
| Compose identity+expression | strong | n/a | strong | strong | weak (entangled) | strong | via driving video |
| Real-time driving | strong | native | ~1ms solve to FLAME | strong (post-build) | n/a | no (offline) | strong |

This table contains several of the central tensions of the field. FLAME has almost everything except a native renderer. StyleGAN has almost everything except clean composition. LivePortrait has almost everything except parameter-based editing. The sensible move in 2026 is to combine representations: use one for each operation where it excels and bridge between them at the points where their strengths meet.

## A Canonical Example: What Representation Is This Face?

To make the taxonomy concrete, consider a single face. Suppose you have a photo of a person smiling. Different methods see it as different things:

- **OpenSeeFace / VTube Studio** sees 66 2D facial landmarks plus gaze direction plus some ARKit-like blendshape scores. The face is a stream of scalar values, refreshed 30-60 times per second, that drive a rigged Live2D character.
- **ARKit (iPhone TrueDepth)** sees 52 named blendshape scores plus a head pose. The face is those 52 values, refreshed at 60 Hz, used to drive whatever downstream consumer wants them.
- **MediaPipe Face Mesh** sees 468 3D landmarks, optionally with 52 ARKit-compatible blendshape scores computed from them. The face is either the landmarks, the blendshapes, or both.
- **DECA / EMOCA** sees FLAME parameters: a 100-dimensional shape vector, a 50-dimensional expression vector, jaw/neck/eye pose, a camera transform, and a texture map. The face is a full 3D reconstruction.
- **SMIRK** sees the same FLAME parameters but with better expression accuracy, especially for asymmetric or extreme expressions.
- **ArcFace** sees a 512-dimensional identity embedding. The face is a point in face-recognition space; the smile is discarded as nuisance variation.
- **CLIP** sees a semantic-visual embedding. The face is a point in a space where "happy face" and the image are close.
- **StyleGAN encoder** sees a point in W+ space (18 × 512 dimensions for StyleGAN2-FFHQ). The face is a latent vector.
- **Arc2Avatar** sees an ArcFace embedding plus a partially reconstructed 3DGS avatar that can be driven by FLAME parameters.
- **LivePortrait** sees a source image plus implicit keypoints plus an appearance feature map. The face is prepared to be warped toward a driving video.
- **RigFace's Identity Encoder** sees a set of self-attention features extracted from the image via a second copy of an SD UNet. The face is a multi-level feature pyramid.
- **Live2D Cubism Editor** doesn't see the photo at all — it sees whatever a human artist draws after looking at the photo, plus whatever rigging they hand-author.

Eleven representations, one face. The choice of representation is not neutral — each one privileges different properties, discards others, and makes different downstream tasks easy or impossible. There is no single "correct" representation. There is only the right representation for the task at hand, and the bridges between representations when you want to do more than one thing at once.

## Summary

Face representations in 2026 span three dimensionality tiers (2D, 2.5D, 3D), three explicitness regimes (explicit, implicit, hybrid), and three authoring traditions (hand-authored, statistical, learned). The dominant production representations — ARKit blendshapes, Live2D parameters — are hand-authored and explicit. The dominant research representations — FLAME, StyleGAN W, diffusion latents, 3DGS — are statistical or learned. Hybrid representations combining explicit parametric control with implicit learned rendering dominate recent advances (RigFace, Arc2Face+expression, GaussianAvatars, 3D Gaussian Blendshapes). The practically important operations — extract, render, edit, interpolate, compose, drive-in-real-time — are supported unevenly across representations, and most real systems combine representations to get all six.

The rest of this review walks through the communities and methods that sit at each locus in this taxonomy, starting with Live2D in Chapter 02.
