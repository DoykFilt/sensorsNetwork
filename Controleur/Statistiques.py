from Modele.Roles import Roles
from Moteur.Simulateur import Simulateur
from Utilitaires.FileManager import FileManager


class Singleton:
    """
        class Singleton

        Utilisée par la classe FileManager, permet de n'utiliser qu'une seule instance de la classe sur tout le projet

        Cette classe permet de stocker en mémoire les données utilisées dans la fenêtre principale pour afficher les
        informations de performance de la simulation

    """

    # Elements clé pour la création d'un singleton en python
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls)
            cls.__instance.__S_initialized = False
            cls.__instance.__init__()
        return cls.__instance

    def __init__(self):
        """
            Constructeur de la classe, initialise les attributs
            L'attribut __initialised permet de faire appel à l'initialisateur seulement une fois lors de la première
            instanciation de la classe
        """
        if not self.__S_initialized:
            self.S_nombre_etats = 0
            self.S_niveau_de_batterie_moyen = dict()
            self.S_nbr_actifs = dict()
            self.S_resultats = []

            self.__S_initialized = True

    def SgenererTexte(self, _etat):
        """
            Methode qui permet de générer le texte d'information à afficher.
            Les informations sont les suivantes :
                - numéro de l'etat concerné
                - niveau de batterie moyen
                - ratio nombre de capteurs reliés à la passerelle

            :param _etat : Entier, le numéro de l'état à afficher
        """
        _text = ""
        _file_manager = FileManager()

        if _etat < 0 or _etat >= self.S_nombre_etats:
            return ""

        _reseau = _file_manager.FMchargerEtat(_etat)
        if _reseau is None:
            return ""

        # Récupère les informations depuis les stats.
        # Celles-ci contiennent plus d'états transitoire (un par unité de temps)
        # "informatif" contient le numéro de l'état correspondant au moment d'un changement de rôle ou fin de simulation
        _nbr_actif = 0
        for _n in self.S_nbr_actifs.values():
            if _n["informatif"] == _etat:
                _nbr_actif = _n["data"]
        _niveau_de_batterie_moyen = 0
        for _n in self.S_niveau_de_batterie_moyen.values():
            if _n["informatif"] == _etat:
                _niveau_de_batterie_moyen = _n["data"]

        _text += "Résultat de la simulation"
        _text += "Informations sur l'état " + str(_etat) + " de la topologie du réseau\n\n"
        _text += "Niveau moyen des batteries : " + str(_niveau_de_batterie_moyen) + "\n"
        _text += "Nombre de capteurs actifs / Nombre de capteurs total : " + \
                 str(_nbr_actif) + " / " + str(_reseau.R_nbr_noeuds - 1) + \
                 " (soit " + str(int(_nbr_actif / (_reseau.R_nbr_noeuds - 1) * 100)) + \
                 "% de capteurs reliés à la passerelle)\n"
        return _text

    def SajouterDonnees(self, _reseau, _informatif=-1):
        """
            Extrait les données nécessaire au texte généré par la fonction SgenererTexte.
            Cad le nombres de capteurs reliés au puit et le niveau moyen de la batterie

        :param _reseau: Réseau, le réseau depuis lequel extraire les données
        :param _informatif: int,
        Récupère les informations depuis les stats.
        Celles-ci contiennent plus d'états transitoire (un par unité de temps)
        "informatif" contient le numéro de l'état correspondant au moment d'un changement de rôle ou fin de simulation
        -1 par default
        """

        # Récupération du nombre de capteurs connectés à la passerelle
        _, _noeuds_deconnectes = Simulateur.SfinDeVieAtteinte(_reseau)
        _nbr_noeuds_deconnectes = len(_noeuds_deconnectes)
        _nbr_actifs = _reseau.R_nbr_noeuds - _nbr_noeuds_deconnectes - 1  # Moins le puit

        # Récupération du niveau de batterie moyen
        _somme_batterie = 0
        for _noeud in _reseau.R_graphe.nodes():
            if _reseau.R_graphe.nodes()[_noeud]["role"] != Roles._PUIT:
                _somme_batterie += _reseau.R_graphe.nodes()[_noeud]["batterie"]
        _niveau_batterie_moyen = int(_somme_batterie / (_reseau.R_nbr_noeuds - 1))

        self.SajouterDonneesBrutes(_niveau_batterie_moyen, _nbr_actifs, _informatif)

    def SajouterDonneesBrutes(self, _niveau_de_batterie_moyen, _nbr_actifs, _informatif):
        """
            Ajoute les données aux attributs de la classe, utilisé par la méthode SajouterDonnees et lors de
            l'importation d'un résultat

        :param _niveau_de_batterie_moyen: Float
        :param _nbr_actifs: Entier
        :param _informatif: int,
        Récupère les informations depuis les stats.
        Celles-ci contiennent plus d'états transitoire (un par unité de temps)
        "informatif" contient le numéro de l'état correspondant au moment d'un changement de rôle ou fin de simulation
        """

        self.S_niveau_de_batterie_moyen[self.S_nombre_etats] = dict({"data": _niveau_de_batterie_moyen,
                                                                     "informatif": _informatif})
        self.S_nbr_actifs[self.S_nombre_etats] = dict({"data": _nbr_actifs,
                                                       "informatif": _informatif})
        self.S_nombre_etats += 1

    def SviderEtats(self, _garder_etat_initial):
        """
            Supprime l'ensemble des états précédemment enregistré

        :param _garder_etat_initial: Boolean, vrai si le premier état ne doit pas être supprimé
        """

        if _garder_etat_initial and self.S_nombre_etats > 0:
            self.S_nombre_etats = 1
            self.S_niveau_de_batterie_moyen = dict({0: self.S_niveau_de_batterie_moyen[0]})
            self.S_nbr_actifs = dict({0: self.S_nbr_actifs[0]})
        else:
            self.S_nombre_etats = 0
            self.S_niveau_de_batterie_moyen = dict()
            self.S_nbr_actifs = dict()
        self.S_resultats = []

    def SajouterResultat(self, _intervalle, _duree_de_vie):
        """
            Ajoute une valeur à l'ensemble des résultats de durée de vie obtenue par la simulation

        :param _intervalle: Float, L'intervalle de temps de changement de rôle correspondant au cycle de la simulation
        :param _duree_de_vie: Float, La durée de vie atteinte du réseau
        """
        _resultat = dict({"intervalle": _intervalle, "duree": _duree_de_vie})
        self.S_resultats.append(_resultat)

    def SgenererDonneesGraphiques(self):
        """
            Permet d'exporter les données dans un format exploitable par un affichage matplotlib
            Cad une liste pour les abscisses et une liste pour les ordonnées.

        :return: _graphique1 : dict({String : [float], String : [float]})
                 _graphique2 : dict({String : [float], String : [int]})
        """

        _graphique1 = dict({"x": [], "y": []})
        _graphique2 = dict({"x": [], "y": []})

        for _resultat in self.S_resultats:
            _graphique1["x"].append(_resultat["duree"])
            _graphique1["y"].append(_resultat["intervalle"])

        for _etat in range(0, self.S_nombre_etats):
            _graphique2["x"].append(self.S_nbr_actifs[_etat]["data"] * Simulateur.S_intervalle_recolte)
            _graphique2["y"].append(_etat)

        return _graphique1, _graphique2


class Statistiques(Singleton):
    pass
