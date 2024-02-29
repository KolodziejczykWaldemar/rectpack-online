from typing import List

import numpy as np
from matplotlib import patches, pyplot as plt

from rectpack.geometry import HSegment


def convert_figure_to_numpy(fig: plt.Figure) -> np.ndarray:
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data


def draw_rectangles(rectangles,
                    bin_size=(100, 100),
                    color='red',
                    fig: plt.Figure = None) -> plt.Figure:
    if fig is None:
        fig, ax = plt.subplots()
    ax = plt.gca()
    for r in rectangles:
        ax.add_patch(patches.Rectangle((r.x, r.y), r.width, r.height,
                                       fill=True,
                                       facecolor=color,
                                       edgecolor=color,
                                       alpha=0.5))
    ax.set_xlim(0, bin_size[0])
    ax.set_ylim(0, bin_size[1])
    ax.set_aspect('equal', 'box')
    return fig


def draw_skyline(skyline: List[HSegment],
                 bin_size=(100, 100),
                 color: str = 'blue',
                 fig: plt.Figure = None) -> plt.Figure:
    if fig is None:
        fig, ax = plt.subplots()
    ax = plt.gca()
    for bar in skyline:
        ax.plot([bar.start.x, bar.start.x + bar.length], [bar.start.y, bar.start.y], color=color)

    ax.set_xlim(0, bin_size[0])
    ax.set_ylim(0, bin_size[1])
    ax.set_aspect('equal', 'box')
    return fig
