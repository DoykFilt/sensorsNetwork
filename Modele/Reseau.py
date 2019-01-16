import networkx as nx
import math
import random
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

# TODO : Ajouter la notion d'énergie et de puit


class Reseau:
    def __init__(self, _nbr_capteurs, _max_size, _marge, _max_distance, _min_distance):
        """
        Initialisateur de la classe Reseau, génère un réseau connexe

        :param _nbr_capteurs : le nombre de capteurs à placer
        :param _max_size : la taille de la surface carrée à occuper
        :param _marge : la marge à respecter entre le bord de la surface et les noeuds
        :param _max_distance : la distance pour que deux capteurs soient connectés
        :param _min_distance : la distance indicative à ne pas dépasser entre deux capteurs

        :exception _min_distancedoit être inférieure ou égale à la distance maximale
        :exception _max_distance doit être supérieur à 10
        :exception _marge doit être inférieure à la moitiée de la taille maximale
        :exception _nbr_capteurs doit être supérieur à 1

        """
        if _min_distance > _max_distance:
            raise ValueError("La distance minimum doit être inférieure ou égale à la distance maximale")
        if _max_size < 10:
            raise ValueError("La taille maximale doit être supérieur à 10")
        if _marge > _max_size / 2:
            raise ValueError("La marge doit être inférieure à la moitiée de la taille maximale")
        if _nbr_capteurs < 2:
            raise ValueError("Le nombre de capteurs doit être supérieur à 1")

        self.R_nbr_noeuds = _nbr_capteurs

        print("Génération du réseau...")

        # Génération des positions puis du graphe
        _pos = Reseau.RgenererPositions(_nbr_capteurs, _max_size, _marge, _min_distance)
        _graphe = Reseau.RgenerationReseau(_nbr_capteurs, _pos, _max_distance)
        # Réagencement le graphe en un graphe connexe
        self.R_graphe = Reseau.Rconnexeur(_graphe, _max_distance)

        print("Réseau Généré !")

    @staticmethod
    def RgenererPositions(_nbr_noeuds, _max_size, _marge, _min_distance):

        """
        Fonction qui génèe les positions des noeuds afin qu'ils soient mieux reparti
        Elle découpe en aires rectangulaires les surfaces non occupées par les noeuds en prenant en compte la distance minimum
        :param _max_size : la taille de la surface carrée à occuper
        :param _marge : la marge à respecter entre le bord de la surface et les noeuds
        :param _min_distance : la distance indicative à ne pas dépasser entre deux capteurs
        :param _nbr_noeuds : le nombre de noeuds à placer

        :return un dictionnaire des positions des noeuds. exe : {1:(2.5, 3.0), 2:(5.6, 3.1)}
        """
        # L'ensemble d'aires où les noeuds peuvent être placer. Au début contient juste la surface maximale
        _aires_libres = [[(_marge, _marge), (_max_size - _marge, _max_size - _marge)]]
        _pos = {}

        for _noeud in range(0, _nbr_noeuds):
            # Pour commencer on récupère l'aire dont se valeur est la plus grande
            # Le numéro de l'aire dans laquelle le noeud sera placé
            _n_aire = 0
            _grande_valeur = (_aires_libres[0][1][0] - _aires_libres[0][0][0]) * \
                             (_aires_libres[0][1][1] - _aires_libres[0][0][1])
            for _index_aire in range(len(_aires_libres)):
                _valeur = (_aires_libres[_index_aire][1][0] - _aires_libres[_index_aire][0][0]) * \
                          (_aires_libres[_index_aire][1][1] - _aires_libres[_index_aire][0][1])
                if _valeur > _grande_valeur:
                    _grande_valeur = _valeur
                    _n_aire = _index_aire

            # Ensuite on génère aléatoirement les positions dans l'ai
            _pos_x = random.uniform(_aires_libres[_n_aire][0][0], _aires_libres[_n_aire][1][0])
            _pos_y = random.uniform(_aires_libres[_n_aire][0][1], _aires_libres[_n_aire][1][1])
            _pos[_noeud] = (_pos_x, _pos_y)

            # Puis on supprime l'aire du nouveau noeud pour essayer de respecter la distance minimum
            # Plus exactement, quand on pose un nouveau point, un nouveau quadrillage se fait :
            # l'ancien aire se décompose en 8 nouvelles aires qui entourent l'aire du point (représentée par un carré)
            # D'abord on extrait les composantes des coins de l'ancienne aire (a en bas à gauche, d en haut à gauche)
            # et celles de la nouvelle aire (b en bas à gauche, c en haut à droite
            _a = _aires_libres[_n_aire][0]
            _b = (_pos_x - _min_distance, _pos_y - _min_distance)
            if _b[0] < 0:
                _b = (_marge, _b[1])
            if _b[1] < 0:
                _b = (_b[0], _marge)
            _c = (_pos_x + _min_distance, _pos_y + _min_distance)
            if _c[0] > _max_size:
                _c = (_max_size - _marge, _c[1])
            if _c[1] > _max_size:
                _c = (_c[0], _max_size - _marge)
            _d = _aires_libres[_n_aire][1]
            # Ici on définit l'ensemble des nouvelles aires
            _nouvelles_aires = [
                [(_a[0], _c[1]), (_b[0], _d[1])],  # coin supérieur gauche
                [(_b[0], _c[1]), (_c[0], _d[1])],  # milieu supérieur
                [(_c[0], _c[1]), (_d[0], _d[1])],  # coin supérieur droit
                [(_a[0], _b[1]), (_b[0], _c[1])],  # gauche
                [(_c[0], _b[1]), (_d[0], _c[1])],  # droite
                [(_a[0], _a[1]), (_b[0], _b[1])],  # coin inférieur gauche
                [(_b[0], _a[1]), (_c[0], _b[1])],  # milieu inférieur
                [(_c[0], _a[1]), (_d[0], _b[1])]]  # coin inférieur droit
            # On supprime les aires nulles
            _temp = []
            for _aire in _nouvelles_aires:
                if _aire[1][0] - _aire[0][0] > 0 and _aire[1][1] - _aire[0][1] > 0:
                    _temp.append(_aire)
            _aires_libres.pop(_n_aire)
            _aires_libres.extend(_temp)

        # self.RafficherPositions(_pos, _max_size, _min_distance)
        return _pos

    @staticmethod
    def RafficherPositions(_pos, _max_size, _min_distance):

        """
        Fonction permet de visualiser sur une fenêtre matplotlib la disposition d'un nuage de point avec un cercle par
        point qui correspond à la distance minimum que doivent avoir les noeuds entre eux
        :param _pos : dictionnaire des positions des noeuds. exe : {1:(2.5, 3.0), 2:(5.6, 3.1)}
        :param _max_size : la taille de la surface carrée à occuper
        :param _min_distance : la distance indicative à ne pas dépasser entre deux capteurs
        """
        _list_x, _list_y = [], []
        _list = []
        ax = plt.gca(aspect='equal')
        ax.cla()
        ax.set_xlim((0, _max_size))
        ax.set_ylim((0, _max_size))
        # Affichage de le cercle autour du point, en rouge
        for _index in _pos:
            ax.add_artist(
                plt.Circle((_pos[_index][0], _pos[_index][1]), _min_distance, color=(0.5, 0.2, 0.2), fill=False))
        # Affichage du point en bleu
        for _index in _pos:
            ax.add_artist(plt.Circle((_pos[_index][0], _pos[_index][1]), _min_distance / 100, color=(0, 0, 1)))

        plt.show()

    @staticmethod
    def Rconnexeur(_graphe, _max_distance):
        """
            Connecte entre eux les sous-graphes sur multi-graphe passé en paramètre afin d'en créer un unique

        :param _graphe : le graphe networkX à traiter
        :param _max_distance : la distance pour que deux capteurs soient connectés

        :return le graphe connexe
        """

        # On récupère d'abord l'ensemble des positions sous la forme d'une dictionnaire
        _pos = {}
        _nbr_noeuds_graphe = 0
        for _node in _graphe:
            _pos[_node] = (_graphe.node[_node]['pos'])
            _nbr_noeuds_graphe += 1

        # Récupère les sous-graphes, _count les dénombe
        _subgraphs_generator = nx.connected_component_subgraphs(_graphe, copy=True)
        _count = 0
        _subgraphs = []
        for _subgraph in _subgraphs_generator:
            _subgraphs.append(_subgraph)
            _count += 1
        print("Nombre de sous-graphes : " + str(_count))

        # Boucle tant qu'il n'y a encore des sous-graphes
        while _count > 1:
            print("Réagencement de la topologie")
            # Récupération du plus grand sous graphe
            _sub_graph_plus_grand = _subgraphs[0]
            # _nbr_plus_grand = len(_subgraphs[0])
            # _sub_graph_plus_grand = _subgraphs[0]
            # for _subgraph in _subgraphs:
            #     if len(_subgraph) > _nbr_plus_grand:
            #         _nbr_plus_grand = len(_subgraph)
            #         _sub_graph_plus_grand = _subgraph
            # On le retire de la liste pour ne pas affecter les calculs suivants
            _subgraphs.remove(_sub_graph_plus_grand)

            # Calcul du centre de gravité g du plus grand graphe
            _x, _y = 0, 0
            _nbr_noeuds = 0
            for _node in _sub_graph_plus_grand.node:
                _x += _sub_graph_plus_grand.node[_node]['pos'][0]
                _y += _sub_graph_plus_grand.node[_node]['pos'][1]
                _nbr_noeuds += 1
            _g_x = _x / _nbr_noeuds
            _g_y = _y / _nbr_noeuds

            # Calcul de la distance entre chaque sous-graphe et le plus grand pour savoir lequel est le plus proche
            # On calcul d'abord ces valeur sur le premier sous-graphe pour avoir une référence
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
            # Puis on applique les calculs sur les autres graphes
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
            _distance_min = math.sqrt(
                math.pow(_g_x - _sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][0], 2) +
                math.pow(_g_y - _sub_graph_plus_pres.node[_noeuds_plus_proche_pres]['pos'][1], 2))
            for _node in _sub_graph_plus_pres.node:
                _distance = math.sqrt(math.pow(_g_x - _sub_graph_plus_pres.node[_node]['pos'][0], 2) +
                                      math.pow(_g_y - _sub_graph_plus_pres.node[_node]['pos'][1], 2))
                if _distance < _distance_min:
                    _distance_min = _distance
                    _noeuds_plus_proche_pres = _node

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
            _d = math.sqrt(_x ** 2 + _y ** 2)
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
            _graphe = Reseau.RgenerationReseau(_nbr_noeuds_graphe, _pos, _max_distance)

            _subgraphs_generator = nx.connected_component_subgraphs(_graphe, copy=True)
            _count = 0
            _subgraphs = []
            for _subgraph in _subgraphs_generator:
                _subgraphs.append(_subgraph)
                _count += 1

            print("Nombre de sous-graphes : " + str(_count - 1))
        return _graphe

    @staticmethod
    def RgenerationReseau(_nbr_noeuds, _pos, _max_distance):

        """
        Génère le réseau à partir d'une liste de positions des noeuds

        :param _nbr_noeuds : le nombre de noeuds du réseau
        :param _pos : dictionnaire des positions des noeuds. exe : {1:(2.5, 3.0), 2:(5.6, 3.1)}
        :param _max_distance : la distance pour que deux capteurs soient connectés

        :return Un graphe networkX
        """

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
        _weights = [0.5] * _nbr_noeuds
        return nx.geographical_threshold_graph(_nbr_noeuds,
                                               _teta,
                                               pos=_pos,
                                               dim=1,
                                               weight=_weights,
                                               p_dist=p_dist)

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

