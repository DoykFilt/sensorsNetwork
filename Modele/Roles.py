from enum import Enum


class Roles(Enum):
    """
        Enumération qui liste les roles que peut avoir un noeud :
            - puit
            - émetteur
            - émetteur / récepteur

    """

    # surcharge de conversion en string, renvoit la valeur correspondante
    def __str__(self):
        return str(self.value)

    _PUIT = 0
    _EMETTEUR = 1
    _EMETTEUR_RECEPTEUR = 2

