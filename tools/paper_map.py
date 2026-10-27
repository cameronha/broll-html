"""Paper-cut map pieces from Natural Earth (public domain, assets/naturalearth/*.geojson).

    m = PaperMap(center=(-101.65, 24.5), px_per_deg=40)
    m.xy(lon, lat)                       -> frame pixels (equirectangular, x scaled by cos(center lat))
    m.land("Mexico", "#F2C46B")          -> <path> for a country (ADMIN name)
    m.state("Texas", "#F6D9A8")          -> <path> for a state/province (50m: US, CA, AU, BR, CN, IN, ID, RU, ZA only)
"""
import json, math, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE = os.path.join(HERE, "assets", "naturalearth")
_cache = {}


def _load(name):
    if name not in _cache:
        _cache[name] = json.load(open(os.path.join(NE, name)))["features"]
    return _cache[name]


class PaperMap:
    def __init__(self, center, px_per_deg, size=1080, min_px=6):
        self.c, self.k, self.size, self.min_px = center, px_per_deg, size, min_px
        self.kx = px_per_deg * math.cos(math.radians(center[1]))

    def xy(self, lon, lat):
        return (self.size / 2 + (lon - self.c[0]) * self.kx, self.size / 2 - (lat - self.c[1]) * self.k)

    def _path(self, geom):
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        d = []
        for poly in polys:
            ring = [self.xy(*p) for p in poly[0]]
            xs, ys = [p[0] for p in ring], [p[1] for p in ring]
            if max(xs) - min(xs) < self.min_px and max(ys) - min(ys) < self.min_px:
                continue                                        # specks: too small to cut from paper
            out, last = [], None
            for x, y in ring:                                   # drop points closer than 1.5 px: paper hides them
                if last is None or abs(x - last[0]) + abs(y - last[1]) > 1.5:
                    out.append(f"{x:.1f} {y:.1f}"); last = (x, y)
            d.append("M" + " L".join(out) + "Z")
        return "".join(d)

    def land(self, admin, fill):
        f = next(f for f in _load("ne_50m_admin_0_countries.geojson") if f["properties"]["ADMIN"] == admin)
        return f'<path d="{self._path(f["geometry"])}" fill="{fill}"/>'

    def state(self, name, fill):
        f = next(f for f in _load("ne_50m_admin_1_states_provinces.geojson") if f["properties"]["name"] == name)
        return f'<path d="{self._path(f["geometry"])}" fill="{fill}"/>'
