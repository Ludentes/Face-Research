# Chapter 07 — 3D Gaussian Splatting Avatars: The Real-Time Photorealism Track

## A Rendering Paradigm That Changed the Field

The progression from volumetric neural fields (NeRF) through 3D Gaussian Splatting (3DGS) is the most significant rendering-paradigm shift in neural graphics in the last decade. NeRF, introduced in 2020, produced photorealistic novel-view synthesis by training an MLP to map (position, view direction) to (radiance, density) and then ray-marching through the learned field to produce pixels. The technique was beautiful, general, and slow — early NeRF implementations rendered at 1-10 seconds per frame, and even highly optimized variants (Instant-NGP, KiloNeRF, Plenoxels) rarely crossed 10-30 FPS for avatar-quality outputs. 3D Gaussian Splatting, introduced by Kerbl et al. at SIGGRAPH 2023 [1], replaced the ray-marched MLP with a rasterization-friendly representation: a collection of 3D Gaussian primitives, each with a learned position, covariance, color, and opacity, projected to the screen via a differentiable rasterizer. The representation is explicit, the rendering is fast (a few milliseconds for a full frame), and the quality matches or exceeds NeRF on standard benchmarks. Within eighteen months, 3DGS displaced NeRF in nearly every application domain where real-time rendering mattered, and face avatars were one of the first and most important beneficiaries.

This chapter focuses specifically on how 3D Gaussian Splatting has been applied to the face avatar problem: the architectural patterns, the leading methods, the tradeoffs, and the place 3DGS avatars occupy in the broader landscape. The central observation is that 3DGS avatars bring together two properties that no prior representation offered simultaneously: *real-time photorealistic rendering* (typically 25-370 FPS depending on method and hardware) and *parametric control via blendshape or FLAME driving* (the same ARKit/FLAME signals that drive Live2D rigs and neural renderers). This combination makes 3DGS the current best path for real-time high-quality face avatars, and it is the substrate on which the most ambitious talking-head systems, VTuber research prototypes, and spatial-computing avatar proposals now build.

The trade that 3DGS avatars currently require is that they are *per-identity*: to produce a 3DGS avatar of a specific person, you need a reconstruction pass from multi-view video (or, in more recent methods, a single image with strong priors). This constraint is the subject of active research, and several 2024-2025 papers have started to close the gap between 3DGS avatars and zero-shot identity generation. But as of early 2026, "capture once, render many" is still the dominant workflow for 3DGS face avatars.

## Why 3DGS Won

The technical advantages of 3DGS over NeRF-based methods are numerous, but three matter most for face avatars.

**Rasterization beats ray marching for speed.** NeRF renders pixels by ray-marching through the scene, which requires evaluating the MLP hundreds of times per pixel — on the order of 10^6 MLP evaluations per frame at 512² resolution. 3DGS rasterizes each Gaussian primitive to the screen and composes them with alpha blending, which is a straightforward GPU graphics pipeline operation. The computational gap is large: NeRF avatars rendered at 1-10 FPS on commodity hardware; 3DGS avatars reach hundreds of FPS on the same hardware (up to 370 FPS in the fastest published methods). The gap is the difference between "interactive" and "real-time," and it is the difference between "usable in production" and "research demo."

**Explicit primitives compose with mesh animation.** A NeRF is a continuous field — there is no natural way to "attach" the field to an underlying animation rig. 3DGS primitives are discrete objects with explicit positions and orientations, which means you can attach each Gaussian to a vertex (or a triangle, or a bone) of an animation mesh, and let the mesh deformation carry the Gaussian along. When the mesh moves, the Gaussians move with it. The resulting avatar can be driven by any animation system that operates on the underlying mesh — FLAME parameters, ARKit blendshapes, or explicit vertex deformations — and the rendered output updates at the full 3DGS frame rate. This composability is what makes 3DGS avatars compatible with the parametric animation tradition.

**Per-primitive training is parallel and stable.** Training a 3DGS representation proceeds by gradient descent on the Gaussian parameters independently per primitive, with periodic splitting and pruning based on gradient magnitudes. The training dynamics are more stable than NeRF's (which struggles with floaters, cloud artifacts, and optimization local minima) and converge faster. A typical 3DGS face avatar trains in minutes to an hour on commodity GPUs, compared to hours for a NeRF avatar of comparable quality.

There are also disadvantages — 3DGS is less memory-efficient than NeRF (a full avatar is tens of millions of primitives), the primitives do not naturally interpolate continuously (limiting the smoothness of very close-up rendering), and the rasterization is less physically accurate for certain materials (hair strands, fine fabric). But the practical tradeoffs favor 3DGS decisively for face avatars, and the field has converged on 3DGS as the production path for real-time neural rendering.

## The Canonical Methods

Several 2024 papers established the 3DGS avatar pattern and remain the reference points for subsequent work.

**GaussianAvatars** (Qian et al., CVPR 2024 Highlight) [2] is one of the earliest papers to demonstrate FLAME-rigged 3DGS avatars (arXiv:2312.02069, December 2023), and its architecture is the template for essentially every method that followed. The near-contemporary **PSAvatar** (arXiv:2401.12900, January 2024) independently proposed a similar FLAME + 3DGS pairing, and neither paper cleanly claims priority over the other — the "FLAME-rigged 3DGS" idea converged across multiple groups in late 2023 / early 2024. The approach:

1. Fit a FLAME mesh to multi-view video of the target person using standard photogrammetry and 3DMM fitting.
2. Attach learned 3D Gaussians to the FLAME mesh vertices or triangles. Each Gaussian has a position offset, scale, rotation, color, and opacity, all trained per-primitive.
3. Train the Gaussian parameters to reproduce the input video from the correct camera angles, using photometric loss (reconstruct each frame) and regularization (keep Gaussians attached to their FLAME vertices).
4. At inference, drive the FLAME parameters (from ARKit, from another tracked face, or manually) to move the mesh; the attached Gaussians move along with it; the rasterizer produces the output frame at 100+ FPS.

The key design decision is that the Gaussians' motion is *derived* from the FLAME mesh motion, not learned as a separate component. This is computationally efficient and produces stable results because the motion correctness is inherited from the well-understood FLAME animation. The Gaussian appearance is free to be whatever it needs to be to reproduce the input images, so the system learns fine skin detail, hair highlights, and other appearance that FLAME alone cannot represent.

GaussianAvatars' quality at its best is indistinguishable from real video in controlled conditions — the demo videos on the project page look like footage rather than renders. Quality degrades in the wild (extreme pose, uncontrolled lighting, heavy occlusion) but remains useful across a broad range of conditions.

**SplattingAvatar** (Shao et al., CVPR 2024) [3] takes a slightly different approach, embedding Gaussians on the surface of a triangle mesh rather than attached to vertices. The "mesh embedded" design has some advantages: Gaussians smoothly deform with triangle deformation rather than suffering discretization artifacts at vertex boundaries, and the method is more efficient for certain kinds of avatars. SplattingAvatar is particularly notable for its speed: it achieves 300 FPS on desktop GPUs and 30 FPS on an iPhone 13, making it the most mobile-efficient 3DGS avatar method published as of early 2026. For mobile deployment (AR filters, on-device talking heads, mobile VR), SplattingAvatar is the first method to credibly demonstrate that real-time 3DGS face avatars are possible on phones.

**3D Gaussian Blendshapes** (SIGGRAPH 2024) [4] takes the idea one step further by introducing an explicit blendshape representation directly at the Gaussian level. Each expression blendshape (from FLAME expression components, ARKit blendshapes, or a custom set) is stored as a set of Gaussian offsets — the "how do the Gaussians move when blendshape X fires at strength 1.0" table. At inference, the active blendshape coefficients linearly combine the offset tables, and the Gaussians are displaced accordingly. This architecture is a drop-in for ARKit blendshape driving, which makes the method directly compatible with the production VTuber ecosystem, and it achieves 370 FPS rendering speed — the fastest of the class.

The "3D Gaussian Blendshapes" name deserves attention because it explicitly adopts the blendshape terminology from the ARKit / production animation world and applies it to Gaussian primitives. This reflects the architectural convergence: a rigged 3DGS avatar with per-blendshape Gaussian offsets is, from the outside, a blendshape rig that happens to render via Gaussian splatting instead of triangle rasterization or neural rendering. The driving API is ARKit-compatible, the internals are neural-implicit, and the system bridges the two naturally.

**FlashAvatar** (Xiang et al., CVPR 2024) [5] targets fast reconstruction: it builds a 3DGS avatar from monocular video in a few minutes and then renders at over 300 FPS at 512² on an RTX 3090. The method is among the fastest of its class for monocular input and is suitable for "capture your face in a short video and then stream as that avatar" workflows.

**PSAvatar** and **GaussianHead** (2024) are additional methods in the same family with incremental improvements.

## The Instant-Capture Track

The methods above all require some form of capture pass — multi-view video, monocular video, or at minimum a set of reference images. A parallel line of work targets the "instant from a single image" use case, which is where the 3DGS paradigm meets zero-shot identity generation.

**AniGS** (CVPR 2025) [6] takes a single image and produces an animatable Gaussian avatar. The method uses strong priors (learned from large face datasets) plus an optimization pass to fit the avatar to the single reference. The quality is noticeably below methods with multi-view input, but the workflow is dramatically simpler: upload one photo, receive an animatable avatar. AniGS is the first method in this lineage to make zero-shot-ish 3DGS avatars practical.

**Arc2Avatar** (CVPR 2025) [7] is a particularly interesting method because it solves one of the harder problems in the space: *generating the training set* for a 3DGS avatar from a single reference. The method takes a single portrait, uses Arc2Face (the ArcFace-embedding-conditioned SD model from Chapter 08) to generate many synthetic views of the same identity at different poses and expressions, and then uses the synthetic multi-view data to train a 3DGS avatar with FLAME correspondence. The result is a fully animatable 3DGS avatar that can be driven by FLAME or ARKit parameters, produced from a single input image, with no video capture required.

The architectural significance of Arc2Avatar is that it demonstrates the "identity generation → synthetic views → 3DGS avatar" pipeline works end-to-end. This is the bridge between the diffusion-based generation world (Chapter 08) and the 3DGS rendering world: you can now take an identity embedding (from ArcFace, from a custom projection layer, or from any other source that Arc2Face accepts), generate synthetic reference data, and produce an animatable avatar — without ever capturing video of the target identity.

**HeadStudio** (Zhou et al., ECCV 2024) [8] is the text-to-3DGS-avatar method discussed in Chapter 04. It takes a text description, uses FLAME-based Score Distillation Sampling (F-SDS) to optimize a 3DGS representation against a text prior, and produces a FLAME-rigged avatar that renders at 40+ FPS at 1024² resolution. Generation itself is a multi-hour SDS optimization — far from "instant" — but the output is fully animatable, and the method shows that text is a viable input modality for 3DGS avatar generation if you are willing to wait.

**PrismAvatar** (arXiv:2502.07030, 2025) [9] targets mobile real-time rendering and achieves 60 FPS on iPhone 14 Pro and 4th-gen iPad Pro while maintaining usable quality. Strictly speaking, PrismAvatar is *not* a 3DGS method — its representation is a rigged prism lattice combined with a deformable NeRF distilled to a mesh plus neural textures — but it is mentioned here because it targets the same use case (on-device real-time avatars) and because its deployment story is the best current example of what mobile-targeted neural avatars look like. It is a useful reference for the mobile-rendering push that is coeval with, but architecturally distinct from, mobile 3DGS.

## The Driving Story

The story of 3DGS avatars and their driving signal is the story of how the Gaussian representation connects to the parametric animation world covered in earlier chapters. The connection is tight and intentional:

**FLAME driving.** Because most 3DGS avatar methods attach their Gaussians to a FLAME mesh, driving the avatar is a matter of setting FLAME parameters and re-rendering. A FLAME parameter vector comes from any source — a direct authoring UI, an extractor (DECA/EMOCA/SMIRK) running on a reference image, a solver from ARKit blendshapes, a generation model (HeadStudio for the initial avatar, then manual editing of the parameters for downstream variations) — and the 3DGS avatar responds.

**ARKit blendshape driving.** The 1 ms solver from ARKit to FLAME (Chapter 03) means any ARKit-compatible input drives a FLAME-rigged 3DGS avatar. For 3D Gaussian Blendshapes specifically, the blendshapes can be ARKit-aligned directly without going through FLAME at all. Either way, the upshot is that a 3DGS avatar can be driven by an iPhone running Live Link Face, by a webcam running MediaPipe, or by any other ARKit-producing tracker.

**Real-time capture loop.** The combination of fast tracker (ARKit, 60 FPS) + fast solver (1 ms) + fast renderer (100-370 FPS) means the whole capture-to-render loop runs comfortably at 60 FPS with latency well under 20 ms. For applications that can accept the per-identity capture cost, this is the fastest high-quality face avatar stack currently available.

**Pre-recorded motion driving.** You can also drive the avatar from a pre-recorded animation, a motion-captured performance, or a text-to-motion generation pipeline. The avatar does not care where the FLAME parameters come from; it just renders them.

The driving story is notably clean — cleaner than any other avatar representation in the landscape. Live2D has its own parameter set that requires per-rig mapping; diffusion-based avatars require slow sampling; LivePortrait needs a source image and a driver; 3DGS avatars take parameter vectors and render frames, full stop. This operational simplicity is a major reason 3DGS is the likely platform for the next generation of high-end real-time avatar applications.

## Meta Codec Avatars: The Proprietary Parallel

While the open-source and academic ecosystem has converged on 3DGS with FLAME driving, Meta's Reality Labs has pursued a separate line of research under the name "Codec Avatars" [10]. Codec Avatars are photorealistic face avatars with extremely high fidelity (to the point where they are used in demos to simulate face-to-face conversations in VR), driven by a combination of sparse sensors (eye trackers, mouth cameras) and learned models.

The Codec Avatar architecture uses a combination of neural primitives — Meta has used both volumetric NeRF-adjacent representations and, in more recent work, Gaussian-based representations — with a FACS-adjacent blendshape parameterization and a proprietary capture rig that produces multi-view 4D data. The resulting avatars are in a different quality tier than open-source 3DGS avatars, but the capture infrastructure is not reproducible outside Meta's research labs, and the model weights are not public.

Codec Avatars' relevance for this review is primarily as an existence proof: they demonstrate the ceiling of what real-time photorealistic face avatars can achieve with sufficient engineering investment, and they validate the general architectural pattern (parametric driving + neural rendering + per-identity capture) that the open-source 3DGS work is pursuing. The open-source methods are closing the quality gap gradually, and 3DGS + FLAME + multi-view capture is increasingly producing Codec-Avatar-adjacent results without needing Meta's custom rig.

## What 3DGS Avatars Still Cannot Do

Several limitations of 3DGS avatars are worth being explicit about.

**Per-identity capture (still).** The instant-from-one-image methods (AniGS, Arc2Avatar) have improved the capture workflow dramatically but have not eliminated it. Production-quality avatars still benefit from multi-view video, and the quality gap between "single-image reconstruction" and "multi-view reconstruction" is still large. A commercially deployable product that targets "upload any photo, get a real-time avatar" is not yet possible at the quality tier where users will accept the result as photorealistic; it is possible at a lower quality tier that users might accept as "good enough" for some applications.

**Handling of extreme pose and occlusion.** All 3DGS avatars trained on frontal-to-mid-pose video degrade when rendered from angles or poses that were underrepresented in training. A full profile view, an extreme chin-up angle, or occlusion by hair or hands all produce artifacts. The degradation is gradual — the avatar does not fail catastrophically, it just becomes lower quality — but it is visible enough to limit use in applications that need unconstrained viewing angles.

**Hair, eyes, and mouth interior.** These three regions are consistently the weakest areas of 3DGS avatars. Hair is made of thin strand-like geometry that Gaussians do not represent well. Eyes have subtle specular highlights and geometry that standard 3DGS appearance models do not capture accurately. Mouth interior (teeth, tongue) is often underrepresented in training data because the mouth is usually closed. Specialized variants (separate models for hair, for eyes, for mouth interior) are an active research topic, but most methods handle all three with the same Gaussian primitive, producing compromises.

**Clothing and body.** Avatars that extend below the neck face a harder problem because clothing has complex deformation and dynamics that FLAME does not model. Full-body 3DGS avatars exist (GaussianBody, SMPL-X-rigged 3DGS) but are currently less mature than head-only methods.

**Relighting.** A 3DGS avatar trained under specific lighting conditions produces output that bakes in those lighting conditions. Relighting the avatar under novel lighting — placing it in a scene with different light sources — requires disentangling geometry from appearance in a way that pure 3DGS training does not enforce. Relightable 3DGS avatars are an active research topic (RelightableGaussianAvatars, various proposals) but are not yet at the quality tier of their non-relightable counterparts.

**Cross-identity style transfer.** Taking the motion from one 3DGS avatar and transferring it to another is possible if both are FLAME-rigged, because the FLAME parameters are the driving signal and they are identity-independent. But taking the *appearance* from one avatar and applying it to another's motion is hard, because the Gaussian primitives are per-identity and their appearance properties are entangled with the identity's specific geometry and lighting.

## Locating 3DGS Avatars in the Taxonomy

The three-axis classification:

- **Dimensionality:** 3D. 3DGS avatars have full 3D representation, support novel-view synthesis, and can composite with 3D scene content.
- **Explicitness:** Hybrid. The motion is explicit (FLAME mesh deformation drives the Gaussians), but the appearance is implicit (learned per-Gaussian color, opacity, scale, and orientation). This is the canonical hybrid representation.
- **Authoring origin:** Learned (for the Gaussians themselves) plus statistical (for the FLAME mesh they attach to). The learned component is where most of the appearance quality comes from; the statistical component gives the parametric controllability.

The operations matrix:

| Operation | 3DGS avatar support |
|---|---|
| Extract from photo | Via one-image methods (AniGS, Arc2Avatar) — moderate quality; via multi-view (GaussianAvatars) — high quality |
| Render to image | Native and real-time (100-370 FPS) |
| Edit by parameters | Strong — FLAME or ARKit driving operates as expected |
| Interpolate between instances | Weak at the avatar level (different Gaussian sets); strong at the parameter level (FLAME interpolation drives the single avatar) |
| Compose identity + expression | Strong within a single avatar; cross-avatar identity composition is the open problem |
| Real-time driving | Native, the defining property |

3DGS avatars are the strongest overall representation for real-time high-quality face rendering, and they are the first representation in the landscape to combine photorealistic rendering with clean parametric control at real-time speed. The remaining limitations are around capture (still required) and cross-identity composition (still weak).

## Implications and Where This Is Going

The 12-24 month outlook for 3DGS face avatars has a few concrete elements.

**Mobile deployment will expand dramatically.** SplattingAvatar's 30 FPS on iPhone 13 is a preview of what will be standard by the end of 2026. On-device 3DGS face avatars on flagship phones will reach 60 FPS at 512² resolution, and the AR filter ecosystem that currently uses 2D face tracking will start to integrate 3DGS methods.

**The instant-from-one-image track will mature.** Arc2Avatar's demonstration that synthetic views from a diffusion model can serve as training data for a 3DGS avatar is architecturally important, and the follow-up work will likely close much of the remaining quality gap with multi-view methods. The first practical "upload any photo, get a real-time 3DGS avatar" products will ship within 12 months, targeting casual use cases where the quality bar is below professional broadcasting.

**Live streaming applications will adopt 3DGS over Live2D for high-end broadcasters.** The top tier of VTuber production — currently served by custom proprietary rigs on Unreal Engine — will start to adopt 3DGS avatars as the rendering path, driven by FLAME or ARKit blendshape capture. The Live2D ecosystem will remain dominant for the mid-market and below, but the top of the market will migrate. This is a 24-36 month timeline rather than 12 months.

**Spatial computing and VR will become 3DGS-first.** Apple Vision Pro and the next generation of Meta Quest are both rumored to have native 3DGS capabilities in their development platforms. Face avatars for VR social applications will transition from 2D or simplified 3D representations to 3DGS, and the FLAME-driven 3DGS pattern will be the default architectural choice.

**Full-body 3DGS avatars will mature.** The head-only methods will be extended to full body, and the combination of 3DGS body + SMPL-X parametric rig + audio-driven motion generation will produce the first fully animatable photorealistic full-body avatars from sparse capture. This is early research now and will probably reach prototype quality within 18 months.

**Codec Avatar-adjacent quality will reach open-source.** The specific combination of 3DGS + rich capture + sophisticated learned disentanglement that Meta uses internally will appear in open research within 18-24 months, potentially reducing the quality gap between open and proprietary approaches to minimal.

## Summary

3D Gaussian Splatting avatars are the current best path for real-time photorealistic face rendering, combining 100-370 FPS rendering speed with clean parametric control via FLAME or ARKit blendshape driving. The architectural pattern — attach learned Gaussian primitives to a FLAME mesh, train them to reproduce multi-view video, drive them with parameter-based animation — was established by GaussianAvatars, SplattingAvatar, and 3D Gaussian Blendshapes in 2024 and has become the standard approach. Recent work (AniGS, Arc2Avatar, HeadStudio, FlashAvatar) is closing the gap between multi-view capture and zero-shot identity generation, with Arc2Avatar in particular showing that synthetic views from a diffusion model can serve as training data for a 3DGS avatar. Meta's proprietary Codec Avatars represent the quality ceiling but are not reproducible outside Meta; open-source methods are closing the gap gradually. The 12-24 month outlook sees 3DGS moving into mobile, into high-end VTuber production, into spatial computing, and toward full-body coverage, with the per-identity capture constraint becoming progressively weaker. This is the representation that will probably dominate the high end of real-time face avatars through the rest of the decade.

The next chapter turns to the other major real-time rendering alternative for novel identities: diffusion-based parametric face generation, which is the slowest path but the most flexible for producing new faces from scratch.

## References

[1] Kerbl, B., Kopanas, G., Leimkühler, T., Drettakis, G. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." SIGGRAPH 2023. The foundational 3DGS paper.

[2] Qian, S. et al. "GaussianAvatars: Photorealistic Head Avatars with Rigged 3D Gaussians." CVPR 2024 Highlight. arXiv:2312.02069. `shenhanqian.github.io/gaussian-avatars`.

[3] Shao, Z. et al. "SplattingAvatar: Realistic Real-Time Human Avatars with Mesh-Embedded Gaussian Splatting." CVPR 2024. arXiv:2403.05087. Reports 300+ FPS on RTX 3090 and 30 FPS on iPhone 13.

[4] Ma, S., Weng, Y., Shao, T., Zhou, K. "3D Gaussian Blendshapes for Head Avatar Animation." SIGGRAPH 2024. arXiv:2404.19398. 370 FPS rendering.

[5] Xiang, J. et al. "FlashAvatar: High-fidelity Head Avatar with Efficient Gaussian Embedding." CVPR 2024. arXiv:2312.02214. Over 300 FPS at 512² on RTX 3090.

[6] Qiu, L. et al. "AniGS: Animatable Gaussian Avatar from a Single Image with Inconsistent Gaussian Reconstruction." CVPR 2025. arXiv:2412.02684.

[7] Gerogiannis, D. et al. "Arc2Avatar: Generating Expressive 3D Avatars from a Single Image via ID Guidance." CVPR 2025. arXiv:2501.05379. Builds on Arc2Face synthetic view generation to produce training data.

[8] Zhou, Z. et al. "HeadStudio: Text to Animatable Head Avatars with 3D Gaussian Splatting." ECCV 2024. arXiv:2402.06149. `github.com/ZhenglinZhou/HeadStudio`.

[9] "PrismAvatar: Real-time photorealistic head avatars for mobile devices." arXiv:2502.07030, 2025. Note: uses a rigged prism lattice + deformable NeRF distilled to mesh + neural textures — not a 3DGS method, included for the mobile deployment comparison.

[11] Chen, Z. et al. "PSAvatar: A Point-based Shape Model for Real-Time Head Avatar Animation with 3D Gaussian Splatting." arXiv:2401.12900, January 2024. Near-contemporary FLAME + 3DGS method.

[12] Xu, Y. et al. "Gaussian Head Avatar: Ultra High-fidelity Head Avatar via Dynamic Gaussians." CVPR 2024. `github.com/YuelangX/Gaussian-Head-Avatar`.

[10] Meta Reality Labs. Codec Avatars research program. Multi-year effort, various publications, proprietary capture and models.

Additional references: Qualcomm's December 2024 blog post "Driving photorealistic 3D avatars in real time with on-device 3DGS" describes the mobile deployment story from the silicon vendor's perspective. NVIDIA's Omniverse platform includes 3DGS face avatar support in its Audio2Face integration.

See also `vamp-interface/docs/research/2026-04-12-3dmm-flame-diffusion-vtuber-realtime.md` for the survey of 3DGS avatar methods that underlies this chapter.
