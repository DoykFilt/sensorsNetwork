"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module BarreProgression

    Module utilisé pour la gestion d'un barre de progression

    Possède la classe BarreProgression, concrétisation de cette modélisation
"""

from PyQt5.QtWidgets import QProgressDialog
from PyQt5 import QtCore

from Utilitaires.Log import Log


_log = Log()


class BarreProgression:
    """
        class BarreProgression

        Utilisée pour créer et gérer une boite de dialogue qui affiche une barre de progression
        et des informations complémentaires.

        :var self.BP_barre_progression :  QProgressDialog, La boite de dialogue contenant la barre de progression
    """

    def __init__(self):
        """
            Initialisateur de la classe, créé un objet QProgressDialog et l'initialise

        """
        _log.Linfo("Init -- BarreProgression")

        self.BP_barre_progression = QProgressDialog("", "", 0, 100)
        self.BP_barre_progression.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.BP_barre_progression.setMaximumHeight(100)
        self.BP_barre_progression.setMinimumHeight(100)
        self.BP_barre_progression.setMaximumWidth(300)
        self.BP_barre_progression.setMinimumWidth(300)
        self.BP_barre_progression.setCancelButton(None)
        self.BP_barre_progression.setWindowModality(QtCore.Qt.ApplicationModal)
        self.BP_barre_progression.show()
        self.BP_barre_progression.setValue(0)

    def BPchangementValeur(self, _valeur):
        """
            Permet de changer la position de la barre de progression (avec une valeur comprise entre 0 et 100)

            :param _valeur : la valeur à appliquer
        """
        _log.Linfo("Début ## BarreProgression.BPchangementValeur")

        if _valeur < 0:
            _valeur = 0
        if _valeur > 100:
            _valeur = 100

        self.BP_barre_progression.setValue(_valeur)

    def BPchangementLabel(self, _texte, _temps_restant=None):
        """
            Permet de modifier le texte dans la boite de dialogue

            :param _texte le texte str à afficher
            :param _temps_restant le temps restant estimé à afficher, optionnel
        """
        _log.Linfo("Début ## BarreProgression.BPchangementLabel")

        if _temps_restant is not None:
           _texte += "\n \n" + "Temps restant estimé : " + str(int(_temps_restant)) + " secondes"

        self.BP_barre_progression.setLabelText(_texte)

    def BPfin(self):
        """
            Permet de fermer la boite de dialogue
        """
        _log.Linfo("Début ## BarreProgression.BPfin")

        self.BP_barre_progression.setValue(100)
        self.BP_barre_progression.close()
