import os
import random
import sys

import matplotlib.pyplot as plt

from Modele.Reseau import Reseau
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

    _max_size = 25
    _marge = 1
    _nbr_capteurs = 50
    _max_distance = 5
    _min_distance = 1

    FPFenetrePrincipale = FenetrePrincipale()
    reseau = Reseau(_nbr_capteurs, _max_size, _marge, _max_distance, _min_distance)

    print("Calcul de l'affichage..")
    FPFenetrePrincipale.FPafficherReseau(reseau, "..\\donnees\\reseau", "reseau_000")
    FPFenetrePrincipale.lancer()
    FPFenetrePrincipale.show()

    """Retourne un exit status 
    (0 pour succes, tout le reste pour l'echec"""
    try:
        sys.exit(app.exec_())
    except:
        sys.exit(0)


if __name__ == "__main__":
    main()
