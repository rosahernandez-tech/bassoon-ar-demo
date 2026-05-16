# Bassoon Engineering — AR Congress Demo

Mobile-friendly 3D / AR viewer for the congress poster. Visitors scan a QR code and
can view models in 3D (orbit, zoom) or place them in the real world via AR.

## What's here

| File | Purpose |
|------|---------|
| `index.html` | Gallery landing page — one QR code links here |
| `model.html` | Individual model viewer (loaded via `?m=model_id`) |
| `models/*.glb` | Converted 3D models (from the OBJ files) |
| `qrcodes/*.png` | QR codes to print on your poster |
| `convert_to_glb.py` | Re-run conversion if models change |
| `generate_qr.py` | Generate QR codes after deploying |

## AR compatibility

| Device | AR experience |
|--------|--------------|
| Android (Chrome) | Full AR via WebXR or Google Scene Viewer — model appears in the room |
| iOS 17+ (Safari) | 3D viewer works; AR requires adding a USDZ file (see note below) |
| Desktop | 3D viewer with orbit controls |

**iOS AR note:** To enable AR on iPhone, you need to convert GLB → USDZ using
Apple's [Reality Converter](https://developer.apple.com/augmented-reality/tools/)
(free, Mac only). Then add `ios-src="models/model_name.usdz"` to the `<model-viewer>`
tag in `model.html` for each model.

## Deploy to GitHub Pages (step-by-step)

1. **Create a GitHub account** at github.com if you don't have one.

2. **Create a new repository** — click "New repository", give it a name like
   `bassoon-ar-demo`, set it to Public, click "Create repository".

3. **Upload the `ar-demo/` folder contents** — on the repo page click "uploading an
   existing file", then drag the entire contents of this `ar-demo/` folder (index.html,
   model.html, models/, etc.) into the upload area. Click "Commit changes".

4. **Enable GitHub Pages** — go to Settings → Pages → Source: select "Deploy from a
   branch" → Branch: `main` / `/(root)` → Save.

5. **Wait ~2 minutes**, then your site will be live at:
   `https://YOUR_USERNAME.github.io/bassoon-ar-demo/`

6. **Generate QR codes** with the real URL:
   ```
   cd ar-demo
   python3 generate_qr.py https://YOUR_USERNAME.github.io/bassoon-ar-demo
   ```
   This creates PNG files in `qrcodes/` — use `qr_gallery.png` on your poster.

## Preview locally (before deploying)

```bash
cd ar-demo
python3 -m http.server 8000
# Open http://localhost:8000 in Chrome
# For AR on your phone: use ngrok or deploy to GitHub Pages
```

## Regenerate GLB models (if OBJ files change)

```bash
cd ar-demo
python3 convert_to_glb.py
```
