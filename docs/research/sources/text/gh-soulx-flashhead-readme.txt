SoulX-FlashHead: Oracle-guided Generation of Infinite Real-time Streaming Talking Heads

[Tan Yu*](https://jiayoujiayoujiayoua.github.io/), [Qian Qiao*](https://qianqiaoai.github.io/)
✉
, [Le Shen*](https://openreview.net/profile?id=%7ELe_Shen3), [Ke Zhou](https://github.com/jokerz0624), [Jincheng Hu](#), [Dian Sheng](#), [Bo Hu](#), [Haoming Qin](#), [Jun Gao](#), [Changhai Zhou](#), [Shunshun Yin](#), [Siyuan Liu](#)
✉

*
Equal Contribution

✉
Corresponding Author

## ⚡ Highlights
- **Model_Lite** [Released](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B/tree/main/Model_Lite) get 96 FPS, or 3-concurrent real-time(25+ FPS) streaming on single RTX4090.
- **Model_Pro** [Released](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B/tree/main/Model_Pro) can generate high-quality videos with 10.8 FPS on single RTX4090, or real-time(25+ FPS) on two RTX5090.
- **Model_Pretrained** is coming soon, providing high-performance weights and experimental foundations for community research.

## 🔥 News
- **2026.03.09** - Online demo on HuggingFace is available now. You can [try it out](https://huggingface.co/spaces/Soul-AILab/SoulX-FlashHead) directly.
- **2026.03.04** - Gradio app is available now. Both common and streaming mode are supported.
- **2026.03.02** - The [ComfyUI node](https://github.com/HM-RunningHub/ComfyUI_RH_FlashHead) is now available. Thanks for the comfyui support of [HM-RunningHub](https://github.com/HM-RunningHub).
- **2026.02.12** - The [online demo](#online-experience-qr) is now available via the Soul App. Download it today to try it out.
- **2026.02.12** - We have released the [inference code](https://github.com/Soul-AILab/SoulX-FlashHead), and the [model weights](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B).
- **2026.02.12** - We released **Project page** on [SoulX-FlashHead](https://soul-ailab.github.io/soulx-flashhead/).
- **2026.02.07** - We released [Dataset](https://huggingface.co/datasets/Soul-AILab/VividHead).
- **2026.02.07** - We released **SoulX-FlashHead Technical Report** on [Arxiv](https://arxiv.org/pdf/2602.07449) and [GitHub repository](./assets/SoulX_FlashHead.pdf).

## 📑 Todo List
- [x] Technical report
- [x] Project Page
- [x] Inference code
- [x] Streaming online demo on HuggingFace
- [x] Distilled Checkpoint of Pro-Model & Lite-Model release
- [ ] Pretrained Checkpoint release

## 🌰 Examples
More examples are available in the project.

## 📖 Quickstart
### 🔧 Installation
#### 1. Create a Conda environment
```bash
conda create -n flashhead python=3.10
conda activate flashhead
```
#### 2. Install PyTorch on CUDA
```bash
pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu128
```
#### 3. Install other dependencies
```bash
pip install -r requirements.txt
```
#### 4. FlashAttention installation:
```bash
pip install ninja
pip install flash_attn==2.8.0.post2 --no-build-isolation
```

-- If it takes a long time, we recommend the way below.
1. download wheel file from [here](https://github.com/Dao-AILab/flash-attention/releases/tag/v2.8.0.post2)
2. pip install xxx.whl

#### 5. SageAttention installation (Optional)
```bash
pip install sageattention==2.2.0 --no-build-isolation
```

#### 6. FFmpeg installation
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
| `SoulX-FlashHead-1_3B` | Our 1.3B model| 🤗 [Huggingface](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B) |
| `wav2vec2-base-960h` | wav2vec2-base-960h | 🤗 [Huggingface](https://huggingface.co/facebook/wav2vec2-base-960h) |

```bash
# If you are in china mainland, run this first: export HF_ENDPOINT=https://hf-mirror.com
pip install "huggingface_hub[cli]"
huggingface-cli download Soul-AILab/SoulX-FlashHead-1_3B --local-dir ./models/SoulX-FlashHead-1_3B
huggingface-cli download facebook/wav2vec2-base-960h --local-dir ./models/wav2vec2-base-960h
```
### 🚀 Inference
```bash
# Infer with [Pro-Model] on single GPU
bash inference_script_single_gpu_pro.sh

# Infer with [Pro-Model] on multy GPUs
bash inference_script_multi_gpu_pro.sh
# Real-time inference speed of Pro-Model can only be supported on two RTX-5090 with SageAttention.

# Infer with [Lite-Model] on single GPU
bash inference_script_single_gpu_lite.sh
# Real-time inference speed can be supported on single RTX-4090 (up to 3 concurrent).
```

### ⚡️ Gradio Demo
```bash
# Gradio support needs gradio==5.50.0, and Chrome recommonded.

# common gradio demo
python gradio_app.py

# streaming gradio demo (Only support single GPU)
python gradio_app_streaming.py
```

### 🤗 Streaming online demo
Click [here](https://huggingface.co/spaces/Soul-AILab/SoulX-FlashHead) to experience the real-time streaming demo on HuggingFace Spaces.

### 👋 Online Experience
For a real-time interactive experience, scan the QR code to enter the event link. [2026.2.12~2026.3.11]

Real-time Online Experience
(SoulApp 实时在线体验)

## 📧 Contact Us
If you are interested in leaving a message to our work, feel free to email yutan@soulapp.cn or qiaoqian@soulapp.cn or le.shen@mail.dhu.edu.cn or zhouke@soulapp.cn or liusiyuan@soulapp.cn

We have opened a WeChat group. Additionally, we represent **SoulApp** and warmly welcome everyone to download the app and join our Soul group for further technical discussions and updates!

Join WeChat Group
(加入微信技术群)

Download SoulApp & Join Group
(下载SoulApp加入群组)

## 📚 Citation

If you find our work useful in your research, please consider citing:

```
@article{yu2026soulx,
title={SoulX-FlashHead: Oracle-guided Generation of Infinite Real-time Streaming Talking Heads},
author={Yu, Tan and Qiao, Qian and Shen, Le and Zhou, Ke and Hu, Jincheng and Sheng, Dian and Hu, Bo and Qin, Haoming and Gao, Jun and Zhou, Changhai and others},
journal={arXiv preprint arXiv:2602.07449},
year={2026}
}
```

## 🙇 Acknowledgement
- [Wan](https://github.com/Wan-Video/Wan2.1): the base model we built upon.
- [LTX-Video](https://github.com/Lightricks/LTX-Video): the VAE of our Lite-Model.
- [Self forcing](https://github.com/guandeh17/Self-Forcing): the codebase we built upon.
- [DMD](https://github.com/tianweiy/DMD2) and [Self forcing++](https://github.com/justincui03/Self-Forcing-Plus-Plus): the key distillation technique used by our method.
- [SoulX-FlashTalk](https://github.com/Soul-AILab/SoulX-FlashTalk/) is another model developed by our team, featuring 14B parameters and real-time capabilities.
> [!TIP]
> If you find our work useful, please also consider starring the original repositories of these foundational methods.

## 💡 Star History
