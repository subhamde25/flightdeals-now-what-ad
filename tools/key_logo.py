"""White -> alpha ("color to alpha") for the FlightDeals logo, then crop to the mark.
Usage: python tools/key_logo.py assets/img/logo512.png assets/img/fd-mark.png
(logo512.png is the official 512x512 logo from https://flightdeals.in/logo512.png, on white)"""
import sys, numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float64) / 255.0
a = np.max(1.0 - im, axis=2)                      # distance from white
a = np.clip((a - 0.015) / 0.985, 0, 1)            # kill faint near-white noise
safe = np.where(a > 1e-4, a, 1)
rgb = np.clip((im - (1 - a)[..., None]) / safe[..., None], 0, 1)
out = np.dstack([rgb, a])
ys, xs = np.where(a > 0.02)
y0, y1, x0, x1 = ys.min() - 6, ys.max() + 7, xs.min() - 6, xs.max() + 7
out = out[y0:y1, x0:x1]
Image.fromarray((out * 255).round().astype(np.uint8), 'RGBA').save(dst)
print('saved', dst, out.shape[1], 'x', out.shape[0])
