import sys
from PyQt5.QtWidgets import QApplication

from Controleur.ReseauControleur import ReseauControleur
from Utilitaires.Log import Log
from Vue.FenetreCreation import FenetreCreation
from Vue.FenetrePrincipale import FenetrePrincipale


def main():

    _log = Log()
    # Fonction pour la réception et l'affichage de toutes les erreurs
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        _log.error(traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    _app = QApplication(sys.argv)

    _log.info("Démarrage de l'application")
    # Les deux fenêtres à afficher et le controleur qui fait le lien entre les deux
    _fenetre_principale = FenetrePrincipale()
    _fenetre_principale.setWindowTitle("Simulateur de la consommation énergétique de réseaux de capteurs sans fils")
    _fenetre_creation = FenetreCreation()
    _reseau_controleur = ReseauControleur(_fenetre_principale, _fenetre_creation)

    _fenetre_principale.show()

    """Retourne un exit status 
    (0 pour succes, tout le reste pour l'echec"""
    try:
        sys.exit(_app.exec_())
    except:
        sys.exit(0)


if __name__ == "__main__":
    main()
