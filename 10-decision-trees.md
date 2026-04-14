# Chapter 10 — Decision Trees by Use Case

## The Purpose of This Chapter

The preceding chapters established vocabulary, surveyed the worlds, and cataloged the bridges between them. This chapter folds everything into practical guidance: *given a specific use case, which stack should you build on, and why*. The format is decision trees — sets of questions that narrow the options at each step until a recommendation emerges. The decision trees are opinionated; they reflect the judgments this review has been building up, and readers should feel free to push back on them if their situation has specifics the tree does not capture.

The use cases covered are:

1. **VTubing — professional creator**
2. **VTubing — casual / novelty**
3. **Real-time AI assistant with face**
4. **Dubbing / translation talking-head synthesis**
5. **Data visualization via faces**
6. **Synthetic face data generation for ML training**
7. **Spatial computing / VR avatar**
8. **Photorealistic portrait editing at scale**
9. **Portrait animation from a single image (zero rigging)**
10. **Research on face animation itself**

Each section presents the decision tree, the recommendation, the reasoning, and the typical pitfalls. The trees are meant to be read end-to-end once and then consulted as a reference when specific decisions arise.

## Use Case 1: VTubing — Professional Creator

**Context.** A creator who wants to build or commission a VTuber avatar they will use for streaming, who cares about the specific aesthetic of their character, who is willing to invest time and money in the initial setup, and who expects to use the avatar for hundreds of hours of live content.

**Key questions:**

*Do you need photorealism?* Almost certainly not. The VTubing aesthetic is anime-stylized and the audience expects that. Photorealism actively hurts you in this market.

*Do you have a specific character design in mind, or are you willing to use a generated one?* For a professional creator, the character is the brand. Specific design is the norm. Generated designs are only acceptable if they are used as a starting point and then heavily customized.

*Do you want to commission the work or automate it?* Commission is the default for professional creators. Automation tools in 2026 are not good enough to replace skilled riggers for top-tier work.

**Recommendation:** Commission a custom Live2D Cubism rig from a professional rigger ($1,500-5,000 for mid-to-high tier). Drive via VTube Studio on Windows/Mac with ARKit input from iPhone (Live Link Face) or OpenSeeFace on webcam. Include ARKit-compatible mouth blendshape parameters in the rig specification so that future tracking upgrades work seamlessly. Budget 4-8 weeks for the full delivery cycle including revisions.

**Why not something else?**
- *3DGS avatars* are not yet production-quality for the anime aesthetic that professional VTubers want. They excel at photorealism, which is the wrong goal.
- *LivePortrait* produces video-like output that VTubers find uncanny and unstable compared to hand-rigged Live2D.
- *Inochi2D* is technically viable but has a smaller ecosystem and few professional riggers work in it.
- *Automation tools* (Textoon, CartoonAlive) produce rigs that are acceptable for casual use but do not meet the quality bar for professional creators.

**Pitfalls.** Be specific about the parameter set in the commission brief — a rig delivered with only classic Live2D parameters (no ARKit mouth blendshapes) will be harder to drive with modern trackers. Ask for the `.cmo3` source file, not just the `.moc3` output, so you can edit later. Verify that the rigger's contract allows you to commission follow-up modifications (new expressions, outfit variants) rather than creating vendor lock-in.

## Use Case 2: VTubing — Casual / Novelty

**Context.** A creator who wants to stream as a character without commissioning a rig, who may not have a specific character in mind, and who is willing to accept some quality compromise in exchange for speed and cost. "I want to stream as my selfie" or "I want to stream as this anime illustration I found."

**Key questions:**

*Do you have an existing image (photo or illustration) you want to animate?* Yes, usually.

*Do you need the traditional VTubing aesthetic, or is "my face in motion" acceptable?* Usually the latter, for this segment.

*How important is installation simplicity versus output quality?* Simplicity usually wins.

**Recommendation:** Use FasterLivePortrait with a virtual camera wrapper piped into OBS. For anime-illustration sources, try the model on the illustration directly; if the warp artifacts are too visible, pre-process with a style-preserving image filter or use Thin-Plate Spline Motion Model as an alternative that handles illustrations slightly better.

For a step up in quality without commissioning a rig: use Textoon to generate a Live2D character from a text description and drive it via VTube Studio. This produces a more stable VTubing output than LivePortrait at the cost of giving up the specific-face-of-a-specific-person requirement.

**Why not something else?**
- *Commissioning a rig* is the better quality path but is out of scope for this use case by definition.
- *3DGS avatars* require capture and are overkill.
- *CartoonAlive* assumes already-anime input and does not solve the photo-to-anime problem.
- *Viggle LIVE* has 1-2 second latency which is unacceptable for live streaming.

**Pitfalls.** Test the LivePortrait pipeline end-to-end with your actual streaming setup before committing — the virtual camera integration on Windows has historically been finicky. Expect occasional artifacts; this is the tradeoff for the zero-rigging workflow.

## Use Case 3: Real-Time AI Assistant with Face

**Context.** Building a virtual assistant (chatbot with voice, AI concierge, automated customer service agent) that needs a face to speak the output. The identity is fixed — you want a single brand-consistent face that every user sees. Real-time response matters: latency from input to face animation should be under 500 ms.

**Key questions:**

*Is the identity fixed or per-user?* Fixed for this use case.

*Do you need lip sync accuracy or natural head motion matters equally?* Both, but lip sync is primary.

*What's the deployment platform?* Cloud-server with GPU, or on-device mobile?

**Recommendation (cloud deployment):** Build a 3DGS avatar of your chosen brand identity using GaussianAvatars or FlashAvatar from a professional recording session (one hour of multi-view video). At runtime, drive via NVIDIA Audio2Face (audio → ARKit blendshapes) → ARKit-to-FLAME solver → 3DGS rendering. Expected end-to-end latency: ~100-200 ms including LLM inference. Frame rate: 60+ FPS on a single consumer GPU.

**Recommendation (mobile deployment):** Use SplattingAvatar with the same pipeline. Expected frame rate: 30 FPS on iPhone 13+, with slightly lower output resolution (256²-384²).

**Recommendation (lower budget):** Use SadTalker with a high-quality reference image of your brand identity. Lower quality than 3DGS but production-viable and simpler to deploy.

**Why not something else?**
- *LivePortrait* is great for motion transfer but is not designed for audio-driven lip sync; the pipeline to get audio to drive it is multiple stages with quality loss.
- *Live2D* is aesthetically wrong for most professional assistant use cases (anime stylization does not match enterprise branding).
- *Pure diffusion methods* (EMO, Hallo) are offline-only and cannot hit real-time latency.
- *FLOAT* is close to real-time but still noticeably slower than 3DGS + Audio2Face.

**Pitfalls.** Budget for the capture session — an hour of multi-view video of a person is logistically nontrivial (studio, cameras, lighting, talent release forms). Test with representative audio: models trained on English may produce wrong mouth shapes for other languages. Plan for the "resting face" problem — an idle avatar that just waits for input needs subtle idle animation or it looks disconcerting.

## Use Case 4: Dubbing / Translation Talking-Head Synthesis

**Context.** Taking a pre-recorded video and replacing the audio with new content (e.g., translated speech) while making the speaker's mouth match the new audio. The identity is a specific person in the source video; the new audio is provided. Offline processing is acceptable.

**Key questions:**

*Do you need full-face animation or just mouth region?* Mouth region is usually enough for translation dubbing where you want to preserve the speaker's original head motion and expressions.

*Do you have time for high-quality offline processing or do you need fast turnaround?* Depends on volume — one-off commercial dubbing allows offline quality; high-volume localization needs fast turnaround.

*Is the source video high quality?* Usually yes for professional dubbing.

**Recommendation (mouth-only, fast turnaround):** MuseTalk. 30 FPS processing on consumer GPUs, MIT license, mature tooling, very good lip sync quality within its region-limited scope. Production deployed at scale in several commercial products.

**Recommendation (full-face, best quality):** Hallo or EchoMimic for offline high-quality full-face synthesis. Seconds per second of output, but the quality is worth it for premium content.

**Recommendation (voice-first pipeline that generates both TTS and face):** OmniTalker is designed specifically for the text → TTS → talking-head chain and produces coherent results at 25 FPS.

**Why not something else?**
- *Wav2Lip* is legacy and produces visibly flatter output than current methods. Only use if you need specific licensing or legacy compatibility.
- *FLOAT* is close to state-of-the-art but MuseTalk is simpler for region-only dubbing.
- *3DGS avatar methods* require per-identity capture, which is not applicable when the source is a pre-existing video of an unknown subject.

**Pitfalls.** For translation dubbing, expect some phoneme mismatch when the source and target languages have different phoneme inventories — English "th" sounds do not have clean equivalents in many languages and the mouth shapes the model produces may look slightly wrong. Test on representative segments before committing to a pipeline.

## Use Case 5: Data Visualization via Faces

**Context.** Using face generation to encode multidimensional data points in a visualization. Each data record (a job posting, a user profile, a time-series sample) is rendered as a face whose appearance encodes the record's values. The goal is that humans can rapidly absorb the data by looking at many faces and noticing patterns via face perception rather than feature-by-feature reading.

**Key questions:**

*Photorealistic or stylized faces?* Photorealistic, probably — the holistic "something is wrong with this face" mechanism that makes this visualization approach interesting depends on real-face perception.

*How many distinct data records, and how often do they change?* If thousands of records that rarely change, you can pre-generate and cache. If real-time data feed, you need a fast generation path.

*Is continuity important?* Nearby points in data space should produce nearby faces. This is a core requirement for the visualization to work.

**Recommendation:** Pre-generate faces offline using a diffusion model with parametric conditioning. Specifically: use a fixed anchor face per cluster (from a handful of text-query-derived anchors in your embedding space), and apply parametric edits to encode each record's deviations from its cluster. For best quality use h-space direction-finding in Flux or a similar modern diffusion model, or use Concept Sliders LoRAs for compositional edits. Cache the resulting images and serve them statically.

For continuous encoding specifically: use denoising strength as the primary axis that moves a face away from its anchor (low strength → close to anchor, high strength → further from anchor with uncanny valley emerging). This is the approach vamp-interface takes, and it works well for the fraud-signal-through-uncanny-valley visualization goal.

**Why not something else?**
- *Live2D* is stylized and cannot produce the uncanny valley effect that is load-bearing for the visualization mechanism.
- *LivePortrait* animates an existing face rather than generating a new one, so it is the wrong tool for per-record face generation.
- *3DGS avatars* require per-identity capture, which would require pre-building thousands of avatars — impractical.
- *StyleGAN* has the FFHQ expression range problem and cannot produce the uncanny drift that makes the visualization mechanism work.
- *Real-time diffusion* is not yet feasible, so pre-generation is the only practical pattern.

**Pitfalls.** Verify the continuity property empirically — nearby data points should produce visually similar faces. This is harder than it sounds because diffusion sampling is stochastic, and a small change in input may produce a large change in output if the seed or noise schedule is not fixed. Use fixed seeds per data record and test continuity by perturbing inputs slightly. Plan for the "face identity collision" problem — different records producing nearly-identical faces — which happens when the parametric variation you are encoding is too small relative to the diffusion model's natural variance.

## Use Case 6: Synthetic Face Data Generation for ML Training

**Context.** Generating large numbers of synthetic face images with controlled attributes (age, ethnicity, expression, pose, lighting) to train downstream face recognition, liveness detection, or expression classification models. The data needs to be diverse, parametrically controllable, and legally clean (no real identities).

**Key questions:**

*Do you need identity diversity or expression diversity as the primary axis?* Usually both.

*Do you need the data to match a specific target distribution (e.g., matching the demographics of a deployment population)?* Often yes.

*What's your scale — thousands of images or millions?*

**Recommendation:** MorphFace if its code becomes available, otherwise Arc2Face + expression adapter (the only fully-released option in this lineage). RigFace is architecturally the most ambitious but is currently weights-only with no inference code (see Chapter 08). All provide parametric control over FLAME-based attributes that supervised face learning benefits from. Generate in batches offline. For millions of images, plan for a week-long generation run on a GPU cluster.

For a cheaper alternative that does not require FLAME-conditioned diffusion fine-tuning: Arc2Face + the expression adapter, with programmatic variation of the ArcFace embedding and the FLAME expression vector.

**Why not something else?**
- *StyleGAN* was the default for this use case in 2020-2022 but has been displaced by diffusion for reasons of expression range and quality.
- *Stable Diffusion with text prompts* produces diverse faces but without reliable parametric control over the attributes that matter for ML training.
- *3DGS avatars* are per-identity and inappropriate for generation of diverse new identities.
- *Commercial synthetic face data services* (Datagen, Synthesis AI) are options for teams that prefer not to run their own generation pipelines. They charge per-image or per-dataset.

**Pitfalls.** Verify that the generated data does not leak memorized identities from the training set — diffusion models can memorize training images and produce near-identical outputs, which would undermine the "no real identities" property. Use nearest-neighbor checks against the training data before distributing the synthetic dataset. Document the generation pipeline thoroughly for downstream users who need to understand the distribution properties.

## Use Case 7: Spatial Computing / VR Avatar

**Context.** Building face avatars for VR social applications (VRChat, Meta Horizon, Apple Vision Pro ecosystems) where the user has a VR headset, needs their avatar to render in a 3D scene, and expects the face to be driven by the headset's face tracking sensors.

**Key questions:**

*What's the target platform — Apple Vision Pro, Meta Quest Pro, desktop VR, or multiple?*

*Does the user need photorealism or stylization?* For social VR, both are in demand depending on the specific community.

*Is the avatar per-user (Personal avatar) or a fixed character (Role-play)?*

**Recommendation (personal photorealistic avatar):** 3DGS avatar built via a one-time capture session, rigged with FLAME, driven by the headset's ARKit-compatible face tracking. SplattingAvatar for mobile-VR efficiency, or GaussianAvatars for higher-end desktop VR quality. This is the direction Meta Codec Avatars pointed and that the open-source ecosystem is catching up to.

**Recommendation (stylized fixed character):** VRM avatar in the Unity or Unreal ecosystem, authored once by an artist, driven by ARKit blendshape input. Not 3DGS, not photorealistic, but much cheaper and more flexible for iterative character design.

**Recommendation (unsure which direction):** Start with VRM for stylization + the existing VR content ecosystem, and plan to add 3DGS avatar support as a premium feature.

**Why not something else?**
- *Live2D* is 2D and does not work in VR because VR needs novel-view synthesis.
- *LivePortrait* is 2D and does not work in VR for the same reason.
- *Diffusion-based real-time generation* is not feasible for the real-time VR loop.
- *NeRF avatars* have been superseded by 3DGS.

**Pitfalls.** Test on the actual target hardware early. VR frame rate requirements are strict (90 Hz minimum for most headsets) and mobile VR (Quest) has limited GPU budget. Budget for the capture session if going the 3DGS route. Handle the privacy implications of having a 3D scan of the user's face — users should be able to delete their avatar data on demand.

## Use Case 8: Photorealistic Portrait Editing at Scale

**Context.** Editing photos of people — changing expressions, pose, lighting — for marketing content, stock photography, or consumer photo apps. High quality is required; speed can be traded off for quality.

**Recommendation:** RigFace is the strongest architecture on paper (full fine-tuned SD 1.5 with FLAME conditioning for expression, pose, and lighting, plus full-UNet identity preservation, ~1-2 s per image), but as of 2026-04-14 it is weights-only on HuggingFace (`mengtingwei/rigface`, Apache-2.0) with no inference code released — you would need to reverse-engineer the loader from the paper's method section. For teams unwilling to do that, Arc2Face + expression adapter (see Use Case 9 fallback) is the next-best fully-released option.

**Alternative (for teams that want to fine-tune their own):** Take the Arc2Face + expression adapter architecture and fine-tune on your own data if you have domain-specific requirements (specific demographics, specific image distributions, specific lighting setups).

**Why not something else?**
- *StyleGAN editing* has weaker identity preservation under strong expression edits and suffers from the FFHQ expression range problem.
- *ControlNet + IP-Adapter* is looser parametric control — you are conditioning on images, not directly on semantic parameters.
- *LivePortrait* produces a warped version of the input; the output is recognizably the same photo in motion rather than a genuinely edited image.

**Pitfalls.** DECA-based FLAME extraction (used in RigFace's pipeline) degrades at extreme poses. Test on your specific image distribution before committing. Expect manual cleanup for edge cases.

## Use Case 9: Portrait Animation from a Single Image (Zero Rigging)

**Context.** A user uploads a photo; you need to animate it to match a driving video or a webcam stream. No per-user setup, no multi-view capture. The photo could be of anyone.

**Recommendation:** LivePortrait (or FasterLivePortrait for production deployment). The method was built specifically for this task, it is fast, it handles diverse inputs robustly, and the code and weights are public under MIT.

**Alternative (for mobile):** MobilePortrait if weights are available by deployment time, otherwise target a server-side LivePortrait deployment with a mobile client that uploads the photo and the driver video.

**Why not something else?**
- *3DGS avatars* require capture. Out of scope.
- *Diffusion-based generation* does not handle the "animate a specific photo" task well — it generates *new* identities.
- *Live2D* requires rigging. Out of scope.

**Pitfalls.** Quality degrades on extreme head poses and strong occlusions. Set user expectations accordingly. Plan for the mouth-interior handling — LivePortrait can produce odd results when animating from a closed-mouth photo to an open-mouth state because the interior was never visible in the source.

## Use Case 10: Research on Face Animation Itself

**Context.** A researcher extending the state of the art. The goal is not to ship a product but to publish a paper or a research artifact that advances the field.

**Recommendation:** Use FLAME as your internal representation, use one of the public extractors (DECA, EMOCA, SMIRK) as your preprocessing, and build your contribution on top of the existing ecosystem. If your contribution is on the generation side, fork RigFace or Arc2Face. If your contribution is on the avatar side, fork GaussianAvatars or 3D Gaussian Blendshapes. If your contribution is on the tracking side, benchmark against ARKit / MediaPipe on standard datasets.

**Why not something else?** Because the research community speaks FLAME and reviewers will expect comparisons against FLAME-based baselines. Building on a non-FLAME internal representation is defensible but requires extra effort to justify and benchmark.

**Pitfalls.** Verify the FLAME license applies to your intended use (CC-BY-4.0 as of 2023 is permissive for research). Watch for the extractor lineage: if your results look unusually clean, check whether you are benchmarking on easy AFFECTnet examples rather than hard SMIRK-type extremes. Cite carefully — the field has a habit of re-deriving small variations of the same architecture and it is important to credit the lineage.

## Cross-Use-Case Patterns

Several patterns repeat across use cases and are worth stating explicitly.

**Pattern 1: ARKit at the boundary, FLAME internally.** Almost every multi-component pipeline benefits from using ARKit as the external API (for input from trackers and output to animation consumers) and FLAME internally for any component that benefits from the research ecosystem's tooling. The solver between them is cheap enough that there is no reason to collapse the two.

**Pattern 2: Offline generate, real-time render.** Diffusion for generation, 3DGS or LivePortrait for real-time rendering. Diffusion cannot keep up with a 30+ FPS loop; 3DGS and LivePortrait cannot generate new identities from scratch. Using each for what it does best is the dominant architectural pattern for combined generation-plus-animation pipelines.

**Pattern 3: Capture once, serve many.** Per-identity capture is expensive (multi-view video, optimization pass) but the resulting avatar is then fast to drive and cheap to serve. For applications with a fixed identity (AI assistants, brand avatars, personal VR avatars) the one-time cost is acceptable. For applications with per-user identity (consumer photo apps, data visualization) the cost is not acceptable and you need a zero-shot method.

**Pattern 4: The right aesthetic dominates the technical choice.** VTubers want anime-stylized; spatial computing wants photorealistic; data visualization wants whichever supports the visualization mechanism. The aesthetic requirement is usually the first cut and the technical options narrow quickly once it is fixed.

**Pattern 5: The ecosystem is bigger than any single tool.** Every use case's recommendation involves combining tools from different communities: face tracking from MediaPipe, rigging from Cubism or FLAME tools, generation from Stable Diffusion with adapters, rendering from 3DGS or Live2D runtime, integration through ARKit as the wire protocol. No single tool handles all of it, and the teams that ship successful products understand the ecosystem's structure.

## When to Violate the Trees

The decision trees above are defaults. They reflect what works for most builders most of the time. Several categories of project should explicitly violate them:

- **Researchers on the frontier of a specific representation** should use that representation even if it is not the "right" choice by the tree, because the research goal is to improve the representation.
- **Teams with existing infrastructure** should weigh migration cost against the improvements the tree recommends. A pipeline that is working with a suboptimal representation is usually not worth rebuilding.
- **Builders with specific licensing constraints** may need to avoid the recommended path (e.g., needing to avoid Cubism licensing, needing to avoid FLAME's CC-BY attribution requirement) and use alternatives even at quality cost.
- **Projects with unusual requirements** (non-human faces, extreme speeds, extreme quality, specific hardware constraints) may have needs that the general trees do not address.

In these cases, read the relevant earlier chapters to understand which representations support which operations, then design the pipeline that fits the specific constraints. The trees are there to save time, not to constrain creativity.

## Summary

Face animation decisions hinge primarily on the intersection of three requirements: aesthetic register (photorealistic vs stylized), interactivity (real-time vs offline), and identity scope (fixed vs per-user). Once these are fixed, the technical choice is usually constrained to one or two viable options, and the decision trees in this chapter capture the dominant patterns. The cross-use-case patterns — ARKit-at-boundary-with-FLAME-internal, offline-generate-with-real-time-render, capture-once-serve-many — are the most robust heuristics that generalize beyond specific use cases. The next chapter addresses the market and community reality that wraps around these technical choices: what tools are actually used, where the money flows, and what the community preferences look like.

## References

This chapter is a synthesis of Chapters 02 through 09. Specific methods mentioned here have their primary references in the corresponding chapter:

- Live2D and Cubism ecosystem: Chapter 02.
- ARKit, MediaPipe, and the production tracking stack: Chapter 03.
- FLAME and its extractors: Chapter 04.
- LivePortrait and neural deformation: Chapter 05.
- Talking-head methods (MuseTalk, FLOAT, Hallo, OmniTalker, Audio2Face): Chapter 06.
- 3DGS avatars (GaussianAvatars, SplattingAvatar, 3D Gaussian Blendshapes, FlashAvatar, Arc2Avatar, HeadStudio): Chapter 07.
- Diffusion-based parametric generation (Arc2Face, RigFace, MorphFace, Concept Sliders, h-space): Chapter 08.
- Bridges between representations: Chapter 09.

Market data referenced in Use Case 1: see `vamp-interface/docs/research/2026-04-12-parametric-face-generation-market-scan.md`.
