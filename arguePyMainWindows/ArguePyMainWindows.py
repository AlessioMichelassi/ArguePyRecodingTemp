import os
import subprocess
import sys
from os.path import exists
import platform
from time import time

from PyQt5.QtCore import Qt, QProcess, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from arguePyMainWindows.commonMenu.commonMenu import CommonMenu
from arguePyMainWindows.console.cosole import Console
from arguePyMainWindows.fileExplorer.fileExplorer import FileExplorer
from arguePyMainWindows.settingsIni.settings import Settings
from arguePyMainWindows.widgets.argueTabWidget import ArgueTabWidget


class ArguePy(QMainWindow):
    console: Console
    arguePyTab: ArgueTabWidget
    fileExplorer: FileExplorer
    commonMenu = CommonMenu
    settings: Settings
    process: QProcess
    projectPath = ""
    isProjectFound = False
    isCompiled = False
    version = "1.0.0"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadSettings()
        self.initUI()
        self.initMenu()
        self.statusBar().showMessage("let's Argue")
        self.initMainWindows()
        self.initConnection()

        self.startProject()
        self.process = QProcess(self)
        self.welcomeMessage()

    def initUI(self):
        self.setWindowTitle('rguePy')
        self.setWindowIcon(QIcon(":/resource/icon.png"))
        self.resize(800, 600)

    def initMainWindows(self):
        self.fileExplorer = FileExplorer(self)
        leftDock = QDockWidget(self)
        leftDock.setWidget(self.fileExplorer)
        leftDock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.LeftDockWidgetArea, leftDock)
        bottomDock = QDockWidget(self)
        self.console = Console(self)
        bottomDock.setWidget(self.console)
        bottomDock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottomDock)
        self.arguePyTab = ArgueTabWidget(self)
        self.setCentralWidget(self.arguePyTab)

    def initMenu(self):
        self.commonMenu = CommonMenu(self)
        self.setMenuBar(self.commonMenu)

    def initConnection(self):
        self.fileExplorer.fileClickedSignal.connect(self.onExploreDoubleClickedSignal)

    def checkVersion(self):
        # se il programma è compilato
        if getattr(sys, 'frozen', False):
            if not exists(self.projectPath):
                projectPath = os.path.dirname(sys.executable)
                # create a tempFolder called tmpProject
                if not os.path.exists(projectPath + "/tmpProject"):
                    os.mkdir(projectPath + "/tmpProject")
                self.projectPath = projectPath + "/tmpProject"
                self.isProjectFound = False
            else:
                self.isProjectFound = True
        else:
            if not exists(self.projectPath):
                projectPath = os.path.dirname(os.path.abspath(__file__))
                # create a tempFolder called tmpProject
                if not os.path.exists(projectPath + "/tmpProject"):
                    os.mkdir(projectPath + "/tmpProject")
                self.projectPath = projectPath + "/tmpProject"
                self.isProjectFound = False
            else:
                self.isProjectFound = True
        self.initMain()

    def welcomeMessage(self):
        self.console.append("Welcome to ArguePy!", "bold")
        if self.isCompiled:
            self.console.append(f"compiled version{self.version}\n"
                                f"systemFound: {os.name} - platform: {sys.platform}", "info")
            self.console.append(
                f"{platform.system()} - {platform.release()} - {platform.version()} - {platform.machine()}")
        elif not self.isCompiled:
            self.console.append(f"not compiled test {self.version}", "warning")
            self.console.append(f"systemFound: {os.name} - platform: {sys.platform}", "italic")
            self.console.append(
                f"{platform.system()} - {platform.release()} - {platform.version()} - {platform.machine()}", "info")
        if not self.isProjectFound:
            self.console.append("Project path not found, creating a new one...", "warning")
            self.console.append(f"Project path: {self.projectPath}")
            self.console.append("Project path created!", "success")
            self.console.append("please remember to create a new project or open an existing one", "warning")

    #  ------------------ EVENT FUNCTIONS ------------------ #

    def onExploreDoubleClickedSignal(self, path):
        self.arguePyTab.showTab(path)

    def closeEvent(self, event):
        self.saveSettings()
        self.onSaveProject()
        if self.process:
            self.process.kill()
        self.console.close()
        self.arguePyTab.close()
        self.fileExplorer.close()
        self.commonMenu.close()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.arguePyTab.onTabPressed()
        else:
            super().keyPressEvent(event)

    #  ------------------ PROJECT FUNCTIONS ------------------ #

    @property
    def projectFileDictionary(self):
        return self.fileExplorer.projectFileDictionary

    def startProject(self):
        if self.settings.get("lastProject"):
            self.projectPath = self.settings.get("lastProject")
            self.fileExplorer.startProjectFromDirectory(self.projectPath)
        else:
            self.fileExplorer.openProject()

        # Aggiornamento di lastProject in caso di modifica di projectPath
        if self.projectPath != self.settings.get("lastProject"):
            self.settings.set("lastProject", self.projectPath)
            self.settings.save()

    def loadSettings(self):
        self.settings = Settings("settings.ini")
        self.settings.load()
        self.projectPath = self.settings.get("lastProject")

    def saveSettings(self):
        self.settings.set("lastProject", self.projectPath)
        self.settings.save()

    def onNewProject(self):
        self.arguePyTab.closeAllTab()
        self.fileExplorer.openProject()

    def onOpenProject(self):
        if not self.onSaveProject():
            return
        self.arguePyTab.closeAllTab()
        self.fileExplorer.openProject()

    def onSaveProject(self):
        self.arguePyTab.saveAllTab()

    def autoSaveProject(self):
        self.arguePyTab.saveAllTab()

    def onSaveAsProject(self):
        self.fileExplorer.saveAsProject()

    #  ------------------ RUN THE CODE FUNCTION ------------------ #

    def runCode(self, code):
        """
        ITA:
            Questo metodo esegue il codice scritto dall'utente utilizzando un QProcess, ovvero un processo
            che viene eseguito in un thread separato. Il processo viene eseguito con il comando python
            e il file temporaneo che viene creato con il codice scritto dall'utente.
        ENG:
            This method runs the code written by the user using a QProcess, that is a process
            that is executed in a separate thread. The process is executed with the python command
            and the temporary file that is created with the code written by the user.
        :return:
        """
        self.console.clear()
        if self.onSaveProject():
            currentFile = self.fileExplorer.getCurrentFile()
            self.console.append(f"Run File: {currentFile}")
            absProjectPath = os.path.abspath(self.projectPath)
            self.tryRun('python', currentFile, absProjectPath, 10)
        else:
            self.console.appendError("Project not saved!")

    def onProcessOutput(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.console.append(output)

    def onProcessError(self):
        error = self.process.readAllStandardError().data().decode()
        self.console.appendError(error)

    def onProcessFinished(self):
        exit_code = self.process.exitCode()
        if exit_code == 0:
            self.console.append("Process finished successfully")
        else:
            self.console.appendError(f"Process finished with exit code {exit_code}")

    def tryRun(self, program, arguments, workingDir, timeout=10):
        """
        ITA:
            Esegue il codice scritto dall'utente utilizzando un QProcess, ovvero un processo
            che viene eseguito in un thread separato. Il processo viene eseguito con il comando python
            e il file temporaneo che viene creato con il codice scritto dall'utente.
        ENG:
            Runs the code written by the user using a QProcess, that is a process
            that is executed in a separate thread. The process is executed with the python command
            and the temporary file that is created with the code written by the user.
        :param program:
        :param arguments:
        :param workingDir:
        :param timeout:
        :return:
        """
        try:
            # Esegue il file Python utilizzando subprocess
            # Crea un processo QProcess per eseguire il codice
            self.process = QProcess(self)
            self.process.setProgram(program)
            self.process.setArguments([arguments])
            self.process.setWorkingDirectory(workingDir)
            # Connette i segnali del processo per catturare l'output
            self.process.readyReadStandardOutput.connect(self.onProcessOutput)
            self.process.readyReadStandardError.connect(self.onProcessError)
            self.process.finished.connect(self.onProcessFinished)
            start_time = time()
            # Esegue il processo
            self.process.start()
            self.process.waitForFinished()
            end_time = time()
            elapsed_time = end_time - start_time
            # Aggiungi il tempo di esecuzione all'output
            self.console.append(f"Elapsed time: {elapsed_time:.2f} seconds")
        except subprocess.TimeoutExpired:
            self.console.append(f"subprocess.TimeoutExpired: {subprocess.TimeoutExpired}")

    def getCode(self):
        return self.arguePyTab.getCode()


