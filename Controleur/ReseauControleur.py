from Controleur.FileManager import FileManager
from Modele.Parametres import Parametres
from Modele.Reseau import Reseau
from Moteur.ReseauMoteur import ReseauMoteur
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QProgressDialog, QFileDialog
from PyQt5 import QtCore
from Modele.Signaux import Signaux


class ThreadCreation(QtCore.QObject):
    connecteur = QtCore.pyqtSignal(Signaux, float, str, float)
    resultat = QtCore.pyqtSignal(Reseau)
    finished = QtCore.pyqtSignal()

    def __init__(self, _param, empty_reseau):
        super().__init__()
        self.reseau = empty_reseau
        self.TC_moteur_reseau = ReseauMoteur(self.connecteur)
        self.TC_param = _param

    def run(self):
        self.resultat.emit(self.TC_moteur_reseau.RMcreerReseau(self.TC_param))
        self.finished.emit()


class ReseauControleur(QWidget):

    def __init__(self, _fen_principale, _fen_creation):
        super(ReseauControleur, self).__init__()
        self.RC_fen_principale = _fen_principale
        self.RC_fen_creation = _fen_creation

        self.RC_fen_principale.FPobtenirConnecteur().connect(self.RCactionSignalFenetrePrincipale)
        self.RC_fen_creation.FCobtenirConnecteur().connect(self.RCactionSignalFenetreCreation)

        self.RC_barre_progression_creation = None
        self._thread = QtCore.QThread()
        self.resultat = None

    def enum(**named_values):
        return type('Enum', (), named_values)

    def RCcreerReseau(self, _param):
        if self.RCcontroleParametres(_param):
            # _graphe_sortie = [None]
            # _thread = ThreadCreation(_param, _graphe_sortie)
            # _thread.start()
            # _thread.join()
            # return _graphe_sortie[0]
            result = Reseau()

            self._worker = ThreadCreation(_param, result)
            self._worker.moveToThread(self._thread)
            self._worker.finished.connect(self._thread.quit)
            self._thread.started.connect(self._worker.run)
            self._thread.finished.connect(self.RCupdateAffichage)
            self._worker.connecteur.connect(self.RCactionSignalMoteur)
            self._worker.resultat.connect(self.RCactionSignalMoteurResultat)
            self._thread.start()

    def RCupdateAffichage(self):
        self._worker.deleteLater()
        _fileManager = FileManager()
        _fileManager.FMsauvegarderLocal(_reseau=self.resultat)
        self.RC_fen_principale.FPafficherReseau()

    def RCactionSignalMoteurResultat(self, _reseau):
        self.resultat = _reseau

    def RCResultatCreation(self):
        return self._resultat

    def RCcontroleParametres(self, _param):
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

    def RCactionSignalFenetrePrincipale(self, _signal):

        if _signal == Signaux._GENERER_RESEAU:
            self.RC_fen_creation.show()

        if _signal == Signaux._EXPORTER_XML:

            _options = QFileDialog.Options()
            _options |= QFileDialog.DontUseNativeDialog
            _filename, _ = QFileDialog.getSaveFileName(self, "Spécifier l'endroit où exporter le fichier", "",
                                                      "Fichier XML (*.xml)", options=_options)
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

        if _signal == Signaux._CHARGER_XML:

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

    def RCactionSignalFenetreCreation(self, _signal, _params):
        if _signal == Signaux._ANNULER_PARAMETRES:
            self.RC_fen_creation.close()
        elif _signal == Signaux._VALIDER_PARAMETRES:
            self.RC_fen_creation.close()
            self.RCcreerReseau(_params)

    def RCactionSignalAnnulerCreation(self):
        self._thread.terminate()
        self._thread.wait()

    def RCactionSignalMoteur(self, _signal, _valeur, _texte, _temps):
        if _signal == Signaux._INITIALISATION_CREATION_GRAPHE:
            # Création de la fenetre
            self.RC_barre_progression_creation = QProgressDialog("Création du réseau en cours..", "", 0, 100)
            self.RC_barre_progression_creation.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.RC_barre_progression_creation.setMaximumHeight(100)
            self.RC_barre_progression_creation.setMinimumHeight(100)
            self.RC_barre_progression_creation.setMaximumWidth(300)
            self.RC_barre_progression_creation.setMinimumWidth(300)
            self.RC_barre_progression_creation.setCancelButton(None)
            self.RC_barre_progression_creation.setWindowModality(QtCore.Qt.ApplicationModal)
            self.RC_barre_progression_creation.show()
            self.RC_barre_progression_creation.setValue(0)
            print(_texte)
        elif _signal == Signaux._INFORMATION_CREATION_GRAPHE:
            # ajout du texte
            self.RC_barre_progression_creation.text = _texte
            print(_texte)
        elif _signal == Signaux._AVANCEE_CREATION_GRAPHE:
            # on modifie l'avancée et on ajoute le texte
            self.RC_barre_progression_creation.setValue(_valeur)
            if _temps == -1:
                _temps = "..."
            else:
                _temps = str(int(_temps))
            self.RC_barre_progression_creation.setLabelText("Création du réseau en cours.."
                                                       + "\n \n"
                                                       + "Temps restant estimé : " + _temps + " secondes")
            print(_texte)
        elif _signal == Signaux._FIN_CREATION_GRAPHE:
            # on met à 100% et on ferme la fenêtre
            self.RC_barre_progression_creation.setValue(99)
            self.RC_barre_progression_creation.close()

    @staticmethod
    def RCmessageErreur(_message_erreur):
        _boite = QMessageBox()
        _boite.setIcon(QMessageBox.Critical)
        _boite.setText("Erreur(s)")
        _boite.setWindowTitle("Erreur(s)")
        _boite.setDetailedText("Le(s) erreur(s) suivante(s) ont été détectée(s) : \n" + _message_erreur)
        _boite.setStandardButtons(QMessageBox.Ok)

        _boite.exec_()

    @staticmethod
    def RCmessageInformation(_message_erreur):
        _boite = QMessageBox()
        _boite.setIcon(QMessageBox.Information)
        _boite.setText(_message_erreur)
        _boite.setWindowTitle("Information(s))")
        _boite.setStandardButtons(QMessageBox.Ok)

        _boite.exec_()
