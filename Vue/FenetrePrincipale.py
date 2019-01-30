from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal

from Modele.Signaux import Signaux
from Controleur.FileManager import FileManager
from Vue import fenetreprincipaledesign_ui


class FenetrePrincipale(QtWidgets.QMainWindow, fenetreprincipaledesign_ui.Ui_MainWindow):

    FP_connecteur = pyqtSignal(Signaux)

    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        fenetreprincipaledesign_ui.Ui_MainWindow.__init__(self)

        self.setupUi(self)

        self._view = QWebEngineView()

        self.FPafficherReseau()

        # Signaux
        self.FPD_bouton_generer_reseau.clicked.connect(self.FPactionGenerer)
        self.FPDActionExporterReseau.triggered.connect(self.FPactionExporterReseau)
        self.FPDActionChargerReseau.triggered.connect(self.FPactionChargerReseau)

    def FPafficherReseau(self):

        _fileManager = FileManager()
        _chemin, _exist = _fileManager.FMobtenirCheminHTMLLocal()
        if not _exist:
            _chemin = _fileManager.FMobtenirCheminHTMLVide()

        local_url = QUrl.fromLocalFile(_chemin)
        self._view.load(local_url)
        self.FPD_layout_gauche_haut.addWidget(self._view)


    def FPobtenirConnecteur(self):
        return self.FP_connecteur

    def FPactionGenerer(self):
        self.FP_connecteur.emit(Signaux._GENERER_RESEAU)

    def FPactionChargerReseau(self):
        self.FP_connecteur.emit(Signaux._CHARGER_XML)

    def FPactionExporterReseau(self):
        self.FP_connecteur.emit(Signaux._EXPORTER_XML)
