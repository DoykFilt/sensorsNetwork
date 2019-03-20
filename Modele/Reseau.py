"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Reseau

    Possède la classe Reseau qui regroupe les informations nécessaires pour modéliser un réseau
"""
from Utilitaires.Log import Log


_log = Log()


class Reseau:
    """
        class Reseau

        Regroupe les informations nécessaires pour modéliser un réseau

        :var self.R_nbr_noeuds : int, le nombre de noeuds contenus dans le réseau
        :var self.R_graphe : Graphe NetworkX, le graphe modélisant le réseau
        :var self.R_ensemble_dominant : Graphe Networkx, l'ensemble dominant du graphe R_graphe
        :var self.R_capacite_batterie_max : int, la capacité maximale des batteries des capteurs.
    """

    def __init__(self, _nbr_noeuds=0, _graphe=None):
        """
            Constructeur de la classe

            :param _nbr_noeuds : int, le nombre de noeuds contenus dans le réseau
            :param _graphe : Graphe Networkx, le graphe modélisant le réseau

        """
        _log.Linfo("Init -- Reseau")

        self.R_nbr_noeuds = _nbr_noeuds
        self.R_graphe = _graphe
        self.R_ensemble_dominant = None
        self.R_capacite_batterie_max = 0

    def RensembleFeuilles(self):
        """
        Liste les noeuds qui sont rattachés à l'ensemble dominant, cad les noeuds dont le rôle est simple émetteur

        :return Liste d'entier : liste des noeuds qui n'appartiennent pas à l'ensemble dominant
        """
        _log.Linfo("Début ## Reseau.RensembleFeuilles")

        _feuilles = []
        for _noeud in self.R_graphe.nodes():
            if _noeud not in self.R_ensemble_dominant:
                _feuilles.append(_noeud)
        return _feuilles
