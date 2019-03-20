"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module FenetreCreation

    Module utilisé pour la gestion de la Fenêtre de paramètrage du réseau àque l'utilisateur veut créer

    Il contient la classe FenetreCreation qui correspond à la fenêtre en question.
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt

from Modele.Parametres import ParametresCreation
from Utilitaires.Log import Log
from Vue import fenetrecreationdesign_ui
from Modele.Signaux import Signaux


_log = Log()


class FenetreCreation(QtWidgets.QMainWindow, fenetrecreationdesign_ui.Ui_MainWindow):
    """
        class FenetrePrincipale

        Hérite de
            -   QMainWindow -> fenetre principale Qt
            -   Ui_MainWindow -> le design de la fenetre Qt

        Classe qui représente la fenetre principale de l'application

        :var : self.FC_connecteur : QtCore.pyqtSignal, Utilisé par la fenêtre pour notifier le contrôleur d'une action
             de l'utilisateur sur la fenêtre

        :cvar : self.__FCD_NBR_CAPTEURS_MIN : const int, le nombre de capteurs minimum que l'utilisateur peut saisir
        :cvar : self.__FCD_NBR_CAPTEURS_MAX : const int, le nombre de capteurs maximum que l'utilisateur peut saisir

        :cvar : self.__FCD_CAPACITE_BATTERIE_MIN : const int, la capacité minimum que l'utilisateur peut saisir pour
            les batteries des capteurs
        :cvar : self.__FCD_CAPACITE_BATTERIE_MAX : const int, la capacité maximum que l'utilisateur peut saisir pour
            les batteries des capteurs

        :cvar : self.__FCD_LARGEUR_MIN : const int, la largeur minimum que l'utilisateur peut choisir pour la surface
            carrée sur laquelle seront répartis les capteurs
        :cvar : self.__FCD_LARGEUR_MAX : const int, la largeur maximum que l'utilisateur peut choisir pour la surface
            carrée sur laquelle seront répartis les capteurs

        :cvar : self.__FCD_DISTANCE_MAX_MIN : const int, la distance nécessaire minimum entre deux capteurs, que
            l'utilisateur peut choisir, afin qu'ils établissent une connexion
        :cvar : self.__FCD_DISTANCE_MAX_MAX : const int, la distance maximum entre deux capteurs, que
            l'utilisateur peut choisir, à laquelle ils peuvent établir une connexion

        :cvar : self.__FCD_DISTANCE_MIN_MIN : const int, le minimum que l'utilisateur peut saisir de la distance minimum
        que deux capteurs doivent respecter entre eux
        :cvar : self.__FCD_DISTANCE_MIN_MAX : const int, le maximum que l'utilisateur peut saisir de la distance minimum
        que deux capteurs doivent respecter entre eux

    """

    # Connecteur de la fenetre, permet de reagir depuis l'exterieur de la classe si un boutton a été cliqué
    FC_connecteur = pyqtSignal(Signaux, ParametresCreation)

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
                - text du maximum
                - barre coulissante de choix
                - text du choix
            Pour chaque valeur :
                - Capacité des batteries
                - Taille de la surface à couvrir
                - Nombre de capteurs
                - Distance maximale pour établir une connexion entre deux capteurs
                - Distance minimale entre deux deux capteurs
        """
        _log.Linfo("Init -- FenetreCreation")

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

        self.FCD_distance_max_barre_choix.valueChanged.connect(self.FCcontroleDistances)
        self.FCD_distance_min_barre_choix.valueChanged.connect(self.FCcontroleDistances)

        self.FCupdateValues()

        # Association du clic sur les boutons
        self.FCD_boutton_generer.clicked.connect(self.FCvalider)
        self.FCD_boutton_annuler.clicked.connect(self.FCannuler)

    def FCinitDistances(self):
        """
            Fonction externe à l'initialisateur pour factoriser du code : appellée également lors du changement de
            valeur de la barre glissante, car certaines valeurs en dépendent

        """
        _log.Linfo("Début ## FenetreCreation.FCinitDistances")

        # Distance max
        self.FCD_distance_max_min.setText(str(self.__FCD_DISTANCE_MAX_MIN))
        self.FCD_distance_max_max.setText(str(self.__FCD_DISTANCE_MAX_MAX))
        self.FCD_distance_max_barre_choix.setMinimum(self.__FCD_DISTANCE_MAX_MIN)
        self.FCD_distance_max_barre_choix.setMaximum(self.__FCD_DISTANCE_MAX_MAX)
        self.FCD_distance_max_barre_choix.setTickInterval(1)
        self.FCD_distance_max_barre_choix.valueChanged.connect(self.FCcontroleDistances)

        # Distance min
        self.FCD_distance_min_min.setText(str(self.__FCD_DISTANCE_MIN_MIN))
        self.FCD_distance_min_max.setText(str(self.__FCD_DISTANCE_MIN_MAX))
        self.FCD_distance_min_barre_choix.setMinimum(self.__FCD_DISTANCE_MIN_MIN)
        self.FCD_distance_min_barre_choix.setMaximum(self.__FCD_DISTANCE_MIN_MAX)
        self.FCD_distance_min_barre_choix.setTickInterval(1)
        self.FCD_distance_min_barre_choix.setValue(int((self.__FCD_DISTANCE_MIN_MAX - self.__FCD_DISTANCE_MIN_MIN) / 2))

        # Permet de garder la valeur de distance min plus petite ou égale que la valeur de distance max
        self.FCcontroleDistances()

    def FCupdateValues(self):
        """
            Met à jour l'affichage de la valeur sélectionnée. Appelée au changement de valeur de la barre coulissante
        """
        _log.Linfo("Début ## FenetreCreation.FCupdateValues")

        self.FCD_nbr_capteurs_valeur.setText(str(self.FCD_nbr_capteurs_barre_choix.value()))
        self.FCD_cap_batterie_valeur.setText(str(self.FCD_cap_batterie_barre_choix.value()))
        self.FCD_taille_max_valeur.setText(str(self.FCD_taille_max_barre_choix.value()))
        self.FCD_distance_max_valeur.setText(str(self.FCD_distance_max_barre_choix.value()))
        self.FCD_distance_min_valeur.setText(str(self.FCD_distance_min_barre_choix.value()))

    def FCcontroleDistances(self):
        """
            Permet de s'assurer que la distance max est plus grande que la distance min et  que la distance min est plus
            petite que la distance max
        """
        _log.Linfo("Début ## FenetreCreation.FCcontroleDistances")

        if self.FCD_distance_max_barre_choix.value() < self.FCD_distance_min_barre_choix.value():
            self.FCD_distance_min_barre_choix.setValue(self.FCD_distance_max_barre_choix.value())

        elif self.FCD_distance_min_barre_choix.value() > self.FCD_distance_max_barre_choix.value():
            self.FCD_distance_max_barre_choix.setValue(self.FCD_distance_min_barre_choix.value())

        self.FCupdateValues()

    def FCactionChangementTaille(self):
        """
            Permet de modifier les valeurs maximales des paramètres qui dépendent de la valeur sélectionnée de la taille
        """
        _log.Linfo("Début ## FenetreCreation.FCactionChangementTaille")

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

            :return pyqtSignal : Le connecteur
        """
        return self.FC_connecteur

    def FCvalider(self):
        """
            Emission du signal quand le valider est cliqué
        """
        _log.Linfo("Début ## FenetreCreation.FCvalider")

        self.FC_connecteur.emit(Signaux.VALIDER_PARAMETRES, self.FCobtenirParametres())

    def FCannuler(self):
        """
            Emission du signal quand le annuler est cliqué
        """
        _log.Linfo("Début ## FenetreCreation.FCannuler")

        self.FC_connecteur.emit(Signaux.ANNULER_PARAMETRES, self.FCobtenirParametres())

    def FCobtenirParametres(self):
        """
            Assemble les paramètres choisis dans un objet ParametresCreation

            :return ParametresCreation
        """
        _log.Linfo("Début ## FenetreCreation.FCobtenirParametres")

        return ParametresCreation(_max_size=self.FCD_taille_max_barre_choix.value(),
                                  _marge=int(self.FCD_taille_max_barre_choix.value() / 100),
                                  _max_distance=self.FCD_distance_max_barre_choix.value(),
                                  _min_distance=self.FCD_distance_min_barre_choix.value(),
                                  _nbr_capteurs=self.FCD_nbr_capteurs_barre_choix.value(),
                                  _capacitees_batteries=self.FCD_cap_batterie_barre_choix.value(),
                                  _nbr_puits=1
                                  )

    @staticmethod
    def FCobtenirCapaciteMaxBatterie():
        """
            Permet d'obtenir le choix de la capacité maximal de la batterie, utilisé sur l'affichage de l'échelle de
            couleur pour l'affichage du réseau

        :return: int, La capacité maximale
        """
        return FenetreCreation.__FCD_CAPACITE_BATTERIE_MAX
