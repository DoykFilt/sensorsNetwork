import networkx as nx
import math
from networkx.algorithms.approximation import dominating_set
from networkx.algorithms.shortest_paths.generic import shortest_path

from Modele.Roles import Roles
from Modele.Signaux import Signaux
from Utilitaires.FileManager import FileManager


class Simulateur:
    S_intervalle_recolte = 1
    S_intervalle_roulement = 0
    S_unite_consommation_emission = 5
    S_unite_consommation_reception = 5
    S_unite_consommation_recolte = 1
    S_duree_de_vie = 0
    S_fin_de_vie = 0.8

    def __init__(self, _connecteur):
        super(Simulateur, self).__init__()
        self.S_connecteur = _connecteur

    def SlancerSimulation(self, _reseau):

        _file_manager = FileManager()

        # Sprint 2 : correspond à l'équivalent pour un cycle
        self.__SdeterminationIntervalleTemps()

        _etat, _total = 0, 0
        _reseau = self.SconfigurationTopologique(_reseau)

        _fin_de_vie_atteinte, _e = self.SfinDeVieAtteinte(_reseau)
        self.S_duree_de_vie = 0

        while not _fin_de_vie_atteinte:
            _reseau = self.__SsimulationSurUnRoulement(_reseau)

            _etat, _total = _file_manager.FMenregistrerEtat(_reseau)

            _fin_de_vie_atteinte, _e = self.SfinDeVieAtteinte(_reseau)

        from Controleur.Statistiques import Statistiques
        _statistiques = Statistiques()
        _statistiques.SajouterResultat(self.S_intervalle_roulement, self.S_duree_de_vie)

        self.S_connecteur.emit(Signaux._NOUVEL_ETAT, dict({"etat": _etat, "total": _total}))
        return _reseau

    def __SdeterminationIntervalleTemps(self):
        self.S_intervalle_roulement = 0

    @staticmethod
    def SconfigurationTopologique(_reseau):
        # Déyermination des rôles des capteurs en prenant en compte uniquement l'ensemble dominant
        # TODO Sprint 3 : Prendre en compte le niveau restant de la batterie

        _ensemble_dominant = Simulateur.SdeterminationEnsembleDominant(_reseau)
        _reseau.R_ensemble_dominant = _ensemble_dominant
        # Tous les noeuds de l'ensemble dominant prennent le rôle de Recepteur/Emetteur
        # Les autres prennent le rôle d'Émetteur
        for _noeud in _reseau.R_graphe:
            if _reseau.R_graphe.nodes[_noeud]['role'] != Roles._PUIT:
                if _noeud in _ensemble_dominant.nodes:
                    _reseau.R_graphe.nodes[_noeud]['role'] = Roles._EMETTEUR_RECEPTEUR
                else:
                    _reseau.R_graphe.nodes[_noeud]['role'] = Roles._EMETTEUR
        # Les arcs appartenant à l'arbre dominant sont indiqués comme tel
        for _arc in _reseau.R_graphe.edges:
            if _arc in _ensemble_dominant.edges:
                _reseau.R_graphe.edges[_arc]['dominant'] = Roles._ARC_DOMINANT
            else:
                _reseau.R_graphe.edges[_arc]['dominant'] = Roles._ARC_NON_DOMINANT

        # Finalement on rempli les informations de routage dans chaque noeud
        Simulateur.__SdeterminationRoutage(_reseau, _ensemble_dominant)

        return _reseau

    @staticmethod
    def SdeterminationEnsembleDominant(_reseau):

        # Sélection des noeuds dominants
        _reseau = Simulateur.__SactualisationPoids(_reseau)
        _ensemble_dominant = dominating_set.min_weighted_dominating_set(
            _reseau.R_graphe,
            weight="poids_dominant"
        )

        # On ajoute les puits à l'ensemble dominant si ils n'y sont pas
        for _noeud in _reseau.R_graphe:
            if _reseau.R_graphe.node[_noeud]['role'] == Roles._PUIT:
                if _noeud not in _ensemble_dominant:
                    _ensemble_dominant.add(_noeud)

        # On créer un multigraphe intermédiaire en reprennant les arcs qui concercent les noeuds de l'ensemble dominant
        _noeuds_dominants = {}
        for _n in _ensemble_dominant:
            _noeuds_dominants[_n] = _reseau.R_graphe.node[_n]
        _arcs_dominants = []
        for _a in _reseau.R_graphe.edges():
            if _a[0] in _ensemble_dominant and _a[1] in _ensemble_dominant:
                _arcs_dominants.append(_a)
        _multigraphe = nx.Graph()
        _multigraphe.add_nodes_from(_noeuds_dominants)
        _multigraphe.add_edges_from(_arcs_dominants)

        _pos = {}
        for _n in _multigraphe.nodes():
            _pos[_n] = _reseau.R_graphe.node[_n]['pos']

        nx.set_node_attributes(_multigraphe, _pos, "pos")

        # On rend connexe le graphe en ajoutant dans l'ensemble dominant les noeuds sur le plus court chemin (avec le
        # niveau de la batterie comme poids) entre les deux noeuds les plus proches entre chaque sous-graphe

        # Récupère les sous-graphes, _count les dénombre
        _subgraphs_generator = nx.connected_component_subgraphs(_multigraphe, copy=True)
        _count = 0
        _subgraphs = []
        for _subgraph in _subgraphs_generator:
            _subgraphs.append(_subgraph)
            _count += 1

        while _count > 1:
            # -----------------------------------------------------------------------
            # On prend le premier sous-graphe et le sous-graphe le plus proche de lui
            # -----------------------------------------------------------------------
            _subgraph1 = _subgraphs[0]
            # caclcul du centre de gravité du premier
            _x, _y = 0, 0
            _nbr_noeuds = 0
            for _node in _subgraph1.node:
                _x += _subgraph1.node[_node]['pos'][0]
                _y += _subgraph1.node[_node]['pos'][1]
                _nbr_noeuds += 1
            _g_x = _x / _nbr_noeuds
            _g_y = _y / _nbr_noeuds
            _subgraphs.remove(_subgraph1)

            # puis comparaison avec tout les autres graphes
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
            # ----------------------------------------------------------------------------------------------------
            # Puis on les relit entre eux avec un algo du plus court chemin entre les deux points les plus proches
            # ----------------------------------------------------------------------------------------------------
            # Sélection des deux noeuds les plus proches entre eux
            _noeud_plus_proche_sub1 = None
            for _noeud in _subgraph1.node:
                _noeud_plus_proche_sub1 = _noeud
                break
            _noeud_plus_proche_sub2 = None
            for _noeud in _sub_graph_plus_pres.node:
                _noeud_plus_proche_sub2 = _noeud
                break
            _paire_la_plus_proche = (_noeud_plus_proche_sub1, _noeud_plus_proche_sub2)
            _distance_min = math.sqrt(math.pow(_subgraph1.node[_noeud_plus_proche_sub1]['pos'][0] -
                                               _sub_graph_plus_pres.node[_noeud_plus_proche_sub2]['pos'][0], 2) +
                                      math.pow(_subgraph1.node[_noeud_plus_proche_sub1]['pos'][1] -
                                               _sub_graph_plus_pres.node[_noeud_plus_proche_sub2]['pos'][1], 2))

            for _noeud1 in _subgraph1:
                for _noeud2 in _sub_graph_plus_pres:
                    _distance = math.sqrt(math.pow(_subgraph1.node[_noeud1]['pos'][0] -
                                                   _sub_graph_plus_pres.node[_noeud2]['pos'][0], 2) +
                                          math.pow(_subgraph1.node[_noeud1]['pos'][1] -
                                                   _sub_graph_plus_pres.node[_noeud2]['pos'][1], 2))
                    if _distance < _distance_min:
                        _distance_min = _distance
                        _paire_la_plus_proche = (_noeud1, _noeud2)
            # plus court chemin entre ces deux noeuds sur le graphe initiale

            _plus_court_chemin = shortest_path(_reseau.R_graphe,
                                               _paire_la_plus_proche[0], _paire_la_plus_proche[1],
                                               weight='poids_dominant')
            # On ajoute les nouveaux noeuds et arcs au multigraphe
            for _a in _reseau.R_graphe.edges():
                if (_a[0] in _plus_court_chemin and _a[1] in _plus_court_chemin) or \
                        (_a[0] in _plus_court_chemin and _a[1] in _noeuds_dominants) or \
                        (_a[0] in _noeuds_dominants and _a[1] in _plus_court_chemin):
                    _arcs_dominants.append(_a)
            for _n in _plus_court_chemin:
                _noeuds_dominants[_n] = _reseau.R_graphe.node[_n]
            _multigraphe = nx.Graph()
            _multigraphe.add_nodes_from(_noeuds_dominants)
            _multigraphe.add_edges_from(_arcs_dominants)
            _pos = {}
            for _n in _multigraphe.nodes():
                _pos[_n] = _reseau.R_graphe.node[_n]['pos']

            nx.set_node_attributes(_multigraphe, _pos, "pos")

            # Puis on recompte les sous-graphes
            _subgraphs_generator = nx.connected_component_subgraphs(_multigraphe, copy=True)
            _count = 0
            _subgraphs = []
            for _subgraph in _subgraphs_generator:
                _subgraphs.append(_subgraph)
                _count += 1
        # FIN WHILE

        # Maintenant le graphe connexe, on le transforme en un arbre de racine un puit.

        # return _multigraphe
        # return nx.minimum_spanning_tree(_multigraphe, "poids_dominant", algorithm="boruvka")
        # return nx.minimum_spanning_tree(_multigraphe, "poids_dominant", algorithm="kruskal")
        return nx.minimum_spanning_tree(_multigraphe, "poids_dominant", algorithm="prim")

    @staticmethod
    def __SmigrerPoidsDansArcs(_graphe):
        _datas = {}
        for _edge in _graphe.edges():
            _poids_arc = _graphe.node[_edge[0]]['poids_dominant'] + _graphe.node[_edge[1]]['poids_dominant']
            _datas[_edge[0], _edge[1]] = _poids_arc
        nx.set_edge_attributes(_graphe, _datas, "poids_dominant")

    @staticmethod
    def __SactualisationPoids(_reseau):

        _poids = {}

        for _noeud in _reseau.R_graphe:
            if _reseau.R_graphe.node[_noeud]['batterie'] <= 0:
                _poids[_noeud] = 1
            else:
                _poids[_noeud] = 1 / _reseau.R_graphe.node[_noeud]['batterie']

        nx.set_node_attributes(_reseau.R_graphe, _poids, "poids_dominant")
        Simulateur.__SmigrerPoidsDansArcs(_reseau.R_graphe)

        return _reseau

    @staticmethod
    def __SdeterminationRoutage(_reseau, _ensemble_dominant):
        # Détermine le routage des noeuds Emeteur/Recepteur puis des autres noeuds

        # D'abord on réinitialise le routage
        for _noeud in _ensemble_dominant.nodes():
            _ensemble_dominant.nodes[_noeud]['route'] = -1
        for _noeud in _reseau.R_graphe.nodes():
            _reseau.R_graphe.nodes[_noeud]['route'] = -1

        # On travail sur l'arbre dominant : on part depuis le puit et par récursivité on descend jusqu'aux feuilles
        # en assignant le précédent noeud comme noeud vers lequel envoyer les données.
        _puit = None
        for _noeud in _ensemble_dominant.nodes():
            if _reseau.R_graphe.nodes[_noeud]['role'] == Roles._PUIT:
                _puit = _noeud
                _reseau.R_graphe.nodes[_puit]['route'] = _puit
        Simulateur.__SrouteRecursive(_puit, _reseau, _ensemble_dominant)

        # Ensuite pour tout les noeuds du graphe qui n'ont pas encore de routage (donc qui sont pas dans l'ensemble
        # dominant), on les fait router vers le noeud voisin de l'arbre dominant avec le plus d'énergie
        for _noeud in _reseau.R_graphe.nodes:
            if _reseau.R_graphe.nodes[_noeud]['route'] == -1:
                _meilleur_routage = _noeud
                _meilleur_energie = 0
                for _arc in _reseau.R_graphe.edges():
                    if _arc[0] == _noeud \
                            and _meilleur_energie <= _reseau.R_graphe.nodes[_arc[1]]['batterie'] \
                            and _arc[1] in _reseau.R_ensemble_dominant.nodes:
                        _meilleur_energie = _reseau.R_graphe.nodes[_arc[1]]['batterie']
                        _meilleur_routage = _arc[1]
                    elif _arc[1] == _noeud \
                            and _meilleur_energie <= _reseau.R_graphe.nodes[_arc[0]]['batterie'] \
                            and _arc[0] in _reseau.R_ensemble_dominant.nodes:
                        _meilleur_energie = _reseau.R_graphe.nodes[_arc[0]]['batterie']
                        _meilleur_routage = _arc[0]
                _reseau.R_graphe.nodes[_noeud]['route'] = _meilleur_routage

        return _reseau

    @staticmethod
    def __SrouteRecursive(_noeud, _reseau, _ensemble_dominant):
        for _arc in _ensemble_dominant.edges():
            if _arc[0] == _noeud and _reseau.R_graphe.nodes[_arc[1]]['route'] == -1:
                _reseau.R_graphe.nodes[_arc[1]]['route'] = _noeud
                Simulateur.__SrouteRecursive(_arc[1], _reseau, _ensemble_dominant)
            elif _arc[1] == _noeud and _reseau.R_graphe.nodes[_arc[0]]['route'] == -1:
                _reseau.R_graphe.nodes[_arc[0]]['route'] = _noeud
                Simulateur.__SrouteRecursive(_arc[0], _reseau, _ensemble_dominant)

    def __SsimulationSurUnRoulement(self, _reseau):
        # Sprint 2 : utiliser _intervalle_récolte en lieu et place de intervalle_roulement
        # TODO Sprint 3 : utiliser intervalle_roulement
        self.S_duree_de_vie += self.S_intervalle_roulement

        self.S_duree_de_vie += self.S_intervalle_recolte
        self.__Sconsommation(_reseau)
        return _reseau

    def __Sconsommation(self, _reseau):
        # On prend chaque capteur et on suit le parcourt que suit son envoie de données en diminuant
        # l'énergie des noeuds relais au passage

        # Pour cela on modélise les données générées par le réseau et à transmettre par une liste FIFO
        # La liste contient chaque noeud ayant un ensemble de données à transmettre.
        # On prend comme hypothèse que le chaque ensemble de données à transmettre consomme de l'énergie indépendemment
        # d'autres ensembles à transmettre. Par exemple si un émetteur récepteur receptionne deux ensembles, il devra
        # réceptionner et transmettre ces deux paquets indépendemment.

        _contenants_donnees = []

        # Chaque capteur récolte de l'information (sauf le puit ou si ils n'ont plus d'énergie),
        # ils sont donc tous placés dans la liste
        for _noeud in _reseau.R_graphe.nodes():
            if _reseau.R_graphe.nodes()[_noeud]["role"] != Roles._PUIT:
                # On leur fait consommer l'énergie nécessaire pour générer les donnése
                _reseau.R_graphe.nodes()[_noeud]["batterie"] -= self.S_unite_consommation_recolte
                if _reseau.R_graphe.nodes()[_noeud]["batterie"] > 0:
                    _contenants_donnees.append(_noeud)
                else:
                    _reseau.R_graphe.nodes()[_noeud]["batterie"] = 0

        # Puis on fait passer chaque données de noeud en noeud jusqu'au puit grâce au routage précédemment effectué
        #
        # Tant qu'il y a des données à transmettre
        # Parcourir l'ensemble des noeuds restant puis, si le noeuds et sa route ont encore assez d'énergie,
        # transmettre l'information (supprimer l'émetteur de la liste et ajouter le récepteur)
        # Si le noeud n'a plus d'énergie, le supprimer de la liste. Se le récepteur n'en a plus, supprimer les deux
        while len(_contenants_donnees) > 0:
            _noeud = _contenants_donnees[0]
            _noeud_destinataire = _reseau.R_graphe.nodes()[_noeud]["route"]

            if _reseau.R_graphe.nodes()[_noeud]["batterie"] - self.S_unite_consommation_emission < 0:
                _reseau.R_graphe.nodes()[_noeud]["batterie"] = 0
            elif _reseau.R_graphe.nodes()[_noeud_destinataire]["role"] != Roles._PUIT and \
                    _reseau.R_graphe.nodes()[_noeud_destinataire]["batterie"] - self.S_unite_consommation_reception < 0:
                _reseau.R_graphe.nodes()[_noeud_destinataire]["batterie"] = 0
            else:
                if _reseau.R_graphe.nodes()[_noeud_destinataire]["role"] != Roles._PUIT:
                    _contenants_donnees.append(_noeud_destinataire)
                    _reseau.R_graphe.nodes()[_noeud_destinataire]["batterie"] -= self.S_unite_consommation_reception
                _reseau.R_graphe.nodes()[_noeud]["batterie"] -= self.S_unite_consommation_emission
            _contenants_donnees.remove(_noeud)

        return _reseau

    @staticmethod
    def SfinDeVieAtteinte(_reseau):
        # Pour chaque noeud, suivre la chaine de routage qui le lie au puit. Si la chaîne est brisée décompter ce noeud
        _noeuds_deconnectes = []
        _fin_de_vie_atteinte = False

        for _noeud in _reseau.R_graphe.nodes():
            _, _noeuds_deconnectes = Simulateur.Sparcourt(_noeud, _reseau, _noeuds_deconnectes)

            if len(_noeuds_deconnectes) / (_reseau.R_nbr_noeuds - 1) >= Simulateur.S_fin_de_vie:
                _fin_de_vie_atteinte = True
        return _fin_de_vie_atteinte, _noeuds_deconnectes

    @staticmethod
    def Sparcourt(_noeud, _reseau, _noeuds_deconnectes):

        if _reseau.R_graphe.nodes()[_noeud]["role"] == Roles._PUIT:
            return False, _noeuds_deconnectes

        elif _noeud in _noeuds_deconnectes:
            return True, _noeuds_deconnectes

        else:
            if _reseau.R_graphe.nodes()[_noeud]["batterie"] <= 0:
                _noeuds_deconnectes.append(_noeud)
                return True, _noeuds_deconnectes

            else:
                _chaine_brisee, _noeuds_deconnectes = Simulateur.Sparcourt(_reseau.R_graphe.nodes()[_noeud]["route"],
                                                                           _reseau,
                                                                           _noeuds_deconnectes)
                if _chaine_brisee:
                    _noeuds_deconnectes.append(_noeud)
                    return True, _noeuds_deconnectes
                else:
                    return False, _noeuds_deconnectes
