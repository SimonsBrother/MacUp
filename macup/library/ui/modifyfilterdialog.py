from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog

from macup.ui.modifyfilter import Ui_modifyfilter

from macup.library.classes import RegexFilter, KeywordFilter
from macup.library.constants import *
from macup.library.filter import applyFilter


class ModifyFilterDialogUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_modifyfilter()
        self.ui.setupUi(self)
        self.setWindowTitle("Edit filter")

        # Initialise filter
        self.filter_ = None

        # Initialises the Data label
        self.whenFTypeCBoxChanged()

        self.ui.filtertype_combobox.currentIndexChanged.connect(self.whenFTypeCBoxChanged)
        self.ui.testfileselect_btn.clicked.connect(self.openFilterTestFile)

        # Update filter test output connections
        self.ui.namelineedit.textChanged.connect(self.updateFilterTestOutput)
        self.ui.filtertype_combobox.currentIndexChanged.connect(self.updateFilterTestOutput)
        self.ui.datalineedit.textChanged.connect(self.updateFilterTestOutput)
        self.ui.appcombobox.currentIndexChanged.connect(self.updateFilterTestOutput)
        self.ui.typecombobox.currentIndexChanged.connect(self.updateFilterTestOutput)
        self.ui.whitelistradiobtn.clicked.connect(self.updateFilterTestOutput)
        self.ui.testlineedit.textChanged.connect(self.updateFilterTestOutput)

    def whenFTypeCBoxChanged(self):
        """ Updates some parts of the UI when the type of filter is changed """
        type_ = self.ui.filtertype_combobox.currentText()
        self.ui.datalabel.setText(f"{type_}:")
        if type_ == "Regex":
            self.ui.regex101_label.show()
        else:
            self.ui.regex101_label.hide()

    def buildFilter(self):
        """ Returns either a KeywordFilter or RegexFilter object, depending on the values set in the UI """
        application_index = self.ui.appcombobox.currentIndex()
        if application_index == 0:
            application = PATHS
        else:
            application = FILENAMES

        item_type_index = self.ui.typecombobox.currentIndex()
        if item_type_index == 0:
            item_type = BOTH
        elif item_type_index == 1:
            item_type = DIRECTORY
        else:
            item_type = FILES

        if self.ui.filtertype_combobox.currentText() == "Regex":
            return RegexFilter(
                name=self.ui.namelineedit.text(),
                regex=self.ui.datalineedit.text(),
                application=application,
                item_type=item_type,
                whitelist=self.ui.whitelistradiobtn.isChecked()
            )
        else:
            return KeywordFilter(
                name=self.ui.namelineedit.text(),
                keyword=self.ui.datalineedit.text(),
                application=application,
                item_type=item_type,
                whitelist=self.ui.whitelistradiobtn.isChecked()
            )

    def openFilterTestFile(self):
        """ Opens the QFileDialog to select a path to test the filter on """
        file_dlg = QFileDialog()
        selected_dir = file_dlg.getOpenFileName()[0]  # todo: allow for dir selection if possible

        # Check that the user didn't press cancel, which returns a blank, falsy string
        if selected_dir:
            # Set lineedit
            self.ui.testlineedit.setText(selected_dir)
            self.updateFilterTestOutput()
            return selected_dir

    def updateFilterTestOutput(self):
        """ Updates the output of the filter testing label, also updates the filter attribute to be passed back to main """

        self.filter_ = self.buildFilter()
        regex_filters = [self.filter_] if isinstance(self.filter_, RegexFilter) else []
        kw_filters = [self.filter_] if isinstance(self.filter_, KeywordFilter) else []

        if self.ui.testlineedit.text() == "":
            # Path is blank
            self.ui.testfilteroutputlabel.setText("No item selected.")
        elif applyFilter(regex_filters, kw_filters, self.ui.testlineedit.text()):
            # Item will be copied
            self.ui.testfilteroutputlabel.setText("Item matches this filter, and will be copied.")
        else:
            # Item will not be copied
            self.ui.testfilteroutputlabel.setText("Item does not match this filter, and will not be copied.")


if __name__ == "__main__":
    app = QApplication([])

    window = ModifyFilterDialogUI()
    window.show()
    app.exec()
