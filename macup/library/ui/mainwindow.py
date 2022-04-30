import os

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

import macup.library.config as cfglib
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
        self.delfilter_btn.clicked.connect(self.deleteSelectedFilter)

        self.testfilter_btn.clicked.connect(self.openTestingItemFileDialog)
        self.testfilter_lnedit.textChanged.connect(self.applyFiltersToTest)

        self.backup_btn.clicked.connect(self.startBackup)

        # Unsaved changes detection
        # textEdited must be used - textChanged causes problems when switching between configs
        self.src_line.textEdited.connect(self.noteUnsavedChanges)
        self.target_line.textEdited.connect(self.noteUnsavedChanges)
        self.overwrite_check.stateChanged.connect(self.noteUnsavedChanges)

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
                if QMessageBox.question(self, "",
                                        "Do you want to load the new configuration?") == QMessageBox.StandardButton.Yes:
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

        # The loaded_cfg attribute is modified directly when filters are edited, i.e., filters are directly changed
        # when they are edited

        self.loaded_cfg.overwrite = self.overwrite_check.isChecked()

        cfglib.saveConfig(self.loaded_cfg, self.data_path)
        self.noteSavedChanges()
        QMessageBox.information(self, "", "Save successful.")

    def loadCfg(self, name):
        """ Populate the UI with data from the config specified by name """
        # Set attribute
        self.loaded_cfg = cfglib.loadConfig(name, self.data_path)

        # Set target and source directory
        self.src_line.setText(self.loaded_cfg.source_dir)
        self.target_line.setText(self.loaded_cfg.target_dir)

        # Filters
        self.filter_listwidget.clear()
        self.filter_listwidget.addItems([filter_.name for filter_ in self.loaded_cfg.filters])

        self.overwrite_check.setChecked(self.loaded_cfg.overwrite)

        self.cfgselect_combobox.setCurrentIndex(self.cfgselect_combobox.findText(self.loaded_cfg.name))

    def selectSourceDir(self):
        """ Opens the directory selection when the source directory button is pressed """
        self.openFileDialog(self.src_line)

    def selectTargetDir(self):
        """ Opens the directory selection when the target directory button is pressed """
        self.openFileDialog(self.target_line)

    def openFileDialog(self, target_lineedit=None):
        """ Opens a QFileDialog, configured for selecting directories """
        file_dlg = QtWidgets.QFileDialog()
        selected_dir = file_dlg.getExistingDirectory()

        # Check that the user didn't press cancel, which returns a blank, falsy string
        if selected_dir:
            if target_lineedit is not None:
                target_lineedit.setText(selected_dir)
                self.noteUnsavedChanges()
            return selected_dir

    def openAddFilterDialog(self):
        """ Opens the dialog for adding a filter """
        edit_filter_dlg = ModifyFilterDialogUI()
        edit_filter_dlg.setWindowTitle("Add filter")
        response = edit_filter_dlg.exec()

        if response == 1:
            filter_ = edit_filter_dlg.filter_
            if filter_ is not None:
                self.loaded_cfg.filters.append(filter_)

                self.filter_listwidget.addItem(filter_.name)
                self.noteUnsavedChanges()
                self.applyFiltersToTest()

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
        # Get the filter that matches the filter name supplied
        editing_filter = None
        for filter_ in self.loaded_cfg.filters:
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

        # Fill filter type
        if editing_filter.filter_type == consts.REGEX:
            index = 0
        elif editing_filter.filter_type == consts.KEYWORD:
            index = 1
        else:
            QMessageBox(self, "",
                        "Invalid index for filter type - you shouldn't be seeing this. Please tell the developer.")
            return
        edit_filter_dlg.ui.filtertype_combobox.setCurrentIndex(index)

        # Fill data
        edit_filter_dlg.ui.datalineedit.setText(editing_filter.data)

        # Fill application box
        if editing_filter.application == consts.PATHS:
            index = 0
        elif editing_filter.application == consts.FILENAMES:
            index = 1
        else:
            QMessageBox(self, "",
                        "Invalid index for application - you shouldn't be seeing this. Please tell the developer.")
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
            QMessageBox(self, "",
                        "Invalid index for item type - you shouldn't be seeing this. Please tell the developer.")
            return
        edit_filter_dlg.ui.typecombobox.setCurrentIndex(index)

        # Fill whitelist
        edit_filter_dlg.ui.whitelistradiobtn.setChecked(editing_filter.whitelist)

        # Open UI
        response = edit_filter_dlg.exec()

        if response == 1:
            # Edit filter with new attributes
            for i, filter_ in enumerate(self.loaded_cfg.filters):
                # For each filter, compare its name with the name provided, break after editing the filter if found
                if filter_.name == filter_name:
                    # Apply the edit
                    self.loaded_cfg.filters[i] = edit_filter_dlg.filter_

                    # Note unsaved changes and return
                    self.noteUnsavedChanges()
                    self.applyFiltersToTest()
                    return

            # The filter should have been found
            QMessageBox.warning(self, "", "Filter could not be edited. Please tell the developer.")

    def deleteSelectedFilter(self):
        """ Deletes the selected filter from the list of filters, returns true if successful """
        if len(self.filter_listwidget.selectedItems()) == 0:
            QMessageBox.information(self, "", "No filters selected.")
        elif len(self.filter_listwidget.selectedItems()) == 1:
            filter_to_del_name = self.filter_listwidget.selectedItems()[0].text()
            if QMessageBox.question(self, "", f"Are you sure you want to delete {filter_to_del_name}?") == QMessageBox.StandardButton.Yes:
                # Remove filter
                for i, filter_ in enumerate(self.loaded_cfg.filters):
                    if filter_.name == filter_to_del_name:
                        self.loaded_cfg.filters.pop(i)

                # Update UI
                self.filter_listwidget.takeItem(self.filter_listwidget.selectedIndexes()[0].row())
                self.noteUnsavedChanges()
                self.applyFiltersToTest()
                return True

        return False

    def openTestingItemFileDialog(self):
        """ Opens the FileDialog to select a file to test the filters """
        file_dlg = QtWidgets.QFileDialog()
        selected_dir = file_dlg.getOpenFileName()[0]  # todo: allow for dir selection if possible

        # Check that the user didn't press cancel, which returns a blank, falsy string
        if selected_dir:
            # Set lineedit
            self.testfilter_lnedit.setText(selected_dir)
            self.applyFiltersToTest()
            return selected_dir

    def applyFiltersToTest(self):
        """ Updates the test label """
        from macup.library.filter import applyFilters
        if self.testfilter_lnedit.text() == "":
            # Path is blank
            self.testfilteroutput_label.setText("No item selected.")
        elif applyFilters(self.loaded_cfg.filters, self.testfilter_lnedit.text()):
            # Item will be copied
            self.testfilteroutput_label.setText("Item matches this filter, and will be copied.")
        else:
            # Item will not be copied
            self.testfilteroutput_label.setText("Item does not match this filter, and will not be copied.")

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

    def startBackup(self):
        """ Starts the backup, returns true if successful """
        # Force the configuration to be saved
        if self.unsavedChanges:
            QMessageBox.warning(self, "", "Save the configuration before backing up.")
            return False

        # Check paths are valid
        if not os.path.isdir(self.loaded_cfg.source_dir):
            QMessageBox.warning(self, "", "Invalid source directory.")
            return False
        elif not os.path.isdir(self.loaded_cfg.target_dir):
            QMessageBox.warning(self, "", "Invalid target directory.")
            return False

        from macup.library.backup import backup
        backup(src_dir=self.loaded_cfg.source_dir,
               target_dir=self.loaded_cfg.target_dir,
               filters=self.loaded_cfg.filters,
               overwrite=self.overwrite_check.isChecked())


def main():
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
