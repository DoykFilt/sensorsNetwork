"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module ReseauControleur

    Fait le lien entre les vues, les modèles et les moteurs de la simulation.

    Possède trois classes :
    - ThreadCreation : Thread qui permet de lancer la génération du graphique en parrallèle
    - ThreadSimulation : Thread qui permet de lancer la simulation du réseau en parrallèle
    - ReseauControleur : Le contrôleur de l'application
"""
import textwrap

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5 import QtCore

from Moteur.Simulateur import Simulateur
from Utilitaires.FileManager import FileManager
from Modele.Reseau import Reseau
from Moteur.Generateur import Generateur
from Modele.Signaux import Signaux
from Utilitaires.Log import Log
from Vue.BarreProgression import BarreProgression


_log = Log()


class ThreadCreation(QtCore.QObject):
    """
        class ThreadCreation

        Hérite de QObject pour pouvoir posséder des objets pyqtSignal

        Thread qui permet de lancer la création d'un réseau. Renvoie le résultat dans un signal

        :var self.TC_moteur_reseau : Generateur, Le moteur générateur de Réseau
        :var self.TC_param : ParametresCreation, Les paramètres pour la génération
        :var self.TC_connecteur : QtCore.pyqtSignal, Utilisé par Generateur pour notifier le controleur de l'avancement
        de la création
        :var self.TC_resultat : QtCore.pyqtSignal, Permet de renvoyer au contrôleur le réseau résultant
        :var self.TC_finished : QtCore.pyqtSignal, Permet de notifier le contrôleur de la fin de la génération

    """

    # Déclaration des connecteurs
    TC_connecteur = QtCore.pyqtSignal(Signaux, float, str, float)
    TC_resultat = QtCore.pyqtSignal(Reseau)
    TC_finished = QtCore.pyqtSignal()

    def __init__(self, _param):
        """
            Constructeur de la classe

            :param _param : Parametre, Les paramètres pour la génération

        """
        super().__init__()
        _log.Linfo("Init -- ThreadCreation")

        self.TC_moteur_reseau = Generateur(self.TC_connecteur)
        self.TC_param = _param

    def run(self):
        """
            Execute la création du réseau et emet les signaux en conséquent

        """
        _log.Linfo("Début -- ThreadCreation.run")

        _reseau = self.TC_moteur_reseau.GcreerReseau(self.TC_param)

        # Enregistrement du réseau obtenu
        _file_manager = FileManager()
        _file_manager.FMviderEtats(_garder_etat_initial=False)
        _file_manager.FMenregistrerEtat(_reseau=_reseau, _show_html=True)

        # Ajout des statistiques relevant de cet état initial
        from Controleur.Statistiques import Statistiques
        _statistiques = Statistiques()
        _statistiques.SajouterDonnees(_reseau, 0)
        _file_manager.FMsauvegarderStatistiques()

        # Envoie des signaux
        self.TC_resultat.emit(_reseau)
        self.TC_finished.emit()

        _log.Linfo("Fin -- ThreadCreation.run")


class ThreadSimulation(QtCore.QObject):
    """
        class ThreadSimulation

        Hérite de QObject pour pouvoir posséder des objets pyqtSignal

        Thread qui permet de lancer la simulation du réseau.

        :var self.TS_simulateur, Simulateur : Le simulateur de la vie du réseau
        :var self.TS_reseau, Reseau : Le réseau sur lequel appliquer la simulation
        :var self.TS_show_html, Booléen : Permet de définir si l'état du réseau doit être affiché pendant la simulation
        :var self.TS_connecteur, QtCore.pyqtSignal : Utilisé par Generateur pour notifier le controleur de l'avancement
        de la simulation
        :var self.TS_finished, QtCore.pyqtSignal : Permet de notifier le contrôleur de la fin de la simulation

    """

    # Les connecteurs
    TS_connecteur = QtCore.pyqtSignal(Signaux, dict)
    TS_finished = QtCore.pyqtSignal()

    def __init__(self, _reseau, _show_html):
        """
            Constructeur de la classe

            :param _reseau : Reseau, le réseau sur lequel appliquer la simulation

        """
        super().__init__()
        _log.Linfo("Init -- ThreadSimulation")

        self.TS_simulateur = Simulateur(self.TS_connecteur)
        self.TS_reseau = _reseau
        self.TS_show_html = _show_html

    def run(self):
        """
            Execute la simulation du réseau et emet les signaux en conséquent
        """
        _log.Linfo("Début -- ThreadSimulation.run")

        self.TS_simulateur.SlancerSimulation(self.TS_reseau, self.TS_show_html)
        self.TS_finished.emit()

        _log.Linfo("Fin -- ThreadSimulation.run")


class ReseauControleur (QFileDialog):
    """
        class Simulateur

        Controleur qui fait le lien entre le modèle et la vue. Il gère toutes les intéractons avec les fenêtres et les
        moteurset. Permet de lancer la génération d'un réseau ainsi que la simulation de sa vie

        :var self.RC_fen_principale, FenetrePrincipale
        :var self.RC_fen_creation, FenetreCreation

        :var self.RC_barre_progression_creation, BarreProgression : La barre de progression associée à l'avancement de
        la création du réseau
        :var self.RC_barre_progression_simulation, BarreProgression : La barre de progression associée à l'avancement
        de la simulation

        :var self.RC_thread, QtCore.QThread : Le thread receptacle qui recevra un objet ThreadSimulation ou
        ThreadCreation pour le lancer
        :var self.RC_worker, ThreadSimulation ou ThreadCreation : Instancie un objet qui sera transformé en QThread

        :var self.RC_resultat, Reseau : L'objet dans lequel sera stocké le résultat de la génération

    """

    def __init__(self, _fen_principale, _fen_creation, *__args):
        """
            Constructeur de la classe

            Récupère les fenetres et branche leurs conecteurs

            :param _fen_principale : Le fenêtre principale FenetrePrincipale
            :param _fen_creation : La fenêtre de paramétrage FenetreCreation
            :param __args : Arguments associés à l'héritage de QFileDialog

        """
        super().__init__(*__args)
        _log.Linfo("Init -- ReseauControleur")

        self.RC_fen_principale = _fen_principale
        self.RC_fen_creation = _fen_creation

        self.RC_barre_progression_creation = None
        self.RC_barre_progression_simulation = None

        self.RC_thread = QtCore.QThread()
        self.RC_worker = None
        self.RC_resultat = None

        self.RC_file_manager = FileManager()
        from Controleur.Statistiques import Statistiques
        self.RC_statistiques = Statistiques()

        self.RC_fen_principale.FPobtenirConnecteur().connect(self.RCactionSignalFenetrePrincipale)
        self.RC_fen_creation.FCobtenirConnecteur().connect(self.RCactionSignalFenetreCreation)

        self.RC_fen_principale.FPafficherReseau()

    def RCactionSignalFenetrePrincipale(self, _signal, _data=0):
        """
            Analyse le signal émit par la fenêtre principale et agit en conséquent. Un signal est émit par la fenêtre
            principale lorsque l'utilisateur intéragit avec un boutton

            :param _signal : Enum Signaux, Le signal de type Signals à analyser. Liste des signaux concernés :
                - GENERER_RESEAU : Cas de demande de génération d'un réseau : la fenêtre de création est ouverte
                - EXPORTER_XML : Cas de demande d'exportation d'un état du réseau au format XML
                - CHARGER_XML : Cas de demande d'importation d'un état d'un réseau depuis un fichier XML
                - EXPORTER_RESULTAT : Cas de demande d'exportation du résultat de la simulation, cad l'ensemble des
                    états dans lequel est passé le réseau
                - IMPORTER_RESULTAT : Cas de demande d'importation d'un résultat d'une simulation
                - LANCER_SIMULATION : Cas de demande de lancement de la simulation
                - ARRIERE : Cas de la demande d'affichage de l'état précédent
                - AVANT : Cas de la demande d'affichage de l'état suivant
                - SAUT_ARRIERE : Cas de la demande d'affichage du cycle précédent
                - SAUT_AVANT : Cas de la demande d'affichage du cycle suivant
                - SAUT_TEMPOREL : Cas doù l'utilisateur utilise la barre glissante pour choisir un état précis
            :param _data : est utilisé pour transmettre des données supplémentaires dans le signal. Cas d'utilisations :
                - _LANCER_SIMULATION : permet de transmettre la volonté de l'utilisateur à vouloir afficher les états
                    dans lesquels passe le réseau lors de la simulation. Deux états : 0 = False, R\\{0] = True
                - _SAUT_TEMPOREL : permet de transmettre la position du curseur de la barre défillante. Entier

        """
        _log.Linfo("Début ## ReseauControleur.RCactionSignalFenetrePrincipale")
        _log.Linfo("Info ## Signal = " + str(_signal))

        # =============================================================================
        # Cas de demande de génération d'un réseau : la fenêtre de création est ouverte
        # Signal GENERER_RESEAU
        # =============================================================================
        if _signal == Signaux.GENERER_RESEAU:
            self.RC_fen_creation.show()

        # ==============================================================
        # Cas de demande d'exportation d'un état du réseau au format XML
        # Signal : EXPORTER_XML
        # ==============================================================
        elif _signal == Signaux.EXPORTER_XML:

            # Récupère les données XML du réseau affiché
            _reseau = self.RC_file_manager.FMchargerEtat(self.RC_fen_principale.FP_selection)

            if _reseau is None:
                ReseauControleur.RCmessageErreur("Aucun réseau à exploiter")

            else:
                # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où exporter le fichier
                _options = QFileDialog.Options()
                _options |= QFileDialog.DontUseNativeDialog
                _filename, _ = QFileDialog.getSaveFileName(self, "Spécifier l'endroit où exporter le fichier", "",
                                                           "Fichier XML (*.xml)", options=_options)

                # Enregistre le réseau dans un nouveau fichier XML
                if _filename:
                    self.RC_file_manager.FMsauvegarderReseauVersXML(_reseau, _filename)
                    ReseauControleur.RCmessageInformation("Le réseau a été exporté avec succès !")

        # ========================================================================
        # Cas de demande d'importation d'un état d'un réseau depuis un fichier XML
        # Signal : CHARGER_XML
        # ========================================================================
        elif _signal == Signaux.CHARGER_XML:
            try:
                # Ouvre une boite de dialogue qui demande à l'utilisateur le fichier XML contenant le réseau
                _options = QFileDialog.Options()
                _options |= QFileDialog.DontUseNativeDialog
                _filename, _ = QFileDialog.getOpenFileName(self, "Spécifier le fichier à importer", "",
                                                           "Fichier XML (*.xml)", options=_options)

                # Si le fichier existe
                if _filename:
                    # Charge le réseau
                    _reseau = self.RC_file_manager.FMchargerReseauDepuisXML(_filename)
                    if _reseau is not None:
                        # Puis l'enregistre en local pour le manipuler. Supprime les états déjà présents
                        self.RC_file_manager.FMviderEtats(_garder_etat_initial=False)
                        self.RC_file_manager.FMenregistrerEtat(_reseau, _show_html=True)

                        _log.Linfo("Info ## Réseau importé")
                        ReseauControleur.RCmessageInformation("Le réseau a été importé avec succès !")
                        self.RC_fen_principale.FPuptdateLabelSelection(0, 1)
                        self.RC_fen_principale.FPafficherReseau()
            except Exception as _e:
                _log.Lerror("Erreur lors du chargement du fichier : " + str(_e))
                ReseauControleur.RCmessageErreur("Erreur lors du chargement du fichier : " + str(_e))

        # ============================================================================================================
        # Cas de demande d'exportation du résultat de la simulation, cad l'ensemble des états dans lequel est passé le
        # réseau
        # Signal : EXPORTER_RESULTAT
        # ============================================================================================================
        elif _signal == Signaux.EXPORTER_RESULTAT:
            if len(self.RC_file_manager.FMlisterEtats()) == 0:
                _log.Linfo("WARNING ## Aucune données à exporter")
                ReseauControleur.RCmessageErreur("Aucune données à exporter")

            else:
                # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où exporter le dossier
                _options = QFileDialog.Options()
                _options |= QFileDialog.DontUseNativeDialog
                _options |= QFileDialog.ShowDirsOnly
                _filename = QFileDialog.getExistingDirectory(self, "Spécifier l'endroit où exporter l'ensemble des "
                                                                   "données", "", options=_options)

                _done, _message = self.RC_file_manager.FMexporterResultat(_filename)

                if not _done:
                    _log.Lerror("Erreur lors de l'exportation : \n" + _message)
                    ReseauControleur.RCmessageErreur("Erreur lors de l'exportation : \n" + _message)
                else:
                    _log.Linfo("L'ensemble des fichiers a été exporté avec succès !")
                    ReseauControleur.RCmessageInformation("L'ensemble des fichiers a été exporté avec succès !")

        # ===========================================================
        # Cas de demande d'importation d'un résultat d'une simulation
        # Signal : IMPORTER_RESULTAT
        # ===========================================================
        elif _signal == Signaux.IMPORTER_RESULTAT:
            # Ouvre une boite de dialogue qui demande à l'utilisateur l'endroit où se situe le dossier à importer
            _options = QFileDialog.Options()
            _options |= QFileDialog.DontUseNativeDialog
            _options |= QFileDialog.ShowDirsOnly
            _filename = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier à importer", "",
                                                         options=_options)
            _nbr_imported, _message = self.RC_file_manager.FMimporterResultat(_filename)

            if _nbr_imported == 0:
                _log.Lerror("Erreur lors de l'exportation : \n" + _message)
                ReseauControleur.RCmessageErreur("Erreur lors de l'importation : \n" + _message)
            else:
                _log.Linfo("L'ensemble des fichiers a été importé avec succès !")
                ReseauControleur.RCmessageInformation("L'ensemble des fichiers a été importé avec succès !")
                self.RC_fen_principale.FPuptdateLabelSelection(0, _nbr_imported)
                self.RC_fen_principale.FPafficherReseau()

        # ============================================
        # Cas de demande de lancement de la simulation
        # Signal : LANCER_SIMULATION
        # ============================================
        elif _signal == Signaux.LANCER_SIMULATION:
            # TODO : Version sup., ajouter une fenêtre de paramétrage qui demande les paramètre cf Simulateur
            # _data contient l'information si l'utilisateur veut générer l'html de chaque état pendant la simulation
            _show = True
            if _data == 0:
                _show = False

            _log.Linfo("INFO ## Lancement de la simulation, Generation html : " + str(_show))
            self.RClancerSimulation(_show_html=_show)

        # =================================================
        # Cas de la demande d'affichage de l'état précédent
        # Signal : ARRIERE
        # =================================================
        elif _signal == Signaux.ARRIERE:
            # Seulement si on est pas déjà au premier état
            if self.RC_fen_principale.FP_selection > 0:
                _log.Linfo("INFO ## Récupération de l'état précédent")
                self.RC_fen_principale.FPuptdateLabelSelection(self.RC_fen_principale.FP_selection - 1,
                                                               self.RC_fen_principale.FP_total)
                self.RC_fen_principale.FPafficherReseau()

        # ===============================================
        # Cas de la demande d'affichage de l'état suivant
        # Signal : AVANT
        # ===============================================
        elif _signal == Signaux.AVANT:
            if self.RC_fen_principale.FP_selection < self.RC_fen_principale.FP_total - 1:
                _log.Linfo("INFO ## Récupération de l'état suivant")
                self.RC_fen_principale.FPuptdateLabelSelection(self.RC_fen_principale.FP_selection + 1,
                                                               self.RC_fen_principale.FP_total)
                self.RC_fen_principale.FPafficherReseau()

        # ================================================
        # Cas de la demande d'affichage du cycle précédent
        # Signal : SAUT_ARRIERE
        # ================================================
        if _signal == Signaux.SAUT_ARRIERE:
            _log.Linfo("INFO ## Récupération du premier état du cycle précédent")
            _etat = self.RC_statistiques.S_etatCyclePrecedent(self.RC_fen_principale.FP_selection)

            if _etat != self.RC_fen_principale.FP_selection:
                self.RC_fen_principale.FPuptdateLabelSelection(_etat, self.RC_fen_principale.FP_total)
                self.RC_fen_principale.FPafficherReseau()

        # ==============================================
        # Cas de la demande d'affichage du cycle suivant
        # Signal : SAUT_AVANT
        # ==============================================
        if _signal == Signaux.SAUT_AVANT:
            _log.Linfo("INFO ## Récupération du premier état du cycle suivant")
            _etat = self.RC_statistiques.S_etatCycleSuivant(self.RC_fen_principale.FP_selection)

            if _etat != self.RC_fen_principale.FP_selection:
                self.RC_fen_principale.FPuptdateLabelSelection(_etat, self.RC_fen_principale.FP_total)
                self.RC_fen_principale.FPafficherReseau()

        # ============================================================================
        # Cas doù l'utilisateur utilise la barre glissante pour choisir un état précis
        # Signal : SAUT_TEMPOREL
        # ============================================================================
        if _signal == Signaux.SAUT_TEMPOREL:
            _log.Linfo("INFO ## Changement à l'état " + str(_data))
            self.RC_fen_principale.FPuptdateLabelSelection(_data, self.RC_fen_principale.FP_total)
            self.RC_fen_principale.FPafficherReseau()

    def RClancerSimulation(self, _show_html):
        """
            Démarre, dans un thread, la simulation sur le réseau affiché et connecte ses signaux

            :param _show_html : Booléen, Permet de définir si l'état du réseau doit être affiché pendant la simulation
        """
        _log.Linfo("Début ## ReseauControleur.RClancerSimulation")

        self.RC_file_manager.FMviderEtats(_garder_etat_initial=True)

        _reseau = self.RC_file_manager.FMchargerEtat(0)

        if _reseau is None:
            _log.Linfo("WARNING ## Aucun réseau à exploiter")
            ReseauControleur.RCmessageErreur("Aucun réseau à exploiter")
        else:
            # Création d'abord d'un objet ThreadSimulation et mutation en Thread pour pouvoir manipuler ses connecteurs
            self.RC_worker = ThreadSimulation(_reseau, _show_html=_show_html)
            self.RC_worker.moveToThread(self.RC_thread)

            # Connection des signaux
            self.RC_thread.started.connect(self.RC_worker.run)
            self.RC_thread.finished.connect(self.RC_fen_principale.FPafficherReseau)
            self.RC_worker.TS_finished.connect(self.RC_thread.quit)
            self.RC_worker.TS_connecteur.connect(self.RCactionSignalSimulateur)

            self.RC_thread.start()

    def RCactionSignalSimulateur(self, _signal, _datas):
        """
            Reçoit et analyse les signaux émis par le simulateur
            Principalement utilisé pour instancier et faire progresser une barre de progression

            :param _signal : Enum Signaux, Le signal de type Signals à analyser. Liste des signaux concernés :
                - NOUVEL_ETAT : Cas où un nouvel état a été enregistré et est à afficher (typiquement à la fin de la
                    simulation et à chaque changement de rôle des capteurs)
                - INITIALISATION_SIMULATION : Au début de la simulation, création de la barre de progression
                - PROGRESSION_SIMULATION : Pour modifier les valeurs de la barre de progression
                - FIN_SIMULATION : Ferme la barre de progression et notifie l'utilisateur

            :param _datas : Dict(String : Objet) Les données envoyé lors de l'émission du signal
                Associations :
                Signaux.NOUVEL_ETAT => etat (int) le numéro du nouvel état ; total (int) le nombre d'états
                Signaux.INITIALISATION_SIMULATION => Aucun
                Signaux.PROGRESSION_SIMULATION => avancee (int) la position de 0 à 100 où placer la barre de
                    progression ; text (String) le texte à afficher au dessus de la barre de progression
                Signaux.FIN_SIMULATION => duree (float) le temps qu'a duré la simulation

        """
        _log.Linfo("Début ## ReseauControleur.RCactionSignalSimulateur")

        # ===========================================================================================================
        # Cas où un nouvel état a été enregistré et est à afficher (typiquement à la fin de la simulation et à chaque
        # changement de rôle des capteurs)
        # Signal : NOUVEL_ETAT
        # ===========================================================================================================
        if _signal == Signaux.NOUVEL_ETAT:
            _log.Linfo("Info ## Nouvel état signalé")
            self.RC_fen_principale.FPuptdateLabelSelection(_datas["etat"], _datas["total"])
            self.RC_fen_principale.FPafficherReseau()

        # ==============================================================
        # Au début de la simulation, création de la barre de progression
        # Signal : INITIALISATION_SIMULATION
        # ==============================================================
        elif _signal == Signaux.INITIALISATION_SIMULATION:
            _log.Linfo("Info ## Initialisation de la simulation signalée")
            self.RC_barre_progression_simulation = BarreProgression()

        # ====================================================
        # Pour modifier les valeurs de la barre de progression
        # Signal : PROGRESSION_SIMULATION
        # ====================================================
        elif _signal == Signaux.PROGRESSION_SIMULATION:
            _log.Linfo("Info ## Progression de la simulation signalée")
            self.RC_barre_progression_simulation.BPchangementValeur(_datas["avancee"])
            self.RC_barre_progression_simulation.BPchangementLabel(_datas["text"])

        # ======================================================
        # Ferme la barre de progression et notifie l'utilisateur
        # Signal : FIN_SIMULATION
        # ======================================================
        elif _signal == Signaux.FIN_SIMULATION :
            _log.Linfo("Info ## Fin de la simulation de la simulation signalée")
            if self.RC_barre_progression_simulation is not None:
                # on met à 100% et on ferme la fenêtre
                self.RC_barre_progression_simulation.BPfin()
            self.RCmessageInformation("Simulation terminée, temps d'exécution : " + str(_datas["duree"]) + " secondes")

    def RCactionSignalFenetreCreation(self, _signal, _params=None):
        """
            Reçoit et analyse les signaux émis par la fenêtre de création de réseau

            :param _signal : Enum Signaux, Le signal de type Signals à analyser. Liste des signaux concernés :
                - ANNULER_PARAMETRES : L'utilisateur annule la création du réseau
                - VALIDER_PARAMETRES : L'utilisateur demande la création du réseau
            :param _params: ParametresCreation, l'objet contenant les paramètres saisis par l'utilisateur dans la fenêtre de
                création

        """
        _log.Linfo("Début ## ReseauControleur.RCactionSignalFenetreCreation")

        # ==========================================
        # L'utilisateur annule la création du réseau
        # Signal : ANNULER_PARAMETRES
        # ==========================================
        if _signal == Signaux.ANNULER_PARAMETRES:
            _log.Linfo("Info ## Annulation de la création du réseau")
            self.RC_fen_creation.close()

        # ==========================================
        # L'utilisateur demande la création du réseau
        # Signal : VALIDER_PARAMETRES
        # ==========================================
        elif _signal == Signaux.VALIDER_PARAMETRES and _params is not None:
            _log.Linfo("Info ## Validation de la création du réseau")
            self.RC_fen_creation.close()
            self.RCcreerReseau(_params)

    def RCcreerReseau(self, _param):
        """
            Démarre, dans un thread, la génération d'un réseau

            :param _param : ParametresCreation, Les paramètres reçus pour la création du réseau

        """
        _log.Linfo("Début ## ReseauControleur.RCcreerReseau")

        if self.RCcontroleParametres(_param):
            # Création d'abord d'un objet ThreadCreation et mutation en Thread pour pouvoir manipuler ses connecteurs
            self.RC_worker = ThreadCreation(_param)
            self.RC_worker.moveToThread(self.RC_thread)
            self.RC_worker.TC_finished.connect(self.RC_thread.quit)

            self.RC_thread.started.connect(self.RC_worker.run)
            self.RC_thread.finished.connect(self.RC_fen_principale.FPafficherReseau)

            self.RC_worker.TC_connecteur.connect(self.RCactionSignalGenerateur)
            self.RC_worker.TC_resultat.connect(self.RCactionSignalGenerateurEmissionResultat)

            self.RC_thread.start()

    def RCactionSignalGenerateur(self, _signal, _valeur, _texte, _temps=-1):
        """
            Analyse le signal émit par la création du réseau (Objet Generateur)
            Principalement utilisé pour instancier et faire progresser une barre de progression

            :param _signal : Enum Signaux, Le signal de type Signals à analyser. Liste des signaux concernés :
                - INITIALISATION_CREATION_GRAPHE : Au début de la génération, création de la barre de progression
                - INFORMATION_CREATION_GRAPHE : Informations à placer dans le log, relatives à l'avancement
                - AVANCEE_CREATION_GRAPHE : Pour modifier les valeurs de la barre de progression
                - FIN_CREATION_GRAPHE : Ferme la barre de progression et notifie l'utilisateur
            :param _valeur: int, L'avancement de la création
            :param _texte: String, L'information à afficher
            :param _temps: float, Le temps restant estimé (en secondes)

        """
        _log.Linfo("Début ## ReseauControleur.RCactionSignalGenerateur")

        # ==============================================================
        # Au début de la génération, création de la barre de progression
        # Signal : INITIALISATION_CREATION_GRAPHE
        # ==============================================================
        if _signal == Signaux.INITIALISATION_CREATION_GRAPHE:
            _log.Linfo("Info ## Initialisation de la génération signalée")
            self.RC_barre_progression_creation = BarreProgression()

        # ===========================================================
        # Informations à placer dans le log, relatives à l'avancement
        # Signal : INFORMATION_CREATION_GRAPHE
        # ===========================================================
        elif _signal == Signaux.INFORMATION_CREATION_GRAPHE:
            _log.Linfo("Info ## " + _texte)

        # ====================================================
        # Pour modifier les valeurs de la barre de progression
        # Signal : AVANCEE_CREATION_GRAPHE
        # ====================================================
        elif _signal == Signaux.AVANCEE_CREATION_GRAPHE and self.RC_barre_progression_creation is not None:
            _log.Linfo("Info ## Progresion de la génération signalée")
            # on modifie l'avancée et on ajoute le texte
            self.RC_barre_progression_creation.BPchangementValeur(_valeur)
            if _temps == -1:
                self.RC_barre_progression_creation.BPchangementLabel("Création du réseau en cours..")
            else:
                self.RC_barre_progression_creation.BPchangementLabel("Création du réseau en cours..", _temps)
            _log.Linfo(_texte)

        # ======================================================
        # Ferme la barre de progression et notifie l'utilisateur
        # Signal : FIN_CREATION_GRAPHE
        # ======================================================
        elif _signal == Signaux.FIN_CREATION_GRAPHE and self.RC_barre_progression_creation is not None:
            _log.Linfo("Info ## Réseau créé avec succès")
            self.RCmessageInformation("Réseau créé avec succès")
            self.RC_barre_progression_creation.BPfin()

    def RCactionSignalGenerateurEmissionResultat(self, _reseau):
        """
            Réceptionne le réseau créé par le générateur

            :param _reseau : Reseau, Le résulat émit

        """
        _log.Linfo("Début ## ReseauControleur.RCactionSignalGenerateurEmissionResultat")

        self.RC_resultat = _reseau

        self.RC_fen_principale.FPuptdateLabelSelection(_selection=0, _total=1)

    def RCcontroleParametres(self, _param):
        """
            Permet de controler les paramètres saisis par l'utilisateur.

            :param _param : ParametresCreation, Les paramètres à contrôler.

            :return booléen, faux si les paramètres ne conviennent pas, vrai sinon

        """
        _log.Linfo("Début ## ReseauControleur.RCcontroleParametres")

        _text_erreur = ""

        if _param.PC_min_distance > _param.PC_max_distance:
            _text_erreur += "La distance minimum doit être inférieure ou égale à la distance maximale\n"
        if _param.PC_max_size < 10:
            _text_erreur += "La taille maximale doit être supérieur à 10\n"
        if _param.PC_marge > _param.PC_max_size / 2:
            _text_erreur += "La marge doit être inférieure à la moitiée de la taille maximale\n"
        if _param.PC_nbr_capteurs < 2:
            _text_erreur += "Le nombre de capteurs doit être supérieur à 1\n"

        if _text_erreur != "":
            _log.Linfo("Warning ## " + _text_erreur)
            ReseauControleur.RCmessageErreur(_text_erreur)
            return False
        return True

    @staticmethod
    def RCmessageErreur(_message_erreur):
        """
            Permet d'afficher un message d'erreur dans une boite de dialogue type erreur

            :param _message_erreur : Le message à afficher

        """

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
            Permet d'afficher un message d'information dans une boite de dialogue type information

            :param _message_info : Le message à afficher

        """

        _boite = QMessageBox()
        _boite.setIcon(QMessageBox.Information)
        _boite.setText(_message_info)
        _boite.setWindowTitle("Information(s))")
        _boite.setStandardButtons(QMessageBox.Ok)

        _boite.exec_()
