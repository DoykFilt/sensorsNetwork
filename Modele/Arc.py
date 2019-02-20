

class Arc:
    """
        class Arc

        Classe qui correspond à un lien entre deux noeuds
        Utilisé principalement pour faire le lien entre l'importation/exportation en XML et l'objet graphe networkX

    """

    def __init__(self, _noeud1, _noeud2, _dominant):
        """
            Constructeur de la classe

            :param _noeud1 : entier
            :param _noeud2 : entier
            :param _dominant : Enum Roles

        """
        self.A_noeud1 = _noeud1
        self.A_noeud2 = _noeud2
        self.A_dominant = _dominant
