import time
import copy

import networkx as nx
import math
from networkx.algorithms.approximation import dominating_set
from networkx.algorithms.shortest_paths.generic import shortest_path, has_path

from Modele.Roles import Roles
from Modele.Signaux import Signaux
from Utilitaires.FileManager import FileManager


class Simulateur:
    """
        class Simulateur

        Classe qui regroupe les outils utiles pour la simulation de la vie d'un réseau
        La plupart des méthodes sont déclarées statiques et la méthode principale est SlancerSimulation qui
        lie par cascade l'ensemble des méthodes. Cf diagramme de cas d'utilisation pour le cas général

    """
    # TODO : demander les paramètres suivants à l'utilisateur à travers une fenêtre intermédiaire comme  FenetreCreation
    # Temps entre chaque récolte d'information
    S_intervalle_recolte = 1
    # Temps entre chaque changement de rôle
    S_intervalle_roulement = 0
    # Consommation énergétique d'une émission de données
    S_unite_consommation_emission = 0.05
    # Consommation énergétique d'une réception de données
    S_unite_consommation_reception = 0.025
    # Consommation énergétique d'une récolte de données
    S_unite_consommation_recolte = 0.005
    # Pourcentage de réseaux connectés au puit à partir duquel on considère que la fin de vie du réseau est atteinte
    S_fin_de_vie = 0.8
    # Variable utilisée pour stocker la durée de vie du réseau
    S_duree_de_vie = 0
    # Ratio qui détermine à partir de quand arrêter la simulation. Utilisé dans __SmaximumAtteint, si l'augmentation
    # de durée de vie par rapport à la valeur précédente ne dépasse pas (S_performances x 100)% on arrête la simulation
    S_performance = 0.005

    def __init__(self, _connecteur):
        """
            Initialisateur de la classe

        :param _connecteur: pyqtSignal, connecteur qui permet d'informer le controleur de l'avancement de la simulation
        """
        super(Simulateur, self).__init__()
        self.S_connecteur = _connecteur
        self.S_resultats = []
        self.S_duree_simulation = 0

    def SlancerSimulation(self, _reseau):
        """
            Permet de lancer le processus de simulation de la vie du réseau

        :param _reseau: Reseau, le réseau à traiter
        :return: Reseau, le réseau une fois traité
        """

        from Controleur.Statistiques import Statistiques
        _statistiques = Statistiques()

        # Chrono pour savoir combien de temps la simulation a durée
        _start = time.time()

        _file_manager = FileManager()

        _dernier_roulement = 0
        _reseau_simulation = _reseau
        self.S_duree_simulation = 0
        self.S_duree_de_vie = 0
        self.S_intervalle_roulement = 0
        # Initialisation des compteurs
        _etat = 0
        _total = 1
        _cycle = 0

        while not self.__SmaximumAtteint():

            self.S_connecteur.emit(Signaux._INITIALISATION_SIMULATION, dict())

            _reseau_simulation = copy.deepcopy(_reseau)

            _text_progression = "Simulation en cours.. " \
                                "\nCycle " + str(_cycle) + \
                                "\nintervalle utilisé : " + str(self.S_intervalle_roulement) + " unité(s) de temps"

            self.S_connecteur.emit(Signaux._PROGRESSION_SIMULATION, dict({"avancee": 0,
                                                                          "text": _text_progression}))

            # Configuration topologique du réseau (routage et ensemble dominant)
            _reseau_simulation = self.SconfigurationTopologique(_reseau_simulation)

            _fin_de_vie_atteinte, _capteurs_deconnectes = self.SfinDeVieAtteinte(_reseau_simulation,
                                                                                 self.S_intervalle_roulement)
            self.S_duree_de_vie = 0

            # Tant que la fin de vie du réseau n'a pas été atteinte, on simule consommation énergétique en enregistrant
            # les étapes intermédiaires
            while not _fin_de_vie_atteinte:

                # print(str(self.S_duree_simulation) + " : " + str(len(_capteurs_deconnectes)) + " capteurs déconnectés")

                # Cas où le temps écoulé correspond à l'intervalle de temps de changement de rôles des capteurs.
                if self.S_intervalle_roulement != 0:
                    if self.S_duree_de_vie == 0 \
                            or self.S_duree_de_vie - _dernier_roulement >= self.S_intervalle_roulement:
                        _dernier_roulement = self.S_duree_de_vie
                        _reseau_simulation = self.SconfigurationTopologique(_reseau_simulation)
                        _etat += 1
                        _total += 1
                        _file_manager.FMenregistrerEtat(_reseau_simulation)
                        _statistiques.SajouterDonnees(_reseau_simulation, _cycle, self.S_duree_simulation)
                        self.S_connecteur.emit(Signaux._NOUVEL_ETAT, dict({"etat": _etat, "total": _total}))

                _fin_de_vie_atteinte, _capteurs_deconnectes = self.SfinDeVieAtteinte(_reseau_simulation,
                                                                                     self.S_intervalle_roulement)

                if not _fin_de_vie_atteinte:
                    _reseau_simulation = self.__SsimulationSurUnRoulement(_reseau_simulation, _capteurs_deconnectes)

                    # La valeur de la barre de progression = niveau de batterie moyen / niveau de batterie initial
                    # _niveau_de_batterie_moy = _statistiques.S_obtenir_niveau_de_batterie_moyen(_reseau_simulation)
                    # _capacite_batterie_max = _reseau_simulation.R_capacite_batterie_max
                    # _ratio = (1 - (_niveau_de_batterie_moy / _capacite_batterie_max))
                    _ratio = (len(_capteurs_deconnectes) / _reseau.R_nbr_noeuds)
                    self.S_connecteur.emit(Signaux._PROGRESSION_SIMULATION, dict({"avancee": int(_ratio * 100),
                                                                                  "text": _text_progression}))

            # Ajout de l'état de la fin de vie du réseau
            _etat += 1
            _total += 1
            _file_manager.FMenregistrerEtat(_reseau_simulation)
            _statistiques.SajouterDonnees(_reseau_simulation, _cycle, self.S_duree_simulation)
            self.S_duree_simulation += self.S_intervalle_recolte * 100  # Pour séparer les résultats d'un cycle à lautre
            self.S_connecteur.emit(Signaux._NOUVEL_ETAT, dict({"etat": _etat, "total": _total}))

            # On met la barre de progression à 100%
            self.S_connecteur.emit(Signaux._PROGRESSION_SIMULATION, dict({"avancee": 100, "text": _text_progression}))

            # Une fois la durée de vie du réseau atteinte, plus qu'à ajouter le résultat aux statistiques
            _statistiques.SajouterResultat(self.S_intervalle_roulement, self.S_duree_de_vie)

            self.S_resultats.append(dict({"intervalle": self.S_intervalle_roulement, "resultat": self.S_duree_de_vie}))
            _cycle += 1

            # Détermination de l'intervalle de temps pour le prochain tour
            self.__SdeterminationIntervalleTemps()

        # Fin while, cad fin de la simulation, le maximum a été trouvé

        FileManager.FMsauvegarderStatistiques()

        # Informations sur la durée de la simulation
        _end = time.time()
        _temps = (_end - _start) % 60 // 1
        self.S_connecteur.emit(Signaux._FIN_SIMULATION, dict({"duree": abs(_temps)}))

        return _reseau_simulation

    def __SmaximumAtteint(self):
        """
            Permet de déterminer si la durée de vie maximale a été atteinte.
            On estime que la durée maximale a été atteinte si la durée de vie est plus petite que la précédente ou si
            l'augmentation de la durée de vie par rapport à la précédente ne dépasse pas un paramètre fixé S_performance
        """

        if len(self.S_resultats) > 1:

            _dernier_resultat = self.S_resultats[-1]["resultat"]
            _avant_dernier_resultat = self.S_resultats[-2]["resultat"]

            if _dernier_resultat <= _avant_dernier_resultat:
                return True

            _ratio = (_dernier_resultat - _avant_dernier_resultat) / _dernier_resultat
            if _ratio < self.S_performance:
                return True

        return False

    def __SdeterminationIntervalleTemps(self):
        """
            Permet de déterminer l'intervalle de changement de rôle des capteurs en fonction du précédent et du résultat
            de la précédente simulation.
            L'intervalle est égal à la moitié de sa précédente valeur
        """
        if self.S_intervalle_roulement == 0:
            self.S_intervalle_roulement = self.S_duree_de_vie / 2
        else:
            self.S_intervalle_roulement /= 2

    @staticmethod
    def SconfigurationTopologique(_reseau):
        """
            Permet de déterminer le rôle des capteurs et la table des routage

        :param _reseau: Reseau, le réseau à configurer
        :return: Reseau, le réseau configuré
        """
        # Déyermination des rôles des capteurs en prenant en compte uniquement l'ensemble dominant

        # _reseau = Simulateur.SreseauSansCapteursVides(_reseau)

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
        Simulateur.SdeterminationRoutage(_reseau, _ensemble_dominant)

        return _reseau

    @staticmethod
    def SdeterminationEnsembleDominant(_reseau_initial):
        """
            Permet de déterminer l'ensemble dominant d'un réseau. Prend en compte le niveau restant de la batterie
        :param _reseau: Reseau, le réseau à configurer
        :return: Reseau, le réseau configuré
        """

        # Avant tout on créé un copie du réseau duquel on supprime l'ensemble des noeuds qui n'ont plus de batterie
        # ainsi que les arcs qui y sont reliés
        _reseau, _ = Simulateur.SreseauSansCapteursVides(_reseau_initial)

        # # En premier, stocke dans chaque noeuds et arc un poids inversement égale au niveau de la batterie des noeuds
        # _reseau = Simulateur.SactualisationPoids(_reseau)
        # # Sélection des noeuds dominants avec un algorithme de networkX
        _ensemble_dominant = dominating_set.min_weighted_dominating_set(
            _reseau.R_graphe,
            weight="poids_dominant"
        )
        # _ensemble_dominant = dominating_set.min_edge_dominating_set(_reseau.R_graphe)

        # On ajoute le ou les puits à l'ensemble dominant si ils n'y sont pas
        for _noeud in _reseau.R_graphe:
            if _reseau.R_graphe.node[_noeud]['role'] == Roles._PUIT and _noeud not in _ensemble_dominant:
                _ensemble_dominant.add(_noeud)

        # On créé un multigraphe intermédiaire en reprennant uniquement les arcs et noeuds qui sont dans l'ensemble
        # dominant
        _noeuds_dominants = {}
        for _n in _ensemble_dominant:
            _noeuds_dominants[_n] = _reseau.R_graphe.node[_n]
        _arcs_dominants = []
        for _a in _reseau.R_graphe.edges():
            if _a[0] in _ensemble_dominant and _a[1] in _ensemble_dominant:
                _arcs_dominants.append(_a)

        # _arcs_dominants = []
        # _id_noeuds_dominants = []
        # for _arc in _ensemble_dominant:
        #     if _arc != 0:
        #         _arcs_dominants.append(_arc)
        #         if _arc[0] not in _id_noeuds_dominants:
        #             _id_noeuds_dominants.append(_arc[0])
        #         if _arc[1] not in _id_noeuds_dominants:
        #             _id_noeuds_dominants.append(_arc[1])
        #
        # _noeuds_dominants = {}
        # for _n in _id_noeuds_dominants:
        #     _noeuds_dominants[_n] = _reseau.R_graphe.node[_n]

        _multigraphe = nx.Graph()
        _multigraphe.add_nodes_from(_noeuds_dominants)
        _multigraphe.add_edges_from(_arcs_dominants)

        # Dans ce multigraphe on retranscrit les informations de position
        _pos = {}
        for _n in _multigraphe.nodes():
            _pos[_n] = _reseau.R_graphe.node[_n]['pos']

        nx.set_node_attributes(_multigraphe, _pos, "pos")

        # La suite vise à rendre connexe le multigraphe en ajoutant dans l'ensemble dominant les noeuds sur le plus
        # court chemin (avec le niveau de la batterie comme poids) entre les deux noeuds les plus proches de chaque
        # sous-graphe

        # Récupère les sous-graphes
        _subgraphs_generator = nx.connected_component_subgraphs(_multigraphe, copy=True)
        _subgraphs = []
        for _subgraph in _subgraphs_generator:
            _subgraphs.append(_subgraph)

        # Tant qu'il y a encore des sous-graphes
        while len(_subgraphs) > 1:
            # ----------------------------------------------------------------------------------------------------------
            # On prend le premier sous-graphe et le sous-graphe le plus proche de lui
            # ----------------------------------------------------------------------------------------------------------
            _subgraph1 = _subgraphs[0]
            # Calcul du centre de gravité du premier sous-graphe
            _x, _y = 0, 0
            _nbr_noeuds = 0
            for _node in _subgraph1.node:
                _x += _subgraph1.node[_node]['pos'][0]
                _y += _subgraph1.node[_node]['pos'][1]
                _nbr_noeuds += 1
            _g_x = _x / _nbr_noeuds
            _g_y = _y / _nbr_noeuds
            _subgraphs.remove(_subgraph1)

            # Puis on compare les distances avec tout les autres sous-graphes pour récupérer le plus proche
            _distance_min = 0
            _sub_graph_plus_pres = _subgraphs[0]
            for _subgraph in _subgraphs:
                _x, _y = 0, 0
                _nbr_noeuds = 0
                for _node in _subgraph.node:
                    _x += _subgraph.node[_node]['pos'][0]
                    _y += _subgraph.node[_node]['pos'][1]
                    _nbr_noeuds += 1
                _distance = math.sqrt(math.pow(_g_x - _x / _nbr_noeuds, 2) +
                                      math.pow(_g_y - _y / _nbr_noeuds, 2))
                if _distance_min == 0 or _distance < _distance_min:
                    _distance_min = _distance
                    _sub_graph_plus_pres = _subgraph

            # ----------------------------------------------------------------------------------------------------------
            # Ensuite on récupère les deux points les plus proches entre les deux sous-graphes
            # ----------------------------------------------------------------------------------------------------------

            _paire_la_plus_proche = None
            _distance_min = 0
            for _noeud1 in _subgraph1:
                for _noeud2 in _sub_graph_plus_pres:
                    _distance = math.sqrt(math.pow(_subgraph1.node[_noeud1]['pos'][0] -
                                                   _sub_graph_plus_pres.node[_noeud2]['pos'][0], 2) +
                                          math.pow(_subgraph1.node[_noeud1]['pos'][1] -
                                                   _sub_graph_plus_pres.node[_noeud2]['pos'][1], 2))
                    if _paire_la_plus_proche is None or _distance < _distance_min:
                        _distance_min = _distance
                        _paire_la_plus_proche = (_noeud1, _noeud2)

            # ----------------------------------------------------------------------------------------------------------
            # Puis on relie les deux sous-graphes en incorporant au graphe dominant les arcs et noeuds situés sur le plus
            # cours chemin entre les deux noeuds les plus proches
            # ----------------------------------------------------------------------------------------------------------

            try:
                _plus_court_chemin = shortest_path(_reseau.R_graphe,
                                                   _paire_la_plus_proche[0], _paire_la_plus_proche[1],
                                                   weight='poids_dominant')
            except:
                # Si une exception est retournée c'est qu'il n'est plus possible de relier les deux noeuds :
                # en conséquent on supprime le sous graphe qu'on essayait d'incorporer et on passe au tour de boucle
                # suivant
                _subgraphs.remove(_sub_graph_plus_pres)
                continue

            # On ajoute les nouveaux noeuds et arcs à l'ensemble dominant
            # Arcs
            for _a in _reseau.R_graphe.edges():
                if (_a[0] in _plus_court_chemin and _a[1] in _plus_court_chemin) or \
                        (_a[0] in _plus_court_chemin and _a[1] in _noeuds_dominants) or \
                        (_a[0] in _noeuds_dominants and _a[1] in _plus_court_chemin):
                    _arcs_dominants.append(_a)
            # Noeuds
            for _n in _plus_court_chemin:
                _noeuds_dominants[_n] = _reseau.R_graphe.node[_n]

            # Puis on recréer un multigraphe à partir de ces nouveaux ensembles
            _multigraphe = nx.Graph()
            _multigraphe.add_nodes_from(_noeuds_dominants)
            _multigraphe.add_edges_from(_arcs_dominants)
            _pos = {}
            for _n in _multigraphe.nodes():
                _pos[_n] = _reseau.R_graphe.node[_n]['pos']
            nx.set_node_attributes(_multigraphe, _pos, "pos")

            # Pour finalement diviser le multigraphe en sous-graphe et recommencer un tour de boucle
            _subgraphs_generator = nx.connected_component_subgraphs(_multigraphe, copy=True)
            _subgraphs = []
            for _subgraph in _subgraphs_generator:
                _subgraphs.append(_subgraph)
        # FIN WHILE

        # Maintenant le graphe devenu connexe, on le transforme en un arbre de racine un puit, après plusieurs essais
        # l'algorithme de prim est apparu comme le plus performant car le plus directement connecté au puit.

        # return nx.minimum_spanning_tree(_multigraphe, "poids_dominant", algorithm="boruvka")
        # return nx.minimum_spanning_tree(_multigraphe, "poids_dominant", algorithm="kruskal")
        return nx.minimum_spanning_tree(_multigraphe, "poids_dominant", algorithm="prim")

    @staticmethod
    def SactualisationPoids(_reseau):
        """
            Permet de donner un poids aux éléments du réseau. Ce poids, égal à l'inverse du nivea ude la batterie du
            noeud, est utilisé par les algorithme de la configuration topologique
        :param _reseau: Reseau, le réseau à configurer
        :return: Reseau, le réseau configuré
        """

        _poids = {}

        for _noeud in _reseau.R_graphe:
            if _reseau.R_graphe.node[_noeud]['batterie'] <= 0:
                _poids[_noeud] = 1
            else:
                _poids[_noeud] = 1 / _reseau.R_graphe.node[_noeud]['batterie']

        nx.set_node_attributes(_reseau.R_graphe, _poids, "poids_dominant")
        Simulateur.SmigrerPoidsDansArcs(_reseau.R_graphe)

        return _reseau

    @staticmethod
    def SmigrerPoidsDansArcs(_graphe):
        """
            Permet de déplacer le poids des noeuds dans les arcs les reliants. le poids d'un arc est égal à la somme
            du poids des deux noeuds

        :param _reseau: Reseau, le réseau à configurer
        :return: Reseau, le réseau configuré
        """
        _datas = {}
        for _edge in _graphe.edges():
            _poids_arc = _graphe.node[_edge[0]]['poids_dominant'] + _graphe.node[_edge[1]]['poids_dominant']
            _datas[_edge[0], _edge[1]] = _poids_arc
        nx.set_edge_attributes(_graphe, _datas, "poids_dominant")

    @staticmethod
    def SdeterminationRoutage(_reseau, _ensemble_dominant):
        """
            Détermine pour chaque noeud et à partir de l'ensemble dominant, le noeud vers lequel envoyer les données
            pour se rapprocher de la passerelle

        :param _reseau: Reseau, le réseau à configurer
        :param _ensemble_dominant: Graphe NetworkX
        :return: Reseau, le réseau configuré
        """

        # On commence par réinitialiser le routage
        for _noeud in _ensemble_dominant.nodes():
            _ensemble_dominant.nodes[_noeud]['route'] = -1
        for _noeud in _reseau.R_graphe.nodes():
            _reseau.R_graphe.nodes[_noeud]['route'] = -1

        # On travail sur l'arbre dominant : on part depuis le puit et par récursivité on descend jusqu'aux feuilles
        # en assignant le précédent noeud comme noeud vers lequel envoyer les données.
        # On traite d'abord le cas du puit
        _puit = None
        for _noeud in _ensemble_dominant.nodes():
            if _reseau.R_graphe.nodes[_noeud]['role'] == Roles._PUIT:
                _puit = _noeud
                _reseau.R_graphe.nodes[_puit]['route'] = _puit
        # Appelle à la fonction récursive en partant du puit
        Simulateur.SrouteRecursive(_puit, _reseau, _ensemble_dominant)

        # Ensuite pour tout les noeuds du graphe qui n'ont pas encore de routage (donc qui sont pas dans l'ensemble
        # dominant), on les fait router vers le noeud voisin de l'arbre dominant avec le plus d'énergie
        for _noeud in _reseau.R_graphe.nodes:
            # Si le routage n'a pas été déterminé (donc si il ne fait pas parti de l'ensemble dominant)
            if _reseau.R_graphe.nodes[_noeud]['route'] == -1:
                _meilleur_routage = _noeud
                _meilleur_energie = 0
                # Pour tout arcs, si le noeud est relié au puit c'est incontestablement son meilleur routage possible
                # Sinon on prend le noeud avec le plus de batterie
                for _arc in _reseau.R_graphe.edges():
                    if (_arc[0] == _noeud and _arc[1] == _puit) or (_arc[1] == _noeud and _arc[0] == _puit):
                        _meilleur_routage = _puit
                        break
                    elif _arc[0] == _noeud \
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
    def SrouteRecursive(_noeud, _reseau, _ensemble_dominant):
        """
            Fonction récursive pour déterminer le routage des noeuds précédents le _noeud

        :param _noeud: int, le numéro du noeud source (commencer par le puit pour couvrir l'ensemble du graphe
        :param _reseau: Reseau, le réseau à traiter
        :param _ensemble_dominant: Graphe networkX l'ensemble dominant associé au graphe
        :return:
        """
        # TODO : optimiser la récursivité en excluant les arcs déjà visités

        for _arc in _ensemble_dominant.edges():
            if _arc[0] == _noeud and _reseau.R_graphe.nodes[_arc[1]]['route'] == -1:
                _reseau.R_graphe.nodes[_arc[1]]['route'] = _noeud
                Simulateur.SrouteRecursive(_arc[1], _reseau, _ensemble_dominant)
            elif _arc[1] == _noeud and _reseau.R_graphe.nodes[_arc[0]]['route'] == -1:
                _reseau.R_graphe.nodes[_arc[0]]['route'] = _noeud
                Simulateur.SrouteRecursive(_arc[0], _reseau, _ensemble_dominant)

    def __SsimulationSurUnRoulement(self, _reseau, _capteurs_deconnectes):
        """
            Permet de simuler la consommation énergétique du réseau sur une unité de temps.

        :param _reseau: Reseau, le réseau à traiter
        :return: Reseau, le réseau traité
        """

        self.S_duree_de_vie += self.S_intervalle_recolte
        self.S_duree_simulation += self.S_intervalle_recolte
        self.__Sconsommation(_reseau, _capteurs_deconnectes)
        return _reseau

    def __Sconsommation(self, _reseau, _capteurs_deconnectes):
        """
            permet de simuler la consommation énergétique pour une génération de données. Cad que chaque capteur
            récolte de l'information puis l'envoie vers le puit. Cette méthode simule la consommation  d'NRJ nécessaire
            pour que chaque donnée générée atteigne la passerelle.

        :param _reseau: Reseau, le réseau à traiter
        :return: Reseau, le réseau traité
        """

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
            if _reseau.R_graphe.nodes()[_noeud]["role"] != Roles._PUIT and _noeud not in _capteurs_deconnectes:
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
    def SfinDeVieAtteinte(_reseau_initial, _intervalle_roulement):
        """
            Permet de déterminer si le réseau a atteint sa fin de vie. Un ratio du nombre de capteur relié au puit est
            utilisé.

        :param _reseau: Reseau, le réseau à traiter
        :return:    boolean, vrai si la fin de vie du réseau a été atteinte
                    int[], liste des noeuds déconnectés
        """

        # Pour chaque noeud, suivre la chaine de routage qui le lie au puit. Si la chaîne est brisée décompter ce noeud
        _noeuds_deconnectes = []
        _fin_de_vie_atteinte = False
        _puit = 0

        if _intervalle_roulement != 0:
            _reseau, _noeuds_vides = Simulateur.SreseauSansCapteursVides(_reseau_initial)
            _reseau = Simulateur.SconfigurationTopologique(_reseau)
            _noeuds_deconnectes.extend(_noeuds_vides)

        else:
            _reseau = _reseau_initial

        for _noeud in _reseau.R_graphe.nodes():
            if _reseau.R_graphe.node[_noeud]['role'] == Roles._PUIT:
                _puit = _noeud
                break

        for _noeud in _reseau.R_graphe.nodes():

            if not has_path(_reseau.R_graphe, _noeud, _puit):
                _noeuds_deconnectes.append(_noeud)

            elif _intervalle_roulement == 0:
                # La récurisivité est utilisée pour remonter de routage en routage jusqu'au puit
                _, _noeuds_deconnectes = Simulateur.Sparcourt(_noeud, _reseau, _noeuds_deconnectes)

        if len(_noeuds_deconnectes) / (_reseau.R_nbr_noeuds - 1) >= Simulateur.S_fin_de_vie:
            _fin_de_vie_atteinte = True

        return _fin_de_vie_atteinte, _noeuds_deconnectes

    @staticmethod
    def Sparcourt(_noeud, _reseau, _noeuds_deconnectes):
        """
            Fonction récursive qui permet de parcourir remonter d'un noeud vers le puit et de déterminer si ce noeuds
            n'est pas déconnecté de celui-ci.

        :param _noeud: int, le numéro du noeud d'où partir
        :param _reseau: Le réseau à traiter
        :param _noeuds_deconnectes: int[],  l'ensemble des noeuds déjà parcourus et déconnecté
        :return:    bool, vrai si le noeud est déconnecté, faux sinon
                    _noeuds_deconnectes (int[]), l'ensemble des noeuds déjà parcourus et déconnecté
        """

        # Si le noeud rencontré est le puit on stop la récursivité : le noeud initial n'est pas déconnecté
        if _reseau.R_graphe.nodes()[_noeud]["role"] == Roles._PUIT:
            return False, _noeuds_deconnectes

        # Si le noeud rencontré a déjà été considéré comme déconnecté, on stop : le noeud initial est déconnecté
        elif _noeud in _noeuds_deconnectes:
            return True, _noeuds_deconnectes

        else:
            # Si le noeud n'a plus de batterie on stop : le noeud initial est déconnecté
            if _reseau.R_graphe.nodes()[_noeud]["batterie"] <= 0:
                _noeuds_deconnectes.append(_noeud)
                return True, _noeuds_deconnectes

            else:
                # Sinon on applique la récursivité
                _chaine_brisee, _noeuds_deconnectes = Simulateur.Sparcourt(_reseau.R_graphe.nodes()[_noeud]["route"],
                                                                           _reseau,
                                                                           _noeuds_deconnectes)
                # Suivant les résultats on ajoute ou pas le noeud parmis les noeuds déconnectés
                if _chaine_brisee:
                    _noeuds_deconnectes.append(_noeud)
                    return True, _noeuds_deconnectes
                else:
                    return False, _noeuds_deconnectes

    @staticmethod
    def SreseauSansCapteursVides(_reseau):

        _copie = copy.deepcopy(_reseau)

        _noeuds_vides = []

        for _noeud in _copie.R_graphe.nodes():
            if _copie.R_graphe.nodes()[_noeud]["role"] != Roles._PUIT and \
                    _copie.R_graphe.nodes()[_noeud]["batterie"] == 0:
                _noeuds_vides.append(_noeud)

        _copie.R_graphe.remove_nodes_from(_noeuds_vides)

        return _copie, _noeuds_vides