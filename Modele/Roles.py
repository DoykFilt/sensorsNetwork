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

    def __str__(self):
        """
        Surcharge de la conversion en string, renvoie la valeur correspondante
        :return String, la valeur en chaîne de caractère
        """
        return str(self.value)

    _PUIT = 0
    _EMETTEUR = 1
    _EMETTEUR_RECEPTEUR = 2

    _ARC_DOMINANT = 3
    _ARC_NON_DOMINANT = 4
