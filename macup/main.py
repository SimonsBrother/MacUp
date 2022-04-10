from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

import macup.library.config as cfglib
from macup.library.classes import Configuration

from macup.ui.mainwindow import Ui_MainWindow
from macup.library.ui.addconfig import AddConfigDialogUI
#from macup.library.modifyfilter import Ui_modifyfilter


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("MacUp")

        self.data_path = cfglib.TEST_LOC  # todo: work out somewhere to place configs
        self.unsaved = False
        self.loaded_cfg = None  # This is set by populateCfgBox
        self.configs = []  # Set by populateCfgBox in next line
        self.populateCfgBox()

        self.addcfg_btn.clicked.connect(self.openAddCfg)
        self.delcfg_btn.clicked.connect(self.handleDelCfg)
        self.savecfg_btn.clicked.connect(self.saveCfg)
        self.cfgselect_combobox.textActivated.connect(self.cfgSelected)

    def openAddCfg(self):
        """ Opens the Add configuration UI """
        addcfg_dlg = AddConfigDialogUI()

        if addcfg_dlg.exec():
            cfg_name = addcfg_dlg.ui.name_lineedit.text()

            if not cfg_name:
                # If name blank, warn the user
                QMessageBox.warning(self, "", "Invalid name - configuration name cannot be blank.")

            elif cfglib.checkNameExists(cfg_name, self.data_path):
                # If name used, warn the user
                QMessageBox.warning(self, "", "That name is already used in a configuration file.")

            else:
                # Save the new configuration
                cfglib.saveNewBlankConfig(cfg_name, self.data_path)
                self.populateCfgBox()

                if QMessageBox.question(self, "", "Do you want to load the new configuration?") == QMessageBox.StandardButton.Yes:
                    # Automatically load the new configuration todo: test this behaviour once change detection implemented
                    if not self.loadCfg(cfg_name):
                        QMessageBox.warning(self, "", "Could not load new configuration.")

    def handleDelCfg(self):
        """ Opens a deletion warning box - deletes the open config if that's what the user wants"""
        # todo: change icon to warning
        response = QMessageBox.question(self, "", f"Are you sure you want to delete this configuration: {self.loaded_cfg.name}?")
        if response == QMessageBox.StandardButton.Yes:
            # Delete config
            cfglib.deleteConfig(self.loaded_cfg.name, self.data_path)
            # Reload combobox
            self.populateCfgBox()

    def cfgSelected(self, text):
        """ Handles loading configurations from combo box when selected """
        self.loadCfg(text)

    def saveCfg(self):
        """ Saves the loaded configuration to the persistent file """
        self.loaded_cfg.source_dir = self.src_line.text()
        self.loaded_cfg.target_dir = self.target_line.text()

        # The loaded_cfg property is modified directly when filters are edited

        self.loaded_cfg.overwrite = self.overwrite_check.isChecked()

        cfglib.saveConfig(self.data_path, self.loaded_cfg)
        QMessageBox.information(self, "", "Save successful.")

    def loadCfg(self, name):
        """ Populate the UI with data from the config specified by name - unsaved changes are handled
            :returns true if the config was loaded"""

        if self.unsaved:
            # If there are unsaved changes, ask user
            response = QMessageBox.question(self, "", "There are unsaved configuration changes. Do you want to save first?")
            if response == QMessageBox.StandardButton.Yes:
                # Saves the config
                cfglib.saveConfig(self.data_path, self.loaded_cfg)

            elif response == QMessageBox.StandardButton.Close:
                # todo: test close behaviour
                # Closing the window should cancel the process
                return False

        self.loaded_cfg = cfglib.loadConfig(name, self.data_path)

        self.src_line.setText(self.loaded_cfg.source_dir)
        self.target_line.setText(self.loaded_cfg.target_dir)

        self.filter_listwidget.clear()
        filters = self.loaded_cfg.regex_filters + self.loaded_cfg.keyword_filters
        self.filter_listwidget.addItems([filter_.name for filter_ in filters])

        self.overwrite_check.setChecked(self.loaded_cfg.overwrite)

        self.cfgselect_combobox.setCurrentIndex(self.cfgselect_combobox.findText(self.loaded_cfg.name))

        return True

    def populateCfgBox(self):
        """ Loads config names and populates the combo box with them """
        self.configs = cfglib.loadConfigs(self.data_path)

        selected_name = self.cfgselect_combobox.currentText()

        names = [config.name for config in self.configs]
        self.cfgselect_combobox.clear()
        self.cfgselect_combobox.addItems(names)

        if selected_name in names:
            # If the config still exists, reload it
            name_to_load = selected_name
        else:
            # If the config was deleted, it should load the first config
            # When called at start, selected name is blank, so this runs on start
            self.loaded_cfg = self.configs[0]
            name_to_load = self.loaded_cfg.name

        self.loadCfg(name_to_load)
        self.cfgselect_combobox.setCurrentIndex(self.cfgselect_combobox.findText(name_to_load))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
