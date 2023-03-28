"""
Il QTreeView è un widget di PyQt5 che fornisce una vista gerarchica dei dati in una tabella ad albero. Ogni riga
dell'albero rappresenta un elemento e può essere espansa per mostrare i sotto-elementi.

Il QTreeView dipende da un modello dati, come il QFileSystemModel o il QStandardItemModel, che fornisce i dati
da visualizzare nell'albero.

Ecco un esempio di codice per creare un QTreeView e collegarlo a un modello dati:
"""

from PyQt5.QtWidgets import QApplication, QTreeView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

app = QApplication([])

# Create the model
model = QStandardItemModel()

# Populate the model
item1 = QStandardItem("Item 1")
item2 = QStandardItem("Item 2")
item3 = QStandardItem("Item 3")

item1.appendRow([QStandardItem("Subitem 1"), QStandardItem("Subitem 2")])
item2.appendRow([QStandardItem("Subitem 3"), QStandardItem("Subitem 4")])

model.appendRow([item1, item2, item3])

# Create the tree view
tree_view = QTreeView()
tree_view.setModel(model)



"""
In questo esempio, viene creato un QStandardItemModel e vengono aggiunti alcuni elementi e sotto-elementi. Quindi 
viene creato un QTreeView e viene impostato il modello dati creato in precedenza. Infine, il widget viene mostrato.

Il QTreeView offre molte opzioni di personalizzazione per l'aspetto e il comportamento dell'albero. Ad esempio, 
è possibile impostare la larghezza delle colonne, la modalità di selezione degli elementi, l'animazione delle 
espansioni e delle contrazioni, il drag-and-drop degli elementi, e molto altro ancora.

Per esempio, se si vuole impostare la larghezza della prima colonna del tree view, è possibile utilizzare il 
seguente codice:

"""

tree_view.setColumnWidth(0, 200)

"""
Se invece si vuole impostare la modalità di selezione degli elementi su ExtendedSelection, ovvero permettere la 
selezione multipla, si può utilizzare il seguente codice:"""

tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

"""
Infine, per abilitare la modalità di drag-and-drop degli elementi, si può utilizzare il seguente codice:
"""
tree_view.setDragEnabled(True)
tree_view.setAcceptDrops(True)
tree_view.setDragDropMode(QAbstractItemView.InternalMove)

"""
In questo modo, gli elementi possono essere trascinati e rilasciati all'interno dell'albero.

Questi sono solo alcuni esempi delle opzioni di personalizzazione del QTreeView. Con un po' di esplorazione e 
sperimentazione, è possibile creare alberi complessi e personalizzati che soddisfino le proprie esigenze.
"""


# Show the tree view
tree_view.show()

app.exec_()

