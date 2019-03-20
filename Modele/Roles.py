"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Signaux

    Possède l'énumération Roles qui recenses les différents rôles que peuvent prendre noeuds et arcs du réseau
"""


from enum import Enum


class Roles(Enum):
    """
        Enumération qui liste les roles que peut avoir un noeud :
            - puit
            - émetteur
            - émetteur / récepteur

        ainsi que les rôles que peut avoir un arc :
            - dominant (cad si il relie deux noeuds de l'ensemble dominant
            - non dominant

    """
    # Rôles des noeuds
    PUIT = 0
    EMETTEUR = 1
    EMETTEUR_RECEPTEUR = 2

    # Rôles des puits
    ARC_DOMINANT = 3
    ARC_NON_DOMINANT = 4

    def __str__(self):
        """
        Surcharge de la conversion en string, renvoie la valeur correspondante
        :return String, la valeur en chaîne de caractère
        """
        return str(self.value)

