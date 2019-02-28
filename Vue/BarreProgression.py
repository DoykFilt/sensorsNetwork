from PyQt5.QtWidgets import QProgressDialog
from PyQt5 import QtCore


class BarreProgression:
    """
        class BarreProgression

        Utilisée pour créer et gérer une boite de dialogue qui affiche une barre de progression
        et des informations complémentaires

    """

    def __init__(self):
        """
            Initialisateur de la classe, créé un objet QProgressDialog et l'initialise

        """

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
            Permet de changer la position de la barre de progression (compris entre 0 et 100

            :param _valeur : la velur à appliquer
        """
        self.BP_barre_progression.setValue(_valeur)

    def BPchangementLabel(self, _texte, _temps_restant=None):
        """
            Permet de modifier le texte dans la boite de dialogue

            :param _texte le texte str à afficher
            :param _temps_restant le temps restant estimé à afficher, optionnel
        """
        if _temps_restant is not None:
            self.BP_barre_progression.setLabelText(_texte
                                                   + "\n \n"
                                                   + "Temps restant estimé : " + str(int(_temps_restant)) + " secondes")
        else:
            self.BP_barre_progression.setLabelText(_texte)

    def BPfin(self):
        """
            Permet de fermer la boite de dialogue
        """
        self.BP_barre_progression.setValue(100)
        self.BP_barre_progression.close()
