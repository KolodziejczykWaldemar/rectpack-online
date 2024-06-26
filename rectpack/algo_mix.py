from rectpack.corner_points import CornerPointsSL, CornerPointsMR
from rectpack.maxrects import MaxRects, MaxRectsBl, MaxRectsBssf, MaxRectsBaf, MaxRectsBlsf
from rectpack.skyline import Skyline, SkylineMwf, SkylineMwfl, SkylineBl


class EnsemblePackingAlgorithm:
    def __init__(self, width, height):

        self._packers = [
            MaxRects(width, height, rot=True),
            MaxRectsBl(width, height, rot=True),
            MaxRectsBssf(width, height, rot=True),
            MaxRectsBaf(width, height, rot=True),
            Skyline(width, height, rot=True),
            MaxRectsBlsf(width, height, rot=True),
            # SkylineMwf(width, height, rot=True),
            # SkylineMwfl(width, height, rot=True),
            # SkylineBl(width, height, rot=True),
            CornerPointsMR(width, height, min_adjacency=0, top_adjacent=35, rot=True)
        ]

    def get_candidates(self, width, height, heur_idx=None):
        candidates = []
        for packing_algo in self._packers:
            candidate = packing_algo.select_best_position(width=width, height=height)
            if isinstance(candidate, list):
                candidates.extend(candidate)
            else:
                candidates.append(candidate)

        if heur_idx is not None:
            return [candidates[heur_idx]]

        return list(set(candidates))

    def place_item(self, rect):
        for packing_algo in self._packers:
            packing_algo.place_rect(rect.width, rect.height, rect.x, rect.y)

    @property
    def rectangles(self):
        return self._packers[0].rectangles

