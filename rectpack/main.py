import matplotlib
import numpy as np

from rectpack.algo_mix import EnsemblePackingAlgorithm
from rectpack.corner_points import CornerPointsMR, CornerPointsSL
from rectpack.maxrects import MaxRects
from rectpack.skyline import Skyline
from rectpack.visualization_utils import draw_rectangles, draw_skyline

matplotlib.use('MacOSX')

import matplotlib.pyplot as plt


def place_sample_elements(packer, rectangles):
    for r in rectangles:
        packer.add_rect(*r)

    print(packer.rect_list())

    fig = draw_rectangles(packer.rectangles, (100, 100), 'r')
    if isinstance(packer, Skyline):
        fig = draw_skyline(packer._skyline, (100, 100), 'b', fig)
    plt.show()


def place_interchangeably(packer_1, packer_2, rectangles):
    for idx, r in enumerate(rectangles):
        if idx % 2 == 0:
            added_rect = packer_1.add_rect(*r)
            packer_2.place_rect(added_rect.width, added_rect.height, added_rect.x, added_rect.y)
            fig = draw_rectangles(packer_2.rectangles + [added_rect])
            fig = draw_rectangles(packer_1._max_rects, (100, 100), 'g', fig)
            fig = draw_skyline(packer_2._skyline, (100, 100), 'b', fig)

            plt.show()
        else:
            added_rect = packer_2.add_rect(*r)
            packer_1.place_rect(added_rect.width, added_rect.height, added_rect.x, added_rect.y)
            fig = draw_rectangles(packer_2.rectangles + [added_rect])
            fig = draw_rectangles(packer_1._max_rects, (100, 100), 'g', fig)
            fig = draw_skyline(packer_2._skyline, (100, 100), 'b', fig)
            plt.show()

    # draw_rectangles(packer_1.rectangles)


def place_with_ensemble(packer: EnsemblePackingAlgorithm, rectangles):
    for idx, r in enumerate(rectangles):
        candidates = packer.get_candidates(*r)

        fig = draw_rectangles(packer.rectangles, color='r')
        unique_candidates = list(set(candidates))
        fig = draw_rectangles(unique_candidates, color='g', fig=fig)
        plt.title(f'Total candidates: {len(unique_candidates)}')
        plt.show()

        best_candidate_idx = 0

        packer.place_item(candidates[best_candidate_idx])


def draw_cornerpoints(packer, rectangles):
    for r in rectangles:
        placements = packer.select_best_position(*r)

        fig = draw_rectangles(packer.rectangles, (100, 100), 'r')
        fig = draw_rectangles([p[0] for p in placements], (100, 100), 'g', fig)
        plt.show()

        best_placement = placements[0]
        packer.place_rect(best_placement.width, best_placement.height,
                          x=best_placement.x,
                          y=best_placement.y)


if __name__ == '__main__':
    width = 100
    height = 100
    # rectangles = [(10, 30), (40, 60), (30, 30), (40, 30), (10, 50), (30, 30), (5, 5), (15, 2), (10, 10), (20, 5)]
    # random rectagles
    rectangles = [ (np.random.randint(1, 10), np.random.randint(1, 10))
        for _ in range(30)]

    # packer_mr = MaxRects(width, height, rot=True)
    # packer_sl = Skyline(width, height, rot=True)
    # packer_cp = CornerPointsSL(width, height, rot=True)
    # packer_cp_mr = CornerPointsMR(width, height, rot=True)

    # place_sample_elements(packer_mr, rectangles)
    # place_sample_elements(packer_sl, rectangles)
    # draw_cornerpoints(packer_cp, rectangles)

    # place_interchangeably(packer_mr, packer_sl, rectangles)

    packer = EnsemblePackingAlgorithm(width, height)
    place_with_ensemble(packer, rectangles)
