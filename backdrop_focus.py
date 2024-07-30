import nuke
import nukescripts
from PySide2 import QtWidgets, QtCore

def get_main_window():
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.metaObject().className() == "Foundry::UI::DockMainWindow":
            return widget
    return None

def get_properties_panel(node):
    main_window = get_main_window()
    if not main_window:
        return None

    # Recursively search for the properties panel
    def find_panel(widget, node_name):
        for child in widget.findChildren(QtWidgets.QWidget):
            if node_name in child.windowTitle():
                return child
            result = find_panel(child, node_name)
            if result:
                return result
        return None

    return find_panel(main_window, node.name())

def get_first_qtextedit(panel):
    # Recursively search for the first QTextEdit
    def find_qtextedit(widget):
        for child in widget.findChildren(QtWidgets.QTextEdit):
            return child
        for child in widget.findChildren(QtWidgets.QWidget):
            result = find_qtextedit(child)
            if result:
                return result
        return None

    return find_qtextedit(panel)

def set_focus_on_first_qtextedit(node):
    # Show the properties panel for the node
    nuke.show(node)

    # Get the properties panel
    panel = get_properties_panel(node)
    if not panel:
        print(f"Properties panel for node '{node.name()}' not found")
        return

    # Get the first QTextEdit widget
    widget = get_first_qtextedit(panel)
    if widget:
        widget.setFocus()
        print(f"Focus set on the first QTextEdit widget")
    else:
        print(f"No QTextEdit widget found in properties panel of node '{node.name()}'")

# Example usage
# node = nuke.selectedNode()
# set_focus_on_first_qtextedit(node)
