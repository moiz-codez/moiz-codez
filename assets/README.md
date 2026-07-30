Drop your headshot here as `profile.jpg`, then run:

```
pip install pillow numpy opencv-python-headless rembg onnxruntime
python3 ../scripts/make_portrait.py profile.jpg
```

(run from inside `assets/`, or just `python3 scripts/make_portrait.py` from
the repo root — it looks for `assets/profile.jpg` by default.)

See the tips at the top of `scripts/make_portrait.py` for what makes a photo
convert well (side light, tight crop, real resolution).
