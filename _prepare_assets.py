import fitz
import os
import shutil
import zipfile
from pathlib import Path

SITE = Path(r"C:\Users\lucyl\OneDrive\Documents\Research\qwen-3d.github.io")
FIG = Path(r"C:\Users\lucyl\OneDrive\Documents\Research\overleaf\qwen3d-eccv\figures")
OUT = SITE / "static" / "images"
OUT.mkdir(parents=True, exist_ok=True)
(SITE / "static" / "css").mkdir(parents=True, exist_ok=True)
(SITE / "static" / "js").mkdir(parents=True, exist_ok=True)

for name in ["Arch.png", "flattened_decoder_types.png"]:
    src = FIG / name
    if src.exists():
        dst = OUT / name.lower().replace(" ", "_")
        shutil.copy2(src, dst)
        print("copied", name)

items = [
    ("teaser_v6.pdf", "teaser"),
    ("arch_v3.pdf", "architecture"),
    ("decoders_fig2_v3.pdf", "decoders"),
    ("3D_grounding_viz.pdf", "grounding_3d"),
    ("2d_ground_viz.pdf", "grounding_2d"),
    ("detection.pdf", "detection"),
    ("3dqa.pdf", "vqa"),
    ("failures.pdf", "failures"),
    ("Num_views_ScanRefer.pdf", "num_views"),
    ("pose_vs_depth_noise_scanrefer.pdf", "noise_robustness"),
    ("depth_noise_sensitivity.pdf", "depth_noise"),
    ("pose_noise_sensitivity.pdf", "pose_noise"),
    ("Figure_1.pdf", "figure1"),
    ("Figure_2.pdf", "figure2"),
]

for src_name, dst in items:
    src = FIG / src_name
    if not src.exists():
        print("MISSING", src_name)
        continue
    doc = fitz.open(src)
    zoom = 1.5 if src.stat().st_size > 8_000_000 else 2.0
    mat = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = OUT / (f"{dst}.png" if i == 0 else f"{dst}_{i + 1}.png")
        pix.save(str(out_path))
        print(f"wrote {out_path.name} ({pix.width}x{pix.height})")
    doc.close()

pptx_sources = [
    Path(r"C:\Users\lucyl\OneDrive\Documents\Research\Qwen3D.pptx"),
    Path(r"C:\Users\lucyl\OneDrive\Documents\Qwen3dFigs.pptx"),
    Path(r"C:\Users\lucyl\OneDrive\Documents\Qwen-3D s2s.pptx"),
    Path(r"C:\Users\lucyl\OneDrive\Documents\qwen3d_poster.pptx"),
    Path(r"C:\Users\lucyl\OneDrive\Documents\failures.pptx"),
]

exts = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4"}
for pptx in pptx_sources:
    if not pptx.exists():
        print("skip missing pptx", pptx)
        continue
    dest = OUT / ("pptx_" + "".join(c if c.isalnum() or c in "-_" else "_" for c in pptx.stem))
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(pptx) as zf:
        for info in zf.infolist():
            if not info.filename.startswith("ppt/media/"):
                continue
            name = Path(info.filename).name
            if Path(name).suffix.lower() not in exts:
                continue
            if info.file_size < 80_000:
                continue
            target = dest / name
            with zf.open(info) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)
            count += 1
    print(f"{pptx.name}: extracted {count} media files -> {dest.name}")

print("\nLargest assets:")
files = sorted(OUT.rglob("*"), key=lambda p: p.stat().st_size if p.is_file() else 0, reverse=True)
for p in files[:40]:
    if p.is_file():
        print(f"{p.stat().st_size/1e6:7.2f} MB  {p.relative_to(OUT)}")
print("done")
