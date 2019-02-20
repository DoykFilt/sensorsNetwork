from Moteur.Simulateur import Simulateur
from Utilitaires.FileManager import FileManager


def testEnsembleDominant():

    _file_manager = FileManager()
    _reseau = _file_manager.FMchargerReseauDepuisXML(_file_manager.FMobtenirCheminXMLLocal())
    _simulateur = Simulateur(None)
    print(_simulateur.SdeterminationEnsembleDominant(_reseau))
