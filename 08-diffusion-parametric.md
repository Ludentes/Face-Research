# Chapter 08 — Diffusion-Based Parametric Face Generation

## The Problem the Chapter Addresses

Every chapter so far has discussed ways of representing, animating, and rendering faces that already exist in some form — a photograph of a specific person, a rig authored by an artist, a FLAME mesh fit to a 3D capture, a 3DGS avatar reconstructed from video. This chapter addresses the question of where *new* faces come from: how to produce, from a description or an abstract latent vector, a face that nobody has generated before, while retaining tight parametric control over its attributes. This is the problem of *generation*, and it is where diffusion models have become dominant over the 2022-2026 period, displacing GAN-based generation (StyleGAN and successors) almost entirely.

The chapter's scope is specifically on diffusion methods that combine *identity generation* with *parametric control*. A diffusion model that just generates a face from a text prompt (Stable Diffusion in its default configuration) is not what this chapter is about — that is a task where the parametric control is minimal and the output is whatever the text encoder happens to produce. What this chapter is about is the class of methods that add explicit axes of control on top of diffusion generation: expression parameters from FLAME, identity embeddings from ArcFace, pose parameters, lighting parameters, and combinations thereof. These methods let you ask for a face with specific attributes and receive a face that matches, with the attributes being the axes of variation rather than free-form text.

Several generations of method have explored this space: ControlNet-style adapters that add one channel of control at a time, IP-Adapter-style image conditioning for style transfer, LoRA-based concept sliders that discover semantic axes after training, and the fully fine-tuned FLAME-conditioned methods (RigFace, Arc2Face + expression adapter, MorphFace) that represent the current state of the art. The chapter walks through these in approximate order of increasing integration with the parametric face world and closes with a practical guide to which method fits which use case.

## The StyleGAN Era and Why It Ended

Before diffusion took over, the dominant approach to parametric face generation was StyleGAN and its successors [1]. StyleGAN produced photorealistic faces from a latent vector and supported a flavor of parametric editing through *direction finding* in its W-space and W+ space: by identifying learned directions in the latent space that correspond to semantic changes (add glasses, smile more, age older), a user could edit a generated face by adding a scaled direction vector to its latent. The editing was continuous, predictable within its range, and fast (a single forward pass through the generator, milliseconds per frame).

StyleGAN's limitations were entanglement and expression range. Entanglement meant that learned directions were never cleanly orthogonal — moving along the "age" direction would also slightly shift gender or ethnicity, because the training data had correlations between these attributes that the network encoded as shared latent axes. Multiple techniques (InterFaceGAN, StyleFlow, various disentanglement regularizers) partially addressed this but never eliminated it. The 2024 FactorVAE work by Soulos, Langlois et al. [2] trained a 24-dimensional FactorVAE latent space on face images and found that annotators could reach consensus semantic labels on 16 of the 24 dimensions — a much cleaner disentanglement than prior GAN-based analyses had achieved, though not the training-time enforcement of exactly 16 axes that the earlier framing implied. This improved the situation substantially, but by that point the field had largely moved on.

The expression range limitation was more fatal. StyleGAN was trained primarily on FFHQ, a 70,000-image dataset of professional portrait photographs where nearly every subject has a single neutral-to-slight-smile expression. The W-space therefore has very little variation in the expression direction — you can barely get a full smile out of a StyleGAN trained on FFHQ, let alone surprise, anger, disgust, or subtle emotional states. A generative model whose expression range is "neutral to slight smile" cannot support applications that need the full expressive vocabulary of human faces, and this includes nearly every application this review cares about.

Diffusion models took over in 2022-2023 because they were trained on far more diverse data (LAION, internet-scale image-text pairs) that included the full range of expressions, emotions, and contexts. A Stable Diffusion model generates a frowning face or an angry face without effort because it has seen millions of such examples in training. The tradeoff was speed — diffusion sampling was and is slower than GAN generation — and the loss of StyleGAN's clean direction-finding workflow. The post-2023 research on diffusion-based parametric face generation has been about recovering StyleGAN's parametric control advantages while keeping diffusion's expressive range.

Concept Sliders [3] is the clearest methodological link between the two eras. Concept Sliders are LoRA weight-pair semantic directions in a diffusion model, trained to produce specific semantic changes when added or subtracted from the model's weights. The approach recreates StyleGAN's "named semantic axes" pattern in a diffusion context: you specify a direction (e.g., "younger ↔ older"), you train the LoRA pair to move along that direction, and at inference you can adjust the slider position to produce a family of faces varying along that axis. Crucially, multiple sliders compose without degradation — you can stack 50+ sliders in a Flux model and retain clean results. Concept Sliders show that the StyleGAN-era parametric editing idiom is recoverable in diffusion, and they have become a standard tool in the community for this kind of control.

## Diffusion Bottleneck Activations: The h-Space Paradigm

A separate line of work investigates whether diffusion models have an internal structure comparable to StyleGAN's W-space — a latent space where direction finding is meaningful and editing is clean. The answer, established over a series of papers in 2022-2024, is yes: diffusion models have an *h-space*, specifically the bottleneck activations of their UNet denoisers at specific timesteps, which behaves remarkably similarly to StyleGAN's W-space.

**Asyrp** (Kwon et al., ICLR 2023) [4] was the first paper to identify and exploit h-space in a diffusion model. The method shows that by intervening on the bottleneck activations of the UNet at specific denoising timesteps, you can produce semantic edits to the generated image that are as clean and compositional as StyleGAN's W-space edits. The h-space has properties that are surprising: it is *homogeneous* (the same direction produces the same semantic change regardless of the starting latent), *linear* (two edits compose by vector addition), and *robust* (the edits survive stylistic changes in the input).

**Haas et al.** (IEEE FG 2024) [5] extended the h-space analysis to a broader class of diffusion models and demonstrated that discovering semantic directions in h-space can be done without per-attribute supervision — the directions emerge from the distribution of activations themselves. This is the direct analog of StyleGAN direction-finding methods being applied to diffusion.

The h-space paradigm is relevant for this chapter because it provides a path to parametric face editing in any diffusion model without fine-tuning, LoRA training, or adapter modules: you take an existing diffusion model, discover directions in its h-space that correspond to semantic changes, and edit by adding scaled directions to the bottleneck activations during sampling. The compute cost is minimal (a single forward pass with an injected edit), the code is publicly available for several models, and the approach can be composed with any of the other methods discussed in this chapter.

For a product builder using a current diffusion stack (Flux, SDXL, SD 1.5, SD 3), h-space direction finding is the cheapest way to add parametric control without restructuring the generation pipeline. The cost is that the directions have to be discovered and named by the builder, and the quality of the edit depends on how well the direction-finding process captures the intended semantic axis.

## ControlNet and IP-Adapter: Adapter-Level Control

The earliest and most widely deployed methods for adding parametric-ish control to diffusion-based face generation are ControlNet and IP-Adapter, both of which operate as adapters on top of a pretrained diffusion backbone rather than requiring full fine-tuning.

**ControlNet** (Zhang et al., ICCV 2023) [6] adds structured image conditioning to Stable Diffusion by training a separate neural network (the "ControlNet") that takes a conditioning image (edge map, pose skeleton, depth map, etc.) and injects features into the diffusion denoiser at multiple layers. For face generation specifically, ControlNet variants exist for face meshes (conditioned on MediaPipe face mesh renders), for pose (conditioned on skeleton keypoints), and for depth maps. These let you generate a face with a specific mesh structure or pose, which is a partial form of parametric control — you are controlling the geometry via the conditioning image rather than via named parameters.

ControlNet has the advantage of being cheap (no full fine-tuning required) and widely supported (hundreds of ControlNet variants exist in the community), but the parametric control is indirect. You cannot set "smile = 0.7" directly; you have to produce a conditioning image that *shows* a smile and hope the ControlNet respects it. This works well enough in practice that many face generation pipelines still use ControlNet as their primary parametric control mechanism, but the indirection is real and limits the expressiveness of the control.

**IP-Adapter** (Ye et al., 2023) [7] is the complementary tool: it adds identity/style conditioning to Stable Diffusion by taking a reference image and encoding it via a CLIP-like image encoder, then injecting the resulting image embedding into the diffusion denoiser. For face generation specifically, IP-Adapter Face provides an identity preservation mechanism that lets you generate novel faces "in the style of" a reference face, with the resulting faces bearing recognizable similarity to the reference.

IP-Adapter has the advantage of being cheap, composable with ControlNet, and widely available (dozens of variants exist). The limitation is that CLIP image embeddings lose fine facial detail, so the identity preservation is approximate rather than exact. A face generated with IP-Adapter Face often looks "like a cousin or sibling of" the reference rather than "exactly like" the reference. For applications where loose identity preservation is acceptable, this is fine; for applications that need the generated face to be recognizably the same person as the reference, IP-Adapter is not sufficient.

The combination ControlNet + IP-Adapter defined the 2023-2024 pattern for face generation with parametric control. It is still widely used, especially in production pipelines (Textoon uses exactly this combination), and it will continue to be used because the tooling is mature and the results are good enough for many applications. The methods that improved on it — the fully fine-tuned FLAME-conditioned methods discussed below — provide tighter control but cost more to train and integrate.

## Arc2Face: Identity as a Dedicated Channel

**Arc2Face** (Papantoniou et al., ECCV 2024 Oral) [8] is the key paper for identity-conditioned face generation. It makes the architectural observation that CLIP embeddings are the wrong representation for face identity — CLIP is trained on image-text pairs and captures semantic/visual properties but loses the fine details that make one face recognizable as a specific person — and proposes using ArcFace embeddings instead. ArcFace is a face recognition network trained specifically to produce 512-dimensional identity embeddings where the same person's photos cluster tightly and different people's photos are far apart. It is the canonical identity representation used in face recognition systems.

Arc2Face takes an ArcFace 512-d vector as input and generates a Stable Diffusion image of a face matching that identity. The mapping is learned by fine-tuning SD on a dataset of aligned face images, using the ArcFace embedding as the primary conditioning signal (instead of, or in addition to, text prompts). The result is a face generation model where identity is addressable as a *vector* — you can generate a face, edit its identity vector, and regenerate, and the resulting faces are recognizably different identities with controllable relationship to the original.

Arc2Face's architectural significance is that it establishes *identity as a dedicated cross-attention channel* in the diffusion UNet. The face identity is not mixed into a text prompt; it flows through its own path in the model. This makes identity manipulation clean and composable.

**Arc2Face + expression adapter** (ICCVW 2025) [9] extends Arc2Face by adding a second dedicated channel for expression conditioning, using FLAME blendshape coefficients extracted from a target image via SMIRK. The architecture has two independent cross-attention paths — one for the ArcFace identity embedding, one for the FLAME expression coefficients — and the two are trained to be genuinely orthogonal. The result is that you can hold identity fixed and sweep expression, or hold expression fixed and sweep identity, with minimal bleed between the two channels.

This is the clean two-channel separation that the earlier chapters hinted at: identity and expression as independent addressable vectors. You can generate a face of a specific identity with a specific expression by providing the ArcFace vector and the FLAME expression vector; you can edit either while holding the other; and the whole thing runs in standard Stable Diffusion inference time (~1 second per image). Arc2Face + expression adapter is the current simplest way to get "two-channel parametric face generation" working with public code.

The limitation is that the identity input is constrained to the ArcFace vector space. You cannot directly input an arbitrary semantic embedding (a text embedding from a language model, a custom learned vector) — you have to first project it into ArcFace space, which requires training a projection layer. This is doable but is an extra step, and it means Arc2Face is not a direct path from arbitrary embeddings to faces.

## RigFace: Full Fine-Tuning for Maximum Control

**RigFace** (Wei et al., arXiv:2502.02465, February 2025; paper formally titled "Towards Consistent and Controllable Image Synthesis for Face Editing", with "RigFace" used as the method's internal name; code at `github.com/weimengting/RigFace`) [10] is the most ambitious of the FLAME-conditioned diffusion methods and represents the current state of the art for tightly controlled face editing. Where Arc2Face uses adapters and cross-attention injection, RigFace fully fine-tunes the entire SD 1.5 backbone and adds an entire second UNet as an identity encoder. The thesis of the paper is that adapter-based methods (ControlNet, IP-Adapter, even Arc2Face's expression adapter) cannot achieve the tightest quality of identity preservation under parametric edits; full fine-tuning is necessary.

The RigFace architecture has four components (from the research note in `vamp-interface/docs/research/2026-04-12-rigface-technical-deep-dive.md`):

**Spatial Attribute Provider.** A non-neural pipeline that takes a source portrait and target expression/pose/lighting parameters and produces three outputs: (1) a 3D rendered image of the face at the target pose and lighting using a Lambertian reflectance + spherical harmonics shading model, (2) FLAME expression coefficients extracted via DECA/Deep3DRecon, and (3) a dilated foreground mask from face parsing. The rendered image is the key element — it provides pixel-space guidance that the UNet can interpret directly, rather than requiring the model to learn a mapping from abstract FLAME coefficient vectors to pixels.

**Identity Encoder.** A full second copy of the SD 1.5 UNet, trainable, that processes the reference identity image and extracts multi-level self-attention features from each transformer block. This is a much heavier identity representation than a CLIP embedding or an ArcFace vector — it is the full set of internal features that a denoising UNet produces when processing the reference face. The paper argues that this is what is needed to preserve fine facial details (bone structure, distinctive features, skin characteristics) that adapter-based methods lose.

**FaceFusion.** An identity injection mechanism that concatenates identity features from the Identity Encoder with the main UNet's self-attention features along the width dimension before the self-attention operation in each transformer block. Only half of the concatenated output is retained. This allows identity information to flow into every layer of the denoising process.

**Attribute Rigger + Denoising UNet.** A lightweight convolutional module that injects the spatial conditions (3D renders + expression coefficients + masks) into cross-attention layers at multiple depths. The separation is clean: self-attention is for identity, cross-attention is for attributes.

The training regime: 30,000 image pairs from the Aff-Wild video dataset (same-video pairs guarantee consistent identity while varying expression and pose), trained for 100,000 steps at batch size 8 with learning rate 1e-5, on 2× AMD MI250X GPUs (roughly equivalent to 2× A100), for approximately 24 GPU hours total.

What you control independently:
- **Expression**: FLAME blendshape coefficients from the target
- **Head pose**: FLAME pose parameters rendered to 3D image
- **Lighting**: Spherical harmonics coefficients rendered to 3D image
- **Identity**: Reference portrait via the Identity Encoder (preserved across the edits)

Quality signal: 59.3% of RigFace expression edits were rated more realistic than ground truth in a human perceptual study — meaning the model does not just copy; it interpolates plausibly.

Weaknesses: DECA-based extraction fails at extreme poses (profile, upward angles), so edits that request those poses degrade. Occlusions (hair over face, glasses, hands) also degrade output. Inference is multi-step diffusion, ~1-2 seconds per image, and is not real-time.

RigFace is the reference point for "fully fine-tuned FLAME-conditioned diffusion" and represents the quality ceiling for offline face editing with tight parametric control. For applications that can afford the training cost (24 GPU hours is not trivial but is accessible) and the inference time (1-2 seconds per image), it is the best available option.

## MorphFace and Other FLAME-Conditioned Methods

**MorphFace** (CVPR 2025) [11] uses 3DMM guidance throughout the diffusion denoising process with *context blending*: identity-related styles are emphasized at early timesteps (coarse structure formation) while expression-related styles are emphasized at later timesteps (fine detail). This temporal decomposition allows the model to keep identity and expression disentangled without requiring architectural separation. MorphFace is primarily aimed at generating synthetic training data for face recognition systems — it produces distinct identities with controlled expression and pose variation, with evaluation showing 99.25% LFW accuracy (and 93.32% averaged across LFW, CFP-FP, AgeDB, CPLFW, and CALFW) when using 500K synthetic MorphFace images as training data. The code availability is unconfirmed as of this writing.

**Multimodal Conditional 3D Face Geometry Generation** (arXiv:2407.01074, 2024) [12] takes a different architectural approach: it accepts FLAME parameters as one of several conditioning modalities (alongside images, sketches, masks, text) via IP-Adapter-style cross-attention, and produces 3D facial geometry as output. The conditioning path is not a dedicated FLAME-only MLP but a shared multi-modal adapter, and the method's orientation is toward 3D mesh generation for downstream neural rendering rather than direct image production.

The diversity of FLAME-conditioned diffusion methods is evidence that the architectural space is still being explored. As of early 2026, there is no consensus on the single best architecture, and different methods make different tradeoffs between training cost (adapters cheaper, full fine-tuning more expensive), inference speed (all offline, 1-2 seconds per image, with minor variations), and quality (RigFace and Arc2Face + expression adapter are the strongest).

## The Direct-Embedding Frontier

The methods discussed so far all require some structured conditioning input: an ArcFace vector, a FLAME parameter set, a reference image. An ambitious frontier question is whether diffusion models can be conditioned on *arbitrary* semantic embeddings — a text embedding from a general language model, a learned embedding from a custom space (like a job-posting embedding from a language model, as in the vamp-interface project that sparked parts of this review) — without requiring that embedding to be in ArcFace or FLAME or text-encoder space.

The answer is "yes, with a projection layer." The general pattern is: train a small MLP that maps from the source embedding space into the conditioning space that the diffusion model accepts (ArcFace vector for Arc2Face, CLIP image embedding for IP-Adapter, etc.). The projection layer is learned on pairs (source embedding, target face) where the targets come from a known source. Once trained, you feed source embeddings through the projection and receive faces.

This pattern works but has a catch: the quality of the final faces depends on the quality of the projection, and projection training requires meaningful pairs. If the source embedding space has a natural alignment with the conditioning space (e.g., both encode "visual appearance"), the projection can be learned from a small dataset. If the source embedding space is semantically distant from the conditioning space (e.g., a job-posting embedding and a face identity embedding), the projection is essentially arbitrary — you are defining by training data fiat that "this job posting has this face," which is not a natural mapping.

The interesting use cases for direct-embedding-to-face generation are the ones where the source embedding has meaningful variance that should correspond to meaningful variance in the face. Data visualization applications (like vamp-interface, where job postings are embedded and faces encode cluster membership and fraud verdict) fit this profile: the embedding variation is the signal you want visualized, and the face variation is the visualization language. In these applications, a learned projection from source embedding to face conditioning space is well-motivated.

For applications without this alignment — where the source embedding is arbitrary and the face is just a "visualization" in a loose sense — the projection becomes noise-dominated, and the quality of the result is bounded by the weakness of the link between source and target spaces.

## Speed Is the Fundamental Constraint

Across all the methods discussed in this chapter, the binding constraint is inference speed. Diffusion sampling with a reasonable number of denoising steps (10-50) takes 1-2 seconds per image on a high-end GPU, and there is no known way to make this dramatically faster while preserving quality. Distillation methods (progressive distillation, consistency models, Latent Consistency Models) reduce the step count to 1-8 at modest quality cost; flow matching methods (which we saw in Chapter 06 for talking heads) achieve similar speed gains with similar tradeoffs.

The practical consequence is that diffusion-based parametric face generation is an *offline* tool, not a real-time tool. You generate a face at design time, render it, cache the result, and serve it statically or with low-cost transformations at runtime. You do not put diffusion generation in a 30 FPS loop except for research demos.

For applications that need real-time generation from parametric inputs, the pattern is usually: use diffusion to generate a pool of candidate faces offline (covering the parametric space with dense sampling), and then serve those candidates at runtime based on the input parameters. This is essentially what vamp-interface does: pre-generate one face per job posting, cache them, serve statically. It is also what HeadStudio does for 3DGS avatars: generate the avatar offline (2 hours per character), then drive it at 40+ FPS.

The move toward real-time diffusion-based generation is happening slowly through architectural improvements (flow matching, latent consistency, larger step-conditional networks) but has not reached the point where diffusion can directly replace 3DGS or neural deformation for real-time applications. The division of labor — diffusion for offline generation, 3DGS or LivePortrait for real-time rendering of already-generated content — will probably remain the dominant pattern through 2027.

## Locating Diffusion-Based Parametric Generation in the Taxonomy

The three-axis classification:

- **Dimensionality:** 2D image output (though some variants produce 3D mesh output). The generation happens in 2D image space.
- **Explicitness:** Hybrid. The conditioning inputs are explicit (FLAME coefficients, ArcFace vectors, pose/lighting parameters), but the generation process and the latent space are implicit (diffusion denoising through learned UNet weights).
- **Authoring origin:** Learned (the diffusion backbone), with statistical components (FLAME-derived conditioning) and hand-authored components (architecture design, channel layout).

Operations matrix:

| Operation | Diffusion-based parametric support |
|---|---|
| Extract from photo | Via separate extractors (DECA/EMOCA/SMIRK for FLAME, ArcFace for identity) feeding into the generation model |
| Render to image | Strong, at 1-2 seconds per image |
| Edit by parameters | Strong — the defining property, with different methods giving different kinds of control |
| Interpolate between instances | Strong in the parametric input space; less clean when interpolating between arbitrary generated faces |
| Compose identity + expression | Strong for methods with dedicated channels (Arc2Face + expression adapter, RigFace); weaker for methods using ControlNet/IP-Adapter |
| Real-time driving | Not feasible — diffusion is fundamentally offline |

The summary: diffusion-based parametric face generation is the right choice when you need to produce novel identities with tight parametric control and can afford offline generation. It is the wrong choice when you need real-time animation of already-known identities (use 3DGS or neural deformation) or when you need no parametric control at all (use standard text-to-image).

## Summary

Diffusion models displaced StyleGAN and its successors as the dominant face generation framework by 2023, primarily because their broader training data provided expressive range that StyleGAN's FFHQ-trained latent space could not match. The methods that add parametric control to diffusion generation fall into several families: h-space direction-finding (cheapest, no retraining), ControlNet + IP-Adapter adapters (moderate cost, widely supported), Concept Sliders LoRA pairs (moderate cost, compositionally clean), Arc2Face-style dedicated identity channels (higher cost, better identity preservation), and fully fine-tuned FLAME-conditioned methods like RigFace and MorphFace (highest cost, best quality and tightest control). All of these methods operate at approximately 1-2 seconds per image and are fundamentally offline tools. For real-time applications, the pattern is to use diffusion for offline generation and then hand off to a faster rendering method (3DGS, neural deformation) for the actual interactive loop. The current frontier is closing the gap between "generate a novel identity offline" and "animate it in real-time," with methods like Arc2Avatar (which uses Arc2Face to generate synthetic views, then trains a 3DGS avatar on them) showing how the two paradigms can be combined. The next chapter catalogs the bridges between representations explicitly and walks through the cost and quality of each conversion.

## References

[1] Karras, T. et al. "A Style-Based Generator Architecture for Generative Adversarial Networks." CVPR 2019. StyleGAN2 (2020) and StyleGAN3 (2021) refine the architecture. The FFHQ dataset is described in the original paper.

[2] Langlois, C. et al. "Disentangled deep generative models reveal coding principles of the human face processing network." *PMC*, 2024. The FactorVAE-based disentanglement study identifying 16 semantically independent face dimensions.

[3] Gandikota, R. et al. "Concept Sliders: LoRA Adaptors for Precise Control in Diffusion Models." ECCV 2024.

[4] Kwon, M., Jeong, J., Uh, Y. "Diffusion Models Already Have a Semantic Latent Space." ICLR 2023 (Asyrp).

[5] Haas et al. "Discovering Interpretable Directions in the Semantic Latent Space of Diffusion Models." IEEE FG 2024.

[6] Zhang, L., Rao, A., Agrawala, M. "Adding Conditional Control to Text-to-Image Diffusion Models." ICCV 2023 (ControlNet).

[7] Ye, H. et al. "IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models." 2023.

[8] Papantoniou, F.P. et al. "Arc2Face: A Foundation Model for ID-Consistent Human Faces." ECCV 2024 Oral. arXiv:2403.11641. `github.com/foivospar/Arc2Face`.

[9] "ID-Consistent, Precise Expression Generation with Blendshape-Guided Diffusion." ICCVW 2025. arXiv:2510.04706. Arc2Face's expression adapter paper.

[10] Wei, M., Varanka, T., Li, X., Jiang, H., Khor, H.Q., Zhao, G. "Towards Consistent and Controllable Image Synthesis for Face Editing" (method name: RigFace). arXiv:2502.02465, February 2025. `github.com/weimengting/RigFace`, `huggingface.co/mengtingwei/rigface`.

[11] MorphFace. CVPR 2025. arXiv:2504.00430. 3DMM-guided diffusion with context blending.

[12] "Multimodal Conditional 3D Face Geometry Generation." arXiv:2407.01074, 2024. FLAME parameters as one of several conditioning modalities via IP-Adapter-style cross-attention.

See also: `vamp-interface/docs/research/2026-04-12-embedding-to-face-latent-arithmetic-2026.md` for the h-space and direct-embedding analysis, `vamp-interface/docs/research/2026-04-12-rigface-technical-deep-dive.md` for the detailed RigFace architecture breakdown, `vamp-interface/docs/research/2026-04-12-stylegan-vs-diffusion-decision-review.md` for the review of why StyleGAN was displaced, and `vamp-interface/docs/research/2026-04-12-3dmm-flame-diffusion-vtuber-realtime.md` for the broader 3DMM+diffusion survey.
