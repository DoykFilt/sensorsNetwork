

# TODO : Faire hériter d'une classe Parametres deux filles : ParametresCreation et ParametresSimulation
class Parametres:
    """
        class Parametres

        Regroupe les paramètres utilisés pour la construction d'un réseau

    """
    def __init__(self,
                 _max_size,
                 _marge,
                 _max_distance,
                 _min_distance,
                 _nbr_capteurs,
                 _capacitees_batteries,
                 _nbr_puits):

        """
            Constructeur de la classe

            :param _max_size : entier
            :param _marge : entier
            :param _max_distance : entier
            :param _min_distance : entier
            :param _nbr_capteurs : entier
            :param _capacitees_batteries : entier
            :param _nbr_puits : entier

        """
        self.P_max_size = _max_size
        self.P_marge = _marge
        self.P_max_distance = _max_distance
        self.P_min_distance = _min_distance
        self.P_nbr_capteurs = _nbr_capteurs
        self.P_capacitees_batteries = _capacitees_batteries
        self.P_nbr_puits = _nbr_puits

