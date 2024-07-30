import nuke
import auto_backdrop

nuke.menu("Nuke").addCommand("Your menu/auto backdrop", "auto_backdrop.auto_backdrop()", "shift+b")