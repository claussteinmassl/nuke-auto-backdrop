# auto backdrop for The Foundry's Nuke

## About 
This tool enhances the default behavior from The Foundry's Nuke when creating backdrop nodes.
Nuke will create a backdrop node with a random color, which can be quite unpleasant to the eyes.

This tool will create a backdrop node with only grey colors. If another background is already part of the selection, it will take the z-order into account and make the color a bit darker.
It will also put the focus directly to the backdrop's label, so you can start typing right away.

By default, it uses the shortcut shift-b to create a backdrop node. That way you can very quickly organize your script.

[auto_backdrop.mp4](auto_backdrop.mp4)

## Installation

Clone this repository into your Nuke's user directory or any other directory that is part of the Nuke's plugin path.
> git clone https://github.com/claussteinmassl/nuke-auto-backdrop

Rename the menu_example.py to menu.py and adjust the menu entry to your liking.