"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Noeuds

    Possède la classe Noeud qui modélise un noeud d'un capteur
"""


class Noeud:
    """
        class Noeud

        Modélise un noeud d'un capteur

        :var self.N_pos : tuple de float (x, y)
        :var self.N_role : Enum Role
        :var self.N_route : int le numéro du noeud vers lequel envoyer les données
    """

    def __init__(self, _pos, _role, _route):
        """
            Constructeur de la classe

            :param _pos : tuple de float (x, y)
            :param _role : Enum Role
            :param _route : int le numéro du noeud vers lequel envoyer les données

        """
        self.N_pos = _pos
        self.N_role = _role
        self.N_route = _route
