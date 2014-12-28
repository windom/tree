import math
import random as r
import time

import ui
import graphics as gr
import tree

##############################################################################

def setup():
    return {
        "svg": True,
        "width": 500,
        "height": 500,
        "p1": (250 + r.randint(-20, 20), 480),
        "p2": (250 + r.randint(-20, 20), 280),
        "trunk_color": (139,35,35),
        "leaf_color": (152,251,152),
        "split_color": 0.07,
        "edge_minlen": 5,
        "edge_minwidth": 0.8,
        "edge_widthfactor": 10,
        "branch_defs": [
            ((0.2, 0.6), (+15/180 * math.pi, +45/180 * math.pi), (0.4, 0.7)),
            ((0.2, 0.6), (-15/180 * math.pi, -45/180 * math.pi), (0.4, 0.7)),
            ((1.0, 1.0), (+15/180 * math.pi, +45/180 * math.pi), (0.4, 0.7)),
            ((1.0, 1.0), (-15/180 * math.pi, -45/180 * math.pi), (0.4, 0.7))
        ]
    }
    # return {
    #     "svg": True,
    #     "width": 500,
    #     "height": 500,
    #     "p1": (250 + r.randint(-20, 20), 480),
    #     "p2": (250 + r.randint(-20, 20), 280),
    #     "trunk_color": (139,35,35),
    #     "leaf_color": (152,251,152),
    #     "split_color": 0.07,
    #     "edge_minlen": 5,
    #     "edge_minwidth": 0.8,
    #     "edge_widthfactor": 10,
    #     "branch_defs": [
    #         ((0.2, 0.6), (+15/180 * math.pi, +45/180 * math.pi), (0.4, 0.7)),
    #         ((0.2, 0.6), (-15/180 * math.pi, -45/180 * math.pi), (0.4, 0.7)),
    #         ((1.0, 1.0), (+15/180 * math.pi, +45/180 * math.pi), (0.4, 0.7)),
    #         ((1.0, 1.0), (-15/180 * math.pi, -45/180 * math.pi), (0.4, 0.7))
    #     ]
    # }


##############################################################################

def main():
    opts = setup()

    app = ui.DrawingUi(opts["width"], opts["height"], 'Tree')
    canvas = gr.MyCanvas(app.canvas)
    canvases = [canvas]

    if opts["svg"]:
        svg_name = "svg/" + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + ".svg"
        svg_canvas = gr.SvgCanvas(svg_name)
        canvases.append(svg_canvas)
        print("Save SVG to:", svg_name)

    print("Generating tree..")
    tree.generate(*canvases, **opts)

    if opts["svg"]:
        print("Saving SVG..")
        svg_canvas.save()

    print("Drawing..")
    canvas.flush_calls()

    print("Done.")
    app.run()

main()
