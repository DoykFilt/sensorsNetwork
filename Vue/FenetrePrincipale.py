"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module FenetrePrincipale

    Module utilisé pour la gestion de la Fenêtre principale de l'application

    Il contient la classe FenetrePrincipale qui correspond à la fenêtre en question.
"""

import mplcursors as mplcursors
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Controleur.Statistiques import Statistiques
from Modele.Signaux import Signaux
from Utilitaires.FileManager import FileManager
from Utilitaires.Log import Log
from Vue import fenetreprincipaledesign_ui


_log = Log()


class FenetrePrincipale(QtWidgets.QMainWindow, fenetreprincipaledesign_ui.Ui_MainWindow):

    """
        class FenetrePrincipale

        Hérite de
            -   QMainWindow -> fenetre principale Qt
            -   Ui_MainWindow -> le design de la fenetre Qt

        Classe qui represent la fenetre principale de l'application

        :var self.FP_connecteur : QtCore.pyqtSignal, Utilisé par la fenêtre pour notifier le contrôleur d'une action
             de l'utilisateur sur la fenêtre
        :var self.FP_view : QWebEngineView, Fenêtre de vue sur la page html qui contient la représentation de l'état du
            réseau
        :var self.FP_selection : int, le numéro de l'état du réseau à afficher
        :var self.FP_total : int, le nombre total de réseau à afficher
        :var self.FP_figure_graphique1 : Figure matplotlib, le contenant de l'ensemble des informations du graphique à
            afficher. Le graphique correspond à la durée de vie du réseau en fonction de l'intervalle de temps utilisé
        :var self.FP_canvas_graphique1 : FigureCanvas matplotlib qt, le composant sur lequel sera dessinée la figure 1
        :var self.FP_figure_graphique2 : Figure matplotlib, le contenant de l'ensemble des informations du graphique à
            afficher. Le graphique correspond aux nombres de capteurs connectés à la passerelle en fonction du temps
        :var self.FP_canvas_graphique2 : FigureCanvas matplotlib qt, le composant sur lequel sera dessinée la figure 2

    """

    # Connecteur de la fenetre, permet de reagir depuis l'exterieur de la classe si un boutton a été cliqué
    FP_connecteur = pyqtSignal(Signaux, int)

    def __init__(self):
        """
        Initialisateur de la classe FenetrePrincipale
        """
        _log.Linfo("Init -- FenetrePrincipale")

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

        # Chargement de la page html
        _fileManager = FileManager()
        _qurl = QUrl()
        _chemin = _fileManager.FMchargerHTMLEtat(self.FP_selection)
        _local_url = _qurl.fromLocalFile(_chemin)
        self.FP_view.load(_local_url)

        self.FPD_layout_gauche_haut.addWidget(self.FP_view)

        self.FP_view.show()

    def FPafficherReseau(self):
        """
            Affiche dans la section didiée de la fenêtre, le reseau enregistré en local sous forme d'une page html

        """
        _log.Linfo("Début ## FenetrePrincipale.FPafficherReseau")

        _statistiques = Statistiques()
        self.FPD_aire_informations.setText(_statistiques.SgenererTexte(self.FP_selection))

        _fileManager = FileManager()
        _chemin = _fileManager.FMchargerHTMLEtat(self.FP_selection)

        _qurl = QUrl()
        _local_url = _qurl.fromLocalFile(_chemin)

        self.FP_view.load(_local_url)

        self.FPafficherGraphiques()

    def FPafficherGraphiques(self):
        """
        Affiche dans la section didiée de la fenêtre les deux graphiques
        Premier graphique (en haut) : La durée de vie du réseau en fonction de l'intervalle de changement de
        rôle utilisé
        Second graphique : Le nombre de capteurs connectés à la passerelle en fonction du temps

        Les données sont affichées sous forme de points, les valeurs s'affichent au passage de la souris
        """
        _log.Linfo("Début ## FenetrePrincipale.FPafficherGraphiques")

        _statistiques = Statistiques()
        _donnees_graphique1, _donnees_graphique2 = _statistiques.SgenererDonneesGraphiques()
        # Graphique 1
        _ax = self.FP_figure_graphique1.add_subplot(111)
        _ax.clear()
        _lignes = _ax.plot(_donnees_graphique1["y"], _donnees_graphique1["x"], 'o')
        _ax.set_xlabel("Intervalle de temps entre les changements de rôle")
        _ax.set_ylabel("Durée de vie du réseau")
        _ax.set_title("Résultats durée de vie du réseau")
        mplcursors.cursor(_lignes, hover=True)
        self.FP_figure_graphique1.tight_layout()
        self.FP_canvas_graphique1.draw()

        # Graphique 2
        _ax = self.FP_figure_graphique2.add_subplot(111)
        _ax.clear()
        _lignes = _ax.plot(_donnees_graphique2["y"], _donnees_graphique2["x"], 'o')
        _ax.set_xlabel("Durée de la simulation en unité de temps")
        _ax.set_ylabel("Nombre de capteurs connectés")
        _ax.set_title("Capteurs connectés à la passerelle")
        mplcursors.cursor(_lignes, hover=True)
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
        _log.Linfo("Début ## FenetrePrincipale.FPactionGenerer")

        self.FP_connecteur.emit(Signaux.GENERER_RESEAU, -1)

    def FPactionChargerReseau(self):
        """
        Emission du signal quand charger un reseau est choisi dans le menu

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionChargerReseau")

        self.FP_connecteur.emit(Signaux.CHARGER_XML, -1)

    def FPactionExporterReseau(self):
        """
        Emission du signal quand exporter un reseau est choisi dans le menu

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionExporterReseau")

        self.FP_connecteur.emit(Signaux.EXPORTER_XML, -1)

    def FPactionImporterSimulation(self):
        """
        Emission du signal quand importer un résultat de simulation est choisi dans le menu

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionImporterSimulation")

        self.FP_connecteur.emit(Signaux.IMPORTER_RESULTAT, -1)

    def FPactionExporterSimulation(self):
        """
        Emission du signal quand exporter un résultat de simulation est choisi dans le menu

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionExporterSimulation")

        self.FP_connecteur.emit(Signaux.EXPORTER_RESULTAT, -1)

    def FPactionSimulation(self):
        """
        Emission du signal quand le boutton "Lancer la simulation" est cliqué. Si la case à cocher est coché cela veut
        dire que l'utilisateur souhaite afficher les états intermédiaires que le réseau prendra pendant la simulation

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionSimulation")

        _checked = 0
        if self.FPD_check_box.isChecked():
            _checked = 1
        self.FP_connecteur.emit(Signaux.LANCER_SIMULATION, _checked)

    def FPactionArriere(self):
        """
        Emission du signal quand le bouton "gauche" à côté de la glissière est cliqué

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionArriere")

        self.FP_connecteur.emit(Signaux.ARRIERE, -1)

    def FPactionSautArriere(self):
        """
        Emission du signal quand le bouton "extrème gauche" à côté de la glissière est cliqué

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionSautArriere")

        self.FP_connecteur.emit(Signaux.SAUT_ARRIERE, -1)

    def FPactionAvant(self):
        """
        Emission du signal quand le bouton "gauche" à côté de la glissière est cliqué

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionAvant")

        self.FP_connecteur.emit(Signaux.AVANT, -1)

    def FPactionSautAvant(self):
        """
        Emission du signal quand le bouton "extrème droite" à côté de la glissière est cliqué

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionSautAvant")

        self.FP_connecteur.emit(Signaux.SAUT_AVANT, -1)

    def FPactionBarreTemporelle(self):
        """
        Emission du signal quand la glissière est utilisée

        """
        _log.Linfo("Début ## FenetrePrincipale.FPactionBarreTemporelle")

        self.FP_connecteur.emit(Signaux.SAUT_TEMPOREL, self.FPD_barre_temporelle.value())

    def FPuptdateLabelSelection(self, _selection, _total):
        """
        Permet de mettre à jour les valeurs affichées du nombre total d'états dans lequel le réseau est passé ainsi
        que l'état actuellement affiché

        :param _selection : entier, la sélection actuelle
        :param _total : entier, le nombre d'états

        """
        _log.Linfo("Début ## FenetrePrincipale.FPuptdateLabelSelection")
        _log.Lerror("Info ## selection = " + str(_selection) + ", total = " + str(_total))

        if _selection > _total:
            _log.Lerror("Erreur de valeurs selection / total")
            self.FPD_selection_barre_temporelle.setText("Erreur valeurs")
        else:
            self.FP_selection = _selection
            self.FP_total = _total
            if _total == 0:
                self.FP_total = 1

            self.FPD_selection_barre_temporelle.setText(
                str(self.FP_selection + 1) + " / " + str(self.FP_total))

            self.FPD_barre_temporelle.setMinimum(0)
            self.FPD_barre_temporelle.setMaximum(self.FP_total - 1)
            self.FPD_barre_temporelle.setTickInterval(1)
            self.FPD_barre_temporelle.setValue(self.FP_selection)
