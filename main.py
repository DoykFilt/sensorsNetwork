"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module main

    Module principal, instancie les fenêtres et le contrôleur puis ouvre la fenêtre principale.

"""

import sys
from PyQt5.QtWidgets import QApplication

from Controleur.ReseauControleur import ReseauControleur
from Utilitaires.Log import Log
from Vue.FenetreCreation import FenetreCreation
from Vue.FenetrePrincipale import FenetrePrincipale


def main():
    """
        Méthode principale de l'application
    """
    _log = Log()
    # Fonction pour la réception et l'affichage de toutes les erreurs
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        _log.Lerror(traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    _app = QApplication(sys.argv)

    _log.Linfo("###### Démarrage de l'application ######")

    # Les deux fenêtres à afficher et le controleur qui fait le lien entre les deux
    _fenetre_principale = FenetrePrincipale()
    _fenetre_principale.setWindowTitle("Simulateur de Réseaux de Capteurs Dynamiques")
    _fenetre_creation = FenetreCreation()
    _fenetre_creation.setWindowTitle("Paramétrage du réseau à générer")
    _reseau_controleur = ReseauControleur(_fenetre_principale, _fenetre_creation)

    _fenetre_principale.show()

    """Retourne un exit status (0 pour succes, tout le reste pour l'echec)"""
    try:
        sys.exit(_app.exec_())
    except:
        sys.exit(0)


if __name__ == "__main__":
    main()
