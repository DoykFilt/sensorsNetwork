from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal

from Modele.Signaux import Signaux
from Utilitaires.FileManager import FileManager
from Vue import fenetreprincipaledesign_ui


class FenetrePrincipale(QtWidgets.QMainWindow, fenetreprincipaledesign_ui.Ui_MainWindow):

    """
        class FenetrePrincipale

        Hérite de
            -   QMainWindow -> fenetre principale Qt
            -   Ui_MainWindow -> le design de la fenetre Qt

        Classe qui represent la fenetre principale de l'application

    """

    # Connecteur de la fenetre, permet de reagir depuis l'exterieur de la classe si un boutton a été cliqué
    FP_connecteur = pyqtSignal(Signaux)

    def __init__(self):
        """
        Initialisateur de la classe FenetrePrincipale
        """

        QtWidgets.QMainWindow.__init__(self)
        fenetreprincipaledesign_ui.Ui_MainWindow.__init__(self)

        self.setupUi(self)

        self.FP_view = QWebEngineView()

        self.FPafficherReseau()

        # Assignation des actions aux differents boutton
        self.FPD_bouton_generer_reseau.clicked.connect(self.FPactionGenerer)
        self.FPDActionExporterReseau.triggered.connect(self.FPactionExporterReseau)
        self.FPDActionChargerReseau.triggered.connect(self.FPactionChargerReseau)

    def FPafficherReseau(self):
        """
        Affiche dans la section didiée de la fenêtre le reseau enregistré en local

        """

        _fileManager = FileManager()
        _chemin, _exist = _fileManager.FMobtenirCheminHTMLLocal()
        # Si aucun graphe n'est en sauvegarde on génère une page blanche et on récupère son chemin absolu
        if not _exist:
            _chemin = _fileManager.FMobtenirCheminHTMLVide()

        local_url = QUrl.fromLocalFile(_chemin)
        self.FP_view.load(local_url)
        self.FPD_layout_gauche_haut.addWidget(self.FP_view)


    def FPobtenirConnecteur(self):
        """
        Renvoie le connecteur, permet d'agir à l'extérieur de la classe aux émissions de l'intérieur

        :return Le connecteur pyqtSignal
        """
        return self.FP_connecteur

    def FPactionGenerer(self):
        """
        Emission du signal quand le boutton "Generer un reseau" est cliqué

        """
        self.FP_connecteur.emit(Signaux._GENERER_RESEAU)

    def FPactionChargerReseau(self):
        """
        Emission du signal quand le charger un reseau est choisi dans le menu

        """
        self.FP_connecteur.emit(Signaux._CHARGER_XML)

    def FPactionExporterReseau(self):
        """
        Emission du signal quand le exporter un reseau est choisi dans le menu

        """
        self.FP_connecteur.emit(Signaux._EXPORTER_XML)

