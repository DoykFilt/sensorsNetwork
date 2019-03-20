"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Signaux

    Possède l'énumération Signaux qui recenses les différents signaux envoyé par les connecteurs.
    Cf ReseauControleur pour leurs sens et utilisations
"""


from enum import Enum


class Signaux(Enum):
    """
        Enumération qui liste les différents signaux du projet, elle inclue :
        - La liste des signaux émis lors d'une action de l'utilisateur sur la fenêtre principale
        - La liste des signaux émis lors d'une action de l'utilisateur sur la fenêtre de paramétrage lors de la création
        - La liste des signaux émis lors de la création d'un réseau
        - La liste des signaux émis lors de la simulation d'un réseau

    """

    # Signaux émis par la fenêtre principale
    GENERER_RESEAU = 1.0
    LANCER_SIMULATION = 1.1
    EXPORTER_XML = 1.21
    CHARGER_XML = 1.22
    EXPORTER_RESULTAT = 1.41
    IMPORTER_RESULTAT = 1.42
    ARRIERE = 1.511
    SAUT_ARRIERE = 1.512
    AVANT = 1.521
    SAUT_AVANT = 1.522
    SAUT_TEMPOREL = 1.50

    # Signaux émis par le moteur lors de la génération d'un graphe
    INITIALISATION_CREATION_GRAPHE = 2
    INFORMATION_CREATION_GRAPHE = 2.1
    AVANCEE_CREATION_GRAPHE = 2.2
    FIN_CREATION_GRAPHE = 2.3

    # Signaux émis par la fenêtre de paramétrage des créations d'un réseau
    ANNULER_PARAMETRES = 3
    VALIDER_PARAMETRES = 3.1

    # Signaux émis lors de la simulation
    NOUVEL_ETAT = 4
    INITIALISATION_SIMULATION = 4.1
    PROGRESSION_SIMULATION = 4.2
    FIN_SIMULATION = 4.3

    def __str__(self):
        """
        Surcharge de la conversion en string, renvoie la valeur correspondante
        :return String, la valeur en chaîne de caractère
        """
        return str(self.value)
