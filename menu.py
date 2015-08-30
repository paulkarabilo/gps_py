from gi.repository import Gtk

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='FileQuit' />
    </menu>
  </menubar>
</ui>
"""


class PSMenu:
    def __init__(self):
        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        self.menubar = uimanager.get_widget("/MenuBar")

    @classmethod
    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)
        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", Gtk.main_quit)
        action_group.add_action(action_filequit)

    @classmethod
    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(UI_INFO)
        return uimanager
