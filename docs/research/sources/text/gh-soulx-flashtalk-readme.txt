SoulX-FlashTalk: Real-Time Infinite Streaming of Audio-Driven Avatars via Self-Correcting Bidirectional Distillation

[Le Shen*](https://openreview.net/profile?id=%7ELe_Shen3), [Qian Qiao*](https://qianqiaoai.github.io/), [Tan Yu*](https://jiayoujiayoujiayoua.github.io/), [Ke Zhou](https://github.com/jokerz0624), [Tianhang Yu](#), [Yu Zhan](#), [Zhenjie Wang](#), [Dingcheng Zhen](#), [Ming Tao](#), [Shunshun Yin](#), [Siyuan Liu](#)
✉

*
Equal Contribution

✉
Corresponding Author

## 🔥 News
- **2026.02.12** - We have released the [SoulX-FlashHead](https://github.com/Soul-AILab/SoulX-FlashHead), which is a streaming talking head project that achieves real-time performance on consumer GPUs (e.g., RTX 4090/5090).
- **2026.01.08** - We have released the [inference code](https://github.com/Soul-AILab/SoulX-FlashTalk), and the [model weights](https://huggingface.co/Soul-AILab/SoulX-FlashTalk-14B).
- **2025.12.30** - We released **Project page** on [SoulX-FlashTalk](https://soul-ailab.github.io/soulx-flashtalk/).
- **2025.12.30** - We released **SoulX-FlashTalk Technical Report** on [Arxiv](https://arxiv.org/pdf/2512.23379) and [GitHub repository](./assets/SoulX_FlashTalk.pdf).

## 🤫 Coming soon
**A 4-GPU real-time version of SoulX-FlashTalk.**

## 📑 Todo List
- [x] Technical report
- [x] Project Page
- [x] Inference code
- [x] Checkpoint release
- [ ] Online demo

## 📢 Live Streaming & Video Podcast

## 🎬 Online Demos

## 🌰 Examples

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
# Requires more than 64G of VRAM. Use --cpu_offload to reduce VRAM usage to 40G.
bash inference_script_single_gpu.sh

# Infer on multy GPUs
# Real-time inference speed can only be supported on 8xH800 or higher graphics cards
bash inference_script_multi_gpu.sh
```

### 👋 Online Demo
Coming Soon!

## 📧 Contact Us

If you are interested in leaving a message to our work, feel free to email le.shen@mail.dhu.edu.cn or qiaoqian@soulapp.cn or yutan@soulapp.cn or zhouke@soulapp.cn or liusiyuan@soulapp.cn

Due to Group 1 reaching its capacity, we have opened a new WeChat group. Additionally, we represent **SoulApp** and warmly welcome everyone to download the app and join our Soul group for further technical discussions and updates!

Join WeChat Group
(加入微信技术群)

Download SoulApp & Join Group
(下载SoulApp加入群组)

## 📚 Citation

If you find our work useful in your research, please consider citing:

```
@misc{shen2025soulxflashtalk,
title = {{SoulX-FlashTalk}: Real-Time Infinite Streaming of Audio-Driven Avatars via Self-Correcting Bidirectional Distillation},
author = {Shen, Le and Qiao, Qian and Yu, Tan and Zhou, Ke and Yu, Tianhang and Zhan, Yu and Wang, Zhenjie and Tao, Ming and Yin, Shunshun and Liu, Siyuan},
year = {2025},
eprint = {2512.23379},
archivePrefix = {arXiv},
primaryClass = {cs.CV},
doi = {10.48550/arXiv.2512.23379},
url = {https://arxiv.org/abs/2512.23379}
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
