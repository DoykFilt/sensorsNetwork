from PyQt5 import QtWidgets

from Modele.Parametres import Parametres
from Vue import fenetrecreationdesign_ui
from Modele.Signaux import Signaux
from PyQt5.QtCore import pyqtSignal, Qt
import math


class FenetreCreation(QtWidgets.QMainWindow, fenetrecreationdesign_ui.Ui_MainWindow):
    FC_connecteur = pyqtSignal(Signaux, Parametres)

    _FCD_NBR_CAPTEURS_MIN = 3
    _FCD_NBR_CAPTEURS_MAX = None  # Définit dans l'init

    _FCD_CAPACITE_BATTERIE_MIN = 1
    _FCD_CAPACITE_BATTERIE_MAX = 10

    _FCD_LARGEUR_MIN = 10
    _FCD_LARGEUR_MAX = 500

    _FCD_DISTANCE_MAX_MIN = 1
    _FCD_DISTANCE_MAX_MAX = None  # Définit dans l'init

    _FCD_DISTANCE_MIN_MIN = 0
    _FCD_DISTANCE_MIN_MAX = int(_FCD_LARGEUR_MAX / 100)

    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        fenetrecreationdesign_ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Capacité des batteries
        self.FCD_cap_batterie_min.setText(str(self._FCD_CAPACITE_BATTERIE_MIN))
        self.FCD_cap_batterie_max.setText(str(self._FCD_CAPACITE_BATTERIE_MAX))
        self.FCD_cap_batterie_barre_choix.setMinimum(self._FCD_CAPACITE_BATTERIE_MIN)
        self.FCD_cap_batterie_barre_choix.setMaximum(self._FCD_CAPACITE_BATTERIE_MAX)
        self.FCD_cap_batterie_barre_choix.setTickInterval(1)
        self.FCD_cap_batterie_barre_choix.setValue(
            int((self._FCD_CAPACITE_BATTERIE_MAX - self._FCD_CAPACITE_BATTERIE_MIN) / 2))
        self.FCD_cap_batterie_barre_choix.valueChanged.connect(self.FCupdateValues)

        # Taille
        self.FCD_taille_max_min.setText(str(self._FCD_LARGEUR_MIN))
        self.FCD_taille_max_max.setText(str(self._FCD_LARGEUR_MAX))
        self.FCD_taille_max_barre_choix.setMinimum(self._FCD_LARGEUR_MIN)
        self.FCD_taille_max_barre_choix.setMaximum(self._FCD_LARGEUR_MAX)
        self.FCD_taille_max_barre_choix.setTickInterval(1)
        self.FCD_taille_max_barre_choix.setValue(
            int((self._FCD_LARGEUR_MAX - self._FCD_LARGEUR_MIN) / 2))
        self.FCD_taille_max_barre_choix.valueChanged.connect(self.FCactionChangementTaille)

        # Nombre de capteurs
        self._FCD_NBR_CAPTEURS_MAX = int(self.FCD_taille_max_barre_choix.value() / 2)
        self.FCD_nbr_capteurs_min.setText(str(self._FCD_NBR_CAPTEURS_MIN))
        self.FCD_nbr_capteurs_max.setText(str(self._FCD_NBR_CAPTEURS_MAX))
        self.FCD_nbr_capteurs_barre_choix.setMinimum(self._FCD_NBR_CAPTEURS_MIN)
        self.FCD_nbr_capteurs_barre_choix.setMaximum(self._FCD_NBR_CAPTEURS_MAX)
        self.FCD_nbr_capteurs_barre_choix.setTickInterval(1)
        self.FCD_nbr_capteurs_barre_choix.setValue(
            int((self._FCD_NBR_CAPTEURS_MAX - self._FCD_NBR_CAPTEURS_MIN) / 2))
        self.FCD_nbr_capteurs_barre_choix.valueChanged.connect(self.FCupdateValues)

        # Distances max et min
        self._FCD_DISTANCE_MAX_MAX = int(self.FCD_taille_max_barre_choix.value() / 6)
        self.FCD_distance_max_barre_choix.setValue(
            int((self._FCD_DISTANCE_MAX_MAX - self._FCD_DISTANCE_MAX_MIN) / 2))
        self.FCinitDistances()
        self.FCD_distance_max_barre_choix.valueChanged.connect(self.FCcontroleDistancesMax)
        self.FCD_distance_min_barre_choix.valueChanged.connect(self.FCcontroleDistancesMin)

        self.FCupdateValues()

        self.FCD_boutton_generer.clicked.connect(self.FCvalider)
        self.FCD_boutton_annuler.clicked.connect(self.FCannuler)

    def FCinitDistances(self):
        # Distance max
        self.FCD_distance_max_min.setText(str(self._FCD_DISTANCE_MAX_MIN))
        self.FCD_distance_max_max.setText(str(self._FCD_DISTANCE_MAX_MAX))
        self.FCD_distance_max_barre_choix.setMinimum(self._FCD_DISTANCE_MAX_MIN)
        self.FCD_distance_max_barre_choix.setMaximum(self._FCD_DISTANCE_MAX_MAX)
        self.FCD_distance_max_barre_choix.setTickInterval(1)
        self.FCD_distance_max_barre_choix.valueChanged.connect(self.FCcontroleDistancesMax)

        # Distance min
        self.FCD_distance_min_min.setText(str(self._FCD_DISTANCE_MIN_MIN))
        self.FCD_distance_min_max.setText(str(self._FCD_DISTANCE_MIN_MAX))
        self.FCD_distance_min_barre_choix.setMinimum(self._FCD_DISTANCE_MIN_MIN)
        self.FCD_distance_min_barre_choix.setMaximum(self._FCD_DISTANCE_MIN_MAX)
        self.FCD_distance_min_barre_choix.setTickInterval(1)
        self.FCD_distance_min_barre_choix.setValue(
            int((self._FCD_DISTANCE_MIN_MAX - self._FCD_DISTANCE_MIN_MIN) / 2))
        self.FCcontroleDistancesMin()

    def FCupdateValues(self):
        self.FCD_nbr_capteurs_valeur.setText(str(self.FCD_nbr_capteurs_barre_choix.value()))
        self.FCD_cap_batterie_valeur.setText(str(self.FCD_cap_batterie_barre_choix.value()))
        self.FCD_taille_max_valeur.setText(str(self.FCD_taille_max_barre_choix.value()))
        self.FCD_distance_max_valeur.setText(str(self.FCD_distance_max_barre_choix.value()))
        self.FCD_distance_min_valeur.setText(str(self.FCD_distance_min_barre_choix.value()))

    def FCcontroleDistancesMax(self):
        if self.FCD_distance_max_barre_choix.value() < self.FCD_distance_min_barre_choix.value():
            self.FCD_distance_min_barre_choix.setValue(self.FCD_distance_max_barre_choix.value())
        self.FCupdateValues()

    def FCcontroleDistancesMin(self):
        if self.FCD_distance_min_barre_choix.value() > self.FCD_distance_max_barre_choix.value():
            self.FCD_distance_max_barre_choix.setValue(self.FCD_distance_min_barre_choix.value())
        self.FCupdateValues()

    def FCactionChangementTaille(self):

        if self.FCD_taille_max_barre_choix.value() / 100 <= 1:
            self.FCD_distance_min_barre_choix.setValue(1)
            self.FCD_distance_min_barre_choix.setMaximum(1)
            self.FCD_distance_min_max.setText(str(1))
        else:
            self.FCinitDistances()

        self._FCD_DISTANCE_MAX_MAX = int(self.FCD_taille_max_barre_choix.value() / 6)
        self.FCD_distance_max_max.setText(str(self._FCD_DISTANCE_MAX_MAX))
        self.FCD_distance_max_barre_choix.setMaximum(self._FCD_DISTANCE_MAX_MAX)
        if self.FCD_distance_max_barre_choix.value() > self._FCD_DISTANCE_MAX_MAX:
            self.FCD_distance_max_barre_choix.setValue(self._FCD_DISTANCE_MAX_MAX)

        self._FCD_NBR_CAPTEURS_MAX = int(self.FCD_taille_max_barre_choix.value() / 2)
        self.FCD_nbr_capteurs_max.setText(str(self._FCD_NBR_CAPTEURS_MAX))
        self.FCD_nbr_capteurs_barre_choix.setMaximum(self._FCD_NBR_CAPTEURS_MAX)
        if self.FCD_nbr_capteurs_barre_choix.value() > self._FCD_NBR_CAPTEURS_MAX:
            self.FCD_nbr_capteurs_barre_choix.setValue(self._FCD_NBR_CAPTEURS_MAX)

        self.FCupdateValues()

    def FCobtenirConnecteur(self):
        return self.FC_connecteur

    def FCvalider(self):
        self.FC_connecteur.emit(Signaux._VALIDER_PARAMETRES, self.FCobtenirParametres())

    def FCannuler(self):
        self.FC_connecteur.emit(Signaux._ANNULER_PARAMETRES, self.FCobtenirParametres())

    def FCobtenirParametres(self):
        return Parametres(_max_size=self.FCD_taille_max_barre_choix.value(),
                          _marge=int(self.FCD_taille_max_barre_choix.value() / 100),
                          _max_distance=self.FCD_distance_max_barre_choix.value(),
                          _min_distance=self.FCD_distance_min_barre_choix.value(),
                          _nbr_capteurs=self.FCD_nbr_capteurs_barre_choix.value(),
                          _capacitees_batteries=self.FCD_cap_batterie_barre_choix.value(),
                          _nbr_puits=1
                          )

