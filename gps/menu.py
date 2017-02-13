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

    def add_view_menu_actions(self, action_group):
        action_viewmenu = Gtk.Action("ViewMenu", "View", None, None)
        action_group.add_action(action_viewmenu)
        
        action_viewprocesses = Gtk.Action("ViewProcesses", "Tasks", None, None)
        action_viewprocesses.connect("activate", self.on_view_processes_click)
        action_group.add_action(action_viewprocesses)

        action_viewcpus = Gtk.Action("ViewCPUs", "CPU/Memory usage", None, None)
        action_viewcpus.connect("activate", self.on_view_cpus_cick)
        action_group.add_action(action_viewcpus)
        
        action_viewnetwork = Gtk.Action("ViewNetwork", "Network", None, None)
        action_viewnetwork.connect("activate", self.on_view_network_click)
        action_group.add_action(action_viewnetwork)

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
        uimanager.add_ui_from_file("gps/menu.xml")
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

    def on_view_cpus_cick(self, param):
        self.parent.show_cpus()

    def on_view_network_click(self, param):
        self.parent.show_network()
