

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
