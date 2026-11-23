"""LOCAL STAND-IN for `shapely.geometry` (not installed on this laptop).

The paid driver replaces shapely polygons in the tracker's vector distance functions by Codex's ArrayPolygon
(fast_overlap_array.install()), so shapely is needed only for the import statements. If any code path really tries to
build or intersect a shapely polygon (the serial *_s functions), this raises instead of silently computing something
else."""


class Polygon:
    def __init__(self, *args, **kwargs):
        raise RuntimeError('stand-in shapely.geometry.Polygon was actually used: a serial geometry path was taken')
