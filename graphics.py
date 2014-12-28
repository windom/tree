import binascii
import collections
import math
import struct
import svgwrite

import utils as u


class MyCanvas(u.Deferrable):

    def __init__(self, canvas=None):
        super().__init__()
        self.canvas = canvas

    @u.deferred
    def draw_line(self, source, dest, fill=None, width=None):
        self.canvas.create_line(source.x, source.y,
                                dest.x, dest.y,
                                fill=rgb_to_hex(fill),
                                width=width)

    @u.deferred
    def draw_polygon(self, points, fill=None, outline=None):
        self.canvas.create_polygon(points,
                                   fill=rgb_to_hex(fill),
                                   outline=outline)


class SvgCanvas:

    def __init__(self, name):
        self.dwg = svgwrite.Drawing(name, profile='tiny')
        self.gradient_ids = 0

    def draw_polygon(self, points, **opts):
        def make_command(type, point):
            return "{} {} {}".format(type, point.x, point.y)
        scommands = [make_command('M', points[0])] + \
                    [make_command('L', point) for point in points[1:]] + \
                    ['z']
        self.dwg.add(self.dwg.path(scommands, **opts))

    def draw_line(self, source, dest, fill=None, width=None):
        opts = {
            "stroke-linecap": "round"
        }
        if fill: opts["stroke"] = rgb_to_hex(fill)
        if width: opts["stroke-width"] = width
        self.dwg.add(self.dwg.line(
                     start=source,
                     end=dest,
                     **opts))

    def save(self):
        self.dwg.save()


Point = collections.namedtuple('Point', ['x', 'y'])


def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 +
                     (p1.y - p2.y)**2)


def rgb_to_hex(rgb):
    if not rgb:
        return None
    return "#" + binascii.hexlify(struct.pack('BBB', *rgb)).decode('ascii')


def weighted_color(from_rgb, to_rgb):
    def get_color(weight):
        return (int(from_rgb[0] + weight*(to_rgb[0] - from_rgb[0])),
                int(from_rgb[1] + weight*(to_rgb[1] - from_rgb[1])),
                int(from_rgb[2] + weight*(to_rgb[2] - from_rgb[2])))
    return get_color
