from gi.repository import Gtk
from dialogs import NewProcessDialog, AboutDialog
import os


class PSMenu:
    def __init__(self, parent):
        action_group = Gtk.ActionGroup("my_actions")
        self.add_file_menu_actions(action_group)
        self.add_about_menu_action(action_group)
        self.add_view_menu_actions(action_group)
        self.parent = parent
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        self.menubar = uimanager.get_widget("/MenuBar")

    def _action(self, action_group, **kwargs):
        action = Gtk.Action(kwargs.get('menu_group', None), kwargs.get('menu_item', None),
            None, None, kwargs.get('menu_item_gtk_stock', None))
        cb = kwargs.get('callback', None)
        if cb is not None:
            action.connect('activate', cb)
        action_group.add_action(action)
        return action

    def add_view_menu_actions(self, action_group):
        self._action(action_group, menu_group='ViewMenu', menu_item='View')
        self._action(action_group, menu_group='ViewProcesses', menu_item='Tasks',
            callback=self.on_view_processes_click)
        self._action(action_group, menu_group='ViewCPUs', menu_item='CPU/Memory usage',
            callback=self.on_view_stats_cick)
        self._action(action_group, menu_group='ViewNetwork', menu_item='Network',
            callback=self.on_view_network_click)

    def add_file_menu_actions(self, action_group):
        self._action(action_group, menu_group='FileMenu', menu_item='File')
        self._action(action_group, menu_group='FileQuit', menu_item='Quit',
            menu_item_gtk_stock=Gtk.STOCK_QUIT, callback=Gtk.main_quit)
        self._action(action_group, menu_group='FileNew', menu_item='New',
            menu_item_gtk_stock=Gtk.STOCK_NEW, callback=self.on_new_click)

    def add_about_menu_action(self, action_group):
        self._action(action_group, menu_group='HelpMenu', menu_item='Help')
        self._action(action_group, menu_group='AboutMenu', menu_item='About', callback=self.about_dialog)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_file("gps/views/menu.xml")
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

    def on_view_processes_click(self, param):
        self.parent.show_processes()

    def on_view_stats_cick(self, param):
        self.parent.show_stats()

    def on_view_network_click(self, param):
        self.parent.show_network()
