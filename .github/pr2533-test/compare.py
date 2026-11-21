"""Compare native-vc_reader output, vcr_lite output and the team's published Reader V3 map on the same ROI."""
import json, sys, urllib.request
from pathlib import Path
import numpy as np, tifffile

native, lite, team_path, y0, y1, x0, x1, out_json = sys.argv[1:9]
y0, y1, x0, x1 = map(int, (y0, y1, x0, x1))
a = tifffile.imread(native); b = tifffile.imread(lite)
team = tifffile.imread(team_path)[y0:y1, x0:x1]

def cmp(p, q, name):
    if p.shape != q.shape:
        return {"pair": name, "error": f"shape mismatch {p.shape} vs {q.shape}"}
    d = np.abs(p.astype(np.int16) - q.astype(np.int16))
    return {"pair": name, "pixels": int(d.size), "identical_pct": round(100 * float((d == 0).mean()), 3),
            "within_1_pct": round(100 * float((d <= 1).mean()), 3), "max_diff": int(d.max()),
            "n_different": int((d != 0).sum())}

res = {"roi": [y0, y1, x0, x1], "native_shape": list(a.shape), "lite_shape": list(b.shape),
       "native_dtype": str(a.dtype), "native_nonzero_pct": round(100 * float((a > 0).mean()), 2),
       "comparisons": [cmp(a, b, "native vs vcr_lite"), cmp(a, team, "native vs team Reader V3 map"),
                       cmp(b, team, "vcr_lite vs team Reader V3 map")]}
print(json.dumps(res, indent=2))
Path(out_json).write_text(json.dumps(res, indent=2))
