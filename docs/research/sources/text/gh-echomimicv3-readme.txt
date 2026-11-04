[简体中文](https://github.com/antgroup/echomimic_v3/blob/main/README_zh.md) | English

EchoMimicV3: 1.3B Parameters are All You Need for Unified Multi-Modal and Multi-Task Human Animation

Rang Meng
1

Yan Wang

Weipeng Wu

Ruobing Zheng

Yuming Li
2

Chenguang Ma
2

Terminal Technology Department, Alipay, Ant Group.

1
Core Contributor

2
Corresponding Authors

## 🚀 EchoMimic Series
* EchoMimicV1: Lifelike Audio-Driven Portrait Animations through Editable Landmark Conditioning. [GitHub](https://github.com/antgroup/echomimic)
* EchoMimicV2: Towards Striking, Simplified, and Semi-Body Human Animation. [GitHub](https://github.com/antgroup/echomimic_v2)
* EchoMimicV3: 1.3B Parameters are All You Need for Unified Multi-Modal and Multi-Task Human Animation. [GitHub](https://github.com/antgroup/echomimic_v3)

## 📣 Updates
* [2026.01.22] 🔥 We update our EchoMimicV3-Flash on [Huggingface](https://huggingface.co/BadToBest/EchoMimicV3/tree/main/echomimicv3-flash-pro).
- 🚀 8-step High-quality Generation.
- 🧩 No Face Mask required.
- 💾 12G VRAM Requirement.
- ✅ Supports up to 768×768 Resolution.
* [2025.11.09] 🔥 EchoMimicV3 is accepted by AAAI 2026.
* [2025.08.21] 🔥 EchoMimicV3 gradio demo on [modelscope](https://modelscope.cn/studios/BadToBest/EchoMimicV3) is ready.
* [2025.08.12] 🔥🚀 **12G VRAM is All YOU NEED to Generate Video**. Please use this [GradioUI](https://github.com/antgroup/echomimic_v3/blob/main/app_mm.py). Check the [tutorial](https://www.bilibili.com/video/BV1W8tdzEEVN) from @[gluttony-10](https://github.com/gluttony-10). Thanks for the contribution.
* [2025.08.12] 🔥 EchoMimicV3 can run on **16G VRAM** using [ComfyUI](https://github.com/smthemex/ComfyUI_EchoMimic). Thanks @[smthemex](https://github.com/smthemex) for the contribution.
* [2025.08.09] 🔥 We release our [models](https://modelscope.cn/models/BadToBest/EchoMimicV3) on ModelScope.
* [2025.08.08] 🔥 We release our [codes](https://github.com/antgroup/echomimic_v3) on GitHub and [models](https://huggingface.co/BadToBest/EchoMimicV3) on Huggingface.
* [2025.07.08] 🔥 Our [paper](https://arxiv.org/abs/2507.03905) is in public on arxiv.

## 🌅 Gallery

### Chinese Driven Audio

For more demo videos, please refer to the [project page](https://antgroup.github.io/ai/echomimic_v3/)

## Quick Start
### Environment Setup
- Tested System Environment: Centos 7.2/Ubuntu 22.04, Cuda >= 12.1
- Tested GPUs: A100(80G) / RTX4090D (24G) / V100(16G)
- Tested Python Version: 3.10 / 3.11

### 🛠️Installation for Windows

##### Please use the [one-click installation package](https://pan.baidu.com/share/init?surl=cV7i2V0wF4exDtKjJrAUeA) (passport: glut) to get started quickly for Quantified version.

### 🛠️Installation for Linux
#### 1. Create a conda environment
```
conda create -n echomimic_v3 python=3.10
conda activate echomimic_v3
```

#### 2. Other dependencies
```
pip install -r requirements.txt
```
### 🧱Model Preparation

| Models | Download Link | Notes |
| --------------|-------------------------------------------------------------------------------|-------------------------------|
| Wan2.1-Fun-V1.1-1.3B-InP | 🤗 [Huggingface](https://huggingface.co/alibaba-pai/Wan2.1-Fun-V1.1-1.3B-InP) | Base model
| wav2vec2-base | 🤗 [Huggingface](https://huggingface.co/facebook/wav2vec2-base-960h) | Audio encoder for preview
| chinese-wav2vec2-base | 🤗 [Huggingface](https://modelscope.cn/models/TencentGameMate/chinese-wav2vec2-base) | Audio encoder for Flash
| EchoMimicV3-preview | 🤗 [Huggingface](https://huggingface.co/BadToBest/EchoMimicV3) | preview weights
| EchoMimicV3-preview | 🤗 [ModelScope](https://modelscope.cn/models/BadToBest/EchoMimicV3) | preview weights
| EchoMimicV3-Flash | 🤗 [Huggingface](https://huggingface.co/BadToBest/EchoMimicV3/tree/main/echomimicv3-flash-pro) | Flash weights

-- The **weights** of EchoMimicV3-flash-pro is organized as follows.

```
./flash/
├── Wan2.1-Fun-V1.1-1.3B-InP
├── chinese-wav2vec2-base
└── transformer
└── diffusion_pytorch_model.safetensors
```

-- The **weights** is of EchoMimicV3-preview organized as follows.

```
./preview/
├── Wan2.1-Fun-V1.1-1.3B-InP
├── wav2vec2-base-960h
└── transformer
└── diffusion_pytorch_model.safetensors
```
### 🔑 Quick Inference for EchoMimicV3-flash-pro
```
bash run_flash.sh
```
### 🔑 Quick Inference for EchoMimicV3-preview
```
python infer_preview.py
```
For Quantified GradioUI version for EchoMimicV3-preview:
```
python app_mm.py
```
**images, audios, masks and prompts are provided in `datasets/echomimicv3_demos`**

#### Tips
- Audio CFG: Audio CFG `audio_guidance_scale` works optimally between 1.8~2. Increase the audio CFG value for better lip synchronization, while decreasing the audio CFG value can improve the visual quality.
- Text CFG: Text CFG `guidance_scale` works optimally between 3~6. Increase the text CFG value for better prompt following, while decreasing the text CFG value can improve the visual quality.
- TeaCache: The optimal range for `teacache_threshold` is between 0~0.1.
- Sampling steps: 5 steps for talking head, 15~25 steps for talking body.
- ​Long video generation: If you want to generate a video longer than 138 frames, you can use Long Video CFG.
- Try setting `partial_video_length` to 81, 65 or smaller to reduce VRAM usage.

## 📒 Citation

If you find our work useful for your research, please consider citing the paper :

```
@article{meng2024echomimicv2,
title={EchoMimicV2: Towards Striking, Simplified, and Semi-Body Human Animation},
author={Meng, Rang and Zhang, Xingyu and Li, Yuming and Ma, Chenguang},
journal={arXiv preprint arXiv:2411.10061},
year={2024}
}
@article{meng2025echomimicv3,
title={Echomimicv3: 1.3 b parameters are all you need for unified multi-modal and multi-task human animation},
author={Meng, Rang and Wang, Yan and Wu, Weipeng and Zheng, Ruobing and Li, Yuming and Ma, Chenguang},
journal={arXiv preprint arXiv:2507.03905},
year={2025}
}
@article{meng2026echotorrent,
title={EchoTorrent: Towards Swift, Sustained, and Streaming Multi-Modal Video Generation},
author={Meng, Rang and Wu, Weipeng and Yin, Yingjie and Li, Yuming and Ma, Chenguang},
journal={arXiv preprint arXiv:2602.13669},
year={2026}
}
```
## Reference
- Wan2.1: https://github.com/Wan-Video/Wan2.1/
- VideoX-Fun: https://github.com/aigc-apps/VideoX-Fun/
## 📜 License
The models in this repository are licensed under the Apache 2.0 License. We claim no rights over the your generated contents,
granting you the freedom to use them while ensuring that your usage complies with the provisions of this license.
You are fully accountable for your use of the models, which must not involve sharing any content that violates applicable laws,
causes harm to individuals or groups, disseminates personal information intended for harm, spreads misinformation, or targets vulnerable populations.

## 🌟 Star History
[![Star History Chart](https://api.star-history.com/svg?repos=antgroup/echomimic_v3&type=Date)](https://www.star-history.com/#antgroup/echomimic_v3&Date)
