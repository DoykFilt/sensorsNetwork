import datetime
import math
import random
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly
import networkx as nx
from plotly.utils import numpy

from Modele.Roles import Roles
from Modele.Signaux import Signaux
from Modele.Reseau import Reseau
from Vue.FenetreCreation import FenetreCreation


class Generateur:
    """
        class Generateur

        Classe qui regroupe les outils utiles pour la génération d'un réseau
        La plupart des méthodes sont déclarées statiques

    """

    def __init__(self, _connecteur):
        super(Generateur, self).__init__()
        self.G_connecteur = _connecteur

    def GobtenirConnecteur(self):
        """
        Renvoie le connecteur, permet d'agir à l'extérieur de la classe aux émissions de l'intérieur

        :return Le connecteur pyqtSignal
        """
        return self.G_connecteur

    def GcreerReseau(self, _params):
        """
        Permet de généré un réseau qui respectent les prérequis de l'application

        :param Objet Parametres

        :return Objet Reseau

        """

        self.G_connecteur.emit(Signaux._INITIALISATION_CREATION_GRAPHE, 0,
                               "Initialisation de la création du réseau..", -1)

        _reseau = Reseau()
        _reseau.R_nbr_noeuds = _params.P_nbr_capteurs

        # Génération des positions des capteurs
        self.G_connecteur.emit(Signaux._AVANCEE_CREATION_GRAPHE, 5, "Génération des positions initiales..", -1)
        _pos = Generateur.__GgenererPositions(_params.P_nbr_capteurs,
                                              _params.P_max_size,
                                              _params.P_marge,
                                              _params.P_min_distance)
        self.G_connecteur.emit(Signaux._AVANCEE_CREATION_GRAPHE, 10, "Positions générées", -1)

        # Création du graphe
        self.G_connecteur.emit(Signaux._AVANCEE_CREATION_GRAPHE, 10, "Génération de la topologie du réseau..", -1)
        _graphe = Generateur.__GgenerationReseau(_params.P_nbr_capteurs, _pos, _params.P_max_distance)
        self.G_connecteur.emit(Signaux._AVANCEE_CREATION_GRAPHE, 15, "Topologie générée..", -1)

        # Réagencement du graphe en un graphe connexe
        _reseau.R_graphe = Generateur.Gconnexeur(_graphe, _params.P_max_distance, self.G_connecteur)

        # Assignation des paramètres
        self.G_connecteur.emit(Signaux._AVANCEE_CREATION_GRAPHE, 100, "Mise en place des paramètres réseaux..", -1)
        _reseau.R_graphe = self.__GparametrageReseau(_reseau.R_graphe, _params)

        from Moteur.Simulateur import Simulateur
        Simulateur.SconfigurationTopologique(_reseau)

        self.G_connecteur.emit(Signaux._FIN_CREATION_GRAPHE, 0, "Réseau généré !", 0)

        return _reseau

    @staticmethod
    def __GparametrageReseau(_graphe, _params):
        """
        Permet de placer les paramètres de rôle et niveau de batterie dans les noeuds.
        Le premier noeud correspond au puit

        :param Objet Parametres, Graphe networkX

        :return Graphe networkX

        """

        # Paramètre rôle : Puit, Emetteur/Recepteur, Emetteur
        _roles = {i: Roles._EMETTEUR_RECEPTEUR for i in range(0, _params.P_nbr_capteurs)}
        _roles[0] = Roles._PUIT
        # Niveau initiale de batterie
        _batterie = {i: _params.P_capacitees_batteries for i in range(0, _params.P_nbr_capteurs)}
        _batterie[0] = -1
        # Si les arcs appartiennent à l'ensemble dominant
        _dominant = {e: {"dominant": Roles._ARC_NON_DOMINANT} for e in _graphe.edges()}

        nx.set_node_attributes(_graphe, _roles, "role")
        nx.set_node_attributes(_graphe, _batterie, "batterie")
        nx.set_edge_attributes(_graphe, _dominant)

        return _graphe

    @staticmethod
    def __GgenererPositions(_nbr_noeuds, _max_size, _marge, _min_distance):
        """
        Fonction qui génèe les positions des noeuds afin qu'ils soient mieux reparti
        Elle découpe en aires rectangulaires les surfaces non occupées par les noeuds en prenant en compte la distance
        minimum

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
            # Pour commencer on récupère l'aire dont sa valeur est la plus grande
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
    def __GafficherPositions(_pos, _max_size, _min_distance):
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
    def Gconnexeur(_graphe, _max_distance, _connecteur=None):
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

        # Récupère les sous-graphes, _count les dénombre
        _subgraphs_generator = nx.connected_component_subgraphs(_graphe, copy=True)
        _count = 0
        _subgraphs = []
        for _subgraph in _subgraphs_generator:
            _subgraphs.append(_subgraph)
            _count += 1

        _avancement = 15
        _pas = 0
        if _connecteur is not None:
            _connecteur.emit(Signaux._INFORMATION_CREATION_GRAPHE, 0, "Nombre de sous-graphes : " + str(_count - 1), -1)
            _pas = (100 - _avancement) / _count

        # variables pour l'estimation du temps restant. On mesure d'abord le temps pour un réagencement puis on le
        # multiplie par le nombre de réagencement à effectuer (cad le nombre de sous-graphes restants
        _timer_start = datetime.datetime.now()
        _timer_stop = datetime.datetime.now()
        _temps = 0
        _estimation = -1

        # Boucle tant qu'il n'y a encore des sous-graphes
        while _count > 1:

            _timer_start = datetime.datetime.now()

            if _connecteur is not None:
                if _estimation == -1:
                    _connecteur.emit(Signaux._INFORMATION_CREATION_GRAPHE, 0,
                                     "Reagencement de la topologie du réseau afin qu'il soit connexe",
                                     (_timer_stop - _timer_start).total_seconds())
                else:
                    _connecteur.emit(Signaux._INFORMATION_CREATION_GRAPHE, 0,
                                     "Reagencement de la topologie du réseau afin qu'il soit connexe",
                                     _estimation.total_seconds())
            # Récupération du plus grand sous graphe
            _sub_graph_plus_grand = _subgraphs[0]
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
            _graphe = Generateur.__GgenerationReseau(_nbr_noeuds_graphe, _pos, _max_distance)

            _subgraphs_generator = nx.connected_component_subgraphs(_graphe, copy=True)
            _count = 0
            _subgraphs = []
            for _subgraph in _subgraphs_generator:
                _subgraphs.append(_subgraph)
                _count += 1

            if _connecteur is not None:

                _timer_stop = datetime.datetime.now()
                _temps = _timer_stop - _timer_start
                if _estimation == -1 or _temps * (_count - 1) < _estimation:
                    _estimation = _temps * (_count - 1)

                _avancement += _pas
                _connecteur.emit(Signaux._AVANCEE_CREATION_GRAPHE, _avancement,
                                 "Nombre de sous-graphes : " + str(_count - 1), _estimation.total_seconds())
                _pas = (100 - _avancement) / _count

        return _graphe

    @staticmethod
    def __GgenerationReseau(_nbr_noeuds, _pos, _max_distance):

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

    @staticmethod
    def GcreerReseauAvecCapteursEtArcs(_capteurs, _arcs):
        """
        Génère un réseau à partir d'une liste de capteurs et d'arcs

        :param _capteurs : liste d'objets de type Noeud
        :param _arcs : liste de tuples (arc1, arc2)

        :return Un graphe networkX
        """

        _nbr_noeuds_graphe = 0
        _graphe = nx.Graph()
        for _count in range(0, len(_capteurs)):
            if _capteurs[_count].N_role == Roles._PUIT:
                _graphe.add_node(_count,
                                 pos=_capteurs[_count].N_pos,
                                 batterie=-1,
                                 role=_capteurs[_count].N_role,
                                 route=_count)
            else:
                _graphe.add_node(_count,
                                 pos=_capteurs[_count].N_pos,
                                 batterie=_capteurs[_count].C_vie_batterie,
                                 role=_capteurs[_count].N_role,
                                 route=_capteurs[_count].N_route)
            _nbr_noeuds_graphe += 1

        for _arc in _arcs:
            _graphe.add_edge(_arc.A_noeud1,
                             _arc.A_noeud2,
                             dominant=_arc.A_dominant)
        return Reseau(_nbr_noeuds_graphe, _graphe)

    @staticmethod
    def GgenerationHTML(_reseau):
        """
        Génère l'html de l'affichage à partir d'un réseau

        Algorithme tiré de l'exemple : https://plot.ly/python/network-graphs/

        :param _reseau : Objet de type Reseau

        :return l'HTML dans une chaîne de caractère
        """

        from Moteur.Simulateur import Simulateur
        _simulateur = Simulateur(None)
        _, _ensemble_deconnecte = _simulateur.SfinDeVieAtteinte(_reseau)

        colors = []
        colors_dominant = []
        for _edge in _reseau.R_graphe.edges():
            if _edge in _reseau.R_ensemble_dominant.edges():
                if _edge[0] in _ensemble_deconnecte or _edge[1] in _ensemble_deconnecte:
                    colors_dominant.append("black")
                else:
                    colors_dominant.append("red")
            else:
                if _edge[0] in _ensemble_deconnecte or _edge[1] in _ensemble_deconnecte:
                    colors.append("gray")
                else:
                    colors.append("#A9D0F5")
        _arcs = []
        _arcs_dominants = []
        for _arc in _reseau.R_graphe.edges():
            if _arc in _reseau.R_ensemble_dominant.edges():
                _arcs_dominants.append(_arc)
            else:
                _arcs.append(_arc)

        edge_trace = [dict(
            type='scatter',
            x=[_reseau.R_graphe.node[edge[0]]['pos'][0], _reseau.R_graphe.node[edge[1]]['pos'][0]],
            y=[_reseau.R_graphe.node[edge[0]]['pos'][1], _reseau.R_graphe.node[edge[1]]['pos'][1]],
            mode='lines',
            line=dict(width=2, color=colors[c]))
            for c, edge in enumerate(_arcs)]

        edge_trace_dominant = [dict(
            type='scatter',
            x=[_reseau.R_graphe.node[edge[0]]['pos'][0], _reseau.R_graphe.node[edge[1]]['pos'][0]],
            y=[_reseau.R_graphe.node[edge[0]]['pos'][1], _reseau.R_graphe.node[edge[1]]['pos'][1]],
            mode='lines',
            line=dict(width=2, color=colors_dominant[c]))
            for c, edge in enumerate(_arcs_dominants)]

        _nodes_pos = []
        _nodes_pos_dominant = []
        _nodes_pos_deconnectes = []
        for _noeud in _reseau.R_graphe.nodes():
            if _noeud in _ensemble_deconnecte:
                _nodes_pos_deconnectes.append([_reseau.R_graphe.node[_noeud]['pos'][0],
                                               _reseau.R_graphe.node[_noeud]['pos'][1]])
            elif _noeud in _reseau.R_ensemble_dominant.nodes():
                _nodes_pos_dominant.append([_reseau.R_graphe.node[_noeud]['pos'][0],
                                            _reseau.R_graphe.node[_noeud]['pos'][1]])
            else:
                _nodes_pos.append([_reseau.R_graphe.node[_noeud]['pos'][0], _reseau.R_graphe.node[_noeud]['pos'][1]])
        _nodes_pos = numpy.array(_nodes_pos)
        _nodes_pos_dominant = numpy.array(_nodes_pos_dominant)
        _nodes_pos_deconnectes = numpy.array(_nodes_pos_deconnectes)

        _x, _y = [], []
        for _pos in _nodes_pos:
            _x.append(_pos[0])
            _y.append(_pos[1])
        node_trace = dict(type='scatter',
                          x=_x,
                          y=_y,
                          hoverinfo='text',
                          text=[],
                          mode='markers',
                          marker=dict(
                              showscale=True,
                              cmax=FenetreCreation.FCobtenirCapaciteMaxBatterie(),
                              cmin=0,
                              # colorscale options
                              # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                              # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                              # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                              colorscale='Reds',
                              reversescale=True,
                              color=[],
                              size=10,
                              colorbar=dict(
                                  thickness=15,
                                  title='Niveau de la batterie',
                                  xanchor='left',
                                  titleside='right'
                              )))

        _x, _y = [], []
        for _pos in _nodes_pos_dominant:
            _x.append(_pos[0])
            _y.append(_pos[1])
        node_trace_dominant = dict(type='scatter',
                                   x=_nodes_pos_dominant[:, 0],
                                   y=_nodes_pos_dominant[:, 1],
                                   hoverinfo='text',
                                   text=[],
                                   mode='markers',
                                   marker=dict(
                                       showscale=False,
                                       cmax=FenetreCreation.FCobtenirCapaciteMaxBatterie(),
                                       cmin=0,
                                       # colorscale options
                                       # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                                       # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                                       # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                                       colorscale='Reds',
                                       reversescale=True,
                                       color=[],
                                       size=10,
                                       colorbar=dict(
                                           thickness=15,
                                           title='Niveau de la batterie',
                                           xanchor='left',
                                           titleside='right'
                                       ),
                                       line=dict(width=2, color="red")))

        _x, _y = [], []
        for _pos in _nodes_pos_deconnectes:
            _x.append(_pos[0])
            _y.append(_pos[1])
        if len(_nodes_pos_deconnectes) > 0:
            node_trace_deconnecte = dict(type='scatter',
                                         x=_nodes_pos_deconnectes[:, 0],
                                         y=_nodes_pos_deconnectes[:, 1],
                                         hoverinfo='text',
                                         text=[],
                                         mode='markers',
                                         marker=dict(
                                             showscale=False,
                                             # colorscale options
                                             # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                                             # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                                             # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                                             colorscale='Reds',
                                             reversescale=True,
                                             color=[],
                                             size=10,
                                             line=dict(width=0)))
        else:
            node_trace_deconnecte = []

        if len(_nodes_pos) == 0:
            node_trace_dominant["marker"]["showscale"] = True

        # Ajout des informations pour l'affichage d'informations supplémentaires :
        #   - couleur des noeuds en fonction de leur niveau d'énergie
        #   - information des noeuds au passage de la souris
        for node, adjacencies in enumerate(_reseau.R_graphe.adjacency()):
            # Le puit est dessiné en violet et les capteurs en nuance de couleur en fonction du niveau de leur batterie
            # Sont affichés au passage de la souris :
            #   - Le rôle du noeud (puit, émetteur/récepteur, émetteur)
            #   - l'énergie restante (si ce n'est pas un puit)
            #   - le nombre de capteurs adjacent

            node_info = "Capteur n°" + str(node) + " | Emetteur/Récepteur | " + \
                        "Energie restante : " + str(_reseau.R_graphe.node[node]['batterie']) + " | " + \
                        "Routage : " + str(_reseau.R_graphe.node[node]['route'])

            if node in _ensemble_deconnecte:
                if _reseau.R_graphe.nodes()[node]['batterie'] > 0:
                    node_trace_deconnecte['marker']['color'] += tuple(['gray'])
                else:
                    node_trace_deconnecte['marker']['color'] += tuple(['black'])
                node_trace_deconnecte['text'] += tuple([node_info])
            elif node in _reseau.R_ensemble_dominant:
                if _reseau.R_graphe.node[node]['role'] == Roles._PUIT:
                    node_trace_dominant['marker']['color'] += tuple(['purple'])
                    node_info = "Puit | " + str(len(adjacencies[1])) + " capteurs adjacents"
                else:
                    node_trace_dominant['marker']['color'] += tuple([_reseau.R_graphe.node[node]['batterie']])
                node_trace_dominant['text'] += tuple([node_info])
            else:
                node_trace['marker']['color'] += tuple([_reseau.R_graphe.node[node]['batterie']])
                node_trace['text'] += tuple([node_info])

        if len(_nodes_pos_deconnectes) > 0:
            _datas = edge_trace + [node_trace] + edge_trace_dominant + [node_trace_deconnecte] + [node_trace_dominant]
        else:
            _datas = edge_trace + [node_trace] + edge_trace_dominant + [node_trace_dominant]

        # La création de la figure finale à afficher
        fig = go.Figure(data=_datas,
                        layout=go.Layout(
                            title='',
                            titlefont=dict(size=16),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        # Finalement génération du html
        html = plotly.offline.plot(fig, auto_open=False, output_type='div')
        return """<html><head><meta charset="utf-8" /></head><body><script type="text/javascript">window.PlotlyConfig = 
                    {MathJaxConfig: 'local'};</script>""" \
               + html \
               + """<script type="text/javascript">window.addEventListener("resize", function(){Plotly.Plots.resize(docu
                    ment.getElementById("611e9c72-ed73-4e6f-b171-1737e84f4735"));});</script></body></html>"""
