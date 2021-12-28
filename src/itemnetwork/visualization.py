"""
Usage:
from matplotlib import pyplot as plt
from random import randint
from itemnetwork import LinkedNetwork
from itemnetwork import quick_plot

# network setup
my_network = LinkedNetwork(ignore_key_equality_error=True)
# ignore_key_equality_error=True ignores an item if a == b (you can't connect self to self in a link)
for _ in range(100):
    my_network.add_link(a=randint(1, 10), b=randint(1, 10))

# quick plot
fig, axis = plt.subplots()
quick_plot(my_network,fig, axis)
plt.show()
"""
import math

import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from matplotlib import pyplot as plt

from .itemnetwork import LinkedNetwork, Hashable, HashType, Link


def _unit_circle_positions(item_counts: dict[Hashable, tuple[int, int]], radius=0.45, center_x=0.5,
                           center_y=0.5) -> dict[Hashable, tuple[float, float]]:
    """
    computes equally spaced points on a circle  based on the radius and center positions
    :param item_counts: item dict LinkedNetwork.get_item_link_count_dict()
    :param radius: radius of the circle
    :param center_x: x center position
    :param center_y: y center position
    :return: dict of items and their corresponding positions
    """
    r = radius
    cx, cy = center_x, center_y
    a = math.radians(360) / len(item_counts)
    points = {}
    i = 0
    for key, _ in item_counts.items():
        points[key] = (math.cos(a * i) * r + cx, math.sin(a * i) * r + cy)
        i += 1
    return points


def _set_text_anchor_positions(network: LinkedNetwork, ax: plt.Axes, bbox_style: dict,
                               **kwargs) -> dict[Hashable, plt.Annotation]:
    """

    :param bbox_style:override annotation.bbox style -
        Defaults: boxstyle = "circle", pad =  0.3, fc = "cyan", ec = "b"
    :param kwargs:
    :return:
    """
    item_counts = network.get_item_link_count_dict()
    point_positions: dict[Hashable, tuple[float, float]] = _unit_circle_positions(item_counts)
    item_annotations: dict[Hashable, plt.Annotation] = {}
    for key in item_counts.keys():
        note = ax.annotate(
            text=str(key),
            xy=point_positions[key],
            size=kwargs.get('node_text_size', '12'),
            bbox=bbox_style,
        )
        item_annotations[key] = note
    return item_annotations


def _make_colour_map(network: LinkedNetwork) -> mpl.cm.ScalarMappable:
    """
    :param network:
    :param fig: include fig to auto generate a
    :return:
    """
    vmin = min(i.count for i in network.list_links())
    vmax = max(i.count for i in network.list_links())
    scalar_map = mpl.cm.ScalarMappable(cmap=mpl.cm.get_cmap('Purples'),
                                       norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax))
    return scalar_map


def _set_annotation_lines(network: LinkedNetwork, ax: plt.Axes, annotations: dict[Hashable, plt.Annotation],
                          color_map: mpl.cm.ScalarMappable, **kwargs) -> dict[HashType, mpatches.PathPatch]:
    """
    :param annotations:
    :param kwargs:
    :return:
    """

    def make_path(_xy1: tuple[float, float], _xy2: tuple[float, float], current_link: Link) -> mpatches.PathPatch:
        # create a point equally spaced between positions 1, 2 and the centre of the plot
        # this keeps the centre less cluttered
        xy_mid = (_xy1[0] + _xy2[0] + 0.5) / 3, (_xy1[1] + _xy2[1] + 0.5) / 3
        # noinspection PyTypeChecker
        patch = mpatches.PathPatch(
            mpath.Path((_xy1, xy_mid, _xy2), [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3]),
            transform=ax.transData,
            fc='none',
            ec=color_map.to_rgba(current_link.count),
        )
        ax.add_patch(patch)
        return patch

    path_objects = {}
    for key, link in network.link_items():
        path_objects[link.hash()] = make_path(
            annotations[link.a()].xy,
            annotations[link.b()].xy,
            link
        )

    return path_objects


def _add_colour_bar(ax: plt.Axes, fig: plt.Figure, color_map: mpl.cm.ScalarMappable) -> mpl.colorbar.Colorbar:
    color_bar = fig.colorbar(color_map, ax=[ax])
    return color_bar


def quick_plot(network: LinkedNetwork, fig: plt.Figure, ax: plt.Axes, bbox_style: dict = None, **kwargs):
    """
    :param fig: pyplot figure
    :param ax: Single plot axis to use as the base for plotting ( send as axis[0] if using multiple plots )
    :param bbox_style: override annotation.bbox style -
        Defaults: boxstyle = "circle", pad =  0.3, fc = "cyan", ec = "b"
    :keyword node_text_size: text size to use for each node
    :param network: filled LinkedNetwork to use as a base
    :return:
    """
    if bbox_style is None:
        bbox_style = dict(boxstyle='circle', pad=0.3, fc='cyan', ec='b')
    color_map = _make_colour_map(network)
    annotations = _set_text_anchor_positions(network, ax, bbox_style, **kwargs)
    _set_annotation_lines(network, ax, annotations, color_map, **kwargs)
    _add_colour_bar(ax, fig, color_map)
