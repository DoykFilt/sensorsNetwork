from Modele.Noeud import Noeud


class Capteur(Noeud):
    """
        class Capteur

        Hérite de Noeud, élément de base d'un graphe

        Classe qui represente un capteur, élément du réseau. Utilisé principalement pour faire le lien entre
        l'importation/exportation en XML et l'objet graphe networkX

    """

    def __init__(self, _pos, _vie_batterie, _role, _route):
        """
            Constructeur de la classe

            :param _pos : tuple de float (x, y)
            :param _role : Enum Roles
            :param _vie_batterie : float
            :param _route : int, le noeud vers lequel envoyer les données
        """

        super().__init__(_pos, _role, _route)
        self.C_vie_batterie = _vie_batterie
