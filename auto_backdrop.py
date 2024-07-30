# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# Edit by Claus Steinmassl

import nuke
from backdrop_focus import *

def hex_color(r, g, b):
    return int('%02x%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255), 0), 16)


def node_is_inside(node, backdrop_node):
    """Returns true if node geometry is inside backdrop_node otherwise returns false"""
    top_left_node = [node.xpos(), node.ypos()]
    top_left_back_drop = [backdrop_node.xpos(), backdrop_node.ypos()]
    bottom_right_node = [node.xpos() + node.screenWidth(),
                       node.ypos() + node.screenHeight()]
    bottom_right_backdrop = [backdrop_node.xpos(
    ) + backdrop_node.screenWidth(), backdrop_node.ypos() + backdrop_node.screenHeight()]

    top_left = (top_left_node[0] >= top_left_back_drop[0]) and (
        top_left_node[1] >= top_left_back_drop[1])
    bottom_right = (bottom_right_node[0] <= bottom_right_backdrop[0]) and (
        bottom_right_node[1] <= bottom_right_backdrop[1])

    return top_left and bottom_right


def auto_backdrop():
    """
    Automatically puts a backdrop behind the selected nodes.

    The backdrop will be just big enough to fit all the select nodes in, with room
    at the top for some text in a large font.
    """
    sel_nodes = nuke.selectedNodes()
    if not sel_nodes:
        return nuke.nodes.BackdropNode()

    if sel_nodes[0].screenWidth() == 0:
        screen_width = 100
        screen_height = 100
    else:
        screen_width = 0
        screen_height = 0
    # Calculate bounds for the backdrop node.
    bd_x = min([node.xpos() for node in sel_nodes])
    bd_y = min([node.ypos() for node in sel_nodes])
    bd_w = max([node.xpos() + node.screenWidth() +
              screen_width for node in sel_nodes]) - bd_x
    bd_h = max([node.ypos() + node.screenHeight() +
              screen_height for node in sel_nodes]) - bd_y

    z_order = 0
    selected_backdrop_nodes = nuke.selectedNodes("BackdropNode")
    # if there are backdropNodes selected put the new one immediately behind the farthest one
    if len(selected_backdrop_nodes):
        z_order = min([node.knob("z_order").value()
                     for node in selected_backdrop_nodes]) - 1
    else:
        # otherwise (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
        non_selected_backdrop_nodes = nuke.allNodes("BackdropNode")
        for non_backdrop in sel_nodes:
            for backdrop in non_selected_backdrop_nodes:
                if node_is_inside(non_backdrop, backdrop):
                    z_order = max(z_order, backdrop.knob("z_order").value() + 1)

    # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
    left, top, right, bottom = (-30, -110, 30, 30)
    bd_x += left
    bd_y += top
    bd_w += (right - left)
    bd_h += (bottom - top)

    # start with a dark grey and make the backdrop darker, if it's further in the back
    start_color = 0.35
    color_offset = z_order
    # color_offset should always be positive
    if color_offset < 0:
        color_offset = color_offset * -1
    tmp = start_color - 0.05 * color_offset
    # check, if color would be darker than dag bg
    if tmp < 0.2:
        color_offset += 1
    dst = start_color - 0.05 * color_offset
    # clamp negative colors
    if dst < 0:
        dst = 0
    dst_color_int = hex_color(dst, dst, dst)
    if dst_color_int == 0:
        dst_color_int = 255

    n = nuke.nodes.BackdropNode(xpos=bd_x,
                                bdwidth=bd_w,
                                ypos=bd_y,
                                bdheight=bd_h,
                                tile_color=dst_color_int,
                                z_order=z_order,
                                note_font_size=60,
                                note_font="Verdana Bold")

    n.showControlPanel()
    # revert to previous selection
    n['selected'].setValue(False)
    for node in sel_nodes:
        node['selected'].setValue(True)

    set_focus_on_first_qtextedit(n)

    return n
