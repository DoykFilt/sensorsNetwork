import errno
import os
import shutil
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom

import networkx as nx

from Modele.Arc import Arc
from Modele.Capteur import Capteur
from Modele.Puit import Puit
from Modele.Roles import Roles
from Moteur.Generateur import Generateur


class Singleton(object):
    """
        class Singleton

        Utilisée par la classe FileManager, permet de n'utiliser qu'une seule instance de la classe sur tout le projet

        Cette classe permet de sauvegarder ou exporter un réseau en XML ou HTML

    """

    # Elements clé pour la création d'un singleton en python
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls].__init__()
        return cls._instances[cls]

    def __init__(self):
        """
            Constructeur de la classe, récupère le chemin absolu du dossier de sauvegarde local
        """
        self.FM_chemin_local = _path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\donnees\\reseau"))

    def FMsauvegarderReseauVersXML(self, _reseau, _chemin):
        """
            Permet de sauvegarder un réseau dans un fichier xml. Utilise la bibliothèque xml, en particulier ElementTree

            :param _reseau : le réseau (Reseau) à sauvegarder
            :param _chemin : le chemin (str) du fichier vers lequel sauvegarder le réseau

            La structure du XML est la suivante :
            <reseau>
                <meta>
                    <nbrnoeuds>
                    <nbrnoeuds>
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
                    <nbrnoeuds>
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
        #
        # try:
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
                _capteurs.append(Puit((_x, _y)))
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
        #
        # except:
        #     ReseauControleur.RCmessageErreur("Le fichier est invalide ou corrompu")
        #     return None

        # Test si le nombre de noeuds détecté et celui donné correspondent
        _nbr_noeuds = int(next(_racine.iter("nbrnoeuds")).text)
        if _reseau.R_nbr_noeuds != _nbr_noeuds:
            ReseauControleur.RCmessageErreur("Le nombre de noeuds en meta et réél ne correspondent pas")
            return None

        # Initialisation du réseau
        from Moteur.Simulateur import Simulateur
        Simulateur.SconfigurationTopologique(_reseau)
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

        # Le chemin
        _chemin = self.FM_chemin_local + "\\resultats simulation"
        _liste_etats = self.FMlisterEtats()
        if len(_liste_etats) == 0:
            _numero_etat = 0
        else:
            _numero_etat = _liste_etats[-1] + 1
        _fichier_etat = _chemin + "\\etat" + str(_numero_etat)
        if not os.path.exists(_chemin):
            os.makedirs(_chemin)

        # Enregistrement en XML
        self.FMsauvegarderReseauVersXML(_reseau, _fichier_etat)

        # Enregistrement en HTML
        with open(_fichier_etat + ".html", 'w') as f:
            f.write(Generateur.GgenerationHTML(_reseau))

        return _numero_etat, len(_liste_etats) + 1

    def FMchargerEtat(self, _numero_etat):
        _chemin = self.FM_chemin_local + "\\resultats simulation"
        _fichier_etat = _chemin + "\\etat" + str(_numero_etat) + ".xml"
        if not os.path.exists(_fichier_etat):
            return None
        else:
            return self.FMchargerReseauDepuisXML(_fichier_etat)

    def FMchargerHTMLEtat(self, _numero_etat):
        _chemin = self.FM_chemin_local + "\\resultats simulation" + "\\etat" + str(_numero_etat) + ".html"
        if not os.path.exists(_chemin):
            return self.FMobtenirCheminHTMLVide()
        return _chemin

    def FMviderEtats(self, _garder_etat_initial):
        _chemin = self.FM_chemin_local + "\\resultats simulation"

        if os.path.exists(_chemin):
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

        if os.path.exists(_destination):
            _destination += "\\copy resultats"
        _source = self.FM_chemin_local + "\\resultats simulation"

        if os.path.exists(_source) and len(self.FMlisterEtats()) > 0:
            return self.FMcopierDossier(_source, _destination)

        else:
            return False, "Aucun résultat à exporter"

    def FMimporterResultat(self, _source):
        if os.path.exists(_source):
            _destination = self.FM_chemin_local + "\\resultats simulation"
            _chemin_tampon = self.FM_chemin_local + "\\resultats simulation(temp)"
            self.FMcopierDossier(_destination, _chemin_tampon)

            self.FMviderEtats(_garder_etat_initial=False)

            self.FMcopierDossier(_source, _destination)

            _nbr_importe = len(self.FMlisterEtats())

            if _nbr_importe == 0:
                self.FMviderEtats(_garder_etat_initial=False)
                # On remet le tampon
                self.FMcopierDossier(_chemin_tampon, _destination)
                shutil.rmtree(_chemin_tampon)
                return _nbr_importe, "Le dossier indiqué ne contient pas les données attendues"

            # On efface le tampon
            shutil.rmtree(_chemin_tampon)
            return _nbr_importe, ""
        else:
            return 0, "Le dossier à importer n'existe pas"


class FileManager(Singleton):
    """
        class FileManager

        Classe appelée depuis l'extérieur. Hérite du singleton qui est la structure réelle de la classe

    """
    pass