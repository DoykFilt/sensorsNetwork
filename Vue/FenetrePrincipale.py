import mplcursors as mplcursors
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal

from Controleur.Statistiques import Statistiques
from Modele.Signaux import Signaux
from Utilitaires.FileManager import FileManager
from Vue import fenetreprincipaledesign_ui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

        # Pour gérer la sélection du résultat de la simulation. Si il y a déja un résultat de simulation on affiche
        # le dernier
        self.FP_selection = 0
        self.FP_total = 0
        _file_manager = FileManager()
        _liste_etats = _file_manager.FMlisterEtats()
        if len(_liste_etats) > 0:
            self.FP_total = len(_liste_etats)
            self.FP_selection = _liste_etats[0]

        self.FPuptdateLabelSelection(self.FP_selection, self.FP_total)
        self.FPD_barre_temporelle.valueChanged.connect(self.FPactionBarreTemporelle)

        # Pour ajouter les deux graphiques matplotlib
        self.FP_figure_graphique1 = Figure()
        self.FP_canvas_graphique1 = FigureCanvas(self.FP_figure_graphique1)
        self.FPD_layout_graphiques.addWidget(self.FP_canvas_graphique1)

        self.FP_figure_graphique2 = Figure()
        self.FP_canvas_graphique2 = FigureCanvas(self.FP_figure_graphique2)
        self.FPD_layout_graphiques.addWidget(self.FP_canvas_graphique2)

    def FPafficherReseau(self):
        """
        Affiche dans la section didiée de la fenêtre le reseau enregistré en local

        """
        _statistiques = Statistiques()
        self.FPD_aire_informations.setText(_statistiques.SgenererTexte(self.FP_selection))

        _fileManager = FileManager()
        _chemin = _fileManager.FMchargerHTMLEtat(self.FP_selection)

        local_url = QUrl.fromLocalFile(_chemin)
        self.FP_view.load(local_url)
        self.FPD_layout_gauche_haut.addWidget(self.FP_view)

        self.FPafficherGraphiques()

    def FPafficherGraphiques(self):
        """
        Affiche dans la section didiée de la fenêtre les deux graphiques
        Premier graphique (le plus en haut) : La durée de vie du réseau en fonction de l'intervalle de changement de
        rôle utilisé
        Second graphique : Le nombre de capteurs connectés à la passerelle en fonction du temps
        Les données sont affichées sous forme de points, les valeurs s'affichent au passage de la souris
        """

        _statistiques = Statistiques()
        _donnees_graphique1, _donnees_graphique2 = _statistiques.SgenererDonneesGraphiques()

        # Graphique 1
        _ax = self.FP_figure_graphique1.add_subplot(111)
        _ax.clear()
        _lignes = _ax.plot(_donnees_graphique1["y"], _donnees_graphique1["x"], 'o')
        _ax.set_xlabel("Intervalle de temps entre les changements de rôle")
        _ax.set_ylabel("Durée de vie du réseau")
        _ax.set_title("Durée de vie du réseau")
        _ax.set_aspect("auto")
        mplcursors.cursor(_lignes, hover=True)
        self.FP_figure_graphique1.tight_layout()
        self.FP_canvas_graphique1.draw()

        # Graphique 2
        _ax = self.FP_figure_graphique2.add_subplot(111)
        _ax.clear()
        _lines = _ax.plot(_donnees_graphique2["y"], _donnees_graphique2["x"], 'o')
        _ax.set_xlabel("Durée de la simulation en unité de temps")
        _ax.set_ylabel("Nombre de capteurs connectés")
        _ax.set_title("Capteurs connectés à la passerelle")
        mplcursors.cursor(_lines, hover=True)
        self.FP_figure_graphique2.tight_layout()
        self.FP_canvas_graphique2.draw()

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
        """
        Emission du signal quand importer un résultat de simulation est choisi dans le menu

        """
        self.FP_connecteur.emit(Signaux._IMPORTER_RESULTAT, -1)

    def FPactionExporterSimulation(self):
        """
        Emission du signal quand exporter un résultat de simulation est choisi dans le menu

        """
        self.FP_connecteur.emit(Signaux._EXPORTER_RESULTAT, -1)

    def FPactionSimulation(self):
        """
        Emission du signal quand le boutton "Lancer la simulation" est cliqué

        """
        self.FP_connecteur.emit(Signaux._LANCER_SIMULATION, -1)

    def FPactionArriere(self):
        """
        Emission du signal quand le bouton "gauche" à côté de la glissière est cliqué

        """
        self.FP_connecteur.emit(Signaux._ARRIERE, -1)

    def FPactionSautArriere(self):
        """
        Emission du signal quand le bouton "extrème gauche" à côté de la glissière est cliqué

        """
        self.FP_connecteur.emit(Signaux._SAUT_ARRIERE, -1)

    def FPactionAvant(self):
        """
        Emission du signal quand le bouton "gauche" à côté de la glissière est cliqué

        """
        self.FP_connecteur.emit(Signaux._AVANT, -1)

    def FPactionSautAvant(self):
        """
        Emission du signal quand le bouton "extrème droite" à côté de la glissière est cliqué

        """
        self.FP_connecteur.emit(Signaux._SAUT_AVANT, -1)

    def FPactionBarreTemporelle(self):
        """
        Emission du signal quand la glissière est utilisée

        """
        self.FP_connecteur.emit(Signaux._SAUT_TEMPOREL, self.FPD_barre_temporelle.value())

    def FPuptdateLabelSelection(self, _selection, _total):
        """
        Permet de mettre à jour les valeurs affichées du nombre total d'états dans lequel le réseau est passé ainsi
        que l'état actuellement affiché

        :param _selection : entier, la sélection actuelle
        :param _total : entier, le nombre d'états

        """
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
