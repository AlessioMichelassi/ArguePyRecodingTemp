"""
ITA:

    Ecco una lezione completa sul QFileSystemModel in PyQt!

    Il QFileSystemModel è una classe di PyQt che permette di creare una struttura ad albero che rappresenta il file
    system del computer. La classe è estesa da QAbstractItemModel e quindi si comporta come un modello per le viste
    gerarchiche di PyQt, come ad esempio il QTreeView.

    Il QFileSystemModel permette di visualizzare i file e le cartelle presenti sul file system come una struttura ad
    albero. I file e le cartelle sono rappresentati come nodi dell'albero e sono identificati da un percorso univoco.

    Il QFileSystemModel può essere utilizzato per creare un file explorer, in cui l'utente può navigare all'interno
    del file system, selezionare file e cartelle, e fare operazioni come copiare, spostare e cancellare i file.

    Il QFileSystemModel viene creato indicando il percorso di partenza per l'albero, che rappresenta la radice
    dell'albero. Quando un nuovo nodo viene creato nell'albero, il QFileSystemModel cerca automaticamente i figli del
    nodo.

    Per utilizzare il QFileSystemModel, è necessario creare un'istanza della classe e impostarla come modello per la
    vista. Ci sono due modi per farlo: creare manualmente l'istanza della classe e assegnarla alla vista,
    oppure utilizzare il setModel della vista per assegnare il modello.

    Ecco un esempio di come creare un QTreeView con un QFileSystemModel:

"""

import sys
from PyQt5.QtCore import QDir, QModelIndex, Qt
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QTreeView, QAbstractItemView
from PyQt5.QtWidgets import QFileSystemModel, QWidget, QVBoxLayout


class FileExplorer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # creare il modello e impostare la radice come la directory corrente
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())

        # creare la vista ad albero e assegnare il modello
        treeView = QTreeView()
        treeView.setModel(model)

        # opzioni della vista ad albero
        treeView.setAnimated(False)
        treeView.setIndentation(20)
        treeView.setSortingEnabled(True)

        # layout della finestra
        layout = QVBoxLayout()
        layout.addWidget(treeView)
        self.setLayout(layout)

    """
    ITA:
    
        In questo esempio, viene creato un'istanza del QFileSystemModel, e la radice viene impostata sulla directory 
        corrente del sistema operativo. Viene poi creato un'istanza di QTreeView e assegnato il modello QFileSystemModel 
        alla vista. Infine, viene creato un layout verticale e la vista ad albero viene aggiunta al layout.
    
        Ci sono alcune opzioni disponibili per la vista ad albero, come setAnimated per abilitare l'animazione della 
        vista ad albero, setIndentation per impostare la distanza tra i nodi dell'albero e setSortingEnabled per 
        abilitare l'ordinamento dei nodi.
        
        Il QFileSystemModel consente anche di specificare quali informazioni sono disponibili per ogni file o directory. 
        Queste informazioni sono organizzate in colonne nella vista ad albero e includono, ad esempio, il nome del file, 
        la data di creazione e la dimensione del file.
    
        Per impostare le informazioni disponibili, si utilizza il metodo setHeaderData(). Ad esempio, il seguente codice 
        imposta le informazioni per la vista ad albero per includere il nome del file, la data di creazione e la 
        dimensione del file:
        
    """

    def setHeaderDataExample(self):
        self.model.setHeaderData(0, Qt.Horizontal, "Name")
        self.model.setHeaderData(1, Qt.Horizontal, "Date Modified")
        self.model.setHeaderData(2, Qt.Horizontal, "Size")

    """
    ITA: 
    In questo esempio, abbiamo specificato che la colonna 0 conterrà il nome del file, la colonna 1 la data 
    di modifica e la colonna 2 la dimensione del file.

    Il QFileSystemModel offre inoltre alcune funzionalità avanzate, come la possibilità di monitorare il file system 
    per le modifiche e di notificare la vista ad albero quando ci sono cambiamenti. Per abilitare questa 
    funzionalità, si utilizza il metodo setRootPath() con il flag Watcher. Ad esempio:
    
    """

    def watcherExample(self):
        path = QDir.currentPath()
        self.model.setRootPath(path)
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.model.setNameFilterDisables(False)
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.tree.setColumnWidth(0, 250)

        """
        ITA: 
        in questo esempio, abbiamo utilizzato setRootPath() per specificare la directory radice da 
        monitorare. Abbiamo poi impostato il flag Watcher per monitorare le modifiche nel file system. Infine, 
        abbiamo connesso il segnale directoryLoaded() del modello all'evento onDirectoryLoaded(), che verrà chiamato 
        ogni volta che la directory viene caricata.
        """

        # Watch for changes in the file system
        self.model.setRootPath(path)
        # set resolve symlinks è necessario per monitorare le modifiche ai file
        self.model.setResolveSymlinks(True)
        self.model.setReadOnly(False)
        self.tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.viewport().setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropOverwriteMode(False)
        self.tree.setDragDropMode(QAbstractItemView.InternalMove)
        # Connect the signal directoryLoaded() to the slot onDirectoryLoaded()
        self.model.directoryLoaded.connect(self.onDirectoryLoaded)

    """
    ITA: 
    Infine, il QFileSystemModel offre anche la possibilità di personalizzare l'aspetto dei nodi dell'albero. 
    Ci sono diversi modi per farlo, ad esempio utilizzando il metodo data() del modello per fornire le informazioni 
    personalizzate per un nodo specifico. Ad esempio, il seguente codice imposta il colore di sfondo del nodo in base 
    alla sua posizione nell'albero:
    """


class CustomFileSystemModel(QFileSystemModel):

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.BackgroundRole:
            # Set the background color based on the position of the item
            row = index.row()
            if row % 2 == 0:
                return QBrush(QColor(240, 240, 240))
            else:
                return QBrush(QColor(255, 255, 255))
        return QFileSystemModel.data(self, index, role)

    """
    ITA: In questo esempio, abbiamo creato una classe CustomFileSystemModel che eredita dalla classe 
    QFileSystemModel e sovrascrive il metodo data(). Nel metodo data(), controlliamo il ruolo del dati richiesti (
    role) e, se è Qt.BackgroundRole, impostiamo il colore di sfondo del nodo in base alla sua posizione nell'albero.

    In particolare, usiamo l'indice dell'elemento (index) per ottenere il numero di riga (row) del nodo e 
    verifichiamo se il numero di riga è pari o dispari. In base a questo, impostiamo il colore di sfondo del nodo.
    
    Infine, restituiamo i dati personalizzati chiamando il metodo super() per ottenere i dati di default e 
    sovrascrivendo solo il colore di sfondo.
    
    Per utilizzare la nostra classe CustomFileSystemModel nella nostra vista ad albero, dobbiamo crearne un'istanza e 
    assegnarla come modello alla vista:
    
                            model = CustomFileSystemModel()
                            model.setRootPath("/")
                            tree.setModel(model)
                            
    In questo esempio, abbiamo creato un'istanza della nostra classe CustomFileSystemModel e l'abbiamo assegnata come 
    modello alla nostra vista ad albero (tree.setModel(model)).

    In questo modo, la nostra vista ad albero visualizzerà i nodi con un colore di sfondo diverso in base alla 
    loro posizione nell'albero.

    
    """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileExplorer()
    ex.show()
    sys.exit(app.exec_())
