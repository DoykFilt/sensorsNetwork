from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt

from Modele.Parametres import Parametres
from Vue import fenetrecreationdesign_ui
from Modele.Signaux import Signaux


class FenetreCreation(QtWidgets.QMainWindow, fenetrecreationdesign_ui.Ui_MainWindow):
    """
        class FenetrePrincipale

        Hérite de
            -   QMainWindow -> fenetre principale Qt
            -   Ui_MainWindow -> le design de la fenetre Qt

        Classe qui represent la fenetre principale de l'application

    """

    # Connecteur de la fenetre, permet de reagir depuis l'exterieur de la classe si un boutton a été cliqué
    FC_connecteur = pyqtSignal(Signaux, Parametres)

    # Constantes qui définissent les limites du choix des paramètres
    __FCD_NBR_CAPTEURS_MIN = 3
    __FCD_NBR_CAPTEURS_MAX = None  # Définit dans l'init, dépend de la largeur

    __FCD_CAPACITE_BATTERIE_MIN = 1
    __FCD_CAPACITE_BATTERIE_MAX = 1000

    __FCD_LARGEUR_MIN = 10
    __FCD_LARGEUR_MAX = 500

    __FCD_DISTANCE_MAX_MIN = 1
    __FCD_DISTANCE_MAX_MAX = None  # Définit dans l'init, dépend de la largeur

    __FCD_DISTANCE_MIN_MIN = 0
    __FCD_DISTANCE_MIN_MAX = int(__FCD_LARGEUR_MAX / 100)

    def __init__(self):

        """
        Initialisateur de la fenêtre, définit les valeurs des différents composants :
            - text du minimum
            - text du maximul
            - barre coulissante de choix
            - text du choix
        De chaque valeure :
            - Capacité des batteries
            - Taille de la surface à couvrir
            - Nombre de capteurs
            - Distance maximale pour établir une connexion entre deux capteurs
            - Distance minimale entre deux deux capteurs

        """
        QtWidgets.QMainWindow.__init__(self)
        fenetrecreationdesign_ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Capacité des batteries
        self.FCD_cap_batterie_min.setText(str(self.__FCD_CAPACITE_BATTERIE_MIN))
        self.FCD_cap_batterie_max.setText(str(self.__FCD_CAPACITE_BATTERIE_MAX))
        self.FCD_cap_batterie_barre_choix.setMinimum(self.__FCD_CAPACITE_BATTERIE_MIN)
        self.FCD_cap_batterie_barre_choix.setMaximum(self.__FCD_CAPACITE_BATTERIE_MAX)
        self.FCD_cap_batterie_barre_choix.setTickInterval(1)
        self.FCD_cap_batterie_barre_choix.setValue(
            int((self.__FCD_CAPACITE_BATTERIE_MAX - self.__FCD_CAPACITE_BATTERIE_MIN) / 2))
        self.FCD_cap_batterie_barre_choix.valueChanged.connect(self.FCupdateValues)

        # Taille de la surface à couvrir
        self.FCD_taille_max_min.setText(str(self.__FCD_LARGEUR_MIN))
        self.FCD_taille_max_max.setText(str(self.__FCD_LARGEUR_MAX))
        self.FCD_taille_max_barre_choix.setMinimum(self.__FCD_LARGEUR_MIN)
        self.FCD_taille_max_barre_choix.setMaximum(self.__FCD_LARGEUR_MAX)
        self.FCD_taille_max_barre_choix.setTickInterval(1)
        self.FCD_taille_max_barre_choix.setValue(
            int((self.__FCD_LARGEUR_MAX - self.__FCD_LARGEUR_MIN) / 2))
        self.FCD_taille_max_barre_choix.valueChanged.connect(self.FCactionChangementTaille)

        # Nombre de capteurs
        self.__FCD_NBR_CAPTEURS_MAX = int(self.FCD_taille_max_barre_choix.value() / 2)
        self.FCD_nbr_capteurs_min.setText(str(self.__FCD_NBR_CAPTEURS_MIN))
        self.FCD_nbr_capteurs_max.setText(str(self.__FCD_NBR_CAPTEURS_MAX))
        self.FCD_nbr_capteurs_barre_choix.setMinimum(self.__FCD_NBR_CAPTEURS_MIN)
        self.FCD_nbr_capteurs_barre_choix.setMaximum(self.__FCD_NBR_CAPTEURS_MAX)
        self.FCD_nbr_capteurs_barre_choix.setTickInterval(1)
        self.FCD_nbr_capteurs_barre_choix.setValue(
            int((self.__FCD_NBR_CAPTEURS_MAX - self.__FCD_NBR_CAPTEURS_MIN) / 2))
        self.FCD_nbr_capteurs_barre_choix.valueChanged.connect(self.FCupdateValues)

        # Distances max et min
        self.__FCD_DISTANCE_MAX_MAX = int(self.FCD_taille_max_barre_choix.value() / 5)
        self.FCD_distance_max_barre_choix.setValue(
            int((self.__FCD_DISTANCE_MAX_MAX - self.__FCD_DISTANCE_MAX_MIN) / 2))
        # Appel à une fonction extérieure pour les max et min : Factorisation
        self.FCinitDistances()

        self.FCD_distance_max_barre_choix.valueChanged.connect(self.FCcontroleDistancesMax)
        self.FCD_distance_min_barre_choix.valueChanged.connect(self.FCcontroleDistancesMin)

        self.FCupdateValues()

        # Association du clic sur les boutons
        self.FCD_boutton_generer.clicked.connect(self.FCvalider)
        self.FCD_boutton_annuler.clicked.connect(self.FCannuler)

    def FCinitDistances(self):
        """
        Fonction externe à l'initialisateur, objectif factorisation de code
        Appellée également lors du changement de valeur de la barre glissante, car les valeures suivantes en dépendent

        """

        # Distance max
        self.FCD_distance_max_min.setText(str(self.__FCD_DISTANCE_MAX_MIN))
        self.FCD_distance_max_max.setText(str(self.__FCD_DISTANCE_MAX_MAX))
        self.FCD_distance_max_barre_choix.setMinimum(self.__FCD_DISTANCE_MAX_MIN)
        self.FCD_distance_max_barre_choix.setMaximum(self.__FCD_DISTANCE_MAX_MAX)
        self.FCD_distance_max_barre_choix.setTickInterval(1)
        self.FCD_distance_max_barre_choix.valueChanged.connect(self.FCcontroleDistancesMax)

        # Distance min
        self.FCD_distance_min_min.setText(str(self.__FCD_DISTANCE_MIN_MIN))
        self.FCD_distance_min_max.setText(str(self.__FCD_DISTANCE_MIN_MAX))
        self.FCD_distance_min_barre_choix.setMinimum(self.__FCD_DISTANCE_MIN_MIN)
        self.FCD_distance_min_barre_choix.setMaximum(self.__FCD_DISTANCE_MIN_MAX)
        self.FCD_distance_min_barre_choix.setTickInterval(1)
        self.FCD_distance_min_barre_choix.setValue(int((self.__FCD_DISTANCE_MIN_MAX - self.__FCD_DISTANCE_MIN_MIN) / 2))

        # Permet de garder la valeur de distance min plus petite ou égale que la valeur de distance max
        self.FCcontroleDistancesMin()

    def FCupdateValues(self):
        """
        Met à jour l'affichage de la valeur sélectionnée. Appelée au changement de valeur des barres glissantes

        """
        self.FCD_nbr_capteurs_valeur.setText(str(self.FCD_nbr_capteurs_barre_choix.value()))
        self.FCD_cap_batterie_valeur.setText(str(self.FCD_cap_batterie_barre_choix.value()))
        self.FCD_taille_max_valeur.setText(str(self.FCD_taille_max_barre_choix.value()))
        self.FCD_distance_max_valeur.setText(str(self.FCD_distance_max_barre_choix.value()))
        self.FCD_distance_min_valeur.setText(str(self.FCD_distance_min_barre_choix.value()))

    def FCcontroleDistancesMax(self):
        """
        Permet de s'assurer que la distance max est plus grande que la distance min

        """
        if self.FCD_distance_max_barre_choix.value() < self.FCD_distance_min_barre_choix.value():
            self.FCD_distance_min_barre_choix.setValue(self.FCD_distance_max_barre_choix.value())
        self.FCupdateValues()

    def FCcontroleDistancesMin(self):
        """
        Permet de s'assurer que la distance min est plus petite que la distance max

        """
        if self.FCD_distance_min_barre_choix.value() > self.FCD_distance_max_barre_choix.value():
            self.FCD_distance_max_barre_choix.setValue(self.FCD_distance_min_barre_choix.value())
        self.FCupdateValues()

    def FCactionChangementTaille(self):
        """
        Permet de modifier les valeurs maximales des paramètres qui dépendent de la valeur sélectionnée de la taille

        """
        # Si la valeur de la taille divisé par 100 est plus petite que 1 :
        # la valeur de la distance minimum ne peut être comprise qu'entre 0 et 1
        if self.FCD_taille_max_barre_choix.value() / 100 <= 1:
            self.FCD_distance_min_barre_choix.setValue(1)
            self.FCD_distance_min_barre_choix.setMaximum(1)
            self.FCD_distance_min_max.setText(str(1))
        else:
            self.FCinitDistances()

        # La valeur maximale de la distance maximum est égale à la taille divisé par 6
        self.__FCD_DISTANCE_MAX_MAX = int(self.FCD_taille_max_barre_choix.value() / 6)
        self.FCD_distance_max_max.setText(str(self.__FCD_DISTANCE_MAX_MAX))
        self.FCD_distance_max_barre_choix.setMaximum(self.__FCD_DISTANCE_MAX_MAX)
        if self.FCD_distance_max_barre_choix.value() > self.__FCD_DISTANCE_MAX_MAX:
            self.FCD_distance_max_barre_choix.setValue(self.__FCD_DISTANCE_MAX_MAX)

        # Le nombre maximale de capteur est égal à la moitié de la taille
        self.__FCD_NBR_CAPTEURS_MAX = int(self.FCD_taille_max_barre_choix.value() / 2)
        self.FCD_nbr_capteurs_max.setText(str(self.__FCD_NBR_CAPTEURS_MAX))
        self.FCD_nbr_capteurs_barre_choix.setMaximum(self.__FCD_NBR_CAPTEURS_MAX)
        if self.FCD_nbr_capteurs_barre_choix.value() > self.__FCD_NBR_CAPTEURS_MAX:
            self.FCD_nbr_capteurs_barre_choix.setValue(self.__FCD_NBR_CAPTEURS_MAX)

        self.FCupdateValues()

    def FCobtenirConnecteur(self):
        """
        Renvoie le connecteur, permet d'agir à l'extérieur de la classe aux émissions de l'intérieur

        :return Le connecteur pyqtSignal
        """
        return self.FC_connecteur

    def FCvalider(self):
        """
        Emission du signal quand le valider est cliqué

        """
        self.FC_connecteur.emit(Signaux._VALIDER_PARAMETRES, self.FCobtenirParametres())

    def FCannuler(self):
        """
        Emission du signal quand le annuler est cliqué

        """
        self.FC_connecteur.emit(Signaux._ANNULER_PARAMETRES, self.FCobtenirParametres())

    def FCobtenirParametres(self):
        """
        Assemble un les paramètres choisis dans un objet Parametres

        :return Parametres
        """
        return Parametres(_max_size=self.FCD_taille_max_barre_choix.value(),
                          _marge=int(self.FCD_taille_max_barre_choix.value() / 100),
                          _max_distance=self.FCD_distance_max_barre_choix.value(),
                          _min_distance=self.FCD_distance_min_barre_choix.value(),
                          _nbr_capteurs=self.FCD_nbr_capteurs_barre_choix.value(),
                          _capacitees_batteries=self.FCD_cap_batterie_barre_choix.value(),
                          _nbr_puits=1
                          )

    @staticmethod
    def FCobtenirCapaciteMaxBatterie():
        return FenetreCreation.__FCD_CAPACITE_BATTERIE_MAX
