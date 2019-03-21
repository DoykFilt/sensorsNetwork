"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Statistiques

    Stocke les informations rélatives aux résultats de la simulation

    Possède deux classes :
    - Statistiques : Dérive de Singleton, stocke les informations rélatives aux résultats de la simulation
    - Singleton : Permet de n'avoir qu'une même implémentation possible de la classe Statistique
"""

from Modele.Roles import Roles
from Moteur.Simulateur import Simulateur
from Utilitaires.FileManager import FileManager
from Utilitaires.Log import Log


_log = Log()


class Singleton:
    """
        class Singleton

        Permet de stocker les données relatives du réseau généré et des résultats de sa simulation.

        :var self.__S_initialized : Booléen, Vrai si l'instance unique a déjà été initialisée
        :var self.__instance : Singleton, L'unique instance recupérée lors de l'instanciation de la classe
        :var self.S_nombre_etats : int, le nombre d'états du réseau stockés dans la classe
        :var self.S_niveau_de_batterie_moyen : double[S_nombre_etats], le niveau de batterie moyen pour chaque état
        :var self.S_nbr_actifs : int[S_nombre_etats], le nombre de capteurs reliés à la passerelle pour chaque état
        :var self.S_cycles : int[S_nombre_etats], le numéro du cycle correspondant à l'état associé
        :var self.S_moment_insertion : int[S_nombre_etats], le moment (tps de simulation) de l'insertion des données
            pour chaque état
        :var self.S_resultats : dict{"duree": int, "intervalle": double}, le résultat de la simulation

    """

    # ======================================================
    # Elements clé pour la création d'un singleton en python
    # ======================================================
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls)
            cls.__instance.__S_initialized = False
            cls.__instance.__init__()
        return cls.__instance
    # ======================================================
    # ======================================================

    def __init__(self):
        """
            Constructeur de la classe, initialise les attributs si ils n'ont pas déjà été initialisés.
        """

        if not self.__S_initialized:
            _log.Linfo("Init -- Statistiques.Singleton")

            self.S_nombre_etats = 0
            self.S_niveau_de_batterie_moyen = []
            self.S_nbr_actifs = []
            self.S_cycles = []
            self.S_moment_insertion = []
            self.S_resultats = []

            self.__S_initialized = True

    def SgenererTexte(self, _etat):
        """
            Methode qui permet de générer le texte d'information à afficher.
            Les informations sont les suivantes :
                - numéro de l'etat concerné avec son cycle
                - niveau de batterie moyen
                - ratio nombre de capteurs reliés à la passerelle

            :param _etat : Entier, le numéro de l'état à afficher

            :return String, le texte générer
        """
        _log.Linfo("Début ## Statistiques.Singleton.SgenererTexte")

        _text = ""
        _file_manager = FileManager()

        # Pas de texte à afficher si la valeur est incohérente
        if _etat < 0 or _etat >= self.S_nombre_etats:
            return ""

        _reseau = _file_manager.FMchargerEtat(_etat)
        # Pas de texte à afficher si la valeur est incohérente
        if _reseau is None:
            return ""

        _text += "Résultat de la simulation\n\n"
        _text += "Informations sur l'état " + str(_etat + 1) + \
                 " (cycle " + str(self.S_cycles[_etat]) + ") de la topologie du réseau\n"
        _text += "Niveau moyen des batteries : " + str(self.S_niveau_de_batterie_moyen[_etat]) + "\n"
        _text += "Nombre de capteurs actifs / Nombre de capteurs total : " + \
                 str(self.S_nbr_actifs[_etat]) + " / " + str(_reseau.R_nbr_noeuds - 1) + \
                 " (soit " + str(int(self.S_nbr_actifs[_etat] / (_reseau.R_nbr_noeuds - 1) * 100)) + \
                 "% de capteurs reliés à la passerelle)\n"

        _log.Linfo("Info ## Texte généré : \n" + _text)

        return _text

    def SajouterDonnees(self, _reseau, _cycle, _moment=0):
        """
            Extrait les données suivantes du réseau :
                - nombre de noeuds connectés à la passerelle
                - niveau de batterie moyen

        :param _reseau: Réseau, le réseau depuis lequel extraire les données
        :param _cycle : int, le numéro du cycle associé à l'état du réseau
        :param _moment : int, le moment (tps de simulation) associé à l'état du réseau
        """
        _log.Linfo("Début ## Statistiques.Singleton.SajouterDonnees")

        # Récupération du nombre de capteurs connectés à la passerelle
        if len(self.S_cycles) == 0 or max(self.S_cycles) == 0:
            _intervalle = 0
        else:
            _intervalle = 1
        _, _noeuds_deconnectes = Simulateur.SfinDeVieAtteinte(_reseau, _intervalle)
        _nbr_noeuds_deconnectes = len(_noeuds_deconnectes)
        _nbr_actifs = _reseau.R_nbr_noeuds - _nbr_noeuds_deconnectes - 1  # Moins le puit

        # Récupération du niveau de batterie moyen
        _somme_batterie = 0
        for _noeud in _reseau.R_graphe.nodes():
            if _reseau.R_graphe.nodes()[_noeud]["role"] != Roles.PUIT:
                _somme_batterie += _reseau.R_graphe.nodes()[_noeud]["batterie"]
        _niveau_batterie_moyen = int(_somme_batterie / (_reseau.R_nbr_noeuds - 1))

        self.SajouterDonneesBrutes(_niveau_batterie_moyen, _nbr_actifs, _cycle, _moment)

    def SajouterDonneesBrutes(self, _niveau_de_batterie_moyen, _nbr_actifs, _cycle, _moment=0):
        """
            Stocke les données passées en paramètre en tant que nouvel état

        :param _niveau_de_batterie_moyen : float, le niveau de batterie moyen du réseau
        :param _nbr_actifs : int, nombre de noeuds connectés à la passerelle
        :param _cycle : int, le numéro du cycle associé à l'état du réseau
        :param _moment : int, le moment (tps de simulation) associé à l'état du réseau
        """
        _log.Linfo("Début ## Statistiques.Singleton.SajouterDonneesBrutes")

        self.S_niveau_de_batterie_moyen.append(_niveau_de_batterie_moyen)
        self.S_nbr_actifs.append(_nbr_actifs)
        self.S_cycles.append(_cycle)
        self.S_moment_insertion.append(_moment)
        self.S_nombre_etats += 1

    def SviderEtats(self, _garder_etat_initial):
        """
            Supprime l'ensemble des états précédemment stockés

        :param _garder_etat_initial: booléen, vrai si le premier état ne doit pas être supprimé, faux sinon
        """
        _log.Linfo("Début ## Statistiques.Singleton.SviderEtats")

        # Cas où l'on garde les informations concernant l'état initial
        if _garder_etat_initial and self.S_nombre_etats > 0:
            self.S_nombre_etats = 1
            self.S_niveau_de_batterie_moyen = [self.S_niveau_de_batterie_moyen[0]]
            self.S_nbr_actifs = [self.S_nbr_actifs[0]]
            self.S_cycles = [self.S_cycles[0]]
            self.S_moment_insertion = [self.S_moment_insertion[0]]
        # Cas où on efface tout
        else:
            self.S_nombre_etats = 0
            self.S_niveau_de_batterie_moyen = []
            self.S_nbr_actifs = []
            self.S_cycles = []
            self.S_moment_insertion = []

        # Dans tout les cas on supprime les résultats de la simulation
        self.S_resultats = []

    def SajouterResultat(self, _intervalle, _duree_de_vie):
        """
            Stocke un nouveau résultat

        :param _intervalle: float, L'intervalle de temps de changement de rôle des capteurs utilisé
        :param _duree_de_vie: int, La durée de vie atteinte du réseau
        """
        _log.Linfo("Début ## Statistiques.Singleton.SajouterResultat")

        self.S_resultats.append(dict({"intervalle": _intervalle, "duree": _duree_de_vie}))

    def SgenererDonneesGraphiques(self):
        """
            Permet d'exporter les données dans un format exploitable par un affichage matplotlib
            Cad une liste pour les abscisses et une liste pour les ordonnées par graphique.

        :returns: - _graphique1 : dict({String : [float], String : [float]})
                  - _graphique2 : dict({String : [float], String : [int]})
        """
        _log.Linfo("Début ## Statistiques.Singleton.SgenererDonneesGraphiques")

        _graphique1 = dict({"x": [], "y": []})
        _graphique2 = dict({"x": [], "y": []})

        # Pour le graphique de la durée de vie du réseau en fonction des intervalles
        for _resultat in self.S_resultats:
            _graphique1["x"].append(_resultat["duree"])
            _graphique1["y"].append(_resultat["intervalle"])

        # Pour le graphique du nombre de capteurs reliés à la passerelle en fonction du temps
        for _etat in range(0, self.S_nombre_etats):
            _graphique2["x"].append(self.S_nbr_actifs[_etat])
            _graphique2["y"].append(self.S_moment_insertion[_etat])

        return _graphique1, _graphique2

    def S_obtenir_niveau_de_batterie_moyen(self, _reseau):
        """
            Permet d'obtenir le dernier niveau de batterie moyen enregistré. Si aucun n'a été enregistré, est retourné
            le niveau de batterie initial, récupéré dans le réseau passé en paramètre correspondant à un état quelconque

        :param _reseau: Reseau, un état quelconque du réseau
        :return: int, le niveau de batterie correspondant
        """
        _log.Linfo("Début ## Statistiques.Singleton.S_obtenir_niveau_de_batterie_moyen")

        if len(self.S_niveau_de_batterie_moyen) == 0:
            return _reseau.R_capacite_batterie_max
        else:
            return self.S_niveau_de_batterie_moyen[-1]

    def S_etatCyclePrecedent(self, _etat_initial):
        """
            Permet de récupérer le cycle précédent du cycle correspond à l'état indiqué.

        :param _etat_initial: int
        :return: int, le numéro du cycle. 0 si la valeur d'_etat est incohérente ou si aucun cycle n'a été trouvé
        """
        _log.Linfo("Début ## Statistiques.Singleton.S_etatCyclePrecedent")

        _etat_final = 0

        # Cas où le numéro de l'état demandé n'est pas cohérent avec ceux stockés
        if not (_etat_initial >= self.S_nombre_etats or _etat_initial <= 0 or self.S_nombre_etats < 1):
            _cycle = self.S_cycles[_etat_initial]

            # Si on est placé sur l'état initial d'un cycle, on se place sur le dernier du cycle précédent pour
            # récupérer son état initial
            if self.S_cycles[_etat_initial - 1] != _cycle:
                _cycle = self.S_cycles[_etat_initial - 1]

            # Parcourt les états depuis l'état inital vers le premier état avec un pas de -1
            for _etat in range(len(self.S_cycles[:_etat_initial]) - 1, -1, -1):
                # Si on rencontre un nouveau cycle on transmette le numéro de l'état suivant : c'est l'état 1 du cycle
                if self.S_cycles[_etat] != _cycle:
                    _etat_final = _etat + 1
                    break

        _log.Linfo("Info ## état initial = " + str(_etat_initial) + ", état final = " + str(_etat_final))

        return _etat_final

    def S_etatCycleSuivant(self, _etat_initial):
        """
            Permet de récupérer le cycle suivant du cycle correspond à l'état indiqué.

        :param _etat_initial: int
        :return: int, le numéro du cycle. 0 si la valeur d'_etat est incohérente ou si aucun cycle n'a été trouvé
        """
        _log.Linfo("Début ## Statistiques.Singleton.S_etatCycleSuivant")

        _etat_final = self.S_nombre_etats - 1

        # Cas où le numéro de l'état demandé n'est pas cohérent avec ceux stockés : on retourn le dernier etat
        if not (_etat_initial >= self.S_nombre_etats or _etat_initial < 0 or self.S_nombre_etats < 1):
            _cycle = self.S_cycles[_etat_initial]

            # Parcourt les états depuis l'état inital vers le dernier état
            for _etat in range(_etat_initial, len(self.S_cycles)):
                # Si on rencontre un nouveau cycle on transmette le numéro de l'état : c'est l'état initial du cycle
                if self.S_cycles[_etat] != _cycle:
                    _etat_final = _etat
                    break

        _log.Linfo("Info ## état initial = " + str(_etat_initial) + ", état final = " + str(_etat_final))

        return _etat_final


class Statistiques(Singleton):
    """
        class Statistiques

        Hérite de Statistiques.Singleton pour récupérer l'ensemble des ses méthodes et attributs

    """
    pass
