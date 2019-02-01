from enum import Enum


class Signaux(Enum):
    """
        Enumération qui liste les différents signaux du projet

    """

    # Signaux émis par la fenêtre principale
    _GENERER_RESEAU = 1
    _LANCER_SIMULATION = 1.1
    _EXPORTER_XML = 1.2
    _CHARGER_XML = 1.3
    _EXPORTER_RESULTAT = 1.4

    # Signaux émis par le moteur lors de la génération d'un graphe
    _INITIALISATION_CREATION_GRAPHE = 2
    _INFORMATION_CREATION_GRAPHE = 2.1
    _AVANCEE_CREATION_GRAPHE = 2.2
    _FIN_CREATION_GRAPHE = 2.3

    # Signaux émis par la fenêtre de paramétrage des créations de graphe
    _ANNULER_PARAMETRES = 3
    _VALIDER_PARAMETRES = 3.1

