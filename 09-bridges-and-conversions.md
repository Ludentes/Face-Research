# Chapter 09 — Bridges: Conversions Between Representations

## The Pattern

Every real face animation system uses more than one representation. A VTuber rig exposes ARKit blendshapes at its input boundary and Live2D parameters at its animation core. A research talking-head pipeline accepts audio input and produces FLAME-driven 3DGS output. A data visualization tool starts with a text embedding, projects into ArcFace space, generates through a diffusion model, and serves the resulting image statically. These systems work because there is a bridge at every boundary — a converter that maps one representation into another at acceptable cost and quality.

This chapter catalogs the bridges. It is the most practically useful chapter in the review for anyone building a face animation system, because architectural decisions about which representations to use internally and which to expose externally depend on knowing which bridges exist, how expensive they are, and where they break down. The observation that motivates the chapter is that the face animation landscape does not have a single dominant representation, and probably never will, because different representations are good at different operations; but the landscape does have a *dense graph of bridges* that let a product builder pick the representation that is best for each operation and route data between them. Knowing the graph is more important than knowing any single representation.

The chapter is organized as a conversion matrix: for each pair of representations, it describes whether a bridge exists, what the bridge is, how much it costs, and what its limitations are. The bridges vary along three dimensions: **availability** (is there public code that does this, or does someone need to build it), **cost** (compute time per conversion, ranging from one millisecond to one hour), and **quality loss** (does the conversion preserve the information faithfully, or does it degrade the representation).

## The Primary Representations

For reference, the representations that appear in the conversion matrix:

1. **Live2D parameters** — per-rig named scalar parameters, ~20-130 per rig
2. **ARKit 52 blendshapes** — standardized named parameter set, `[0, 1]` bounded
3. **MediaPipe 468 landmarks** — 3D landmark positions in image space
4. **FLAME shape PCA (β)** — 300-dim or 100-dim truncated
5. **FLAME expression PCA (ψ)** — 100-dim or 50-dim truncated
6. **FLAME pose parameters** — explicit rotation/translation
7. **ArcFace 512-d identity embedding**
8. **CLIP image embedding** — face-specific variants
9. **StyleGAN W / W+ latent** — 512-d or 18 × 512-d
10. **Diffusion h-space activation** — UNet bottleneck, model-specific dimensionality
11. **LivePortrait motion tensor** — K × 3 implicit keypoints plus rotation/expression/translation/scale
12. **3DGS avatar parameters** — per-identity set of learned Gaussians plus FLAME rigging
13. **Raw face image** — RGB pixels

The chapter below organizes bridges by source representation. Not every pair has a direct bridge; some conversions require two or three hops through intermediate representations. The routing through the graph is typically done via ARKit or FLAME, which sit at central nodes in the bridge graph because they were designed to interconnect with many things.

## From Raw Face Image

The face image is the natural starting point for any system with user-facing input, because photographs and video frames are what users provide. Extracting structured representations from images is the first bridge in most pipelines.

**Image → MediaPipe landmarks.** Run MediaPipe Face Mesh. Cost: ~5-20 ms per image on CPU, faster on GPU. Quality: strong for standard face orientations, degrades at extreme angles. Availability: Apache-licensed, free, runs everywhere. This is the fastest path from pixels to any structured face representation, and it is usually the first step in any pipeline starting from an image.

**Image → ARKit blendshapes.** Run MediaPipe Face Mesh with the blendshape output head, or run OpenSeeFace, or use ARKit on an iPhone. Cost: 10-30 ms on CPU, faster on mobile NPU. Quality: strong for the range of expressions that the fifty-two can represent, weak outside that range. Availability: public and mature. This is the standard face tracking bridge and is the foundation of the entire VTubing ecosystem.

**Image → FLAME parameters.** Run DECA, EMOCA, or SMIRK. Cost: 100-500 ms per image on GPU, offline for most use cases. Quality: strong for overall shape, moderate for expression with EMOCA, strong for expression with SMIRK. Availability: all three are public with code and weights on GitHub. This is the standard offline "photo to parametric 3D face" pipeline and is used by essentially every FLAME-based generative method as its preprocessing step.

**Image → ArcFace embedding.** Run an ArcFace face recognition network (InsightFace, DeepFace, etc.). Cost: 5-20 ms per image on GPU. Quality: preserves identity information perfectly for face recognition tasks; does not preserve expression or pose. Availability: multiple public implementations, MIT or similar licenses, mature tooling. This is the bridge used by Arc2Face and related methods for identity conditioning.

**Image → CLIP embedding.** Run OpenAI CLIP or a face-specific CLIP variant. Cost: 5-10 ms per image on GPU. Quality: captures semantic/style information about the face; loses fine identity details. Availability: OpenAI CLIP is MIT-licensed, face-specific variants are community projects. This is the bridge for IP-Adapter and related style transfer methods.

**Image → StyleGAN latent.** Run a GAN inversion method (pSp, e4e, HyperStyle, ReStyle). Cost: 50-500 ms for direct encoders, multiple seconds for optimization-based inversion. Quality: loses fine details and is bounded by the StyleGAN training distribution. Availability: several public implementations exist but the quality varies. This bridge is less widely used in 2026 than it was in 2022-2023 because StyleGAN has largely been displaced by diffusion.

**Image → diffusion h-space.** Run the diffusion model forward on the image with DDIM inversion. Cost: 1-5 seconds for DDIM inversion with typical step counts. Quality: preserves the image exactly (the inversion is reconstructible), but the h-space location it produces is specific to the chosen denoising timestep. Availability: inversion code exists for major diffusion models. This bridge is used by h-space direction-finding methods to encode a target image into editable latent coordinates.

**Image → 3DGS avatar.** Run AniGS (single image), Arc2Avatar (single image via synthetic views), or one of the multi-view capture methods (GaussianAvatars, FlashAvatar). Cost: 2 minutes to 2 hours depending on method and input. Quality: strong for multi-view, moderate for single-image. Availability: public code exists for most methods. This is the slowest bridge in the chapter and is the main cost center for any 3DGS-based pipeline.

**Image → LivePortrait motion state.** Run LivePortrait's Appearance Extractor and Motion Extractor. Cost: 20-50 ms per image. Quality: captures motion state implicitly; the representation is not interpretable as named parameters but is sufficient for driving the LivePortrait warp. Availability: MIT-licensed, public. This bridge is internal to LivePortrait's pipeline.

## From ARKit Blendshapes

ARKit blendshapes sit at a central node in the bridge graph because they are the production API standard. Most other representations have paths from ARKit.

**ARKit → Live2D parameters.** Direct assignment when the Live2D rig is authored with ARKit-compatible parameters (HaiMeng, Textoon-compatible rigs), otherwise a manual mapping step configured in VTube Studio. Cost: zero for direct assignment, one-time authoring cost for manual mapping. Quality: direct assignment is lossless; manual mapping is lossy in proportion to the rigger's care. Availability: ARKit parameter sets are supported in any recent Live2D tool.

**ARKit → FLAME expression.** Run a least-squares solver. The `PeizhiYan/mediapipe-blendshapes-to-flame` library does exactly this. Cost: ~1 ms per frame on CPU. Quality: good for the range of expressions both representations can cover, lossy outside that range. Availability: public Python library, simple API. This is the critical bridge that lets FLAME-based tools consume ARKit input and vice versa.

**ARKit → MetaHuman face rig.** Direct assignment via Live Link Face. Cost: zero (Live Link streams blendshape data at 60 Hz to MetaHuman). Quality: lossless at the parameter level; the MetaHuman rig applies its own interpretation of the parameters internally. Availability: Epic Games, free with Unreal Engine. This is the canonical "intended" use of ARKit blendshapes.

**ARKit → VRM / VRChat.** Direct assignment for VRM models authored with ARKit parameters. Cost: zero. Quality: lossless. Availability: native in VRM spec.

**ARKit → 3DGS avatar.** Via ARKit → FLAME bridge, then FLAME driving the 3DGS mesh. Cost: ~1 ms per frame for the solver plus the 3DGS rendering cost. Quality: same as FLAME bridge. Availability: works with any FLAME-rigged 3DGS avatar.

**ARKit → diffusion generation.** No direct bridge as of early 2026. Must go via ARKit → FLAME → FLAME-conditioned diffusion (RigFace, Arc2Face + expression adapter). Cost: 1 ms solver plus 1-2 seconds diffusion. Quality: FLAME bridge loss plus diffusion generation quality. Availability: composition of existing tools. This is the bridge that would benefit from a direct "ARKit-conditioned diffusion" method; no such method has been published yet.

**ARKit → LivePortrait sliders.** Indirect via the PowerHouseMan slider mapping, which is not designed to accept ARKit input directly but can be driven from a subset of ARKit parameters with manual mapping. Cost: one-time manual authoring. Quality: approximate. Availability: community-maintained.

## From FLAME

FLAME is the other central node in the bridge graph, serving as the internal representation for most research-grade face models.

**FLAME expression → ARKit blendshapes.** Inverse of the solver bridge above. Cost: ~1 ms per frame. Quality: same as forward direction (good for overlapping expressive range). Availability: requires the inverse pseudo-inverse matrix, easy to compute from the FLAME basis.

**FLAME → raw mesh.** Run the FLAME generator function. Cost: ~12 ms per generation on GPU, batchable. Quality: exact within the FLAME parameter space. Availability: FLAME PyTorch and TensorFlow implementations are public. This is the trivial bridge that FLAME supports natively — it is what FLAME *is*.

**FLAME → 3DGS avatar.** Pre-existing avatar: FLAME driving the attached Gaussians. Cost: fast rendering (100+ FPS). Quality: strong when the avatar was trained for the FLAME configuration. Availability: GaussianAvatars, 3D Gaussian Blendshapes, etc. This is the bridge that makes 3DGS avatars animatable.

**FLAME → diffusion-conditioned image.** Via RigFace, Arc2Face + expression adapter, MorphFace, or Multimodal 3D Face Geometry. Cost: 1-2 seconds per image. Quality: state of the art for parametric face editing. Availability: Arc2Face has public code and weights; RigFace has weights-only (HF `mengtingwei/rigface`, Apache-2.0), no inference code — see Chapter 08.

**FLAME → UV-mapped raw render.** Apply a UV texture map and render via any standard 3D pipeline (PyTorch3D, OpenGL, Blender). Cost: ~10-50 ms per render. Quality: low (early 2000s game quality), but sufficient for mesh visualization and for producing conditioning inputs for diffusion methods that expect rendered images.

**FLAME → SMPL-X face component.** Direct substitution (SMPL-X's face *is* FLAME). Cost: zero. Quality: lossless.

## From MediaPipe Landmarks

MediaPipe landmarks are a geometric representation in image space, and their bridges are mostly to other geometric representations or to ARKit (via the companion blendshape output).

**MediaPipe landmarks → ARKit blendshapes.** Run MediaPipe's blendshape head or OpenSeeFace's landmark-to-blendshape regression. Cost: 2-5 ms per frame. Quality: moderate — the landmark-to-blendshape mapping is learned and has inherent noise. Availability: public.

**MediaPipe landmarks → face crop.** Compute the bounding box from the landmark extremes. Cost: trivial. Quality: exact. Availability: native. This is the standard preprocessing step for any downstream face model that expects a tight face crop.

**MediaPipe landmarks → face alignment.** Apply affine transformation based on specific landmark positions (typically eye centers and mouth center) to produce a canonically-aligned face image. Cost: trivial. Quality: exact. Availability: standard. This is the preprocessing step for ArcFace and most face recognition and generation models.

**MediaPipe landmarks → ControlNet conditioning image.** Rasterize the landmarks into a 2D image (connected lines, filled face mesh, etc.) and feed into a face-trained ControlNet. Cost: trivial rasterization plus diffusion generation time. Quality: depends on the ControlNet. Availability: standard.

**MediaPipe landmarks → FLAME.** No direct bridge — go via MediaPipe landmarks → blendshape head → FLAME solver. Cost: 2-5 ms + 1 ms = ~5 ms total. Quality: compounded losses from both bridges. Availability: via the chain.

## From Neural Deformation (LivePortrait)

LivePortrait's internal representations (implicit keypoints, motion tensor, appearance features) are specific to the LivePortrait architecture and do not have clean bridges to external representations. The practical bridges are mostly *out from* LivePortrait's rendered output rather than *from* its internal state.

**LivePortrait output image → any image-starting bridge.** Run the LivePortrait pipeline and then apply any of the "from raw face image" bridges to the output. Cost: 12-30 ms for LivePortrait + the image-side bridge cost. Quality: depends on LivePortrait fidelity plus the image-side bridge. Availability: composable.

**LivePortrait slider position → PowerHouseMan slider interpretation → motion tensor.** Via the community-reverse-engineered slider mapping. Cost: microseconds. Quality: approximate (the sliders were hand-tuned post hoc). Availability: ComfyUI-AdvancedLivePortrait plugin.

**No direct LivePortrait ↔ FLAME bridge exists.** This is the clearest gap in the bridge graph: LivePortrait's motion representation cannot be directly converted to FLAME parameters or vice versa. If you want to drive a LivePortrait-animated portrait from FLAME parameters, you have to go FLAME → render image → LivePortrait driver input, which is a several-step chain with quality loss at each step. A direct FLAME-to-LivePortrait motion tensor bridge would be valuable but has not been published.

## From ArcFace Embedding

ArcFace embeddings are the production representation for face identity and feed directly into identity-conditioned generation methods.

**ArcFace → generated image (via Arc2Face).** Direct bridge, the primary design of Arc2Face. Cost: 1-2 seconds per image. Quality: strong identity preservation. Availability: public code and weights.

**ArcFace → text description.** No direct bridge. Could be built by training a projection from ArcFace space to a language model's text encoder space, but no standard tool exists.

**ArcFace → ArcFace nearest-neighbor in a face database.** Standard face recognition operation. Cost: depends on database size, milliseconds for small databases. Quality: exact. Availability: standard face recognition tools.

**ArcFace → FLAME shape.** No direct bridge. Could be approximated by running Arc2Face to generate an image, then running DECA/EMOCA/SMIRK to extract FLAME, but this is a multi-step chain with generation overhead.

## From Diffusion Latents (h-space)

Diffusion h-space direction-finding operates within a single diffusion model and does not produce outputs that bridge cleanly to other representations, but it is an internal bridge that is worth noting.

**h-space activation → generated image.** Continue the diffusion sampling process with the activation intervention. Cost: the remaining diffusion sampling time, typically 500 ms to 2 seconds depending on how late in the denoising trajectory the intervention happens. Quality: determined by the direction's quality. Availability: public code for several models.

**Image → h-space activation.** DDIM inversion, as noted above. Cost: 1-5 seconds. Quality: reconstructible.

## From 3DGS Avatar

A fully reconstructed 3DGS avatar is self-contained — it renders via its own pipeline and is driven by FLAME or ARKit parameters. The bridges in and out are:

**3DGS avatar + FLAME parameters → rendered image.** Native rasterization. Cost: 3-15 ms per frame. Quality: state of the art photorealism. Availability: public for most 3DGS avatar methods.

**3DGS avatar + ARKit parameters → rendered image.** Via ARKit → FLAME bridge, then FLAME driving. Cost: ~1 ms solver plus rendering. Quality: same. Availability: direct.

**3DGS avatar → mesh export.** Some methods support exporting the underlying FLAME mesh plus per-vertex appearance data. Cost: trivial. Quality: loses the Gaussian appearance richness; the mesh alone is a degraded representation.

**3DGS avatar → 2D image library (pre-rendered atlas).** Render the avatar at many parameter settings offline and cache the images. Cost: generation time × number of samples, offline. Quality: exact at the cached samples, zero between samples. Availability: trivial. This is a useful pattern for deploying 3DGS quality without requiring 3DGS runtime.

## Bridge Routing and the Central Nodes

Examining the bridges, two nodes stand out as the central hubs through which most routings pass:

**ARKit blendshapes** is the production hub. Most external APIs expect ARKit; most face trackers produce ARKit; most downstream animation consumers accept ARKit. If you are building a system that interoperates with the production ecosystem, ARKit should be your wire protocol and the system's external representation.

**FLAME** is the research and generation hub. Most generation methods condition on FLAME; most 3DGS avatars are rigged on FLAME; most research-grade face extractors produce FLAME. If you are building a system that leverages the research ecosystem for generation or reconstruction quality, FLAME should be your internal representation.

The canonical architecture for a system that combines production interoperability with research-grade quality is: ARKit at the external API boundary, FLAME internally for generation and representation, and a 1 ms solver bridging them. This is what Chapter 03 argued from the ARKit side, and this chapter confirms it from the bridge perspective: the graph structure makes ARKit-FLAME routing essentially free, and routing through other pairs is more expensive and less reliable.

## Bridge Quality and Multi-Hop Degradation

A practical warning: quality degradation compounds when you chain multiple bridges. A pipeline that goes:

`Image → MediaPipe → FLAME → diffusion → output image`

has four bridges, each with its own quality loss. A pipeline that goes:

`ARKit → FLAME → 3DGS avatar → rendered image`

has three bridges. A pipeline that goes:

`Text → ArcFace projection → Arc2Face → generated image → EMOCA → FLAME → 3DGS avatar → rendered image`

has six bridges and will be unusable for any application that requires high fidelity.

The rule of thumb is: minimize the number of bridges the data crosses in any single pipeline, and route through the cleanest available path even if it means using a less favored internal representation. A product that uses ARKit internally throughout is simpler and more reliable than a product that converts ARKit to FLAME to internal format and back, even if the internal format is "better" by some abstract measure.

## Open Bridges That Would Be Valuable

Several bridges do not exist and would be commercially or scientifically useful if built:

**ARKit blendshapes → diffusion conditioning directly.** Trains a diffusion model to accept ARKit blendshape vectors as input conditioning, skipping the FLAME intermediate. Would let production pipelines generate faces from ARKit input without the FLAME solver step. Low-to-medium research effort.

**LivePortrait motion tensor ↔ FLAME parameters.** A bidirectional bridge between LivePortrait's internal motion representation and FLAME parameter space. Would let parametric systems drive LivePortrait and let LivePortrait's output be analyzed in FLAME terms. Medium research effort.

**Text embedding → face identity directly.** A learned mapping from natural language descriptions (as text embeddings from a modern language model) to face identities (as ArcFace or FLAME shape vectors) without the intermediate text-to-image generation. Would enable "describe a person in language, get a specific face identity back" without running diffusion. Medium-to-high research effort; might be limited by the weak relationship between language descriptions and specific face identities.

**Live2D parameter ↔ FLAME expression.** A learned mapping between Live2D expression parameter sets and FLAME expression vectors. Would allow Live2D rigs to be driven by FLAME-based tools and vice versa. Limited value (few pipelines need this specific conversion), but useful for one specific case: porting FLAME-based expressions into Live2D rigs for compatibility.

**Multi-rig Live2D parameter translation.** A learned mapping that transfers animation from one Live2D rig to another (different parameter sets, different rigging styles). Would let riggers reuse animation across characters. Low-to-medium research effort.

## Summary

The face animation landscape does not have a single dominant representation, but it has a dense graph of bridges between representations that let practitioners pick the right representation for each operation and route data between them at low cost. The two central hubs in the bridge graph are ARKit blendshapes (the production API standard) and FLAME (the research substrate), connected by a 1 ms least-squares solver. Most other representations have clean bridges to one or both of these. The architectural implication for product builders is: use ARKit as the external API, FLAME internally for any generation or reconstruction component, and the solver to route between them. Minimize the number of bridges any single data flow crosses, because quality degrades multiplicatively. Several potentially valuable bridges do not yet exist (direct ARKit→diffusion, LivePortrait↔FLAME, text→ArcFace) and would be useful research contributions. The next chapter folds this bridge knowledge into explicit decision trees organized by use case.

## References

The ARKit↔FLAME bridge library: Yan, P. `github.com/PeizhiYan/mediapipe-blendshapes-to-flame`. Maps MediaPipe/ARKit blendshape scores to FLAME expression coefficients via least-squares.

StyleGAN inversion methods: Richardson et al. "pSp: Encoding in Style" CVPR 2021; Tov et al. "Designing an Encoder for StyleGAN Image Manipulation" (e4e), SIGGRAPH 2021; Alaluf et al. "HyperStyle" CVPR 2022; Alaluf et al. "ReStyle" ICCV 2021.

DDIM inversion for diffusion: Song, Meng, Ermon. "Denoising Diffusion Implicit Models." ICLR 2021. The original DDIM paper; inversion is straightforward for deterministic DDIM sampling.

This chapter's bridge matrix is the synthesis of the Live2D, ARKit, FLAME, neural deformation, 3DGS, and diffusion chapters. For primary-source documentation of each bridge, consult the relevant chapter and its references.
