import random

import matplotlib.pyplot as plt

from Modele.Reseau import Reseau
from Vue.FenetrePrincipale import FenetrePrincipale

# TODO : Tkinter : option charger ou sauvegarder un réseau + barre de chargement lors de la création

def main():

    _max_size = 25
    _marge = 1
    _nbr_capteurs = 50
    _max_distance = 1
    _min_distance = 1

    reseau = Reseau(_nbr_capteurs, _max_size, _marge, _max_distance, _min_distance)
    print("Calcul de l'affichage..")
    FPFenetrePrincipale = FenetrePrincipale()
    FPFenetrePrincipale.FPafficherReseau(reseau, "networkx")


if __name__ == "__main__":
    main()
