# AptAvatar: Fast and Vivid Long-Form Audio-Driven Video Generation for Production-Ready Avatars

**Links are placeholders for now and will be updated as project pages, model cards, community channels, and reports become available.**

## ✨ Key Features

- **Endpoint-Anchored Distribution Distillation**: It augments vanilla distribution matching with a dedicated Anchor Score Estimator trained on the trajectory-endpoint distribution defined from a frozen pretrained 4-step bridge generator. This provides an attainable endpoint-level anchor for the evolving two-step student.
- **Self-Generated History Replay**: It reuses cached outputs from earlier generator checkpoints as history conditions during chunk-wise training. This approximates inference-time self-conditioning, mitigating quality degradation from accumulated history errors

## 🔥 News

- **2026.06.29** - Released the initial AptAvatar repository with open-source inference code.

## 📋 Todo

- [x] Technical report
- [x] Project page
- [x] Inference code
- [x] Checkpoint release
- [ ] Additional demos

## 🧩 Pipeline

## 🎬 Examples

## 🚀 Quick Start

### 🛠️ Installation

Create and activate the environment:

```bash
conda create -n aptavatar python=3.10
conda activate aptavatar
```

Install PyTorch:

```bash
pip install torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Install FlashAttention:

```bash
pip install ninja
pip install flash_attn==2.8.0.post2 --no-build-isolation
```

> [!NOTE]
> If `flash_attn_3` is installed in your environment, please uninstall it, as it conflicts with the FlashAttention-3 kernels bundled in `xformers`:
>
> ```bash
> pip uninstall flash_attn_3
> ```

Install FFmpeg:

```bash
# Ubuntu / Debian
apt-get install ffmpeg

# CentOS / RHEL
yum install ffmpeg ffmpeg-devel
```

or install through conda:

```bash
conda install -c conda-forge ffmpeg==7
```

### 📦 Model Preparation

The current repository provides inference code only. After checkpoints are released, place them under the following paths:

| Component | Expected Path | Status |
| --- | --- | --- |
| AptAvatar checkpoint | `models/AptAvatar` | [AptAvatar](https://huggingface.co/TaoLiveAIGC/AptAvatar) |
| Audio encoder | `models/chinese-wav2vec2-base` | [chinese-wav2vec2-base](https://huggingface.co/TencentGameMate/chinese-wav2vec2-base) |

```bash
# Placeholder commands. Replace the repository names after release.
pip install "huggingface_hub[cli]"
huggingface-cli download TaoLiveAIGC/AptAvatar --local-dir ./models/AptAvatar
huggingface-cli download TencentGameMate/chinese-wav2vec2-base --local-dir ./models/chinese-wav2vec2-base
```

### 🎥 Inference

Single-GPU inference:

```bash
bash inference_script_single_gpu.sh
```

Multi-GPU inference:

```bash
bash inference_script_multi_gpu.sh
```

The default scripts use:

```text
examples/woman.png
examples/woman.wav
examples/woman.txt
```

You can edit the shell scripts or call `generate_video.py` directly with your own image, audio, and prompt.

### 📝 Structured Prompt

Besides free-form prompts, AptAvatar supports **structured prompts** that describe the motion step by step with explicit frame ranges. See [examples/woman_template.txt](examples/woman_template.txt) for full examples. Each prompt follows the format:

```text
步骤1：*帧
~
*
步骤2：*帧
~
*
步骤3：*帧
~
*

```

- Each step starts with `步骤x：` followed by a frame range marker `*帧 xx~xx*` and a motion description.
- We recommend using **1~3 steps** per prompt.

Example:

```text
步骤1：*帧 0~20*女主播面向镜头站立，右手先抬起至胸前高度并张开手掌，掌心朝前，身体保持稳定，视线面向镜头。步骤2：*帧 25~45*她的右手由张开状态逐渐收拢成松拳，手腕和手指动作清晰，头部和身体保持正向稳定。步骤3：*帧 50~70*女主播左手随后抬起至与右肩相近的高度，双手同时张开并向身体两侧展开，形成对称的展示姿态后保持定格。
```

## 📊 Evaluation Results

We evaluate AptAvatar on our internal short-form benchmark for audio-driven avatar generation. Results will be reported at **720p**.

### Metrics

| Category | Metrics | Direction |
| --- | --- | --- |
| Audio-Visual Alignment | Sync-C, Sync-D | Sync-C higher is better; Sync-D lower is better |
| Image Quality | FID | Lower is better |
| Aesthetic Analysis | ASE, Q-Align | Higher is better |
| VBench | Subject Consistency (Subject-C), Background Consistency (BG-C), Motion Smoothness (Motion-S), and Temporal
Flickering (Temporal-F) | higher is better |

### Compared Methods

| Group | Method | NFE |
| --- | --- | ---: |
| Many-NFE | InfiniteTalk | 120 |
| Many-NFE | Wan-S2V | 80 |
| Few-NFE | LongCat-Video-Avatar 1.5 | 8 |
| Few-NFE | LiveAvatar | 4 |
| Few-NFE | SoulX-FlashTalk | 4 |
| Few-NFE | AptAvatar | 2 |

### 720p Results on our internal short-form benchmark

| Method | Group | NFE | Sync-C ↑ | Sync-D ↓ | FID ↓ | ASE ↑ | Subject-C ↑ | BG-C ↑ | Motion Smoothness ↑ | Temporal Flickering ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| InfiniteTalk | Many-NFE | 120 | 7.172 | 8.010 | 24.808 | 3.146 | 96.889 | 95.568 | 99.512 | 99.318 |
| Wan-S2V | Many-NFE | 80 | 5.626 | 9.376 | 43.542 | 3.119 | 97.151 | 95.663 | 99.385 | 99.216 |
| LongCat-Video-Avatar 1.5 | Few-NFE | 8 | 4.140 | 11.433 | 36.582 | 3.191 | 96.338 | 94.533 | 99.550 | 99.332 |
| LiveAvatar | Few-NFE | 4 | 5.986 | 8.586 | 37.868 | 3.184 | 97.804 | 95.718 | 99.409 | 99.226 |
| SoulX-FlashTalk | Few-NFE | 4 | 7.743 | 7.912 | 28.039 | 3.172 | 98.580 | 96.530 | 99.550 | 99.434 |
| **AptAvatar** | **Few-NFE** | **2** | **7.865** | **7.739** | **24.759** | **3.307** | **98.589** | **96.844** | **99.561** | **99.456** |

## 📁 Repository Layout

```text
AptAvatar/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── requirements.txt
├── config.json
├── generate_video.py
├── gradio_app.py
├── inference_script_single_gpu.sh
├── inference_script_multi_gpu.sh
├── examples/
│ ├── woman.png
│ ├── woman.wav
│ └── woman.txt
├── assets/
│ └── *.mp4
├── sample_results/
│ └── *.mp4
├── models/ # created after downloading checkpoints
│ ├── AptAvatar/
│ │ ├── config.json
│ │ ├── configuration.json
│ │ ├── diffusion_pytorch_model-0000*-of-00008.safetensors
│ │ ├── diffusion_pytorch_model.safetensors.index.json
│ │ ├── Wan2.1_VAE.pth
│ │ ├── models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth
│ │ ├── models_t5_umt5-xxl-enc-bf16.pth
│ │ ├── google/
│ │ │ └── umt5-xxl/ # T5 tokenizer files
│ │ └── xlm-roberta-large/ # CLIP tokenizer files
│ └── chinese-wav2vec2-base/
│ ├── config.json
│ ├── preprocessor_config.json
│ └── pytorch_model.bin
└── AptAvatar/
├── inference.py
├── configs/
├── infinite_talk/
├── src/
└── wan/
```

## ⚖️ License Agreement

This repository is released under the **Apache License 2.0**. See [LICENSE](LICENSE) for the full license text.

The current release contains inference code. Model weights, datasets, benchmark assets, demo media, and third-party dependencies may be released under separate terms when they become available. Users are responsible for checking and complying with the licenses of all external models, datasets, audio encoders, and media assets used with this repository.

## ⚠️ Usage Considerations

AptAvatar is intended for research and responsible application development in audio-driven avatar video generation. Users should carefully evaluate outputs before deployment, especially in identity-sensitive, public-facing, or commercial scenarios.

- Obtain appropriate rights and consent for all input images, audio, prompts, and generated likenesses.
- Do not use the system to impersonate real people, mislead audiences, or generate deceptive content.
- Clearly disclose synthetic or AI-generated avatar content when required by law, platform policy, or product context.
- Test robustness across languages, accents, speaking styles, lighting conditions, identities, and long-form generation settings before production use.
- Follow applicable laws and regulations related to privacy, biometric data, publicity rights, copyright, and content safety.

## 📚 Citation

Citation information will be added after the technical report is released.

```bibtex
@misc{taoavatar2026,
title = {AptAvatar: Fast and Vivid Long-Form Audio-Driven Video Generation for Production-Ready Avatars},
author = {TBD},
year = {2026},
archivePrefix = {arXiv},
eprint = {TBD},
primaryClass = {cs.CV},
url = {TBD}
}
```

## 🙏 Acknowledgements

AptAvatar builds on the progress of the open-source video generation and audio-driven avatar communities. We sincerely thank the authors and contributors of the following projects:

- [InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk) and [Wan](https://github.com/Wan-Video/Wan2.1): foundational video generation and audio-conditioned avatar backbones that AptAvatar builds upon.
- [Self-Forcing](https://github.com/guandeh17/Self-Forcing): an important reference codebase for long-horizon self-conditioned video generation.
- [DMD](https://github.com/tianweiy/DMD2) and [Self-Forcing++](https://github.com/justincui03/Self-Forcing-Plus-Plus): key references for distribution matching distillation and self-forcing-style training.

> [!TIP]
> If you find AptAvatar useful, please also consider starring the original repositories of these foundational methods.
