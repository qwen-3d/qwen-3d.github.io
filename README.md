# Qwen-3D Project Page

Static academic project website for **Qwen-3D: A Generalist 3D Vision-Language Model for Spatial Understanding**.

Style inspiration: [Real-3DQA](https://real-3dqa.github.io/) / [Nerfies](https://nerfies.github.io/) project pages.

## Local preview

```bash
cd qwen-3d.github.io
python -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Deploy (GitHub Pages)

1. Create a GitHub repo named `qwen-3d.github.io` (or enable Pages on any repo's `main` branch `/` root).
2. Push this folder.
3. In repo Settings → Pages, set source to `main` / root.

## Assets

- Paper figures converted from `overleaf/qwen3d-eccv/figures`
- Selected media from `Research/Qwen3D.pptx` and related decks in `Documents`
- Re-run asset prep if figures change:

```bash
python _prepare_assets.py
```
