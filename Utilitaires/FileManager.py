import errno
import os
import shutil
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom

import networkx as nx

from Modele.Arc import Arc
from Modele.Capteur import Capteur
from Modele.Passerelle import Passerelle
from Modele.Roles import Roles
from Moteur.Generateur import Generateur


class Singleton(object):
    """
        class Singleton

        Utilisée par la classe FileManager, permet de n'utiliser qu'une seule instance de la classe sur tout le projet

        Cette classe permet de sauvegarder ou exporter un réseau, un résultat de simulation en XML ou HTML.

    """

    # Elements clé pour la création d'un singleton en python
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls].__init__()
        return cls._instances[cls]

    FM_chemin_local = _path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\donnees\\reseau"))
    # def __init__(self):
    #     """
    #         Constructeur de la classe, récupère le chemin absolu du dossier de sauvegarde local
    #     """

    def FMsauvegarderReseauVersXML(self, _reseau, _chemin):
        """
            Permet de sauvegarder un réseau dans un fichier xml. Utilise la bibliothèque xml, en particulier ElementTree

            :param _reseau : le réseau (Reseau) à sauvegarder
            :param _chemin : le chemin (str) du fichier vers lequel sauvegarder le réseau

            La structure du XML est la suivante :
            <reseau>
                <meta>
                    <nbrnoeuds>
                    </nbrnoeuds>
                    <capbatteriemax>
                    </capbatteriemax>
                </meta>
                <graphe>
                    <noeuds>
                        <noeud>
                            <numero><numero/>
                            <role></role>
                            <batterie></batterie>
                            <posx></posx>
                            <posy></posy>
                            <route></route>
                        </noeud>
                        ...
                    </noeuds>
                    <arcs>
                        <arc>
                            <noeud1><noeud1/>
                            <noeud2><noeud2/>
                            <dominant><dominant/>
                        </arc>
                        ...
                    </arcs>
                </graphe
            </reseau>
        """

        # La racine
        _racine = Element("reseau")

        # Les meta données
        _metadonnees = SubElement(_racine, "meta")
        _nbrnoeuds = SubElement(_metadonnees, "nbrnoeuds")
        _nbrnoeuds.text = str(_reseau.R_nbr_noeuds)
        _capacite_batterie_max = SubElement(_metadonnees, "capbatteriemax")
        _capacite_batterie_max.text = str(_reseau.R_capacite_batterie_max)

        # Le graphe
        _graphe = SubElement(_racine, "graphe")
        # Avec ses noeuds
        _noeuds = SubElement(_graphe, "noeuds")
        for _noeud in _reseau.R_graphe.nodes:
            _n = SubElement(_noeuds, "noeud")
            SubElement(_n, "numero").text = str(_noeud)
            SubElement(_n, "role").text = str(_reseau.R_graphe.nodes[_noeud]['role'])
            SubElement(_n, "batterie").text = str(_reseau.R_graphe.nodes[_noeud]['batterie'])
            SubElement(_n, "posx").text = str(_reseau.R_graphe.nodes[_noeud]['pos'][0])
            SubElement(_n, "posy").text = str(_reseau.R_graphe.nodes[_noeud]['pos'][1])
            SubElement(_n, "route").text = str(_reseau.R_graphe.nodes[_noeud]['route'])
        # Et ses arcs
        _arcs = SubElement(_graphe, "arcs")
        _arcs_attributs = nx.get_edge_attributes(_reseau.R_graphe, 'dominant')
        for _arc in _reseau.R_graphe.edges:
            _a = SubElement(_arcs, "arc")
            _noeud1 = SubElement(_a, "noeud1")
            _noeud1.text = str(_arc[0])
            _noeud2 = SubElement(_a, "noeud2")
            _noeud2.text = str(_arc[1])
            _dominant = SubElement(_a, "dominant")
            _dominant.text = str(_arcs_attributs[_arc])

        # Deux lignes pour bien mettre en page l'xml
        _xml = tostring(_racine, 'utf-8')
        _xml = minidom.parseString(_xml)

        # Si le nom de fichier donné contient une extension on l'enlève et on la remplace par xml en sauvegardant
        if len(_chemin.split(".")) > 1:
            _chemin = _chemin.split(".")[0]
        with open(_chemin + ".xml", 'w') as f:
            f.write(_xml.toprettyxml("  "))

    def FMchargerReseauDepuisXML(self, _chemin):
        """
            Permet de charger un réseau depuis un fichier xml. Utilise la bibliothèque xml, en particulier ElementTree

            :param _chemin : le chemin (str) du fichier depuis lequel charger le réseau

            :return le réseau (Reseau) créé

            La structure du XML doit être la suivant :

            <reseau>
                <meta>
                    <nbrnoeuds>
                    </nbrnoeuds>
                    <capbatteriemax>
                    </capbatteriemax>
                </meta>
                <graphe>
                    <noeuds>
                        <noeud>
                            <numero><numero/>
                            <role></role>
                            <batterie></batterie>
                            <posx></posx>
                            <posy></posy>
                            <route></route>
                        </noeud>
                        ...
                    </noeuds>
                    <arcs>
                        <arc>
                            <noeud1><noeud1/>
                            <noeud2><noeud2/>
                            <dominant><dominant/>
                        </arc>
                        ...
                    </arcs>
                </graphe
            </reseau>
        """
        # Importation en local pour éviter les conflits
        from Controleur.ReseauControleur import ReseauControleur

        _capteurs = []
        _arcs = []

        _racine = parse(_chemin)

        # Récupération des noeuds
        for _noeud in _racine.iter("noeud"):
            _num = int(next(_noeud.iter("numero")).text)
            _x = float(next(_noeud.iter("posx")).text)
            _y = float(next(_noeud.iter("posy")).text)
            _batterie = float(next(_noeud.iter("batterie")).text)
            _route = int(next(_noeud.iter("route")).text)
            _role = Roles(int(next(_noeud.iter("role")).text))
            if _role == Roles._PUIT:
                _capteurs.append(Passerelle((_x, _y)))
            else:
                _capteurs.append(Capteur((_x, _y), _batterie, _role, _route))

        # Récupération des arcs
        for _arc in _racine.iter("arc"):
            _noeud1 = int(next(_arc.iter("noeud1")).text)
            _noeud2 = int(next(_arc.iter("noeud2")).text)
            _dominant = Roles(int(next(_arc.iter("dominant")).text))
            _arcs.append(Arc(_noeud1, _noeud2, _dominant))

        # Création du réseau
        _reseau = Generateur.GcreerReseauAvecCapteursEtArcs(_capteurs, _arcs)

        _capacite_batterie_max = float(next(_racine.iter("capbatteriemax")).text)
        _reseau.R_capacite_batterie_max = _capacite_batterie_max

        # Test si le nombre de noeuds détecté et celui donné correspondent
        _nbr_noeuds = int(next(_racine.iter("nbrnoeuds")).text)
        if _reseau.R_nbr_noeuds != _nbr_noeuds:
            ReseauControleur.RCmessageErreur("Le nombre de noeuds en meta et réél ne correspondent pas")
            return None

        from Moteur.Simulateur import Simulateur
        _reseau.R_ensemble_dominant = Simulateur.SdeterminationEnsembleDominant(_reseau)

        return _reseau

    def FMobtenirCheminHTMLVide(self):
        """
            Permet de générer une page html vide dans les données de l'application

            :return Le chemin str vers la page html
        """
        _chemin = self.FM_chemin_local + "\\pagevide.html"
        if not os.path.exists(_chemin):
            if not os.path.exists(self.FM_chemin_local):
                os.makedirs(self.FM_chemin_local)
            with open(_chemin, 'w') as f:
                f.write(""" 
<!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title></title>
      </head>
      <body>
      </body>
    </html>
                        """)
        return _chemin

    def FMenregistrerEtat(self, _reseau):
        """

            Permet de sauvegarder un état du réseau en local

        :param _reseau: Reseau, reseau dont l'état est à enregistrer comme une nouvelle étape de la simulation

        :return:    int, le numéro de l'état attribué
                    int, le nombre total d'états
        """

        # Récopération du chemin, le nom se base sur le numéro de l'état
        _chemin = self.FM_chemin_local + "\\resultats simulation"
        _liste_etats = self.FMlisterEtats()
        if len(_liste_etats) == 0:
            _numero_etat = 0
        else:
            _numero_etat = _liste_etats[-1] + 1
        _fichier_etat = _chemin + "\\etat" + str(_numero_etat)
        if not os.path.exists(_chemin):
            os.makedirs(_chemin)

        # Enregistrement au format XML
        self.FMsauvegarderReseauVersXML(_reseau, _fichier_etat)

        # Enregistrement au format HTML
        with open(_fichier_etat + ".html", 'w') as f:
            f.write(Generateur.GgenerationHTML(_reseau))

        return _numero_etat, len(_liste_etats) + 1

    def FMchargerEtat(self, _numero_etat):
        """

            Permet de charger un état en local

        :param _numero_etat : int, le numéro de l'état à charger
        :return: Reseau, le reseau à l'état chargé, None si inexistant

        """
        _chemin = self.FM_chemin_local + "\\resultats simulation"
        _fichier_etat = _chemin + "\\etat" + str(_numero_etat) + ".xml"
        if not os.path.exists(_fichier_etat):
            return None
        else:
            _reseau = self.FMchargerReseauDepuisXML(_fichier_etat)

            return _reseau

    def FMchargerHTMLEtat(self, _numero_etat):
        """

            Permet de récupérer le chemin vers le fichier HTML représentant l'état voulu

        :param _numero_etat: int, le numéro de l'état à récupérer
        :return: String, le chemin vers le fichier
        """
        _chemin = self.FM_chemin_local + "\\resultats simulation" + "\\etat" + str(_numero_etat) + ".html"
        if not os.path.exists(_chemin):
            return self.FMobtenirCheminHTMLVide()
        return _chemin

    def FMviderEtats(self, _garder_etat_initial):
        """
            Permet de supprimer l'ensemble des fichiers sauvegardés en local

        :param _garder_etat_initial: boolean, si vrai ne supprime pas les données relatives au premier etat
        """
        _chemin = self.FM_chemin_local + "\\resultats simulation"

        if os.path.exists(_chemin):
            from Controleur.Statistiques import Statistiques
            _statistiques = Statistiques()
            _statistiques.SviderEtats(_garder_etat_initial)
            if _garder_etat_initial:
                for _fichier in os.listdir(_chemin):
                    _acces = os.path.join(_chemin, _fichier)
                    try:
                        if os.path.isfile(_acces) and "etat0" not in _fichier:
                            os.unlink(_acces)
                    except Exception as e:
                        print(e)

            else:
                shutil.rmtree(_chemin)

    def FMlisterEtats(self):
        """
            Permet d'obtenir les numéros d'état déjà utilisés

        :return: int[], ensemble des numéros d'état
        """
        _numeros_etats = []
        _numero_etat = 0
        _chemin = self.FM_chemin_local + "\\resultats simulation"
        _fichier_etat = _chemin + "\\etat" + str(_numero_etat) + ".xml"
        while os.path.exists(_fichier_etat):
            _numeros_etats.append(_numero_etat)
            _numero_etat += 1
            _fichier_etat = _chemin + "\\etat" + str(_numero_etat) + ".xml"
        return _numeros_etats

    def FMcopierDossier(self, _source, _destination):
        """
            Permet de copier un dossier d'un endroit vers un autre

        :param _source: String, le chemin du dossier à déplacer
        :param _destination: String, le chemin du dossier vers lequel déplacer le dossier
        :return:    bool, vrai si déplacement effectué
                    String, contient le message d'erreur si il y a lieu
        """

        try:
            shutil.copytree(_source, _destination)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(_source, _destination)
            else:
                return False, "Erreur lors de la copie. Erreur : " + str(e)
        return True, ""

    def FMexporterResultat(self, _destination):
        """
            Permet d'exporter le résultat de la simulation

        :param _destination: String, le chemin vers lequel copier les résultats
        :return:    bool, vrai si déplacement effectué
                    String, contient le message d'erreur si il y a lieu
        """

        if os.path.exists(_destination):
            _destination += "\\copy resultats"
        _source = self.FM_chemin_local + "\\resultats simulation"

        if os.path.exists(_source) and len(self.FMlisterEtats()) > 0:
            return self.FMcopierDossier(_source, _destination)

        else:
            return False, "Aucun résultat à exporter"

    def FMimporterResultat(self, _source):
        """
            Permet d'importer un résultat

        :param _source: String, le chemin où le dossier à importer est situé
        :return:    bool, vrai si déplacement effectué
                    String, contient le message d'erreur si il y a lieu
        """

        if os.path.exists(_source):
            # On copie les résultats déjà présents en local vers un dossier tempon. Cette sauvegarde est utilisé si la
            # tentative de copie échoue
            _destination = self.FM_chemin_local + "\\resultats simulation"
            _chemin_tampon = self.FM_chemin_local + "\\resultats simulation(temp)"
            self.FMcopierDossier(_destination, _chemin_tampon)

            self.FMviderEtats(_garder_etat_initial=False)

            # Essaie de copier du dossier
            _resultat, _erreur = self.FMcopierDossier(_source, _destination)

            # Test du cas où la copie aurait échoué directement
            if not _resultat:
                self.FMviderEtats(_garder_etat_initial=False)
                self.FMcopierDossier(_chemin_tampon, _destination)
                return 0, "Erreur lors de la copie du dossier\n" + _erreur

            # Test du cas où aucun état n'a pu être importé
            _nbr_importe = len(self.FMlisterEtats())
            if _nbr_importe == 0:
                self.FMviderEtats(_garder_etat_initial=False)
                # On remet le tampon
                self.FMcopierDossier(_chemin_tampon, _destination)
                shutil.rmtree(_chemin_tampon)
                return _nbr_importe, "Le dossier indiqué ne contient pas les données attendues"

            # On efface le tampon
            shutil.rmtree(_chemin_tampon)

            self.FMchargerStatistiques()

            return _nbr_importe, ""
        else:
            return 0, "Le dossier à importer n'existe pas"

    @staticmethod
    def FMsauvegarderStatistiques():
        """
            Permet de sauvegarder en local dans un fichier XML les informations contenues dans le singleton Statistique

            Les données sont stockées sous la forme suivante :

            <statistique>
                <nbretats>
                <nbrresultats>
                <etats>
                    <etat>
                        <numero_etat>
                        </numero_etat>
                        </niveau_de_batterie_moyen>
                        <niveau_de_batterie_moyen>
                        </niveau_de_batterie_moyen>
                        <nbr_actifs>
                        </nbr_actifs>
                        <moment_insertion>
                        </moment_insertion>
                        <cycle>
                        </cycle>
                    </etat>
                    <etat>
                        ...
                    </etat>
                    ...
                </etats>
                <resultats>
                    <resultat>
                        <intervalle></intervalle>
                        <dureedevie></dureedevie>
                    </resultat>
                <resultats>
            </statistique>
        """
        from Controleur.Statistiques import Statistiques
        _statistiques = Statistiques()

        _chemin = FileManager.FM_chemin_local + "\\resultats simulation\\statistiques"
        # La racine
        _racine = Element("statistique")

        # Sauvegarde des états
        _nbretats = SubElement(_racine, "nbretats")
        _nbretats.text = str(_statistiques.S_nombre_etats)

        _etats = SubElement(_racine, "etats")
        for _etat in range(0, _statistiques.S_nombre_etats):

            _e = SubElement(_etats, "etat")

            SubElement(_e, "numero_etat").text = str(_etat)

            SubElement(_e, "niveau_de_batterie_moyen").text = str(_statistiques.S_niveau_de_batterie_moyen[_etat])

            SubElement(_e, "nbr_actifs").text = str(_statistiques.S_nbr_actifs[_etat])

            SubElement(_e, "cycle").text = str(_statistiques.S_cycles[_etat])

            SubElement(_e, "moment_insertion").text = str(_statistiques.S_moment_insertion[_etat])

        # Sauvegarde des résultats
        _nbrresultats = SubElement(_racine, "nbrresultats")
        _nbrresultats.text = str(len(_statistiques.S_resultats))

        _resultats = SubElement(_racine, "resultats")
        for _resultat in _statistiques.S_resultats:
            _r = SubElement(_resultats, "resultat")

            SubElement(_r, "intervalle").text = str(_resultat["intervalle"])
            SubElement(_r, "duree").text = str(_resultat["duree"])

        # Deux lignes pour bien mettre en page l'xml
        _xml = tostring(_racine, 'utf-8')
        _xml = minidom.parseString(_xml).toprettyxml("  ")

        with open(_chemin + ".xml", 'w') as f:
            f.write(_xml)

    def FMchargerStatistiques(self):
        """
            Permet de charger en local depuis un fichier XML les informations contenues dans le singleton Statistique

            Les données sont stockées sous la forme suivante :

            <statistique>
                <nbretats>
                <nbrresultats>
                <etats>
                    <etat>
                        <numero_etat>
                        </numero_etat>
                        <niveau_de_batterie_moyen>
                        </niveau_de_batterie_moyen>
                        <nbr_actifs>
                        </nbr_actifs>
                        <cycle>
                        </cycle>
                        <moment_insertion>
                        </moment_insertion>
                    </etat>
                    <etat>
                        ...
                    </etat>
                    ...
                </etats>
                <resultats>
                    <resultat>
                        <intervalle></intervalle>
                        <dureedevie></dureedevie>
                    </resultat>
                <resultats>
            </statistique>
        """

        _chemin = self.FM_chemin_local + "\\resultats simulation\\statistiques.xml"

        if os.path.exists(_chemin):
            from Controleur.Statistiques import Statistiques
            _statistiques = Statistiques()

            _racine = parse(_chemin)

            # Récupération des états
            for _etat in _racine.iter("etat"):
                _netat = int(next(_etat.iter("numero_etat")).text)
                _niveau_batterie_moyen = int(next(_etat.iter("niveau_de_batterie_moyen")).text)
                _nbr_actifs = int(next(_etat.iter("nbr_actifs")).text)
                _cycle = int(next(_etat.iter("cycle")).text)
                _moment = int(next(_etat.iter("moment_insertion")).text)

                _statistiques.SajouterDonneesBrutes(_niveau_batterie_moyen, _nbr_actifs, _cycle, _moment)

            # Récupérations des résultats de performance de la simulation
            for _resultat in _racine.iter("resultat"):
                _intervalle = float(next(_resultat.iter("intervalle")).text)
                _dureedevie = float(next(_resultat.iter("duree")).text)

                _statistiques.SajouterResultat(_intervalle, _dureedevie)

            # Test si le nombre d'états détectés et celui donné correspondent
            _nbr_etats = int(next(_racine.iter("nbretats")).text)
            if _statistiques.S_nombre_etats != _nbr_etats:
                from Controleur.ReseauControleur import ReseauControleur
                ReseauControleur.RCmessageInformation("Le nombre d'état en meta et réél ne correspondent pas. "
                                                      "Chargement des informations statistiques échoué")

            # Test si le nombre de résultats détecté et celui donné correspondent
            _nbr_resultats = int(next(_racine.iter("nbrresultats")).text)
            if len(_statistiques.S_resultats) != _nbr_resultats:
                from Controleur.ReseauControleur import ReseauControleur
                ReseauControleur.RCmessageInformation("Le nombre de résultats en meta et réél ne correspondent pas. "
                                                      "Chargement des informations statistiques échoué")


class FileManager(Singleton):
    """
        class FileManager

        Classe appelée depuis l'extérieur. Hérite du singleton qui est la structure réelle de la classe

    """
    pass
