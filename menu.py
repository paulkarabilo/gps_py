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
        uimanager = Gtk.UIManager()
        action_group = Gtk.ActionGroup('menu_actions')
        self.add_file_menu_actions(action_group)

        uimanager.add_ui_from_string(UI_INFO)
        self.accel_group = uimanager.get_accel_group()

        uimanager.insert_action_group(action_group)

        self.menubar = uimanager.get_widget("/MenuBar")


    def add_file_menu_actions(self, action_group):
        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", Gtk.main_quit)
        action_group.add_action(action_filequit)
