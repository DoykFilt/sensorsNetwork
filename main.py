import os
import random
import sys

import matplotlib.pyplot as plt

from Controleur.ReseauControleur import ReseauControleur
from Modele.Reseau import Reseau
from Vue.FenetreCreation import FenetreCreation
from Vue.FenetrePrincipale import FenetrePrincipale
from PyQt5.QtWidgets import QApplication


# TODO : Tkinter : option charger ou sauvegarder un réseau + barre de chargement lors de la création

def main():

    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    app = QApplication(sys.argv)

    _fenetre_principale = FenetrePrincipale()
    _fenetre_principale.setWindowTitle("Simulateur de la consommation énergétique de réseaux de capteurs sans fils")
    _fenetre_creation = FenetreCreation()
    _reseau_controleur = ReseauControleur(_fenetre_principale, _fenetre_creation)

    _fenetre_principale.show()

    """Retourne un exit status 
    (0 pour succes, tout le reste pour l'echec"""
    try:
        sys.exit(app.exec_())
    except:
        sys.exit(0)


if __name__ == "__main__":
    main()