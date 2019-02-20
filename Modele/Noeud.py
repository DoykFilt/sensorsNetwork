

class Noeud:
    """
        class Noeud

        Classe qui regroupe les éléments communs entre les capteurs et les puits.
        Utilisé principalement pour faire le lien entre l'importation/exportation en XML et l'objet graphe networkX

    """

    def __init__(self, _pos, _role, _route):
        """
            Constructeur de la classe

            :param _pos : tuple de float (x, y)
            :param _role : Enum Role

        """
        self.N_pos = _pos
        self.N_role = _role
        self.N_route = _route
