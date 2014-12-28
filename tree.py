import math
import random as r
from collections import deque

import graphics as gr


def branch(edge, pos_ratio, angle, len_ratio):
    ep1, ep2 = edge

    p1 = gr.Point(ep1.x + (ep2.x - ep1.x) * pos_ratio,
                  ep1.y + (ep2.y - ep1.y) * pos_ratio)

    x = ep2.x - ep1.x
    y = ep2.y - ep1.y
    xr = x*math.cos(angle) -y*math.sin(angle)
    yr = x*math.sin(angle) + y*math.cos(angle)
    xr *= len_ratio
    yr *= len_ratio

    p2 = gr.Point(p1.x + xr, p1.y + yr)

    return (p1, p2)


def skew_interval(split, w):
    """
        [0, split] -> [0, 1-split]
        [split, 1] -> [1-split, split]
    """
    lsplit = 1-split
    if w <= split:
        return w * lsplit / split
    else:
        return lsplit + (w - split) * split / lsplit


def generate(*canvases, **opts):
    edges = deque([(
                  gr.Point(*opts['p1']),
                  gr.Point(*opts['p2'])
                  )])

    def get_color(weight,
                  weighted_color=gr.weighted_color(opts['leaf_color'],
                                                   opts['trunk_color']),
                  split_color=opts['split_color']):
        return weighted_color(skew_interval(split_color, weight))

    def get_width(weight,
                  min_width = opts['edge_minwidth'],
                  factor = opts['edge_widthfactor']):
        return max(min_width, factor * edge_weight)

    edge_count = 0
    edge_maxlen = None
    while edges:
        edge_count += 1

        edge = edges.popleft()
        edge_len = gr.dist(*edge)
        if edge_maxlen is None: edge_maxlen = edge_len
        edge_weight = edge_len / edge_maxlen
        edge_color = get_color(edge_weight)
        edge_width = get_width(edge_weight)

        for canvas in canvases:
            canvas.draw_line(*edge, fill=edge_color, width=edge_width)

        if edge_len > opts["edge_minlen"]:
            for pos_ratio_interval, angle_interval, len_ratio_interval in opts['branch_defs']:
                new_edge = branch(edge,
                                  r.uniform(*pos_ratio_interval),
                                  r.uniform(*angle_interval),
                                  r.uniform(*len_ratio_interval))
                edges.append(new_edge)

    print("Generated", edge_count, "edges")
