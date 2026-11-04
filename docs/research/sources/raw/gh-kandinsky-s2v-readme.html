# Kandinsky S2V 1.0









<p>
  <a href="https://kandinskyavatar.github.io"><img src="https://img.shields.io/badge/Project-Page-green" alt="Project Page"></a>
  <a href="https://huggingface.co/collections/kandinskylab/kandinsky-s2v-10-6ab65ebe8f765b6dd9d706d7"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-blue" alt="Hugging Face"></a>
  <a href="https://huggingface.co/spaces/kandinskylab/Kandinsky-S2V-1.0-Demo"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Demo-yellow" alt="Demo"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License"></a>
</p>

Speech-to-video inference: an avatar video generated from a **reference frame**
and a **speech track**. The whole figure is animated, not only the head.

Output is 25 fps in SD or HD resolution, at the reference frame's aspect ratio.
Long speech is generated in 5-second chunks.

## Examples

Each is one reference frame plus one speech track. More examples — other
languages, cartoon characters and animals, long videos — are on the
[project page](https://kandinskyavatar.github.io).

<table>
  <tr>
    <td width="50%"><video src="https://github.com/user-attachments/assets/8e8960ad-b68c-4f79-b560-13c4930d92cb" controls loop></video></td>
    <td width="50%"><video src="https://github.com/user-attachments/assets/69ed311a-c3b6-4d0a-ac0c-626973f8b147" controls loop></video></td>
  </tr>
</table>

<table>
  <tr>
    <td width="25%"><video src="https://github.com/user-attachments/assets/f0fd2967-a442-4d56-bfdd-266018508535" controls loop></video></td>
    <td width="25%"><video src="https://github.com/user-attachments/assets/60661415-05e3-4a0b-823c-ac3fef5f25d1" controls loop></video></td>
    <td width="50%"><video src="https://github.com/user-attachments/assets/2f8ebc97-89c9-4810-a90b-640da7e5d31e" controls loop></video></td>
  </tr>
</table>

## Requirements

One NVIDIA GPU with 48 GB or more (80 GB for HD) and a driver ≥ 580, which the
CUDA 13 build of `torch` needs. `offload.vae_tiling: true` brings the peak down
to about 28 GB at the cost of faint tile seams.

## Install

```bash
git clone https://github.com/kandinskylab/kandinsky-s2v
cd kandinsky-s2v
uv sync            # or: pip install -e .
```

[uv](https://docs.astral.sh/uv/) drives the environment and
[just](https://github.com/casey/just) the tasks; neither is required, and every
recipe in the [JUSTFILE](JUSTFILE) is a plain command you can run yourself.

## Generate

```bash
just generate \
    --config src/kandinsky_s2v/configs/s2v_lite_distill.yaml \
    --audio speech.wav \
    --image reference.png \
    --out out.mp4
```

The number of chunks follows the audio length; pass `--chunks N` to override.
`--prompt` / `--negative` override the canned prompts in the config, and
`--steps`, `--guidance`, `--seed` override the sampler defaults.

### Several GPUs

To speed a generation up, split it across the GPUs of one node:

```bash
just generate-parallel 8 \
    --config src/kandinsky_s2v/configs/s2v_pro_distill.yaml \
    --audio speech.wav --image reference.png --out out.mp4
```

This is `torchrun --nproc-per-node 8` around the same command: every process
holds the full weights and denoises one slice of the token sequence. N must
divide the attention heads — 2 or 4 on Lite, 2, 4 or 8 on Pro.

## Configurations

Each configuration is a YAML file in
[src/kandinsky_s2v/configs/](src/kandinsky_s2v/configs/), passed with
`--config`. The table gives the time to generate one second of video and the
peak GPU memory, measured as follows:

- one H100 with FA3, at 512×768 (1280×768 for the HD rows), on a warm run of
  one chunk (125 frames, 5 s);
- `with compile` is `compile.strategy: torch` (off by default); on top of these
  times, a run spends ~20 s compiling once at the start;
- `4 / 8 GPUs` is the [same generation split](#several-gpus) across 4 GPUs for
  Lite and 8 for Pro, and counts DiT sampling alone.

Distillation buys roughly 5.1× on Lite, 4.5× on Pro and 5.6× on Pro in HD.

| Config | Model | Time per 1 s of video | with `compile` | 4 / 8 GPUs | Peak VRAM | Weights |
|---|---|---|---|---|---|:---:|
| `s2v_lite_distill.yaml` | Lite 2B distilled | 8.7 s | 7.1 s | 3.8 s | 57 GiB | <a href="https://huggingface.co/kandinskylab/Kandinsky-S2V-1.0-Lite-distill"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" height="16" alt="🤗"></a> |
| `s2v_lite.yaml` | Lite 2B | 44 s | 35 s | 14 s | 57 GiB | <a href="https://huggingface.co/kandinskylab/Kandinsky-S2V-1.0-Lite"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" height="16" alt="🤗"></a> |
| `s2v_pro_distill.yaml` | Pro 21B distilled | 41.5 s | 33.6 s | 11.4 s | 46 GiB | <a href="https://huggingface.co/kandinskylab/Kandinsky-S2V-1.0-Pro-distill"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" height="16" alt="🤗"></a> |
| `s2v_pro.yaml` | Pro 21B | 189 s | 152 s | 32 s | 46 GiB | <a href="https://huggingface.co/kandinskylab/Kandinsky-S2V-1.0-Pro"><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" height="16" alt="🤗"></a> |
| `s2v_pro_distill_hd.yaml` | Pro 21B distilled, HD | 137 s | 122 s | 29 s | 55 GiB | same as `s2v_pro_distill.yaml` |
| `s2v_pro_hd.yaml` | Pro 21B, HD | 773 s | 678 s | 114 s | 55 GiB | same as `s2v_pro.yaml` |

## Weights

Nothing to download by hand: the first run fetches every weight from the Hub —
about 25 GB for Lite and 65 GB for Pro — and `huggingface_hub` caches it
afterwards. That is the DiT from `kandinskylab/Kandinsky-S2V-1.0-*` and the
three third-party pieces from upstream: `hunyuanvideo-community/HunyuanVideo/vae`,
`Qwen/Qwen2.5-Omni-7B` and `openai/clip-vit-large-patch14`.

An entry in `paths` may also be a local path.

## Diffusers

The same model is available as a Diffusers
[modular pipeline](https://huggingface.co/docs/diffusers/modular_diffusers/overview)
— the `-Diffusers` repositories in the
[collection](https://huggingface.co/collections/kandinskylab/kandinsky-s2v-10-6ab65ebe8f765b6dd9d706d7).
It was merged in [huggingface/diffusers#15164](https://github.com/huggingface/diffusers/pull/15164)
and is not in a release yet, so install Diffusers from `main`:

```bash
pip install git+https://github.com/huggingface/diffusers librosa
```

```python
import librosa
import torch
from diffusers import ModularPipeline
from diffusers.utils import encode_video, load_image

pipe = ModularPipeline.from_pretrained("kandinskylab/Kandinsky-S2V-1.0-Lite-distill-Diffusers")
pipe.load_components(dtype=torch.bfloat16)
pipe.to("cuda")

image = load_image("reference.png")
audio, _ = librosa.load("speech.wav", sr=16000)  # a mono waveform at 16 kHz, for the model
speech, sample_rate = librosa.load("speech.wav", sr=None)  # the original track, added to the output video

video = pipe(image=image, audio=audio, output="videos")[0]
encode_video(
    video,
    fps=25,
    output_path="avatar.mp4",
    audio=torch.from_numpy(speech)[None],
    audio_sample_rate=sample_rate,
)
```

The pipeline reads no files: `image` is a PIL image and `audio` a mono waveform
at 16 kHz. `from_pretrained` picks the base or distilled blocks from the
checkpoint. The Pro bundles do not fit an 80 GB card with every component
resident; offload them through a `ComponentsManager`:

```python
import librosa
import torch
from diffusers import ComponentsManager, ModularPipeline
from diffusers.utils import encode_video, load_image

manager = ComponentsManager()
pipe = ModularPipeline.from_pretrained("kandinskylab/Kandinsky-S2V-1.0-Pro-distill-Diffusers", components_manager=manager)
pipe.load_components(dtype=torch.bfloat16)
manager.enable_auto_cpu_offload(device="cuda", memory_reserve_margin="40GiB")  # after load_components

image = load_image("reference.png")
audio, _ = librosa.load("speech.wav", sr=16000)
speech, sample_rate = librosa.load("speech.wav", sr=None)

video = pipe(image=image, audio=audio, output="videos")[0]
encode_video(
    video,
    fps=25,
    output_path="avatar.mp4",
    audio=torch.from_numpy(speech)[None],
    audio_sample_rate=sample_rate,
)
```

## Responsible use

The model animates a real person from a single photograph, driven by a
voice that need not be theirs. Use a reference frame you have the subject's
consent to animate, and do not present the result as a genuine recording of
anyone.

## Licence

The code in this repository is MIT, see [LICENSE](LICENSE). The published
weights carry their own licence, stated on each model card.

## Development

```bash
just test        # unit tests, no GPU and no weights needed
just lint
```
