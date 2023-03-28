from PyQt5 import QtWidgets, QtGui


class CustomTabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        # Imposta il font di FontAwesome
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(":/fonts/fontawesome-webfont.ttf")
        font_family = font_db.applicationFontFamilies(font_id)[0]
        font = QtGui.QFont(font_family)
        font.setPointSize(12)
        self.setFont(font)

        # Aggiunge una tab
        tab1 = QtWidgets.QWidget()
        tab_label = QtWidgets.QLabel("Tab 1")
        tab_close_button = QtWidgets.QPushButton("  \uf00d  ")
        tab_layout = QtWidgets.QHBoxLayout(tab1)
        tab_layout.addWidget(tab_label)
        tab_layout.addWidget(tab_close_button)
        self.addTab(tab1, "Tab 1")
