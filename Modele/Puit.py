from Modele.Noeud import Noeud
from Modele.Roles import Roles


class Puit(Noeud):
    """
        class Puit

        Hérite de Noeud, élément de base d'un graphe

        Classe qui represente un puit, élément du réseau. Utilisé principalement pour faire le lien entre
        l'importation/exportation en XML et l'objet graphe networkX

    """
    def __init__(self, _pos):
        """
            Constructeur de la classe

            :param _pos : tuple de float (x, y)

        """
        super().__init__(_pos, Roles._PUIT, -1)

