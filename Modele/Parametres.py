"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Parametres

    Module qui possède les classes permettant de stocker les Paramètres :
        - Parametres
        - ParametresCreation
        - ParametresSimulation
"""


class Parametres:
    """
        class Parametres

        Classe mère pour stocker des paramètres

    """
    pass


class ParametresCreation(Parametres):
    """
        class ParametresCreation, hérite de Parametres

        Regroupe les paramètres utilisés pour la construction d'un réseau.

        :var self.PC_max_size : int, la taille maximale que peut prendre la surface de répartition des capteurs
        :var self.PC_marge : int, la marge qui doit être respecter sur les rebords de la surface
        :var self.PC_max_distance : int, la distance maximale pour que deux capteurs établissent une connection
        :var self.PC_min_distance : int, la distance minimale à respecter entre deux capteurs
        :var self.PC_nbr_capteurs : int, le nombre de capteurs
        :var self.PC_capacitees_batteries : int, la capacité de la batterie des capteurs
        :var self.PC_nbr_puits : int, le nombre de passerelles à placer dans le réseau

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
        self.PC_max_size = _max_size
        self.PC_marge = _marge
        self.PC_max_distance = _max_distance
        self.PC_min_distance = _min_distance
        self.PC_nbr_capteurs = _nbr_capteurs
        self.PC_capacitees_batteries = _capacitees_batteries
        self.PC_nbr_puits = _nbr_puits


# TODO : Développer la classe en parallèle d'une fenêtre de paramétrage pour le lancement de la simulation
class ParametresSimulation(Parametres):
    """
        class ParametresSimulation, hérite de Parametres

        Regroupe les paramètres utilisés pour la simulation d'un réseau.

    """
    pass
