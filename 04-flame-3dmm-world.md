# Chapter 04 — The FLAME World: 3D Morphable Models and the Research Lineage

## A Parametric Model, Not a Renderer

FLAME — Faces Learned with an Articulated Model and Expressions — is a parametric 3D face model published in 2017 by Li, Bolkart, Black, Li, and Romero at the Max Planck Institute for Intelligent Systems [1]. It is the direct descendant of Blanz and Vetter's 1999 3D Morphable Model, the progenitor of a research lineage now nearly three decades old, and it is by a wide margin the most-used face model in academic computer vision and graphics today. If you read a paper published between 2019 and 2026 that involves a 3D parametric representation of a human face, the most likely single answer to the question "what representation does it use" is FLAME.

The first and most important thing to understand about FLAME is what it is *not*. FLAME is not a renderer. It is not a texture model. It is not a neural network. It is not a face tracker. It is a parametric description of the *shape* of a human head — a system that takes a small number of scalar parameters as input and outputs a 3D triangle mesh of 5,023 vertices. The output mesh is geometrically correct but visually minimal: a smooth gray mannequin with the topology of a human head, the size and proportion of a specific person's face, and the pose and expression indicated by the parameters. It has no texture, no skin detail, no eye color, no hair, no lighting, and no photograph-like quality of any kind. To produce an image that looks like a person, you have to layer something else on top — a UV texture map, a neural renderer, a diffusion model, a 3D Gaussian splat avatar — that takes the FLAME mesh as input and produces pixels as output.

This separation between "shape representation" and "appearance rendering" is the central architectural fact about FLAME and explains almost everything else about its ecosystem. FLAME occupies one very specific slot in a larger pipeline: the slot where you need a compact, parametric, editable description of the geometry of a face. Every tool around FLAME — the extractors that recover FLAME parameters from photos, the renderers that produce images from FLAME meshes, the diffusion models that condition on FLAME parameters, the Gaussian splatting avatars that attach themselves to FLAME vertices — is a tool for interfacing with that specific slot. FLAME itself is small and well-defined. The ecosystem around it is large and sprawling because that one slot sits at a natural joint in the problem of modeling faces, and a lot of different tools want to plug into it.

## Technical Specifications

A FLAME model instance is specified by a vector of parameters and produces a fixed-topology 3D mesh. The components:

**Mesh geometry.** FLAME's template mesh has 5,023 vertices arranged in a hand-authored topology. The mesh covers the full head (not just the face) and includes separate eyeball vertices (indices 3931-5022), neck vertices, and jaw vertices. The topology is fixed — every FLAME mesh in the universe has the same vertex count and the same edge connectivity, and only the vertex positions vary. This fixed topology is operationally important: it means that two FLAME meshes can be directly compared vertex-to-vertex, interpolated linearly, or used as conditioning for a network that expects a specific input structure.

By modern game-engine standards, 5,023 vertices is low-poly. A high-end MetaHuman character has tens of thousands of vertices in the face alone. The raw FLAME mesh renders like an early-2000s game asset — recognizable as a face, clearly synthetic, with the smooth gray appearance that comes from uniform geometry without surface detail. UV-mapped textures at 1024 or 2048 pixels can produce an improved look that is roughly comparable to a pre-HD console game cutscene, but still unmistakably computer-generated. Photorealism is not in the scope of the raw model and requires the neural rendering layer discussed below.

**Shape parameters (β).** FLAME's identity is encoded in a 300-dimensional vector of shape parameters. These are the coefficients of a PCA basis computed over 3,800 neutral-expression 3D head scans from the CAESAR dataset and additional MPI-IS captures. The basis is ordered by variance — the first principal component is the direction in the scan data with the largest variance, the second is the orthogonal direction with the next-largest variance, and so on. Typical usage takes the first 10 to 100 components; the remaining dimensions are mostly noise. The first few components capture high-level identity properties like overall face width, nose prominence, and jaw shape, though their individual semantics are not labeled — they are statistical, not semantic. A user who wants to adjust "nose shape" cannot find a "nose" parameter; they have to either (a) find which linear combination of the first few PCs moves the nose, which is an empirical exercise per-model, or (b) adjust vertex positions directly and project back into the PCA basis.

**Expression parameters (ψ).** Expression is encoded in a 100-dimensional PCA vector computed from 4D (3D-over-time) dynamic capture sequences in the D3DFACS dataset and additional captures. The expression basis is orthogonal to the shape basis — changing the expression vector does not change the underlying identity. This orthogonality is one of FLAME's most important properties and is the reason FLAME-based systems support clean composition of identity and expression (you can extract expression from one face and apply it to another by swapping ψ values). Typical usage takes 50 to 100 components; the first few capture the largest expression modes (mouth open, smile, brow raise) while later components encode subtler nuances.

**Pose parameters.** Pose is encoded as a set of explicit rotation parameters for named joints — neck rotation (3 DOF), head rotation (3 DOF), jaw rotation (3 DOF), and separate left and right eye rotations. Unlike shape and expression, pose is hand-authored rather than statistical: the joints are anatomically specified, and the parameters are rotation angles with clear physical meaning. Total pose is 6 DOF for global translation and roughly 12 DOF for joint rotations, depending on which version of the model is counted.

The full parameter space, taking the canonical usage, is approximately: 100 shape dimensions + 50 expression dimensions + 15 pose dimensions ≈ 165 scalars. This is small enough to store, transmit, and optimize over cheaply — a FLAME description of a face fits comfortably in under a kilobyte — and it is large enough to capture meaningful variation in identity, expression, and pose for a broad range of human faces.

**Inference speed.** Generating a mesh from a FLAME parameter vector takes roughly 12 milliseconds on a commodity GPU, though the operation is simple enough (matrix multiplies and joint rotations) that it can be batched and accelerated heavily. The bottleneck for FLAME in real-time applications is not mesh generation — it is parameter extraction from input images, which is discussed in the extractor section below.

## Why Not Other 3DMMs?

FLAME is not the only 3D morphable face model, and understanding why it became dominant requires a brief comparison with its competitors.

**Basel Face Model (BFM)** is the direct predecessor: a 3DMM released by the University of Basel in 2009 (with an update in 2017). BFM uses a PCA basis over approximately 200 neutral face scans and provides shape and texture components. It was the standard 3D face research tool until FLAME displaced it. The reasons for the shift are primarily quantitative: FLAME's shape basis achieves lower reconstruction error (approximately 0.85 mm Chamfer distance versus 1.2 mm for BFM on standard benchmarks) and encodes more expressive variation because it trains on a larger and more diverse dataset. FLAME also adds expression and pose in the same unified framework, whereas BFM treats texture and shape as the primary axes and handles expression less systematically. For pure geometric reconstruction of neutral faces, BFM is still usable; for any task involving expression, pose, or downstream integration with modern neural renderers, FLAME has no serious competition in the classical-3DMM tradition.

**SMPL-X** is not exactly a competitor but rather a superset. SMPL-X is a full-body parametric model published by the same MPI-IS group; its face component *is* FLAME. A SMPL-X model includes body shape, hand articulation, and facial expression under a single parameter space, and the facial part is literally FLAME vertices and parameters embedded in a larger body context. For research on full-body humans (avatar reconstruction, motion capture, virtual try-on), SMPL-X is the natural choice; for research specifically on faces, using the face component of SMPL-X is equivalent to using FLAME directly.

**StyleMorpheus** (2025) is a newer approach that trains a neural 3DMM with a style-based decoder inspired by StyleGAN. The generated meshes are photorealistic natively — the model directly learns to produce visually convincing geometry plus appearance rather than just shape — and the parameterization is learned rather than PCA-derived. StyleMorpheus is an interesting research direction and may represent the future of the field, but as of early 2026 it has a tiny fraction of FLAME's ecosystem: few downstream tools build on it, few extractors exist, and no rendering pipeline has standardized around it. It is worth tracking but not worth planning around.

**ImFace++** (IEEE TPAMI 2025) uses implicit neural fields (SDFs or occupancy fields) rather than explicit meshes to represent face shape. The resulting model captures fine detail (pores, wrinkles) that mesh-based models cannot, but the representation is less compatible with downstream mesh-consuming tools, and the ecosystem is still research-only. Again, interesting but not yet load-bearing.

**Proprietary face models** (Apple's internal face model, NVIDIA's Audio2Face models, Meta's Codec Avatars models) exist inside specific products and drive specific pipelines, but they are not available as open research tools and do not compete with FLAME in the academic ecosystem.

The cumulative picture: FLAME is dominant in research because of a combination of licensing availability, the strength of its statistical basis, the unification of shape and expression and pose in one framework, the orthogonality of its parameter spaces, and the accumulated network effects of two hundred downstream papers building on it. It is not the best possible representation by any individual metric, but it is the best compromise across all the metrics that matter for research.

## The Extractor Lineage: DECA, EMOCA, SMIRK

The most useful property of FLAME for applied work is not its structure but the fact that reliable extractors exist: systems that take an arbitrary 2D photograph and produce the FLAME parameters of the face in the photo. These extractors are the bridge from images to the parametric representation, and their quality determines how useful FLAME is for any application that starts from photographs or videos.

**DECA** (Detailed Expression Capture and Animation, SIGGRAPH 2021) [2] is the baseline FLAME extractor. It was the first method to reliably recover FLAME shape, expression, pose, and fine detail from a single in-the-wild photograph. The architecture combines a coarse encoder (predicting FLAME parameters directly) with a detail encoder (predicting per-vertex displacement maps that add wrinkles and surface detail on top of the coarse mesh). DECA's reconstruction error improved on prior work by approximately 9%, and its code is publicly available and well-maintained. For roughly three years DECA was the default "photo → FLAME" tool used in downstream research, and many published pipelines still assume DECA as their frontend.

DECA's limitations are mostly around expression accuracy. The system captures overall shape and pose well, but its expression reconstruction is biased toward neutral — it struggles to recover strong expressions, asymmetric expressions, and the subtle micro-expressions that matter for emotion reading. Quantitatively, on the AffectNet dataset, DECA achieves a Pearson correlation of 0.70 for valence prediction and 0.59 for arousal prediction, meaning that when DECA recovers FLAME parameters and a downstream classifier reads emotional state from them, the classifier agrees moderately with human-labeled ground truth but is clearly not perfect. Human evaluators rate 48% agreement on specific emotion categories for DECA outputs versus much higher agreement for the original images.

**EMOCA** (Emotion-Driven Monocular Face Capture and Animation, CVPR 2022; v2 is the current version as of 2026) [3] extends DECA with emotion-aware training. The key change is adding an emotion prediction loss during training: the network is rewarded for producing FLAME parameters that, when rendered, produce a face that an emotion classifier can correctly classify. This forces the expression reconstruction to preserve the emotional content of the input rather than just the geometric fit. EMOCA v2 improves AffectNet valence correlation to 0.78 and arousal to 0.69, with human perceptual emotion agreement rising from DECA's 48% to EMOCA's 60%. The model is still built on DECA's architecture but with this additional supervisory signal, and its outputs are better suited for any downstream task that cares about emotional expression.

EMOCA's remaining weaknesses are around extreme and asymmetric expressions — the kinds of expressions that are rare in the training data and are therefore underrepresented in the statistical PCA basis. A one-sided smirk, a wide grimace, an asymmetric eyebrow raise — these are hard for EMOCA just as they are hard for DECA.

**SMIRK** (Structural Monocular Image-based Reconstruction of the Face, CVPR 2024) [4] is the current state of the art for FLAME extraction, and its innovation is training-time perceptual supervision using a neural renderer. The pipeline works as follows: the input image passes through an encoder that produces candidate FLAME parameters; the FLAME mesh is rendered through a neural renderer that produces a photorealistic image; and the rendered image is compared with the input via perceptual and reconstruction losses. By training the extractor and the renderer jointly, SMIRK learns to produce FLAME parameters that reconstruct the input image *visually*, not just geometrically. This catches expression variations that DECA and EMOCA missed because they were optimizing for mesh fit rather than image fit.

SMIRK's output is still FLAME parameters — it is a better extractor, not a different model — but the parameters it produces are noticeably more accurate for asymmetric, strong, and subtle expressions. For any application requiring clean FLAME extraction from photographs, SMIRK is the 2026 recommendation. The code is available at `github.com/georgeretsi/smirk`.

**Extraction speed.** All three extractors run in the 100-500 millisecond range per photo on GPU, depending on resolution and the specific model configuration. This is fast enough for offline batch processing (extracting FLAME parameters from a dataset of photographs) but too slow for real-time face tracking (a 30 Hz tracking loop has a 33 ms budget, and even a 100 ms extraction blows that budget by 3x). The real-time tracking use case is therefore not directly served by these extractors; real-time systems use ARKit or MediaPipe and then optionally solve into FLAME via the cheap least-squares bridge discussed in Chapter 03.

A separate research effort called **SPARK** (SIGGRAPH Asia 2024) [5] specifically targets real-time FLAME capture by training a lightweight model designed for the tracking loop, and early results suggest real-time FLAME extraction is becoming feasible on high-end hardware. SPARK is still research-only as of early 2026 and has not displaced the "ARKit + solver" path for production tracking.

## The Rendering Layer: From Mesh to Photorealism

FLAME is a mesh; FLAME renders look like PS2-era game assets. The interesting applications of FLAME in 2026 are not the ones that look at the raw mesh — they are the ones that use FLAME as a geometric control signal for a separate rendering layer that produces photorealistic output. The rendering layer varies by use case:

**Raw FLAME mesh** renders as a smooth gray mannequin. Correct pose and topology, no skin detail. Useful as a control rig, not as a visual asset. This is the output you get from running the FLAME generator function directly and viewing it in a standard 3D viewer.

**FLAME with UV textures** renders as a recognizable face, still clearly synthetic. Early 2000s game cutscene quality at best. The UV texture maps for FLAME are available at 256, 512, 1024, and 2048 pixel resolutions from the MPI-IS download page. With a well-chosen texture and proper lighting, the output is adequate for motion-capture reference and for mid-quality avatar rendering, but it does not cross the threshold into "photorealistic."

**FLAME with neural rendering** is where the interesting results start. Several classes of neural renderers take FLAME meshes as geometric scaffolding and add learned appearance on top:

- **GaussianAvatars** (CVPR 2024) attaches 3D Gaussian splats to FLAME mesh vertices. Each splat has a learned position, color, scale, and orientation relative to the attached vertex. As the FLAME mesh deforms, the splats move with it. Rendering produces genuinely photorealistic output — in controlled lighting conditions, GaussianAvatars demo videos are indistinguishable from real video to most human observers. The quality degrades somewhat in the wild (uncontrolled lighting, extreme pose, occlusion) but is still strong. The cost is per-person reconstruction: you need multi-view video of the specific person you want to render, and an optimization pass to fit their splats onto the shared FLAME topology.

- **SPARK** (the same paper mentioned for real-time extraction) produces a real-time FLAME-driven neural renderer with fine albedo and shading. It is per-person like GaussianAvatars but faster to fit.

- **Diffusion-based FLAME rendering** — RigFace, Arc2Face with expression adapter, MorphFace — takes FLAME parameters as conditioning input and produces a photorealistic face image via a diffusion model. Photorealistic stills, ~1-2 seconds per image, not real-time. The key advantage is that these methods do not require per-person reconstruction — any FLAME parameter vector can be rendered through the general model. The key disadvantage is the speed; diffusion sampling is fundamentally too slow for a 30 Hz tracking loop.

The pattern: FLAME provides the shape and motion signal; the rendering layer provides the appearance and photorealism. Different rendering layers offer different tradeoffs between speed (3DGS fast, diffusion slow), quality (both can be photorealistic in their best case), and generality (diffusion works without per-person reconstruction, 3DGS typically does not).

## FLAME in Diffusion Models

The most active research front involving FLAME as of 2026 is its use as a conditioning signal for diffusion models. Chapter 08 covers this in depth; this section provides a summary for completeness.

**Arc2Face + blendshape expression adapter** (ECCV 2024 + ICCVW 2025) uses ArcFace identity embeddings as one cross-attention channel and FLAME expression coefficients as a separate cross-attention channel in a Stable Diffusion backbone. Identity and expression are genuinely orthogonal — you can hold identity fixed and sweep expression, or hold expression fixed and sweep identity. The code is public.

**RigFace** (arXiv 2502, June 2025) fully fine-tunes SD 1.5 with DECA-derived 3D renders, expression coefficients, and masks as conditioning. Identity is preserved via a full-UNet Identity Encoder rather than a small adapter, and the full backbone is trained rather than just a plugin module. The result is high-fidelity editing with clean disentanglement of expression, pose, and lighting. The code and weights are public.

**MorphFace** (CVPR 2025) uses FLAME parameters to guide diffusion denoising timesteps, with identity styles emphasized at early timesteps and expression styles at later timesteps. Aimed at generating synthetic training data for face recognition systems. Code availability is unconfirmed as of this writing.

**HeadStudio** (ECCV 2024) takes text descriptions as input and produces FLAME-rigged 3D Gaussian avatars at 40+ FPS rendering speed. The generation takes approximately 2 hours per character on an A6000, so it is not interactive, but the output is real-time drivable by FLAME parameters. This is the closest published system to the "generate a new face from a description, then animate it in real time" target.

In all these systems, FLAME plays the same architectural role: it is the compact, interpretable, parametric description of face geometry that the generation model is conditioned on. The generation model provides the photorealism; FLAME provides the controllability. Swapping FLAME for a different parametric representation would be possible in principle — one could train a diffusion model conditioned on ARKit blendshapes instead, or on a custom learned parameterization — but nobody has done so yet, partly because FLAME's orthogonal decomposition of shape / expression / pose is exactly what you want when training a diffusion model with separate cross-attention channels for each axis. Losing that decomposition means losing the clean editability.

This is the practical meaning of "FLAME is the research lingua franca": when a paper needs a compact 3D face description to feed into a generation model, FLAME is the default, and the downstream research community knows how to interpret the results.

## The Licensing History and Its Consequences

A small but important detail: FLAME was released under a non-commercial research license until 2023, when the authors relicensed it under CC-BY-4.0. Before 2023, you could use FLAME for academic research but not for any commercial product. This licensing friction is the primary reason FLAME built up a large research ecosystem but never built a corresponding commercial ecosystem — commercial face products were legally blocked from using FLAME, so they built around other representations (Apple's internal face model, Epic's MetaHuman rig, NVIDIA's proprietary models) and never came back even after the license changed.

The CC-BY-4.0 relicensing in 2023 is recent enough that the commercial ecosystem has not yet fully responded. Commercial products built on FLAME after 2023 exist (a handful of small research-adjacent startups, a few academic spin-offs) but there is no major commercial product line that uses FLAME as its foundation. The question of whether this changes in the next two years is open. My prediction is that it will change only slowly: the ecosystem around ARKit and proprietary models is now deep enough that switching has high switching costs, and the clearest advantage FLAME offers — research ecosystem integration and clean parametric control — is an advantage that matters primarily for research projects and for the specific niche of products that want to leverage FLAME-based generation models.

The practical consequence for a 2026 product builder: FLAME is now commercially usable, so if your product needs FLAME internally (because you want to use RigFace, Arc2Face, or similar generation models), there is no licensing obstacle. But FLAME is not the right thing to expose externally, because no consumer of your output will know how to work with it. ARKit remains the right external API, as Chapter 03 argued.

## Locating FLAME in the Taxonomy

Returning to the three-axis taxonomy:

- **Dimensionality:** 3D. FLAME commits fully to a 3D mesh representation with explicit vertex positions.
- **Explicitness:** Explicit. Shape, expression, and pose are separate parameter vectors with known dimensionality and known orthogonal structure. Within each vector the parameters are *statistically* explicit (PCA components) rather than *semantically* explicit (named parameters), but they are still addressable by index and composable by linear operations.
- **Authoring origin:** Statistical (for shape and expression) and hand-authored (for pose). This is a hybrid on the third axis — the most mature face model in the world uses statistical bases for what PCA handles well and hand-authored rotations for what PCA handles poorly.

The operations matrix:

| Operation | FLAME support |
|---|---|
| Extract from photo | Strong — DECA, EMOCA, SMIRK are the standard extractors, 100-500 ms offline |
| Render to image | Weak by itself (gray mannequin); strong with neural rendering layer (GaussianAvatars, diffusion) |
| Edit by parameters | Strong — orthogonal shape, expression, and pose spaces |
| Interpolate between instances | Strong — linear interpolation in PCA space is mathematically well-defined |
| Compose identity + expression | Strong — the orthogonal decomposition is designed for this |
| Real-time driving | Medium — cannot natively handle real-time extraction, but integrates with ARKit via 1 ms solver |

FLAME's profile is the complement of ARKit's: strong at shape, strong at composition, strong at the underlying geometric representation, and dependent on external tooling for extraction (extractors), rendering (neural renderers), and real-time driving (ARKit bridge). It is the research substrate that connects many other methods, not a complete system in itself.

## Summary

FLAME is a 300-shape-dimension plus 100-expression-dimension plus small-pose-parameter parametric 3D face model, developed at MPI-IS and published in 2017, that has become the dominant face representation in academic computer vision and graphics research. It is a shape representation, not a renderer — raw FLAME meshes render as smooth gray mannequins — and the interesting applications all involve a separate rendering layer (GaussianAvatars, SPARK, diffusion-based methods) that produces photorealistic output on top of the FLAME scaffolding. Extractors (DECA, EMOCA, SMIRK) recover FLAME parameters from arbitrary photos at 100-500 ms per photo with increasing accuracy; real-time extraction is an active research front (SPARK) but not yet production-ready. FLAME's non-commercial licensing until 2023 kept it out of commercial ecosystems, which now default to ARKit and proprietary models; the 2023 CC-BY-4.0 relicense has opened the door to commercial use but the ecosystem has not fully responded. Product builders in 2026 should treat FLAME as an internal implementation detail for generation pipelines and keep ARKit as the external API, using the 1 ms ARKit-to-FLAME solver to bridge between them. The next chapter turns to the other major 2D animation tradition — neural deformation methods (LivePortrait and heirs) that bypass FLAME and 3DMMs entirely.

## References

[1] Li, T., Bolkart, T., Black, M. J., Li, H., Romero, J. "Learning a model of facial shape and expression from 4D scans." ACM Transactions on Graphics (SIGGRAPH Asia) 2017. `flame.is.tue.mpg.de`.

[2] Feng, Y. et al. "DECA: Detailed Expression Capture and Animation." SIGGRAPH 2021. `github.com/YadiraF/DECA`.

[3] Daněček, R., Black, M. J., Bolkart, T. "EMOCA: Emotion Driven Monocular Face Capture and Animation." CVPR 2022. `github.com/radekd91/emoca`. EMOCA v2 is the current maintained version.

[4] Retsinas, G. et al. "SMIRK: 3D Face Reconstruction with Neural Rendering for Expression Recovery." CVPR 2024. `github.com/georgeretsi/smirk`.

[5] SPARK. SIGGRAPH Asia 2024 — real-time FLAME capture with neural rendering.

See also: `vamp-interface/docs/research/2026-04-12-flame-technical-overview.md`, `vamp-interface/docs/research/2026-04-12-flame-ecosystem-map.md`, and `vamp-interface/docs/research/2026-04-12-rigface-technical-deep-dive.md` for the primary research underlying this chapter.

Additional ecosystem resources: FLAME PyTorch implementation at `github.com/soubhiksanyal/FLAME_PyTorch`; TensorFlow implementation at `github.com/TimoBolkart/TF_FLAME`; Blender add-on at `github.com/TimoBolkart/FLAME-Blender-Add-on`; FLAME-Universe resource index at `github.com/TimoBolkart/FLAME-Universe`.
