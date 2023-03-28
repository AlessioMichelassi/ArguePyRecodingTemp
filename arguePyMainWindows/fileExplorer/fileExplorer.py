import json
import os
import shutil
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QFileSystemModel, QTreeWidgetItem, QMenu, QAction, \
    QInputDialog, QMessageBox, QAbstractItemView, QFileDialog

from arguePyMainWindows.fileExplorer.customIconProvider import CustomFileIconProvider
from arguePyMainWindows.fileExplorer.treeViewOverride import treeViewOverride


class CustomFileSystemModel(QFileSystemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Aggiungi la cartella di root come elemento nell'albero
        root_path = QDir.rootPath()
        root_index = self.index(root_path)
        self.setRootPath(root_path)
        self.insertRow(0, root_index)


class FileExplorer(QWidget):
    model: QFileSystemModel
    tree: treeViewOverride
    fileClickedSignal = pyqtSignal(str, name="fileClicked")
    currentPath = ""
    currentFile = ""
    fileRenameSignal = pyqtSignal(str, str, name="fileRenamed")
    projectFileDictionary = {0: "main.py"}

    def __init__(self, mainWindows, parent=None):
        super().__init__(parent)
        self.mainWindows = mainWindows
        self.initUI()
        self.initConnection()

    def initUI(self):
        # Create the file system model
        self.initModel()

        # Create the tree view
        self.initTreeView()
        self.initDragAndDrop()
        # Aggiungi la vista a albero al layout
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def initModel(self):
        """
        ITA:
            Questo metodo inizializza il modello del file system.
            setRootPath: imposta la root del file system
            setNameFilterDisables: abilita il filtro dei nomi dei file può tornare utile per mostrare solo
                                    i file con estensione .py o per tenere cartelle nascoste come env o .git
                                    __pyCache__
                                    model.setNameFilters(["*", "!__pycache__"])
                                    model.setNameFilterDisables(False)
            setReadOnly: abilita la scrittura del file system e permette di fare operazioni di spostamento e copia
                          senza questo non funziona il drag and drop dei file
        ENG:
            This method initializes the file system model.
            setRootPath: sets the root of the file system
            setNameFilterDisables: enables the file name filter can be useful to show only
                                    files with .py extension or to keep hidden folders like env or .git
                                    __pycache__
                                    model.setNameFilters(["*", "!__pycache__"])
                                    model.setNameFilterDisables(False)
            setReadOnly: enables the file system writing and allows to do operations of movement and copy
                            without this the drag and drop of files does not work
        :return:
        """
        self.model = CustomFileSystemModel()
        self.model.setRootPath(str(Path(self.mainWindows.projectPath).parent))
        self.model.setNameFilterDisables(False)
        # read only false abilita la scrittura del file system e permette di fare operazioni di spostamento e copia
        self.model.setReadOnly(False)
        # mostra l'header 0 con il nome del file
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "File Name")
        # this set icon for all file
        iconProvider = CustomFileIconProvider()
        # set the custom icon provider for the model
        self.model.setIconProvider(iconProvider)

    def initTreeView(self):
        """
        ITA:
            Questo metodo inizializza la vista a albero.
        ENG:
            This method initializes the tree view.
        :return:
        """
        self.tree = treeViewOverride()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.mainWindows.projectPath))
        print(f"self.mainWindows.projectPath: {self.mainWindows.projectPath}")
        root_index = self.model.index(self.mainWindows.projectPath)
        self.tree.setExpanded(root_index, True)
        self.tree.setColumnWidth(0, 250)
        # nasconde la colonna dei dettagli
        self.tree.setHeaderHidden(True)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

    def initDragAndDrop(self):
        """
        ITA:
            Questo metodo inizializza il drag and drop.
        ENG:
            This method initializes the drag and drop.
        :return:
        """
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        # self.tree.setDefaultDropAction(Qt.DropAction.CopyAction)
        # self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def initConnection(self):
        """
        ITA:
            Questo metodo inizializza le connessioni tra i segnali e i metodi.
        ENG:
            This method initializes the connections between the signals and the methods.
        :return:
        """
        self.tree.clicked.connect(self.onTreeviewClicked)
        self.tree.doubleClicked.connect(self.onTreeviewDoubleClicked)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def onTreeviewClicked(self, index: QModelIndex):
        """
        ITA:
            Questo metodo viene chiamato quando si fa click su un file nella vista a albero.
            Non fa praticamente niente a parte settare la path del file cliccato in modo che possa essere usata
            da altri metodi tipo per creare nuovi file o per creare directory
        ENG:
            This method is called when you click on a file in the tree view.
            It does not do anything except set the path of the clicked file so that it can be used
            by other methods like to create new files or to create directories
        """
        file_info = self.model.fileInfo(index)
        if not file_info.isFile() or not file_info.isReadable():
            # Il file non può essere letto o non è un file regolare, non fare nulla
            return
        file_path = self.model.filePath(index)
        self.currentFile = file_path
        diPath = os.path.dirname(file_path)
        self.currentPath = diPath

    def onTreeviewDoubleClicked(self, index: QModelIndex):
        """
        ITA:
            Questo metodo viene chiamato quando si fa doppio click su un file nella vista a albero.
        ENG:
            This method is called when you double click on a file in the tree view.
        """
        file_info = self.model.fileInfo(index)
        if not file_info.isFile() or not file_info.isReadable():
            # Il file non può essere letto o non è un file regolare, non fare nulla
            return
        file_path = self.model.filePath(index)
        try:
            with open(file_path, "r") as file:
                content = file.read()
        except UnicodeDecodeError:
            # Il file non è in formato testo, non fare nulla
            return

        self.fileClickedSignal.emit(file_path)

    def showContextMenu(self, pos):
        """
        ITA:
            Questo metodo mostra il menu contestuale.
        ENG:
            This method shows the context menu.
        :param pos:
        :return:
        """
        contextMenu = QMenu(self)
        newFileAction = QAction("new file")
        newDirAction = QAction("new directory")
        copyFileAction = QAction("copy")
        pasteFileAction = QAction("paste")
        renameFileAction = QAction("rename")
        deleteFileAction = QAction("delete")

        contextMenu.addAction(newFileAction)
        contextMenu.addAction(newDirAction)
        contextMenu.addSeparator()
        contextMenu.addAction(copyFileAction)
        contextMenu.addAction(pasteFileAction)
        contextMenu.addSeparator()
        contextMenu.addAction(renameFileAction)
        contextMenu.addSeparator()
        contextMenu.addAction(deleteFileAction)
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == newFileAction:
            self.onFileNew()
        elif action == newDirAction:
            self.onDirNew()
        elif action == copyFileAction:
            self.onFileCopy()
        elif action == pasteFileAction:
            self.onFilePaste()
        elif action == renameFileAction:
            self.onFileRename()
        elif action == deleteFileAction:
            self.onFileDelete()

    # ------------------------------------ GETTER ------------------------------------

    def getCurrentFile(self):
        """
        ITA:
            Questo metodo ritorna il file corrente.
        ENG:
            This method returns the current file.
        :return:
        """
        return self.currentFile

    def getCurrentPath(self):
        """
        ITA:
            Questo metodo ritorna la path del file corrente.
        ENG:
            This method returns the path of the current file.
        :return:
        """
        return self.currentPath

    def setCurrentPath(self, path):
        """
        ITA:
            Questo metodo setta la path del file corrente.
        ENG:
            This method sets the path of the current file.
        :param path:
        :return:
        """
        self.currentPath = path
        self.model.setRootPath(self.currentPath)
        self.tree.setRootIndex(self.model.index(self.currentPath))
        root_index = self.model.index(self.mainWindows.projectPath)
        self.tree.setExpanded(root_index, True)

    def openProject(self):
        """
        ITA:
            Questo metodo apre un progetto.
        ENG:
            This method opens a project.
        :param path:
        :return:
        """
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.mainWindows.projectPath = path
        if path:
            self.currentPath = path
            self.model.setRootPath(self.currentPath)
            self.tree.setRootIndex(self.model.index(self.currentPath))
            self.tree.expandAll()
            self.createFileList()

    def startProjectFromDirectory(self, path):
        """
        ITA:
            Questo metodo crea un progetto partendo da una cartella.
        ENG:
            This method creates a project starting from a folder.
        :return:
        """
        if path:
            self.currentPath = path
            self.mainWindows.projectPath = path
            self.model.setRootPath(self.currentPath)
            self.tree.setRootIndex(self.model.index(self.currentPath))
            self.tree.expandAll()
            self.createFileList()
        else:
            print("No path")

    def saveAsProject(self):
        """
        ITA:
            Questo metodo salva il progetto in una nuova cartella.
        ENG:
            This method saves the project in a new folder.
        :return:
        """
        newDirectory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if newDirectory:
            # copia tutti i file nella nuova directory
            for root, dirs, files in os.walk(self.currentPath):
                for file in files:
                    shutil.copy(os.path.join(root, file), newDirectory)
            self.currentPath = newDirectory
            self.mainWindows.currentProject = newDirectory
            self.model.setRootPath(self.currentPath)
            self.tree.setRootIndex(self.model.index(self.currentPath))
            self.tree.expandAll()

    # ------------------------------------ PROJECT FILE ACTIONS ------------------------------------

    def createFileList(self):
        self.projectFileDictionary = {}
        for root, dirs, files in os.walk(self.currentPath):
            for file in files:
                filepath = os.path.abspath(os.path.join(root, file)).replace("\\", "/")
                self.projectFileDictionary[filepath] = file

        self.serializeFileList()

    def serializeFileList(self):

        jsonDictionary = json.dumps(self.projectFileDictionary, indent=4)
        print(jsonDictionary)

    # ------------------------------------ MENU ACTIONS ------------------------------------

    def onFileNew(self):
        """
        ITA:
            Crea un nuovo file e lo mette nella posizione selezionata nella vista a albero.
        ENG:
            Create a new file and put it in the selected position in the tree view.
        :return:
        """
        nameDialog = QInputDialog()
        nameDialog.setInputMode(QInputDialog.InputMode.TextInput)
        nameDialog.setLabelText("File name:")
        nameDialog.setWindowTitle("New file")
        nameDialog.exec_()
        if nameDialog.result() == QInputDialog.DialogCode.Accepted:
            # create a new file in the current directory
            index = self.tree.currentIndex()
            if not index.isValid():
                return
            fileName = nameDialog.textValue()
            newFilePath = os.path.join(self.currentPath, fileName)
            if not os.path.exists(newFilePath):
                with open(newFilePath, "w") as file:
                    file.write("")

    def onFileNewWithName(self, fileName):
        """
        ITA:
            Crea un nuovo file e lo mette nella posizione selezionata nella vista a albero.
        ENG:
            Create a new file and put it in the selected position in the tree view.
        :return:
        """
        # create a new file in the current directory
        index = self.tree.currentIndex()
        if not index.isValid():
            return
        newFilePath = os.path.join(self.currentPath, fileName)
        if not os.path.exists(newFilePath):
            with open(newFilePath, "w") as file:
                file.write("")

    def onDirNew(self):
        nameDialog = QInputDialog()
        nameDialog.setInputMode(QInputDialog.InputMode.TextInput)
        nameDialog.setLabelText("Directory name:")
        nameDialog.setWindowTitle("New directory")
        nameDialog.exec_()
        if nameDialog.result() == QInputDialog.DialogCode.Accepted:
            # create a new file in the current directory
            index = self.tree.currentIndex()
            if not index.isValid():
                return
            filePath = self.model.filePath(index)
            dirName = nameDialog.textValue()
            newFilePath = os.path.join(self.currentPath, dirName)
            if not os.path.exists(newFilePath):
                os.mkdir(newFilePath)

    def onFileCopy(self):
        # copia il file selezionato in memoria
        index = self.model.index(self.tree.currentIndex().row(), 0, self.tree.currentIndex().parent())
        if not index.isValid():
            return
        filePath = self.model.filePath(index)
        self.mainWindows.clipboard = filePath

    def onFilePaste(self):
        pass

    def onFileRename(self):
        index = self.model.index(self.tree.currentIndex().row(), 0, self.tree.currentIndex().parent())
        if not index.isValid():
            return
        filePath = self.model.filePath(index)
        dirPath = os.path.dirname(filePath)
        oldName = os.path.basename(filePath)
        newName, ok = QInputDialog.getText(self, "Rename", "new Name:", text=oldName)
        if ok and newName:
            new_path = os.path.join(dirPath, newName)
            self.fileRenameSignal.emit(oldName, new_path)
            if os.path.exists(new_path):
                QMessageBox.warning(self, "Rinomina", f"Il file '{newName}' esiste già.")
                return
            os.rename(filePath, new_path)
            self.projectFileDictionary[newName] = self.projectFileDictionary.pop(oldName)

    def onFileDelete(self):
        index = self.model.index(self.tree.currentIndex().row(), 0, self.tree.currentIndex().parent())
        if not index.isValid():
            return
        filePath = self.model.filePath(index)
        # se il path di una directory
        if os.path.isdir(filePath):
            self.deleteDir(filePath)
        else:
            self.deleteFile(filePath)

    def deleteDir(self, dirPath):
        for file in os.listdir(dirPath):
            filePath = os.path.join(dirPath, file)
            if os.path.isdir(filePath):
                self.deleteDir(filePath)
            else:
                self.deleteFile(filePath)
                self.projectFileDictionary.pop(os.path.abspath(filePath))
        if os.path.exists(dirPath):
            os.rmdir(dirPath)
        self.model.remove(self.tree.currentIndex())

    def deleteFile(self, filePath):
        os.remove(filePath)
        self.model.remove(self.tree.currentIndex())
        self.serializeFileList()

    # ------------------------------------ DRAG AND DROP ------------------------------------

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            # Handle the dropped file(s)
            # ...

        event.acceptProposedAction()
