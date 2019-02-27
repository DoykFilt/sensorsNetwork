from Modele.Roles import Roles
from Moteur.Simulateur import Simulateur
from Utilitaires.FileManager import FileManager


class Singleton:

    # Elements clé pour la création d'un singleton en python
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls)
            cls.__instance.__initialized = False
            cls.__instance.__init__()
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.S_nombre_etats = 0
            self.S_niveau_de_batterie_moyen = dict()
            self.S_nbr_actifs = dict()
            self.S_resultats = []

            self.__initialized = True

    def SgenererTexte(self, _etat):
        _text = ""
        _file_manager = FileManager()

        if _etat < 0 or _etat >= self.S_nombre_etats:
            return ""

        _reseau = _file_manager.FMchargerEtat(_etat)
        if _reseau is None:
            return ""

        _text += "Informations sur l'état " + str(_etat) + " du résultat de la simulation\n\n"
        _text += "Niveau moyen des batteries : " + str(self.S_niveau_de_batterie_moyen[_etat]) + "\n"
        _text += "Nombre de capteurs actifs / Nombre de capteurs total : " + \
                 str(self.S_nbr_actifs[_etat]) + " / " + str(_reseau.R_nbr_noeuds - 1) + \
                 " (soit " + str(int(self.S_nbr_actifs[_etat] / (_reseau.R_nbr_noeuds - 1) * 100)) + \
                 "% de capteurs reliés à la passerelle)\n"
        return _text

    def SajouterDonnees(self, _reseau):

        _, _noeuds_deconnectes = Simulateur.SfinDeVieAtteinte(_reseau)
        _nbr_noeuds_deconnectes = len(_noeuds_deconnectes)
        self.S_nbr_actifs[self.S_nombre_etats] = _reseau.R_nbr_noeuds -_nbr_noeuds_deconnectes - 1 # moins le puit

        _somme_batterie = 0
        for _noeud in _reseau.R_graphe.nodes():
            if _reseau.R_graphe.nodes()[_noeud]["role"] != Roles._PUIT:
                _somme_batterie += _reseau.R_graphe.nodes()[_noeud]["batterie"]
        self.S_niveau_de_batterie_moyen[self.S_nombre_etats] = int(_somme_batterie / (_reseau.R_nbr_noeuds - 1))

        self.S_nombre_etats += 1

    def SajouterDonneesBrutes(self, _niveau_de_batterie_moyen, _nbr_actifs):

        self.S_niveau_de_batterie_moyen[self.S_nombre_etats] = _niveau_de_batterie_moyen
        self.S_nbr_actifs[self.S_nombre_etats] = _nbr_actifs
        self.S_nombre_etats += 1

    def SviderEtats(self, _garder_etat_initial):

        if _garder_etat_initial and self.S_nombre_etats > 0:
            self.S_nombre_etats = 1
            self.S_niveau_de_batterie_moyen = dict({0: self.S_niveau_de_batterie_moyen[0]})
            self.S_nbr_actifs = dict({0: self.S_nbr_actifs[0]})
            self.S_resultats = [self.S_resultats[0]]
        else:
            self.S_nombre_etats = 0
            self.S_niveau_de_batterie_moyen = dict()
            self.S_nbr_actifs = dict()
        self.S_resultats = []

    def SajouterResultat(self, _intervalle, _duree_de_vie):
        _resultat = dict({"intervalle": _intervalle, "duree": _duree_de_vie})
        self.S_resultats.append(_resultat)

    def SgenererDonneesGraphiques(self):

        _graphique1 = dict({"x": [], "y": []})
        _graphique2 = dict({"x": [], "y": []})

        for _resultat in self.S_resultats:
            _graphique1["x"].append(_resultat["duree"])
            _graphique1["y"].append(_resultat["intervalle"])

        for _etat in range(0, self.S_nombre_etats):
            _graphique2["x"].append(self.S_nbr_actifs[_etat] * Simulateur.S_intervalle_recolte)
            _graphique2["y"].append(_etat)

        return _graphique1, _graphique2


class Statistiques(Singleton):
    pass
