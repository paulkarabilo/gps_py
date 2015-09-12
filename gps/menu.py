from gi.repository import Gtk
from dialogs import NewProcessDialog, AboutDialog
import os

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileNew' />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='AboutMenu' />
    </menu>
  </menubar>
</ui>
"""


class PSMenu:
    def __init__(self, parent):
        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)
        self.add_about_menu_action(action_group)
        self.parent = parent
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        self.menubar = uimanager.get_widget("/MenuBar")

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)
        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", Gtk.main_quit)
        action_group.add_action(action_filequit)
        action_filenew = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_filenew.connect("activate", self.on_new_click)
        action_group.add_action(action_filenew)

    def add_about_menu_action(self, action_group):
        action_helpmenu = Gtk.Action("HelpMenu", "Help", None, None)
        action_group.add_action(action_helpmenu)
        action_aboutmenu = Gtk.Action("AboutMenu", "About", None, None)
        action_aboutmenu.connect("activate", self.about_dialog)
        action_group.add_action(action_aboutmenu)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(UI_INFO)
        return uimanager

    def about_dialog(self, param):
        about = AboutDialog()
        about.run()
        about.destroy()

    def on_new_click(self, param):
        dialog = NewProcessDialog(self.parent)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            procname = dialog.get_procname()
            os.system(procname)
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()