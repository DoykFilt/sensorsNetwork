import networkx as nx
import math
import random
from scipy.spatial import Delaunay

from Vue.FenetrePrincipale import FenetrePrincipale

# TODO : Écarter les noeuds d'une distance minimale lors de leur création
# TODO : Utiliser Delaunay seulement si il y a plus de deux noeuds

class Reseau:
    def __init__(self, _nbr_capteurs, _max_size, _marge, _max_distance, _min_distance):

        self.R_nbr_noeuds = _nbr_capteurs
        # Calcul aléatoire des positions (x, y) de chaque point.
        # Les positions sont comprises entre 0 et la taille maximale et en enlevant la marge de chaque côté
        _pos = [(random.uniform(_marge, _max_size - _marge), random.uniform(_marge, _max_size - _marge))
                for i in range(self.R_nbr_noeuds)]
        # L'algorithme de Delaunay permet de mieux répartir les points sur la surface (méthode de triangulisation)
        _pos_triees = Delaunay(_pos)
        # _ = delaunay_plot_2d(_pos_triees)
        # plt.show()
        _pos = {i: (_pos_triees.points[i][0], _pos_triees.points[i][1]) for i in range(self.R_nbr_noeuds)}

        # Fonction utilisée lors de la génération du graphe, permet de définir si un arc doit être créer entre deux
        # noeuds en fonction de la distance entre eux passée en paramètre
        def p_dist(_r):
            if _max_distance >= _r:
                return 1
            else:
                return -1

        # Génération du réseau. Un arc est créé entre deux noeuds a et b si :
        # (weight(a) + weight(b)) * p_dist(r) >= teta
        # On prend teta = 1 et weight(x) = 0.5 pour influencer le choix seulement en fonction de la distance
        _teta = 1
        _weights = [0.5] * self.R_nbr_noeuds
        self.R_graphe = nx.geographical_threshold_graph(self.R_nbr_noeuds,
                                                        _teta,
                                                        pos=_pos,
                                                        dim=1,
                                                        weight=_weights,
                                                        p_dist=p_dist)

        FPFenetrePrincipale = FenetrePrincipale()
        FPFenetrePrincipale.FPafficherReseau(self, "Disconnected")

        """ 
            Une fois notre premier réseau de créé, on va l'ajuster pour qu'il soit convexe.
            Pour cela on récupère les sous-graphe, on récupère le plus grand et le plus proche de celui-ci
            On calcule la distance entre les deux capteurs les plus proches puis on déplace le proche vers le grand
            Les arcs sont recalculés et on réitère jusqu'à ce que le graphe est connexe
        """
        _subgraphs_generator = nx.connected_component_subgraphs(self.R_graphe, copy=True)
        _count = 0
        _subgraphs = []
        for _subgraph in _subgraphs_generator:
            _subgraphs.append(_subgraph)
            _count += 1
        print("Nombre de sous-graphes : " + str(_count))
        while _count > 1:
            print("Réagencement de la topologie")
            # Récupération du plus grand sous graphe et du plus petit
            _nbr_plus_grand = len(_subgraphs[0])
            _sub_graph_plus_grand = _subgraphs[0]
            for _subgraph in _subgraphs:
                if len(_subgraph) > _nbr_plus_grand:
                    _nbr_plus_grand = len(_subgraph)
                    _sub_graph_plus_grand = _subgraph

            _subgraphs.remove(_sub_graph_plus_grand)

            # Calcul du centre de gravité g du plus grand
            _x, _y = 0, 0
            _nbr_noeuds = 0
            for _node in _sub_graph_plus_grand.node:
                _x += _sub_graph_plus_grand.node[_node]['pos'][0]
                _y += _sub_graph_plus_grand.node[_node]['pos'][1]
                _nbr_noeuds += 1
            _g_x = _x / _nbr_noeuds
            _g_y = _y / _nbr_noeuds

            # Calcul de la distance entre chaque sous-graphe et le plus grand pour savoir lequel est le plus proche
            # Sur le premier pour avoir une référence..
            _x, _y = 0, 0
            _nbr_noeuds = 0
            for _node in _subgraphs[0].node:
                _x += _subgraphs[0].node[_node]['pos'][0]
                _y += _subgraphs[0].node[_node]['pos'][1]
                _nbr_noeuds += 1
            _g_proche_x = _x / _nbr_noeuds
            _g_proche_y = _y / _nbr_noeuds
            _distance_min = math.sqrt(math.pow(_g_x - _g_proche_x, 2) + math.pow(_g_y - _g_proche_y, 2))
            _sub_graph_plus_pres = _subgraphs[0]
            # Puis les autres
            for _subgraph in _subgraphs:
                _x, _y = 0, 0
                _nbr_noeuds = 0
                for _node in _subgraph.node:
                    _x += _subgraph.node[_node]['pos'][0]
                    _y += _subgraph.node[_node]['pos'][1]
                    _nbr_noeuds += 1
                _distance = math.sqrt(math.pow(_g_x - _x / _nbr_noeuds, 2) +
                                      math.pow(_g_y - _y / _nbr_noeuds, 2))
                if _distance < _distance_min:
                    _distance_min = _distance
                    _sub_graph_plus_pres = _subgraph

            # Récupération de la position du noeud le plus proche de g dans le sous-graphe le plus proche
            _noeuds_plus_proche_pres = list(_sub_graph_plus_pres)[0]
            _distance_min = math.sqrt(math.pow(_g_x - _sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][0], 2) +
                                      math.pow(_g_y - _sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][1], 2))
            for _node in _sub_graph_plus_pres.node:
                _distance = math.sqrt(math.pow(_g_x - _sub_graph_plus_pres.node[_node]['pos'][0], 2) +
                                      math.pow(_g_y - _sub_graph_plus_pres.node[_node]['pos'][1], 2))
                if _distance < _distance_min:
                    _distance_min = _distance
                    _noeuds_plus_proche_pres = _node
            # _distance_finale = _distance_min
            # Récupération de la position du noeud du grand sous-graphe le plus proche du second sous-graphe
            _noeuds_plus_proche_grand = list(_sub_graph_plus_grand)[0]
            _distance_min = math.sqrt(
                    math.pow(_sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][0] -
                             _sub_graph_plus_grand.node[_noeuds_plus_proche_grand]['pos'][0], 2) +
                    math.pow(_sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][1] -
                             _sub_graph_plus_grand.node[_noeuds_plus_proche_grand]['pos'][1], 2)
                )
            for _node in _sub_graph_plus_grand.node:
                _distance = math.sqrt(
                        math.pow(_sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][0] -
                                 _sub_graph_plus_grand.node[_node]['pos'][0], 2) +
                        math.pow(_sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][1] -
                                 _sub_graph_plus_grand.node[_node]['pos'][1], 2)
                    )
                if _distance < _distance_min:
                    _distance_min = _distance
                    _noeuds_plus_proche_grand = _node

            # On calcule le vecteur entre les deux points les plus proches pour pouvoir l'appliquer sur
            # les autres points du petit
            _vecteur = (_sub_graph_plus_grand.node[_noeuds_plus_proche_grand]['pos'][0] -
                        _sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][0],
                        _sub_graph_plus_grand.node[_noeuds_plus_proche_grand]['pos'][1] -
                        _sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][1])

            # Avant d'effectuer le déplacement on calcule la distance à enlever pour que le nouveau noeud respecte
            # la distance maximale pour une connexion, noté m (réduit de 50% pour avoir des chances de créer d'autres
            # liens avec des noeuds voisins)
            # Pour cela on considère notre vecteur et ses composantes x et y. On a d la longueur du vecteur, d² = x² +y²
            # On veut x' et y' telles que (d - m)² = x'² + y'²
            # Pour celà on applique le théorème de Thalès
            _m = _max_distance * 0.5
            _x = _vecteur[0]
            _y = _vecteur[1]
            _d = math.sqrt(_x**2 + _y**2)
            _x2 = (_d - _m) * _x / _d
            _y2 = (_d - _m) * _y / _d
            _vecteur = (_x2, _y2)

            # Ensuite on déplace le petit vers le grand (directement les positions du graphe complet)
            for _node in _sub_graph_plus_pres.nodes():
                _x = _pos[_node][0]
                _y = _pos[_node][1]
                _pos[_node] = (_x + _vecteur[0],
                               _y + _vecteur[1])

            # Finalement Recalcule du graphe et de ses sous-graphes
            self.R_graphe = nx.geographical_threshold_graph(self.R_nbr_noeuds,
                                                            _teta,
                                                            pos=_pos,
                                                            dim=1,
                                                            weight=_weights,
                                                            p_dist=p_dist)

            _subgraphs_generator = nx.connected_component_subgraphs(self.R_graphe, copy=True)
            _count = 0
            _subgraphs = []
            for _subgraph in _subgraphs_generator:
                _subgraphs.append(_subgraph)
                _count += 1

            print("Nombre de sous-graphes : " + str(_count - 1))
        print("Réseau Généré")



    @property
    def R_nbr_noeuds(self):
        return self.__R_nbr_noeuds

    @R_nbr_noeuds.setter
    def R_nbr_noeuds(self, _nbr_noeuds):
        self.__R_nbr_noeuds = _nbr_noeuds

    @property
    def R_graphe(self):
        return self.__R_graphe

    @R_graphe.setter
    def R_graphe(self, _graphe):
        self.__R_graphe = _graphe