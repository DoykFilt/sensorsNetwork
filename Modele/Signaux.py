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
    _GENERER_RESEAU = 1.0
    _LANCER_SIMULATION = 1.1
    _EXPORTER_XML = 1.21
    _CHARGER_XML = 1.22
    _EXPORTER_RESULTAT = 1.41
    _IMPORTER_RESULTAT = 1.42
    _ARRIERE = 1.511
    _SAUT_ARRIERE = 1.512
    _AVANT = 1.521
    _SAUT_AVANT = 1.522
    _SAUT_TEMPOREL = 1.50

    # Signaux émis par le moteur lors de la génération d'un graphe
    _INITIALISATION_CREATION_GRAPHE = 2
    _INFORMATION_CREATION_GRAPHE = 2.1
    _AVANCEE_CREATION_GRAPHE = 2.2
    _FIN_CREATION_GRAPHE = 2.3

    # Signaux émis par la fenêtre de paramétrage des créations d'un réseau
    _ANNULER_PARAMETRES = 3
    _VALIDER_PARAMETRES = 3.1

    # Signaux émis lors de la simulation
    _NOUVEL_ETAT = 4

