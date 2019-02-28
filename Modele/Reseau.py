

class Reseau:
    """
        class Reseau

        Représente un réseau. Contient le nombre de capteurs dans le réseau et le graphe qui le modélise

    """
    def __init__(self, _nbr_noeuds=0, _graphe=None):
        """
            Constructeur de la classe

            :param _nbr_noeuds : entier
            :param _graphe : Graphe Networkx

        """
        self.R_nbr_noeuds = _nbr_noeuds
        self.R_graphe = _graphe
        self.R_ensemble_dominant = None

    def RensembleFeuilles(self):
        """
        Liste les noeuds qui sont rattachés à l'ensemble dominant, cad les noeuds dont le rôle est simple émetteur

        :return Liste d'entier : liste des noeuds qui n'appartiennent pas à l'ensemble dominant
        """
        _feuilles = []
        for _noeud in self.R_graphe.nodes():
            if _noeud not in self.R_ensemble_dominant:
                _feuilles.append(_noeud)
        return _feuilles
