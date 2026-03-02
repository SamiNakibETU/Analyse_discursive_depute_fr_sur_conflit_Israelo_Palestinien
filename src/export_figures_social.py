# -*- coding: utf-8 -*-
"""
Exporte les figures principales en formats adaptés au partage.
À exécuter après avoir généré les PNG avec les notebooks.

Formats : 1080×1080 (carré), 1200×628 (paysage).

Usage : python src/export_figures_social.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import FIGURES_DIR

try:
    from PIL import Image
except ImportError:
    print("Installer Pillow : pip install Pillow")
    sys.exit(1)

FIGURES_CLES = [
    "fig10_stance_ribbon",
    "fig12_diff_in_diff",
    "fig33_convergence_batch",
    "fig28_variables_batch",
    "fig11_stance_panel_b4",
    "fig22_fighting_words_temporal",
    "fig40_portraits_transfuges",
    "fig43_registres_par_batch",
]

SIZES = {
    "1080x1080": (1080, 1080),
    "1200x628": (1200, 628),
}


def resize_fit_pad(img, target_w, target_h, bg_color=(255, 255, 255)):
    """Redimensionne en conservant le ratio, puis pad pour atteindre les dimensions."""
    w, h = img.size
    ratio = min(target_w / w, target_h / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    out = Image.new("RGB", (target_w, target_h), bg_color)
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    if resized.mode == "RGBA":
        out.paste(resized, (x, y), resized)
    else:
        out.paste(resized, (x, y))
    return out


def main():
    if not FIGURES_DIR.exists():
        print(f"Créer d'abord {FIGURES_DIR} en exécutant les notebooks.")
        return

    out_dir = FIGURES_DIR / "social"
    out_dir.mkdir(exist_ok=True)

    found = 0
    for name in FIGURES_CLES:
        src = FIGURES_DIR / f"{name}.png"
        if not src.exists():
            continue
        found += 1
        img = Image.open(src)
        if img.mode == "RGBA":
            bg = (255, 255, 255)
        else:
            bg = (255, 255, 255)

        for label, (tw, th) in SIZES.items():
            out_img = resize_fit_pad(img, tw, th, bg)
            out_path = out_dir / f"{name}_{label}.png"
            out_img.save(out_path, "PNG")
            print(f"  {out_path.name}")

    if found == 0:
        print("Aucune figure trouvée. Exécuter les notebooks 01-07 d'abord.")
    else:
        print(f"\n{found} figures exportées vers {out_dir}")


if __name__ == "__main__":
    main()
