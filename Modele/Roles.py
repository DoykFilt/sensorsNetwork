from enum import Enum


class Roles(Enum):

    def __str__(self):
        return str(self.value)

    _PUIT = 0
    _EMETTEUR = 1
    _EMETTEUR_RECEPTEUR = 2

