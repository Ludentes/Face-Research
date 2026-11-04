# A Deployment Benchmark of Popular Open-Source Talking-Avatar Models Released in 2025-2026

**Ethan Jiang, Tight Studio**<br>
Technical report 1.0.0 - August 29, 2026<br>
Benchmark observation date: August 23, 2026

## Abstract

Talking-avatar projects increasingly claim real-time generation, identity preservation, expressive motion, and long-duration stability, but their published examples use different portraits, speech, resolutions, hardware, and timing boundaries. We evaluated every project that met two predeclared eligibility rules on August 23, 2026: an official usable release during the prior year and more than 1,000 GitHub stars. Seven projects qualified. Six produced videos from the same public portrait and 3.63-second narration; LTX-2.3 DubIt was blocked before GPU allocation because the official checkpoint required approval unavailable to the test environment.

The completed official pipelines occupied a wide infrastructure range. Peak VRAM varied from 5,763 MiB for SoulX-FlashHead Lite to 61,401 MiB for LiveAvatar. End-to-end measured generation time ranged from 181.44 seconds for LiveAvatar to 780.29 seconds for Wan2.2-S2V. Qualitative inspection found LiveAvatar to be the sharpest heavyweight result, EchoMimicV3-Flash the strongest practical balance on a 48 GB-class GPU, LongCat-Video-Avatar 1.5 the most expressive, and FlashHead Lite the least memory-intensive. These findings characterize deployable official paths, not architecture-only speed or a controlled human-preference ranking.

## 1. Research question

Which recent, meaningfully adopted open-source talking-avatar projects can turn a single portrait and short narration into a convincing talking video, and what does each official runnable path require in time, memory, storage, and compute cost?

The question is intentionally narrower than “which model is best.” Deployment decisions combine visual behavior with the ability to obtain weights, install the official stack, fit the model into available GPU memory, amortize compilation, and serve outputs at a sustainable cost.

## 2. Cohort selection

A model qualified only when both conditions were true on August 23, 2026:

1. Its first official usable code and weights were released from August 23, 2025 through August 23, 2026.
2. Its official GitHub repository had more than 1,000 stars.

GitHub stars measure attention rather than scientific or product quality. For Wan2.2 and LTX-2.3, the count belongs to the parent project because the avatar feature ships within that repository. Projects released before the cutoff were excluded even when they remained popular.

| Model | Stars | First public release | Official input | Outcome |
|---|---:|---|---|---|
| Wan2.2-S2V-14B | 17,261 | 2025-08-26 | Image + audio; optional pose | Completed |
| LTX-2.3 DubIt | 9,226 | 2026-05-11 | Voiced video + target text | Blocked by gated checkpoint |
| LongCat-Video-Avatar 1.5 | 7,515 | 2026-05-21 | Image + audio | Completed |
| LiveAvatar | 2,384 | 2025-12-08 | Image + audio | Completed |
| SoulX-FlashTalk | 1,476 | 2026-01-08 | Image + audio | Completed |
| EchoMimicV3-Flash | 1,025 | 2026-01-22 | Image + audio | Completed |
| SoulX-FlashHead | 1,006 | 2026-02-12 | Image + audio | Completed |

## 3. Inputs and ethics

Every successful run used the same frame from a silent, AI-generated Pexels video by AI25.Studio. The reference creator does not endorse the comparison. The narration said, “Open source avatar models can now generate convincing videos from one image.” Its duration was 3.63 seconds.

The original internal runs used a macOS system voice. Because Apple's current software license does not permit public redistribution of System Voice output, this repository does not include the source waveform and publishes muted MP4s. The visual bitstreams were copied without re-encoding. Researchers reproducing this benchmark should use speech they own or are licensed to publish. See `ASSET_NOTICES.md` for the complete boundary.

Talking-avatar technology can be used for consensual localization, accessibility, education, and presentation workflows, but also for impersonation and fraud. The runners should be used only with authorized identities and voices. The benchmark does not evaluate watermarking, disclosure, provenance metadata, abuse resistance, or deepfake detection.

## 4. Execution environment and pinning

All projects ran on Modal in model-specific CUDA containers. Each runner pins the official Git repository commit and every downloaded checkpoint revision. Model weights were stored on persistent Modal Volumes before timed generation. The measured interval begins when the generation container starts and ends when the final MP4 is ready to return. It therefore includes container startup, model loading, preprocessing, inference, decoding, and muxing while excluding the one-time internet download of weights.

The runners call official inference entry points with minimal compatibility changes. These changes primarily pin PyTorch/CUDA combinations, install missing reader dependencies, set single-GPU distributed variables where required, and choose documented quantized or distilled paths. They do not modify model architectures or replace official checkpoints.

Model-specific prompts are preserved because the official interfaces and conditioning conventions differ. All models receive the same visual identity and spoken content, but this is not a prompt-identical experiment.

## 5. Measurements

We recorded:

- wall-clock generation-function time;
- peak total GPU memory reported by `nvidia-smi`, polled every 0.5 seconds while the official inference subprocess ran;
- output duration, dimensions, and frame rate;
- persistent model-cache size;
- an estimated Modal compute charge for requested GPU, CPU, and memory over the measured function duration; and
- normalized waveform correlation between supplied and output audio.

The always-on monthly column is a GPU-only capacity estimate for 720 hours using the least expensive Modal GPU class we expected to run the measured configuration without redesign. It is not a minimum bill: Modal can scale to zero. CPU, memory, volumes, and transfer are additional.

## 6. Quantitative results

| Model | GPU | Peak VRAM | Time | Output | Est. compute | Cache |
|---|---:|---:|---:|---:|---:|---:|
| Wan2.2-S2V-14B | H200 | 58,681 MiB | 780.29 s | 512 x 896, 16 fps | $1.3692 | 45.76 GiB |
| LTX-2.3 DubIt | None | None | Blocked | No output | $0 GPU | Gated |
| LongCat-Video-Avatar 1.5 | H200 | 46,827 MiB | 233.08 s | 480 x 832, 25 fps | $0.4011 | 44.82 GB |
| LiveAvatar | H200 | 61,401 MiB | 181.44 s | 384 x 704, 25 fps | $0.3184 | 47.03 GiB |
| SoulX-FlashTalk | H200 | 57,805 MiB | 331.93 s | 416 x 720, 25 fps | $0.5825 | 51.07 GiB |
| EchoMimicV3-Flash | L40S | 33,726 MiB | 251.94 s | 480 x 848, 25 fps | $0.2120 | 22.28 GiB |
| SoulX-FlashHead Lite | L40S | 5,763 MiB | 235.31 s | 512 x 512, 25 fps | $0.1980 | 7.60 GiB |

None of the successful cold jobs generated faster than playback duration. LiveAvatar had the smallest observed real-time factor at 48.77x, while Wan required 204.64 seconds of measured work per output second. FlashTalk and FlashHead cold results include first-request TorchInductor compilation. Later chunks were much faster: approximately 3.75 seconds for FlashTalk and 0.19 seconds for FlashHead, so a warmed streaming service would have different latency economics.

The measured VRAM results form three practical groups. FlashHead Lite clearly fits below 16 GB. EchoMimic fits comfortably in a 48 GB class. LongCat's 46,827 MiB is too close to a nominal 48 GB ceiling for comfortable operational headroom, while Wan, LiveAvatar, FlashTalk, and LongCat are safest on 80 GB-class hardware for these configurations.

## 7. Qualitative observations

### 7.1 Wan2.2-S2V-14B

Wan preserved identity and background well and kept facial movement restrained. The 16 fps result was less fluid than the 25 fps outputs. It was the slowest completed run by a wide margin and its estimated compute cost was more than four times LiveAvatar's. The official setup also required packages used by audio and video readers before inference could start; failed pre-denoising attempts are excluded from timing.

### 7.2 LongCat-Video-Avatar 1.5

LongCat produced the most visible performance, including head, face, upper-body motion, and a hand gesture absent from the reference image. Identity remained recognizable, although several mouth frames looked exaggerated. The official example uses two GPUs; the benchmark used one H200 with context parallelism set to one and the eight-step INT8 path.

### 7.3 LiveAvatar

LiveAvatar delivered the sharpest identity, convincing mouth shapes, blinking, and restrained expression among the heavyweight models. Its four-step FP8 path was the fastest successful H200 job. It remained a large deployment: peak VRAM was 61,401 MiB, and the final VAE decode relied on model offloading. The upstream single-GPU runner also required distributed-process environment variables and was run with compilation disabled.

### 7.4 SoulX-FlashTalk

FlashTalk produced a stable face with clear mouth motion and is designed for chunked continuous generation. Its first chunk took 119.58 seconds because TorchInductor compiled the graph; later chunks took about 3.75 seconds. The full cold job peaked at 57,805 MiB and used the largest cache in the study, 51.07 GiB.

### 7.5 EchoMimicV3-Flash

EchoMimic offered the strongest balance for deployment. Its 1.3B, eight-step path preserved the face, produced clean 25 fps motion, and ran on an L40S rather than an H200. Motion was subtler than LongCat's, with fewer distracting full-frame changes. The observed 33,726 MiB peak corresponds to the official 768-area configuration and is not a claim about the project's theoretical minimum-memory modes.

### 7.6 SoulX-FlashHead Lite

FlashHead Lite used only 5,763 MiB, roughly one-tenth of the large generators. Its first chunk took 155.7 seconds because of compilation; later chunks took about 0.19 seconds. The result was tightly cropped, softer in identity, and weaker in mouth movement than the alternatives. It is most interesting when memory and warm streaming speed matter more than presentation polish.

### 7.7 LTX-2.3 DubIt

DubIt differs from the six image-and-audio pipelines. It accepts a voiced reference video and target text, then aims to create matching speech and mouth motion while retaining vocal identity. The official `Lightricks/LTX-2.3-22b-IC-LoRA-DubIt` checkpoint returned an authorization error during CPU-only weight preparation. We did not use an unofficial mirror or allocate a GPU, so the result is recorded as blocked rather than failed inference.

## 8. Voice behavior

The six completed models animate supplied speech and mux that speech into their output; they do not select or clone a voice. Correlation with the aligned input waveform ranged from 0.999198 to 0.999897. The small differences are consistent with resampling and AAC encoding rather than creation of a different speaker.

DubIt is the exception in interface design: it takes target text and learns vocal identity from a voiced reference video. That makes it a dubbing system rather than a waveform-preserving image animator.

## 9. Deployment interpretation

- **Use LiveAvatar** when the sharpest heavyweight result matters most and 80 GB-class GPU capacity is available.
- **Use EchoMimicV3-Flash** when quality, cache size, and 48 GB-class deployment need to balance.
- **Use LongCat-Video-Avatar 1.5** when expressive body motion matters more than conservative motion.
- **Use SoulX-FlashHead Lite** when low memory and warmed streaming speed are dominant constraints.

These recommendations describe the observed settings, not every mode advertised by each project. Compilation, batching, longer sequences, parallelism, consumer GPUs, lower-resolution modes, and quantization can materially change the result.

## 10. Limitations

1. **One portrait and one short English sentence.** The benchmark does not measure demographic variation, languages, profile views, occlusion, emotion, long-duration drift, multiple speakers, or challenging audio.
2. **No blinded human study.** Visual judgments are the authors' qualitative observations, not mean-opinion scores or pairwise preference statistics.
3. **Official paths differ.** Resolution, frames per second, inference steps, quantization, prompts, and hardware are not held constant.
4. **Cold-job timing.** Compilation-heavy streaming models are disadvantaged relative to warmed service latency.
5. **VRAM polling resolution.** A 0.5-second poll can miss shorter allocation spikes.
6. **Cloud-specific cost.** Modal prices and scheduling behavior are point-in-time infrastructure observations, not universal total cost of ownership.
7. **Summary logs only.** The repository publishes normalized result records and pinned runners, but not full internal container logs or gated weights.
8. **Access can change.** A gated checkpoint may become available later, and licenses, stars, dependencies, and official recommendations may change.

## 11. Reproducibility package

The accompanying repository contains exact runner code, pinned upstream commits and checkpoint revisions, machine-readable CSV and JSON, SHA-256 checksums, the public reference frame, muted output videos, poster frames, and build/validation scripts. `REPRODUCING.md` gives the rerun commands and defines each measurement boundary.

A fully controlled follow-up should repeat several seeds per model, use rights-cleared multilingual voices and a diverse consented portrait set, separate cold-start from warmed throughput, include failure rate, and conduct a preregistered blinded perceptual study. That extension should remain a new dated dataset rather than overwrite this cohort.

## 12. Conclusion

Recent open-source talking-avatar pipelines can generate convincing short portrait videos from a single image, but deployment requirements differ by an order of magnitude. LiveAvatar led heavyweight visual quality in this test. EchoMimic came close while using a cheaper GPU and less than half the model storage of the large generators. FlashHead demonstrated that a complete generator can fit well below 16 GB, though with visible quality tradeoffs. For teams choosing a serving stack, checkpoint size, memory headroom, warm-up behavior, and access terms matter as much as the best sample frame.

## References

1. Wan-Video. [Wan2.2](https://github.com/Wan-Video/Wan2.2).
2. Lightricks. [LTX-2](https://github.com/Lightricks/LTX-2) and [DubIt guide](https://docs.ltx.io/open-source-model/feature-guides/audio/dub-it-beta).
3. Meituan. [LongCat-Video](https://github.com/meituan-longcat/LongCat-Video).
4. Alibaba Quark. [LiveAvatar](https://github.com/Alibaba-Quark/LiveAvatar).
5. Soul AI Lab. [SoulX-FlashTalk](https://github.com/Soul-AILab/SoulX-FlashTalk).
6. Ant Group. [EchoMimicV3](https://github.com/antgroup/echomimic_v3).
7. Soul AI Lab. [SoulX-FlashHead](https://github.com/Soul-AILab/SoulX-FlashHead).
8. Pexels. [Reference video](https://www.pexels.com/video/a-man-talking-to-the-camera-8136210/) and [license](https://www.pexels.com/license/).
9. Modal. [Pricing](https://modal.com/pricing), observed August 23, 2026.
