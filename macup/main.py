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
        self.configs = cfglib.loadConfigs(self.data_path)
        self.loaded_cfg = self.configs[0]
        self.unsaved = False

        self.loadCfg(self.loaded_cfg.name)

        self.addcfg_btn.clicked.connect(self.openAddCfg)

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
                cfglib.saveNewConfig(cfg_name, self.data_path)
                if QMessageBox.question(self, "", "Do you want to load the new configuration?") == QMessageBox.StandardButton.Yes:
                    # Automatically load the new configuration todo: test this behaviour
                    if not self.loadCfg(cfg_name):
                        QMessageBox.warning(self, "", "Could not load new configuration.")

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

        # Load the data into the UI
        self.loaded_cfg = cfglib.loadConfig(name, self.data_path)

        self.src_line.setText(self.loaded_cfg.source_dir)
        self.target_line.setText(self.loaded_cfg.target_dir)

        self.filter_listwidget.clear()
        filters = self.loaded_cfg.regex_filters + self.loaded_cfg.keyword_filters
        self.filter_listwidget.addItems([filter_.name for filter_ in filters])

        self.overwrite_check.setChecked(self.loaded_cfg.overwrite)

        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
