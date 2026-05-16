"""
Generate QR codes for the congress poster.

Usage (after deploying to GitHub Pages):
  python3 generate_qr.py https://yourname.github.io/your-repo-name

If no URL is given, uses a localhost preview URL.
"""
import sys
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

BASE_URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "qrcodes")
os.makedirs(OUT_DIR, exist_ok=True)

TARGETS = [
    {
        "id":    "gallery",
        "label": "All Models (Gallery)",
        "url":   f"{BASE_URL}/index.html",
    },
    {
        "id":    "bassoon_reed",
        "label": "Bassoon Reed — v5",
        "url":   f"{BASE_URL}/model.html?m=bassoon_reed",
    },
    {
        "id":    "bassoon_reed_all_scans",
        "label": "DAVID Scan Overlays",
        "url":   f"{BASE_URL}/model.html?m=bassoon_reed_all_scans",
    },
    {
        "id":    "scan_shaped_reed",
        "label": "Scanned Shaped Reed",
        "url":   f"{BASE_URL}/model.html?m=scan_shaped_reed",
    },
    {
        "id":    "bassoon_reed_point_cloud",
        "label": "Reed Point Cloud",
        "url":   f"{BASE_URL}/model.html?m=bassoon_reed_point_cloud",
    },
]

BG    = (13,  17,  23)
FG    = (88, 166, 255)
WHITE = (230, 237, 243)

def make_qr(url, label, out_path):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color=FG, back_color=BG).convert("RGB")
    qr_w, qr_h = qr_img.size

    # Label strip below the QR code
    label_h = 56
    total_h  = qr_h + label_h
    canvas   = Image.new("RGB", (qr_w, total_h), BG)
    canvas.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # Try to use a system font, fall back to default
    try:
        font_big   = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except Exception:
        font_big   = ImageFont.load_default()
        font_small = font_big

    lw = draw.textlength(label, font=font_big)
    draw.text(((qr_w - lw) / 2, qr_h + 10), label, fill=WHITE, font=font_big)

    url_short = url.replace("https://", "").replace("http://", "")
    sw = draw.textlength(url_short, font=font_small)
    draw.text(((qr_w - sw) / 2, qr_h + 32), url_short, fill=(139, 148, 158), font=font_small)

    canvas.save(out_path)
    print(f"  {out_path}")

print(f"Generating QR codes for: {BASE_URL}\n")
for t in TARGETS:
    out = os.path.join(OUT_DIR, f"qr_{t['id']}.png")
    make_qr(t["url"], t["label"], out)

print(f"\nDone. {len(TARGETS)} QR codes saved to qrcodes/")
print("\nTo print on posters: use qr_gallery.png for a single QR linking to all models,")
print("or use individual QR codes for specific models.")
