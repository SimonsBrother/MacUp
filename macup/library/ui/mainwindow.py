from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

import macup.library.config as cfglib
from macup.library.classes import Configuration, RegexFilter, KeywordFilter
import macup.library.constants as consts

from macup.ui.mainwindow import Ui_MainWindow
from macup.library.ui.addconfig import AddConfigDialogUI
from macup.library.ui.modifyfilterdialog import ModifyFilterDialogUI


window_title = "MacUp"


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(window_title)

        self.data_path = cfglib.TEST_LOC  # todo: work out somewhere to place configs
        self.selected_config_log = []
        self.unsavedChanges = False
        self.loaded_cfg = None  # This is set by populateCfgBox
        self.configs = []  # Set by populateCfgBox in next line
        self.populateCfgBox()

        self.addcfg_btn.clicked.connect(self.openAddCfg)
        self.delcfg_btn.clicked.connect(self.handleDelCfg)
        self.savecfg_btn.clicked.connect(self.saveCfg)
        self.cfgselect_combobox.textActivated.connect(self.cfgSelected)
        self.cfgselect_combobox.activated.connect(self.recordConfigSelection)
        self.src_btn.clicked.connect(self.selectSourceDir)
        self.target_btn.clicked.connect(self.selectTargetDir)
        self.addfilter_btn.clicked.connect(self.openAddFilterDialog)
        self.editfilter_btn.clicked.connect(self.openEditFilterDialog_byBtn)

        # Unsaved changes detection
        # textEdited must be used - textChanged causes problems when switching between configs
        self.src_line.textEdited.connect(self.noteUnsavedChanges)
        self.target_line.textEdited.connect(self.noteUnsavedChanges)

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
                # Offer to load
                if QMessageBox.question(self, "", "Do you want to load the new configuration?") == QMessageBox.StandardButton.Yes:
                    # Automatically load the new configuration depending on user's actions
                    save = self.unsavedChangesCheck()
                    if save != QMessageBox.StandardButton.Cancel:
                        if save == QMessageBox.StandardButton.Save:
                            self.saveCfg()
                        self.loadCfg(cfg_name)
                        self.populateCfgBox(cfg_name)
                    else:
                        # If cancelled, just update cfg box
                        self.populateCfgBox()
                else:
                    self.populateCfgBox()

    def handleDelCfg(self):
        """ Opens a deletion warning box - deletes the open config if that's what the user wants"""
        # todo: change icon to warning
        response = QMessageBox.question(self, "",
                                        f"Are you sure you want to delete this configuration: {self.loaded_cfg.name}?")
        if response == QMessageBox.StandardButton.Yes:
            # Delete config
            cfglib.deleteConfig(self.loaded_cfg.name, self.data_path)
            # Reload combobox
            self.populateCfgBox()

    def cfgSelected(self, text):
        """ Handles loading configurations from combo box when selected """

        response = self.unsavedChangesCheck()
        if response != QMessageBox.StandardButton.Cancel:
            if response == QMessageBox.StandardButton.Save:
                # Save changes
                self.saveCfg()

            # Load the config selected
            self.loadCfg(text)
            # Unsaved changes have been managed
            self.noteSavedChanges()

        else:
            # If cancelled, return to previous config
            self.cfgselect_combobox.setCurrentIndex(self.selected_config_log[-2])
            self.selected_config_log.pop(-1)

    def saveCfg(self):
        """ Saves the loaded configuration to the persistent file """
        self.loaded_cfg.source_dir = self.src_line.text()
        self.loaded_cfg.target_dir = self.target_line.text()

        # The loaded_cfg property is modified directly when filters are edited

        self.loaded_cfg.overwrite = self.overwrite_check.isChecked()

        cfglib.saveConfig(self.data_path, self.loaded_cfg)
        self.noteSavedChanges()
        QMessageBox.information(self, "", "Save successful.")

    def loadCfg(self, name):
        """ Populate the UI with data from the config specified by name """

        self.loaded_cfg = cfglib.loadConfig(name, self.data_path)

        self.src_line.setText(self.loaded_cfg.source_dir)
        self.target_line.setText(self.loaded_cfg.target_dir)

        self.filter_listwidget.clear()
        filters = self.loaded_cfg.regex_filters + self.loaded_cfg.keyword_filters
        self.filter_listwidget.addItems([filter_.name for filter_ in filters])

        self.overwrite_check.setChecked(self.loaded_cfg.overwrite)

        self.cfgselect_combobox.setCurrentIndex(self.cfgselect_combobox.findText(self.loaded_cfg.name))

    def selectSourceDir(self):
        self.openFileDialog(self.src_line)

    def selectTargetDir(self):
        self.openFileDialog(self.target_line)

    def openFileDialog(self, target_lineedit=None):
        file_dlg = QtWidgets.QFileDialog()
        selected_dir = file_dlg.getExistingDirectory()

        # Check that the user didn't press cancel, which returns a blank, falsy string
        if selected_dir:
            if target_lineedit is not None:
                target_lineedit.setText(selected_dir)
                self.noteUnsavedChanges()
            return selected_dir

    def openAddFilterDialog(self):
        edit_filter_dlg = ModifyFilterDialogUI()
        edit_filter_dlg.setWindowTitle("Add filter")
        response = edit_filter_dlg.exec()

        if response == 1:
            filter_ = edit_filter_dlg.filter_
            if isinstance(filter_, RegexFilter):
                self.loaded_cfg.regex_filters.append(filter_)
            # Use elif in case None returned
            elif isinstance(filter_, KeywordFilter):
                self.loaded_cfg.keyword_filters.append(filter_)

            self.filter_listwidget.addItem(filter_.name)
            self.noteUnsavedChanges()

    def openEditFilterDialog_byBtn(self):
        """ Handles the opening of the dialog for editing a filter by edit btn, :returns true if successful """
        if len(self.filter_listwidget.selectedItems()) == 0:
            QMessageBox.information(self, "", "No filters selected.")
            return False
        else:
            self.openEditFilterDialog(self.filter_listwidget.selectedItems()[0].text())
            return True

    def openEditFilterDialog(self, filter_name):
        """ Handles opening a dialog for editing a filter, given an argument. To be called by other functions. """
        # todo: known bug with changing type of filter, going to change filter system
        # Get the filter that matches the filter name supplied
        editing_filter = None
        for filter_ in (self.loaded_cfg.regex_filters + self.loaded_cfg.keyword_filters):
            # For each filter, compare its name with the name provided, break out after noting the filter if found
            if filter_.name == filter_name:
                editing_filter = filter_
                break

        if editing_filter is None:
            # No non-existent filter name should be found.
            QMessageBox.warning(self, "", "Filter could not be found. Please tell the developer.")
            return

        edit_filter_dlg = ModifyFilterDialogUI()
        # Fill and disable name line edit
        edit_filter_dlg.ui.namelineedit.setText(editing_filter.name)
        edit_filter_dlg.ui.namelineedit.setEnabled(False)

        # Fill filter type and data
        edit_filter_dlg.ui.filtertype_combobox.setCurrentIndex(edit_filter_dlg.ui.filtertype_combobox.findText(editing_filter.filter_type))
        edit_filter_dlg.ui.datalineedit.setText(editing_filter.data)

        # Fill application box
        if editing_filter.application == consts.PATHS:
            index = 0
        elif editing_filter.application == consts.FILENAMES:
            index = 1
        else:
            QMessageBox(self, "", "Invalid index - you shouldn't be seeing this. Please tell the developer.")
            return
        edit_filter_dlg.ui.appcombobox.setCurrentIndex(index)

        # Fill item type box
        if editing_filter.item_type == consts.BOTH:
            index = 0
        elif editing_filter.item_type == consts.DIRECTORY:
            index = 1
        elif editing_filter.item_type == consts.FILES:
            index = 2
        else:
            QMessageBox(self, "", "Invalid index - you shouldn't be seeing this. Please tell the developer.")
            return
        edit_filter_dlg.ui.typecombobox.setCurrentIndex(index)

        # Fill whitelist
        edit_filter_dlg.ui.whitelistradiobtn.setChecked(editing_filter.whitelist)

        # Open UI
        response = edit_filter_dlg.exec()

        if response == 1:
            # Edit filter with new attributes
            for filter_ in (self.loaded_cfg.regex_filters + self.loaded_cfg.keyword_filters):
                # For each filter, compare its name with the name provided, break after editing the filter if found
                if filter_.name == filter_name:

                    # Set the filter being edited
                    filter_.filter_type = edit_filter_dlg.filter_.filter_type
                    filter_.data = edit_filter_dlg.filter_.data
                    filter_.application = edit_filter_dlg.filter_.application
                    filter_.item_type = edit_filter_dlg.filter_.item_type
                    filter_.whitelist = edit_filter_dlg.filter_.whitelist

                    # Note unsaved changes and return
                    self.noteUnsavedChanges()
                    return

            # The filter should have been found
            QMessageBox.warning(self, "", "Filter could not be edited. Please tell the developer.")

    def unsavedChangesCheck(self):
        """ Checks if there are unsaved changes, and asks the user what they want to do about it """
        if self.unsavedChanges:
            # If there are unsaved changes, ask user
            response = QMessageBox.warning(self, "", "There are unsaved changes.  Do you want to save?",
                                           buttons=QMessageBox.StandardButton.Save | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                                           defaultButton=QMessageBox.StandardButton.Save,
                                           )
            if response == QMessageBox.StandardButton.Yes:
                # Saves the config
                cfglib.saveConfig(self.data_path, self.loaded_cfg)
            return response

    def populateCfgBox(self, target=None):
        """ Loads config names and populates the combo box with them """
        self.configs = cfglib.loadConfigs(self.data_path)

        selected_name = self.cfgselect_combobox.currentText()

        names = [config.name for config in self.configs]
        self.cfgselect_combobox.clear()
        self.cfgselect_combobox.addItems(names)

        # Because the box is cleared and refilled, the selected item is reset to the top one. This can cause
        # the box to go out of sync with the rest of the UI.
        if target:
            # Force the box to select the item provided, if provided
            name_to_load = target
        elif selected_name not in names:
            # If the config was deleted, it should load the first config.
            # When called at start, selected name is blank, so this runs on start
            self.loaded_cfg = self.configs[0]
            name_to_load = self.loaded_cfg.name
            # Loads the first config too
            self.loadCfg(name_to_load)
        else:
            # Otherwise, try to stay with the original name
            name_to_load = selected_name

        self.recordConfigSelection(self.cfgselect_combobox.findText(name_to_load))
        self.cfgselect_combobox.setCurrentIndex(self.cfgselect_combobox.findText(name_to_load))

    def noteUnsavedChanges(self):
        self.setWindowTitle(window_title + "*")
        self.unsavedChanges = True

    def noteSavedChanges(self):
        self.setWindowTitle(window_title)
        self.unsavedChanges = False

    def recordConfigSelection(self, index):
        self.selected_config_log.append(index)


def main():
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
