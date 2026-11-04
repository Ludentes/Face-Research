---
license: apache-2.0
language:
- en
tags:
- portrait-animation
- real-time
- diffusion
pipeline_tag: image-to-video
library_name: diffusers
---

SoulX-FlashTalk: Real-Time Infinite Streaming of Audio-Driven Avatars via Self-Correcting Bidirectional Distillation

[Le Shen*](https://openreview.net/profile?id=%7ELe_Shen3), [Qian Qiao*](https://qianqiaoai.github.io/), [Tan Yu*](https://jiayoujiayoujiayoua.github.io/), [Ke Zhou](https://github.com/jokerz0624), [Tianhang Yu](#), [Yu Zhan](#), [Zhenjie Wang](#), [Dingcheng Zhen](#), [Ming Tao](#), [Shunshun Yin](#), [Siyuan Liu](#)
✉

*
Equal Contribution

✉
Corresponding Author

## 🔥 News
- **2026.01.08** - We have released the [inference code](https://github.com/Soul-AILab/SoulX-FlashTalk), and the [model weights](https://huggingface.co/Soul-AILab/SoulX-FlashTalk-14B).
- **2025.12.30** - We released **Project page** on [SoulX-FlashTalk](https://soul-ailab.github.io/soulx-flashtalk/).
- **2025.12.30** - We released **SoulX-FlashTalk Technical Report** on [Arxiv](https://arxiv.org/pdf/2512.23379) and [GitHub repository](./assets/SoulX_FlashTalk.pdf).

## 🤫 Coming soon
**A 4-GPU version of SoulX-FlashTalk and a new open-source real-time streaming digital human model designed specifically for consumer-grade GPUs like 4090 etc.**

## 📑 Todo List
- [x] Technical report
- [x] Project Page
- [x] Inference code
- [x] Checkpoint release
- [ ] Online demo

## 🌰 Examples

Portrait Style

Animal Animation

Fast Paced Rap

## 📖 Quickstart
### 🔧 Installation
#### 1. Create a Conda environment
```bash
conda create -n flashtalk python=3.10
conda activate flashtalk
```
#### 2. Install PyTorch on CUDA
```bash
pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu128
```
#### 3. Install other dependencies
```bash
pip install -r requirements.txt
```
#### 4. Flash-attention installation:
```bash
pip install ninja
pip install flash_attn==2.8.0.post2 --no-build-isolation
```
#### 5. FFmpeg installation
```bash
# Ubuntu / Debian
apt-get install ffmpeg
# CentOS / RHEL
yum install ffmpeg ffmpeg-devel
```
or
```bash
# Conda (no root required)
conda install -c conda-forge ffmpeg==7
```
### 🤗 Model download
| Model Component | Description | Link |
| :--- | :--- | :---: |
| `SoulX-FlashTalk-14B` | Our 14b model| 🤗 [Huggingface](https://huggingface.co/Soul-AILab/SoulX-FlashTalk-14B) |
| `chinese-wav2vec2-base` | chinese-wav2vec2-base | 🤗 [Huggingface](https://huggingface.co/TencentGameMate/chinese-wav2vec2-base) |

```bash
# If you are in china mainland, run this first: export HF_ENDPOINT=https://hf-mirror.com
pip install "huggingface_hub[cli]"
huggingface-cli download Soul-AILab/SoulX-FlashTalk-14B --local-dir ./models/SoulX-FlashTalk-14B
huggingface-cli download TencentGameMate/chinese-wav2vec2-base --local-dir ./models/chinese-wav2vec2-base
```
### 🚀 Inference
```bash
# Infer on single GPU
# Requires more than 64G of VRAM
bash inference_script_single_gpu.sh

# Infer on multy GPUs
# Real-time inference speed can only be supported on 8xH800 or higher graphics cards
bash inference_script_multi_gpu.sh
```

### 👋 Online Demo
Coming Soon!

## 📧 Contact Us
If you are interested in leaving a message to our work, feel free to email le.shen@mail.dhu.edu.cn or qiaoqian@soulapp.cn or yutan@soulapp.cn or zhouke@soulapp.cn or liusiyuan@soulapp.cn

You’re welcome to join our WeChat group for technical discussions, updates.

## 📚 Citation

If you find our work useful in your research, please consider citing:

```
@misc{shen2025soulxflashtalktechnicalreport,
title={SoulX-FlashTalk: Real-Time Infinite Streaming of Audio-Driven Avatars via Self-Correcting Bidirectional Distillation},
author={Le Shen and Qian Qiao and Tan Yu and Ke Zhou and Tianhang Yu and Yu Zhan and Zhenjie Wang and Ming Tao and Shunshun Yin and Siyuan Liu},
year={2025},
eprint={2512.23379},
archivePrefix={arXiv},
primaryClass={cs.CV},
url={https://arxiv.org/abs/2512.23379},
}
```

## 🙇 Acknowledgement
- [Infinitetalk](https://github.com/MeiGen-AI/InfiniteTalk) and [Wan](https://github.com/Wan-Video/Wan2.1): the base model we built upon.
- [Self forcing](https://github.com/guandeh17/Self-Forcing): the codebase we built upon.
- [DMD](https://github.com/tianweiy/DMD2) and [Self forcing++](https://github.com/justincui03/Self-Forcing-Plus-Plus): the key distillation technique used by our method.
> [!TIP]
> If you find our work useful, please also consider starring the original repositories of these foundational methods.

## 💡 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Soul-AILab/SoulX-FlashTalk&type=date&legend=top-left)](https://www.star-history.com/#Soul-AILab/SoulX-FlashTalk&type=date&legend=top-left)
