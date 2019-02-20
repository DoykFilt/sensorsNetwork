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
    FP_connecteur = pyqtSignal(Signaux, int)

    def __init__(self):
        """
        Initialisateur de la classe FenetrePrincipale
        """

        QtWidgets.QMainWindow.__init__(self)
        fenetreprincipaledesign_ui.Ui_MainWindow.__init__(self)

        self.setupUi(self)

        self.FP_view = QWebEngineView()

        # Assignation des actions aux differents boutton
        self.FPD_bouton_generer_reseau.clicked.connect(self.FPactionGenerer)
        self.FPDActionExporterReseau.triggered.connect(self.FPactionExporterReseau)
        self.FPDActionChargerReseau.triggered.connect(self.FPactionChargerReseau)
        self.FDPActionExporterSimulation.triggered.connect(self.FPactionExporterSimulation)
        self.FPDActionChargerResultats.triggered.connect(self.FPactionImporterSimulation)

        self.FPD_bouton_lancer_simulation.clicked.connect(self.FPactionSimulation)

        self.FPD_boutton_arrire.clicked.connect(self.FPactionArriere)
        self.FPD_boutton_avant.clicked.connect(self.FPactionAvant)
        self.FPD_boutton_saut_arriere.clicked.connect(self.FPactionSautArriere)
        self.FPD_boutton_saut_avant.clicked.connect(self.FPactionSautAvant)

        self.FP_selection = 0
        self.FP_total = 0
        _file_manager = FileManager()
        _liste_etats = _file_manager.FMlisterEtats()
        if len(_liste_etats) > 0:
            self.FP_total = _liste_etats[-1]
            self.FP_selection = _liste_etats[0]

        self.FPuptdateLabelSelection(self.FP_selection, self.FP_total)
        self.FPD_barre_temporelle.valueChanged.connect(self.FPactionBarreTemporelle)

        self.FPafficherReseau()

    def FPafficherReseau(self):
        """
        Affiche dans la section didiée de la fenêtre le reseau enregistré en local

        """

        _fileManager = FileManager()
        _chemin = _fileManager.FMchargerHTMLEtat(self.FP_selection)

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
        self.FP_connecteur.emit(Signaux._GENERER_RESEAU, -1)

    def FPactionChargerReseau(self):
        """
        Emission du signal quand charger un reseau est choisi dans le menu

        """
        self.FP_connecteur.emit(Signaux._CHARGER_XML, -1)

    def FPactionExporterReseau(self):
        """
        Emission du signal quand exporter un reseau est choisi dans le menu

        """
        self.FP_connecteur.emit(Signaux._EXPORTER_XML, -1)

    def FPactionImporterSimulation(self):
        self.FP_connecteur.emit(Signaux._IMPORTER_RESULTAT, -1)

    def FPactionExporterSimulation(self):
        self.FP_connecteur.emit(Signaux._EXPORTER_RESULTAT, -1)

    def FPactionSimulation(self):
        """
        Emission du signal quand le boutton "Lancer la simulation" est cliqué

        """
        self.FP_connecteur.emit(Signaux._LANCER_SIMULATION, -1)

    def FPactionArriere(self):
        self.FP_connecteur.emit(Signaux._ARRIERE, -1)

    def FPactionSautArriere(self):
        self.FP_connecteur.emit(Signaux._SAUT_ARRIERE, -1)

    def FPactionAvant(self):
        self.FP_connecteur.emit(Signaux._AVANT, -1)

    def FPactionSautAvant(self):
        self.FP_connecteur.emit(Signaux._SAUT_AVANT, -1)

    def FPactionBarreTemporelle(self):
        self.FP_connecteur.emit(Signaux._SAUT_TEMPOREL, self.FPD_barre_temporelle.value())

    def FPuptdateLabelSelection(self, _selection, _total):
        if _selection > _total:
            self.FPD_selection_barre_temporelle.setText("Values error")
        else:
            self.FP_selection = _selection
            self.FP_total = _total
            if _total == 0:
                self.FP_total = 1

            self.FPD_selection_barre_temporelle.setText(str(self.FP_selection + 1) + " / " + str(self.FP_total))

            self.FPD_barre_temporelle.setMinimum(0)
            self.FPD_barre_temporelle.setMaximum(self.FP_total - 1)
            self.FPD_barre_temporelle.setTickInterval(1)
            self.FPD_barre_temporelle.setValue(self.FP_selection)
