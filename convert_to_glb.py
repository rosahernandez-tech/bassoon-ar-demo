"""
Convert selected OBJ models to GLB for use with <model-viewer> AR demo.
Run from the ar-demo/ directory: python3 convert_to_glb.py
"""
import os
import sys
import trimesh

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)

MODELS = [
    {
        "id":  "bassoon_reed",
        "obj": "BassoonEngineeringProject/caña/bassoon_reed.obj",
    },
    {
        "id":  "bassoon_reed_all_scans",
        "obj": "BassoonEngineeringProject/caña/bassoon_reed_all_scans.obj",
    },
    {
        "id":  "scan_shaped_reed",
        "obj": "reed_point_cloud_experiment/scan_shaped_reed.obj",
    },
    {
        "id":  "bassoon_reed_point_cloud",
        "obj": "reed_point_cloud_experiment/bassoon_reed_point_cloud.obj",
    },
]

os.makedirs(os.path.join(SCRIPT_DIR, "models"), exist_ok=True)

for m in MODELS:
    obj_path = os.path.join(BASE_DIR, m["obj"])
    glb_path = os.path.join(SCRIPT_DIR, "models", m["id"] + ".glb")

    if not os.path.exists(obj_path):
        print(f"  MISSING: {m['obj']}")
        continue

    if os.path.exists(glb_path):
        size_mb = os.path.getsize(glb_path) / 1024 / 1024
        print(f"  Exists:  models/{m['id']}.glb  ({size_mb:.1f} MB) — skipping")
        continue

    print(f"Converting {m['id']} ...", flush=True)
    try:
        loaded = trimesh.load(obj_path, force="scene")
        loaded.export(glb_path)
        size_mb = os.path.getsize(glb_path) / 1024 / 1024
        print(f"  Done:    models/{m['id']}.glb  ({size_mb:.1f} MB)")
    except Exception as exc:
        print(f"  ERROR:   {exc}", file=sys.stderr)

print("\nAll done. Check the models/ folder.")
