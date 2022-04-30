from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog

from macup.ui.modifyfilter import Ui_modifyfilter

from macup.library.classes import Filter
from macup.library.constants import *
from macup.library.filter import applyFilters


class ModifyFilterDialogUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_modifyfilter()
        self.ui.setupUi(self)
        self.setWindowTitle("Edit filter")

        # Initialise filter
        self.filter_ = None

        # Initialises the Data label
        self.whenFilterTypeCBoxChanged()

        self.ui.filtertype_combobox.currentIndexChanged.connect(self.whenFilterTypeCBoxChanged)
        self.ui.testfileselect_btn.clicked.connect(self.openFilterTestFile)

        # Update filter test output connections
        self.ui.namelineedit.textChanged.connect(self.updateFilterTestOutput)
        self.ui.filtertype_combobox.currentIndexChanged.connect(self.updateFilterTestOutput)
        self.ui.datalineedit.textChanged.connect(self.updateFilterTestOutput)
        self.ui.appcombobox.currentIndexChanged.connect(self.updateFilterTestOutput)
        self.ui.typecombobox.currentIndexChanged.connect(self.updateFilterTestOutput)
        self.ui.whitelistradiobtn.clicked.connect(self.updateFilterTestOutput)
        self.ui.testlineedit.textChanged.connect(self.updateFilterTestOutput)

    def whenFilterTypeCBoxChanged(self):
        """ Updates some parts of the UI when the type of filter is changed """
        filter_type = self.ui.filtertype_combobox.currentText()
        self.ui.datalabel.setText(f"{filter_type}:")

        # Hide/show the regex101 link
        if filter_type == REGEX:
            self.ui.regex101_label.show()
        else:
            self.ui.regex101_label.hide()

    def buildFilter(self):
        """ Returns a Filter object, depending on the values set in the UI """

        filter_type = self.ui.filtertype_combobox.currentIndex()
        if filter_type == 0:
            filter_type = REGEX
        else:
            filter_type = KEYWORD

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

        return Filter(
            name=self.ui.namelineedit.text(),
            filter_type=filter_type,
            data=self.ui.datalineedit.text(),
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

        if self.ui.testlineedit.text() == "":
            # Path is blank
            self.ui.testfilteroutputlabel.setText("No item selected.")
        elif applyFilters([self.filter_], self.ui.testlineedit.text()):
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
    print(window.buildFilter())
