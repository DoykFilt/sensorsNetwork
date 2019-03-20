"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Arc

    Possède la classe Arc qui modélise l'arc d'un graphe
"""


class Arc:
    """
        class Arc

        Modélise l'arc d'un graphe

        :var self.A_noeud1 : int, le premier noeud du graphe
        :var self.A_noeud2 : int, le second noeud du graphe
        :var self.A_dominant : Enum Roles, _ARC_DOMINANT si l'arc appartient à l'ensemble dominant _ARC_NON_DOMINANT sinon
    """

    def __init__(self, _noeud1, _noeud2, _dominant):
        """
            Constructeur de la classe

            :param _noeud1 : int, le premier noeud du graphe
            :param _noeud2 : int, le second noeud du graphe
            :param _dominant : Enum Roles, _ARC_DOMINANT si l'arc appartient à l'ensemble dominant _ARC_NON_DOMINANT sinon

        """
        self.A_noeud1 = _noeud1
        self.A_noeud2 = _noeud2
        self.A_dominant = _dominant
