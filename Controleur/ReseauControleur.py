from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5 import QtCore

from Moteur.Simulateur import Simulateur
from Utilitaires.FileManager import FileManager
from Modele.Reseau import Reseau
from Moteur.Generateur import Generateur
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
    # connecteur est utilisé par Generateur pour pour notifier de l'avancement de la création
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
        self.TC_moteur_reseau = Generateur(self.TC_connecteur)
        self.TC_param = _param

    def run(self):
        """
            Execute la création du réseau et emet les signaux en conséquent

        """

        _reseau = self.TC_moteur_reseau.GcreerReseau(self.TC_param)

        # Enregistrement du réseau obtenu
        _file_manager = FileManager()
        _file_manager.FMviderEtats(_garder_etat_initial=False)
        _file_manager.FMenregistrerEtat(_reseau=_reseau)

        # Ajout des statistiques relevant de cet état initial
        from Controleur.Statistiques import Statistiques
        _statistiques = Statistiques()
        _statistiques.SajouterDonnees(_reseau, _informatif=0)
        _file_manager.FMsauvegarderStatistiques()

        self.TC_resultat.emit(_reseau)
        self.TC_finished.emit()


class ThreadSimulation(QtCore.QObject):
    """
        class ThreadSimulation

        Hérite de QObject pour pouvoir posséder un objet pyqtSignal

        Thread qui permet de lancer la simulation du réseau. Renvoie le informations de l'avancement dans un signal

    """
    # Les connecteurs
    # connecteur est utilisé par Simulator pour pour notifier de l'avancement de la simulation
    TS_connecteur = QtCore.pyqtSignal(Signaux, dict)
    TS_finished = QtCore.pyqtSignal()

    def __init__(self, _reseau):
        """
            Constructeur de la classe

            :param _reseau : Reseau, le réseau sur lequel appliquer la simulation

        """

        super().__init__()
        self.TS_simulateur = Simulateur(self.TS_connecteur)
        self.TS_reseau = _reseau

    def run(self):
        """
            Execute la simulation du réseau et emet les signaux en conséquent
        """

        self.TS_simulateur.SlancerSimulation(self.TS_reseau)
        self.TS_finished.emit()


class ReseauControleur:
    """
        class Simulateur

        Controleur qui le lien entre le modèle et la vue. Il gère toutes les intéractons avec les fenêtres et permet
        de lancer la génération d'un réseau ainsi que la simulation

    """

    def __init__(self, _fen_principale, _fen_creation):
        """
            Constructeur de la classe

            Récupère les fenetres et leurs conecteurs

            :param _fen_principale : Le fenêtre principale FenetrePrincipale
            :param _fen_creation : La fenêtre de paramétrage FenetreCreation

        """

        self.RC_fen_principale = _fen_principale
        self.RC_fen_creation = _fen_creation

        self.RC_fen_principale.FPobtenirConnecteur().connect(self.RCactionSignalFenetrePrincipale)
        self.RC_fen_creation.FCobtenirConnecteur().connect(self.RCactionSignalFenetreCreation)

        self.RC_barre_progression_creation = None
        self.RC_barre_progression_simulation = None
        self.RC_thread = QtCore.QThread()
        self.RC_worker = None
        self.RC_resultat = None

        _file_manager = FileManager()
        _file_manager.FMchargerStatistiques()
        self.RC_fen_principale.FPafficherReseau()

    def RCactionSignalFenetrePrincipale(self, _signal, _saut=0):
        """
            Analyse le signal émit par la fenêtre principale et agit en conséquent

            :param _signal : Le signal de type Signals à analyser
            :param _saut : entier utilisé uniquement dans le cas d'un changement de valeur non incrémentale du choix de
            l'état à afficher

        """

        # Cas de demande de génération d'un réseau : la fenêtre de création est ouverte
        if _signal == Signaux._GENERER_RESEAU:
            self.RC_fen_creation.show()

        # Cas de demande d'exportation au format XML
        if _signal == Signaux._EXPORTER_XML:

            _file_manager = FileManager()
            _reseau = _file_manager.FMchargerEtat(self.RC_fen_principale.FP_selection)

            if _reseau is None:
                ReseauControleur.RCmessageErreur("Aucun réseau à exploiter")

            else:
                # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où exporter le fichier
                _options = QFileDialog.Options()
                _options |= QFileDialog.DontUseNativeDialog
                _filename, _ = QFileDialog.getSaveFileName(self, "Spécifier l'endroit où exporter le fichier", "",
                                                           "Fichier XML (*.xml)", options=_options)

                # Récupère les données XML du réseau affiché et l'enregistre dans un nouveau fichier XML
                if _filename:
                    _file_manager.FMsauvegarderReseauVersXML(_reseau, _filename)
                    ReseauControleur.RCmessageInformation("Le réseau a été exporté avec succès !")

        # Cas de demande d'importation depuis un fichier XML
        if _signal == Signaux._CHARGER_XML:
            try:
                # Ouvre une boite de dialogue qui demande à l'utilisateur le fichier XML contenant le réseau
                _options = QFileDialog.Options()
                _options |= QFileDialog.DontUseNativeDialog
                _filename, _ = QFileDialog.getOpenFileName(self, "Spécifier le fichier à importer", "",
                                                           "Fichier XML (*.xml)", options=_options)
                if _filename:
                    _file_manager = FileManager()
                    _reseau = _file_manager.FMchargerReseauDepuisXML(_filename)
                    if _reseau is not None:
                        _file_manager.FMviderEtats(_garder_etat_initial=False)
                        _file_manager.FMenregistrerEtat(_reseau)

                        ReseauControleur.RCmessageInformation("Le réseau a été importé avec succès !")
                        self.RC_fen_principale.FPuptdateLabelSelection(0, 1)
                        self.RC_fen_principale.FPafficherReseau()
            except Exception as _e:
                ReseauControleur.RCmessageErreur("Erreur lors du chargement du fichier : " + str(_e))

        # Cas de demande d'exportation du résultat de la simulation
        if _signal == Signaux._EXPORTER_RESULTAT:
            _file_manager = FileManager()
            if len(_file_manager.FMlisterEtats()) == 0:
                ReseauControleur.RCmessageErreur("Aucune données à exporter")

            else:
                # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où exporter le dossier
                _options = QFileDialog.Options()
                _options |= QFileDialog.DontUseNativeDialog
                _options |= QFileDialog.ShowDirsOnly
                _filename = QFileDialog.getExistingDirectory(self, "Spécifier l'endroit où exporter l'ensemble des "
                                                                   "données", "", options=_options)

                _done, _message = _file_manager.FMexporterResultat(_filename)

                if not _done:
                    ReseauControleur.RCmessageErreur("Erreur lors de l'exportation : \n" + _message)
                else:
                    ReseauControleur.RCmessageInformation("L'ensemble des fichiers a été exporté avec succès !")

        # Cas de demande d'importation du résultat de la simulation
        if _signal == Signaux._IMPORTER_RESULTAT:
            # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où se situe le dossier à importer
            _options = QFileDialog.Options()
            _options |= QFileDialog.DontUseNativeDialog
            _options |= QFileDialog.ShowDirsOnly
            _filename = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier à importer", "",
                                                         options=_options)
            _file_manager = FileManager()
            _nbr_imported, _message = _file_manager.FMimporterResultat(_filename)

            if _nbr_imported == 0:
                ReseauControleur.RCmessageErreur("Erreur lors de l'exportation : \n" + _message)
            else:
                ReseauControleur.RCmessageInformation("L'ensemble des fichiers a été exporté avec succès !")
                self.RC_fen_principale.FPuptdateLabelSelection(0, _nbr_imported)
                self.RC_fen_principale.FPafficherReseau()

        # Cas de demande de lancement de la simulation
        if _signal == Signaux._LANCER_SIMULATION:
            # TODO : Ajouter une fenêtre de paramétrage
            self.RClancerSimulation()

        # Cas de la demande d'affichage de l'état précédent
        if _signal == Signaux._ARRIERE:
            if self.RC_fen_principale.FP_selection > 0:
                self.RC_fen_principale.FPuptdateLabelSelection(self.RC_fen_principale.FP_selection - 1,
                                                               self.RC_fen_principale.FP_total)
                self.RC_fen_principale.FPafficherReseau()

        if _signal == Signaux._SAUT_ARRIERE:
            # TODO Sprint 3 : Permettre la navigation entre chaque changement de rôle
            pass

        # Cas de la demande de l'affichage de l'état suivant
        if _signal == Signaux._AVANT:
            if self.RC_fen_principale.FP_selection < self.RC_fen_principale.FP_total - 1:
                self.RC_fen_principale.FPuptdateLabelSelection(self.RC_fen_principale.FP_selection + 1,
                                                               self.RC_fen_principale.FP_total)
                self.RC_fen_principale.FPafficherReseau()

        if _signal == Signaux._SAUT_AVANT:
            # TODO Sprint 3 : Permettre la navigation entre chaque changement de rôle
            pass

        # Cas de la demande de changement de valeur brusque de l'état affiché
        if _signal == Signaux._SAUT_TEMPOREL:
            self.RC_fen_principale.FPuptdateLabelSelection(_saut, self.RC_fen_principale.FP_total)
            self.RC_fen_principale.FPafficherReseau()

    def RClancerSimulation(self):
        """
            Démarre, dans un thread, la simulation sur le réseau affiché et connecte ses signaux

        """

        _file_manager = FileManager()
        _file_manager.FMviderEtats(_garder_etat_initial=True)

        _reseau = _file_manager.FMchargerEtat(0)

        if _reseau is None:
            ReseauControleur.RCmessageErreur("Aucun réseau à exploiter")
        else:
            # Création d'abord d'un objet ThreadSimulation et mutation en Thread pour pouvoir manipuler ses connecteurs
            self.RC_worker = ThreadSimulation(_reseau)
            self.RC_worker.moveToThread(self.RC_thread)
            self.RC_worker.TS_finished.connect(self.RC_thread.quit)

            self.RC_thread.started.connect(self.RC_worker.run)
            self.RC_thread.finished.connect(self.RC_fen_principale.FPafficherReseau)

            self.RC_worker.TS_connecteur.connect(self.RCactionSignalSimulateur)

            self.RC_thread.start()

    def RCactionSignalSimulateur(self, _signal, _datas):
        """
            Analyse le signal émit par le simulateur

            :param _signal : Enum Signaux
            :param _datas : Dict(String : Objet) Les données envoyé lors de l'émission du signal

            Associations :
            Signaux._NOUVEL_ETAT => etat, total
            Signaux._INITIALISATION_SIMULATION => None
            Signaux._PROGRESSION_SIMULATION => avancee, text
            Signaux._FIN_SIMULATION => duree

        """
        # Cas où un nouvel état a été enregistré et est à afficher (généralement à la fin de la simulation et à chaque
        # changement de rôle des capteurs
        if _signal == Signaux._NOUVEL_ETAT:
            print(_datas["etat"])
            print(_datas["total"])
            self.RC_fen_principale.FPuptdateLabelSelection(_datas["etat"], _datas["total"])
            self.RC_fen_principale.FPafficherReseau()

        # Au début de la simulation, initilisation de la barre de progression
        elif _signal == Signaux._INITIALISATION_SIMULATION:
            self.RC_barre_progression_simulation = BarreProgression()

        # Quand on veut modifier les valeurs de la barre de progression
        elif _signal == Signaux._PROGRESSION_SIMULATION:
            self.RC_barre_progression_simulation.BPchangementValeur(_datas["avancee"])
            self.RC_barre_progression_simulation.BPchangementLabel(_datas["text"])

        # A la fin de la simulation
        elif _signal == Signaux._FIN_SIMULATION :
            if self.RC_barre_progression_simulation is not None:
                # on met à 100% et on ferme la fenêtre
                self.RC_barre_progression_simulation.BPfin()
            self.RCmessageInformation("Simulation terminée, temps d'exécution : " + str(_datas["duree"]) + " secondes")

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
            self.RC_thread.finished.connect(self.RC_fen_principale.FPafficherReseau)

            self.RC_worker.TC_connecteur.connect(self.RCactionSignalMoteur)
            self.RC_worker.TC_resultat.connect(self.RCactionSignalMoteurResultat)

            self.RC_thread.start()

    def RCactionSignalMoteur(self, _signal, _valeur, _texte, _temps):
        """
            Analyse le signal émit par la création du réseau (Objet Generateur)
            Utiliser pour instancier et faire progresser une barre de progression

            :param _signal : Le signal de type Signals à analyser
            :param _valeur: int L'avancement de la création
            :param _texte: str L'information à afficher
            :param _temps: float Le temps restant (en secondes) estimé

        """
        _log = Log()

        # Création de la fenetre
        if _signal == Signaux._INITIALISATION_CREATION_GRAPHE:
            self.RC_barre_progression_creation = BarreProgression()
            _log.Linfo(_texte)

        # Informations relatives à l'avancement
        elif _signal == Signaux._INFORMATION_CREATION_GRAPHE:
            _log.Linfo(_texte)

        # Gestion de la barre de progression
        elif _signal == Signaux._AVANCEE_CREATION_GRAPHE and self.RC_barre_progression_creation is not None:
            # on modifie l'avancée et on ajoute le texte
            self.RC_barre_progression_creation.BPchangementValeur(_valeur)
            if _temps == -1:
                self.RC_barre_progression_creation.BPchangementLabel("Création du réseau en cours..")
            else:
                self.RC_barre_progression_creation.BPchangementLabel("Création du réseau en cours..", _temps)
            _log.Linfo(_texte)

        # Fin de la création du graphe
        elif _signal == Signaux._FIN_CREATION_GRAPHE and self.RC_barre_progression_creation is not None:
            # on met à 100% et on ferme la fenêtre
            _log.Linfo("Réseau créé avec succès")
            self.RC_barre_progression_creation.BPfin()

    def RCactionSignalMoteurResultat(self, _reseau):
        """
            Récupère le réseau créé par le générateur

            :param _reseau : le résulat émit (Reseau)

        """

        self.RC_resultat = _reseau

        self.RC_fen_principale.FPuptdateLabelSelection(_selection=0, _total=1)

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
        _log.Lerror(_message_erreur)

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
        _log.Linfo(_message_info)

        _boite = QMessageBox()
        _boite.setIcon(QMessageBox.Information)
        _boite.setText(_message_info)
        _boite.setWindowTitle("Information(s))")
        _boite.setStandardButtons(QMessageBox.Ok)

        _boite.exec_()
