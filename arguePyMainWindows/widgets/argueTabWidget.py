import os
from os.path import exists

from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QPoint
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton, QFileDialog, QApplication, QLabel, \
    QHBoxLayout, QTabBar

from arguePyMainWindows.codeEditorOverride.arguePyWidget import ArguePyWidget


class TabPressEvent:
    pass


class ArgueTabWidget(QTabWidget):
    fileNameCounter = 0

    def __init__(self, mainWindow, parent=None):
        super(ArgueTabWidget, self).__init__(parent)
        self.mainWindow = mainWindow
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, index):
        self.saveFile()
        self.removeTab(index)

    @property
    def projectFileDictionary(self):
        return self.mainWindow.projectFileDictionary

    def addCodeTab(self, path):
        """
        ITA:
            Quando si aggiunge un tab con del codice, viene creato un nuovo widget per l'editor di codice e
            ovviamente viene creato un nuovo file con un nome univoco.
        ENG:
            When adding a tab with code, a new widget for the code editor is created and of course a new file
            is created with a unique name.
        :return:
        """
        editorWidget = ArguePyWidget(self)
        newTab = QWidget()
        name = os.path.basename(path)
        code = ""
        with open(path, "r") as file:
            code = file.read()
        editorWidget.setCode(code)
        self.projectFileDictionary[self.fileNameCounter] = name
        newTab.setObjectName(name)
        layout = QVBoxLayout(newTab)
        layout.addWidget(editorWidget)
        self.addTab(newTab, name.replace(".py", ""))
        self.setCurrentWidget(newTab)
        button = self.tabBar().tabButton(self.count() - 1, QTabBar.RightSide)
        button.move(button.pos() + QPoint(5, 0))

    def getCode(self):
        # se non ci sono tab aperti non ritorna codice
        if self.count() > 0:
            return self.currentWidget().layout().itemAt(0).widget().getCode()

    def setCode(self, code):
        self.currentWidget().layout().itemAt(0).widget().setCode(code)

    def onRun(self):
        self.mainWindow.runCode(self.getCode())

    def showTab(self, index):
        """
        ITA:
            Questo metodo viene chiamato quando si clicca su un file nella vista a albero.
        ENG:
            This method is called when you click on a file in the tree view.
        :param index:
        :return:
        """
        if isinstance(index, int):
            if self.count() <= index:
                self.addEmptyTab()
                self.setCurrentIndex(index)
            self.setCurrentIndex(index)
        elif isinstance(index, str):
            path = index
            name = os.path.basename(path)
            isTabFound = False
            for i in range(self.count()):
                if self.tabText(i) == name.replace(".py", ""):
                    self.setCurrentIndex(i)
                    isTabFound = True
                    return
            if not isTabFound:
                self.addCodeTab(path)

    def saveFile(self):
        """
        ITA:
            Questo metodo salva il file corrente.
        ENG:
            This method saves the current file.
        :return:
        """
        path = self.mainWindow.projectPath
        absFileName = os.path.abspath(self.projectFileDictionary[self.currentIndex()])
        # absFileName = os.path.join(path, self.projectFileDictionary[self.currentIndex()])
        with open(absFileName, "w") as file:
            file.write(self.getCode())
        return True

    def saveAllTab(self):
        """
        ITA:
            Questo metodo salva tutti i file.
        ENG:
            This method saves all files.
        :return:
        """

        # salva tutti i file nel dictionario self.projectFileDictionary
        for path, name in self.projectFileDictionary.items():
            absFileName = os.path.abspath(os.path.dirname(path))
            if self.getCode():
                with open(absFileName, "w") as file:
                    file.write(self.getCode())

    def onTabPressed(self):
        """
        ITA:
            Questo metodo viene chiamato quando si preme il tasto tab nella finestra principale e
            serve che venga intercettato nel editorCode.
        ENG:
            This method is called when the tab key is pressed in the main window and
            serves to be intercepted in the editorCode.
        :param event:
        :return:
        """
        tabPressEvent = TabPressEvent()
        QApplication.sendEvent(self.currentWidget().layout().itemAt(0).widget(), tabPressEvent)

    def getCurrentFile(self):
        return self.projectFileDictionary[self.currentIndex()]

    def renameFile(self, oldName, newName):
        """
        ITA:
            cerca la tab con il nome vecchio e la rinomina con il nuovo nome
        ENG:
            search for the tab with the old name and rename it with the new name
        :param oldName:
        :param newName:
        :return:
        """

        for i in range(self.count()):
            if self.tabText(i) == oldName.replace(".py", ""):
                self.projectFileDictionary[i] = newName
                niceName = newName.split("/")[-1]
                niceName = niceName.split("\\")[-1]
                self.setTabText(i, niceName)
                self.widget(i).setObjectName(niceName)
                return
