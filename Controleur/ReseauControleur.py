from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5 import QtCore

from Utilitaires.FileManager import FileManager
from Modele.Reseau import Reseau
from Moteur.ReseauMoteur import ReseauMoteur
from Modele.Signaux import Signaux
from Utilitaires.Log import Log
from Vue.BarreProgression import BarreProgression


class ThreadCreation(QtCore.QObject):
    """
        class ThreadCreation

        Hérite de QObject pour pouvoir posséder un objet pyqtSignal

        Thread qui permet de lancer la création d'un réseau. Renvoie le résultat dans un signal

    """
    # Les connecteurs
    # connecteur est utilisé par ReseauMoteur pour pour notifier de l'avancement de la création
    # resultat renvoie le Reseau résultant
    # finished permet d'agir une fois l'execution terminée
    TC_connecteur = QtCore.pyqtSignal(Signaux, float, str, float)
    TC_resultat = QtCore.pyqtSignal(Reseau)
    TC_finished = QtCore.pyqtSignal()

    def __init__(self, _param):
        """
            Constructeur de la classe

            :param _param : Parametre, pour la création du réseau

        """

        super().__init__()
        self.TC_moteur_reseau = ReseauMoteur(self.TC_connecteur)
        self.TC_param = _param

    def run(self):
        """
            Execute la création du réseau et emet les signaux en conséquent

        """

        self.TC_resultat.emit(self.TC_moteur_reseau.RMcreerReseau(self.TC_param))
        self.TC_finished.emit()


class ReseauControleur(QWidget):
    """
        class ReseauControleur

        Controleur qui le lien entre le modèle et la vue. Il gère toutes les intéractons avec les fenêtres

    """

    def __init__(self, _fen_principale, _fen_creation):
        """
            Constructeur de la classe

            Récupère les fenetres et leurs conecteurs

            :param _fen_principale : Le fenêtre principale FenetrePrincipale
            :param _fen_creation : La fenêtre de paramétrage FenetreCreation

        """

        super(ReseauControleur, self).__init__()

        self.RC_fen_principale = _fen_principale
        self.RC_fen_creation = _fen_creation

        self.RC_fen_principale.FPobtenirConnecteur().connect(self.RCactionSignalFenetrePrincipale)
        self.RC_fen_creation.FCobtenirConnecteur().connect(self.RCactionSignalFenetreCreation)

        self.RC_barre_progression_creation = None
        self.RC_thread = QtCore.QThread()
        self.RC_worker = None
        self.RC_resultat = None

    def RCactionSignalFenetrePrincipale(self, _signal):
        """
            Analyse le signal émit par la fenêtre principale et agit en conséquent

            :param _signal : Le signal de type Signals à analyser

        """

        # Cas de demande de génération d'un réseau : la fenêtre de création est ouverte
        if _signal == Signaux._GENERER_RESEAU:
            self.RC_fen_creation.show()

        # Cas de demande d'exportation au format XML
        if _signal == Signaux._EXPORTER_XML:

            # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où exporter le fichier
            _options = QFileDialog.Options()
            _options |= QFileDialog.DontUseNativeDialog
            _filename, _ = QFileDialog.getSaveFileName(self, "Spécifier l'endroit où exporter le fichier", "",
                                                       "Fichier XML (*.xml)", options=_options)

            # Récupère les données XML du réseau affiché et l'enregistre dans un nouveau fichier XML
            if _filename:
                _file_manager = FileManager()
                _chemin, _exist = _file_manager.FMobtenirCheminXMLLocal()
                if not _exist:
                    self.RCmessageErreur("Aucun réseau à exporter")
                else:
                    _reseau = _file_manager.FMchargerReseauDepuisXML(_chemin)
                    if _reseau is not None:
                        _file_manager.FMsauvegarderReseauVersXML(
                            _reseau,
                            _filename
                        )
                        ReseauControleur.RCmessageInformation("Le graphe a été exporté avec succès !")

        # Cas de demande d'importation depuis un fichier XML
        if _signal == Signaux._CHARGER_XML:

            # Ouvre une boite de dialogue qui demande à l'utilisateur le fichier XML contenant le réseau
            _options = QFileDialog.Options()
            _options |= QFileDialog.DontUseNativeDialog
            _filename, _ = QFileDialog.getOpenFileName(self, "Spécifier le fichier à importer", "",
                                                       "Fichier XML (*.xml)", options=_options)
            if _filename:
                _file_manager = FileManager()
                _reseau = _file_manager.FMchargerReseauDepuisXML(_filename)
                if _reseau is not None:
                    _file_manager.FMsauvegarderLocal(_reseau)
                    ReseauControleur.RCmessageInformation("Le graphe a été importé avec succès !")
                    self.RC_fen_principale.FPafficherReseau()

    def RCactionSignalFenetreCreation(self, _signal, _params=None):
        """
            Analyse le signal émit par la fenêtre creation

            :param _signal : Le signal de type Signals à analyser
            :param _params: Les paramètres envoyé dans le cas d'un signal de validation

        """

        if _signal == Signaux._ANNULER_PARAMETRES:
            self.RC_fen_creation.close()
        elif _signal == Signaux._VALIDER_PARAMETRES and _params is not None:
            self.RC_fen_creation.close()
            self.RCcreerReseau(_params)

    def RCcreerReseau(self, _param):
        """
            Lance le thread de création du Reseau et connecte ses signaux

            :param _param : Les paramètres reçus pour la création du réseau

        """

        if self.RCcontroleParametres(_param):
            # Création d'abord d'un objet ThreadCreation et mutation en Thread pour pouvoir manipuler ses connecteurs
            self.RC_worker = ThreadCreation(_param)
            self.RC_worker.moveToThread(self.RC_thread)
            self.RC_worker.TC_finished.connect(self.RC_thread.quit)

            self.RC_thread.started.connect(self.RC_worker.run)
            self.RC_thread.finished.connect(self.RCupdateAffichage)

            self.RC_worker.TC_connecteur.connect(self.RCactionSignalMoteur)
            self.RC_worker.TC_resultat.connect(self.RCactionSignalMoteurResultat)

            self.RC_thread.start()

    def RCupdateAffichage(self):
        """
            Sauvegarde en local le réseau obtenu et l'affiche dans la fenêtre principale

        """

        if self.RC_worker is not None:
            self.RC_worker.deleteLater()
        if self.RC_resultat is not None:
            _fileManager = FileManager()
            _fileManager.FMsauvegarderLocal(_reseau=self.RC_resultat)
            self.RC_fen_principale.FPafficherReseau()

    def RCactionSignalMoteur(self, _signal, _valeur, _texte, _temps):
        """
            Analyse le signal émit par la création du réseau (Objet ReseauMoteur)
            Utiliser pour instancier et faire progresser une barre de progression

            :param _signal : Le signal de type Signals à analyser
            :param _valeur: int L'avancement de la création
            :param _texte: str L'information à afficher
            :param _temps: float Le temps restant (en secondes) estimé

        """
        _log = Log()
        if _signal == Signaux._INITIALISATION_CREATION_GRAPHE:
            # Création de la fenetre
            self.RC_barre_progression_creation = BarreProgression()
            _log.info(_texte)
        elif _signal == Signaux._INFORMATION_CREATION_GRAPHE:
            # informations
            _log.info(_texte)
        elif _signal == Signaux._AVANCEE_CREATION_GRAPHE and self.RC_barre_progression_creation is not None:
            # on modifie l'avancée et on ajoute le texte
            self.RC_barre_progression_creation.BPchangementValeur(_valeur)
            if _temps == -1:
                self.RC_barre_progression_creation.BPchangementLabel("Création du réseau en cours..")
            else:
                self.RC_barre_progression_creation.BPchangementLabel("Création du réseau en cours..", _temps)
            _log.info(_texte)
        elif _signal == Signaux._FIN_CREATION_GRAPHE and self.RC_barre_progression_creation is not None:
            # on met à 100% et on ferme la fenêtre
            _log.info("Réseau créé avec succès")
            self.RC_barre_progression_creation.BPfin()

    def RCactionSignalMoteurResultat(self, _reseau):
        """
            Analyse le signal émit  à la fin de la création du réseau (Objet ReseauMoteur)

            :param _reseau : le résulat émit (Reseau)

        """
        self.RC_resultat = _reseau

    def RCcontroleParametres(self, _param):
        """
            Permet de controler les paramètres passés en paramètre. Renvoie les messages d'erreurs si il y a lieu

            :param _param : Objet Parametres

        """

        _text_erreur = ""

        if _param.P_min_distance > _param.P_max_distance:
            _text_erreur += "La distance minimum doit être inférieure ou égale à la distance maximale\n"
        if _param.P_max_size < 10:
            _text_erreur += "La taille maximale doit être supérieur à 10\n"
        if _param.P_marge > _param.P_max_size / 2:
            _text_erreur += "La marge doit être inférieure à la moitiée de la taille maximale\n"
        if _param.P_nbr_capteurs < 2:
            _text_erreur += "Le nombre de capteurs doit être supérieur à 1\n"

        if _text_erreur != "":
            ReseauControleur.RCmessageErreur(_text_erreur)
            return False
        return True

    @staticmethod
    def RCmessageErreur(_message_erreur):
        """
            Permet d'afficher un message d'erreur dans une boite de dialogue

            :param _message_erreur : Le message à afficher

        """
        _log = Log()
        _log.error(_message_erreur)

        _boite = QMessageBox()
        _boite.setIcon(QMessageBox.Critical)
        _boite.setText("Erreur(s)")
        _boite.setWindowTitle("Erreur(s)")
        _boite.setDetailedText("Le(s) erreur(s) suivante(s) ont été détectée(s) : \n" + _message_erreur)
        _boite.setStandardButtons(QMessageBox.Ok)

        _boite.exec_()

    @staticmethod
    def RCmessageInformation(_message_info):
        """
            Permet d'afficher un message d'information dans une boite de dialogue

            :param _message_info : Le message à afficher

        """
        _log = Log()
        _log.info(_message_info)

        _boite = QMessageBox()
        _boite.setIcon(QMessageBox.Information)
        _boite.setText(_message_info)
        _boite.setWindowTitle("Information(s))")
        _boite.setStandardButtons(QMessageBox.Ok)

        _boite.exec_()
