
import os
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom

from Modele.Capteur import Capteur
from Modele.Puit import Puit
from Modele.Reseau import Reseau
from Modele.Roles import Roles
from Moteur.ReseauMoteur import ReseauMoteur


class Singleton(object):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._instances[cls].__init()
        return cls._instances[cls]

    def __init(self):
        self.FM_chemin_local = _path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\donnees\\reseau"))

    def FMsauvegarderReseauVersXML(self, _reseau, _chemin):
        _racine = Element("reseau")
        _metadonnees = SubElement(_racine, "meta")
        _nbrnoeuds = SubElement(_metadonnees, "nbrnoeuds")
        _nbrnoeuds.text = str(_reseau.R_nbr_noeuds)
        _graphe = SubElement(_racine, "graphe")
        _noeuds = SubElement(_graphe, "noeuds")

        for _noeud in _reseau.R_graphe.nodes:
            _n = SubElement(_noeuds, "noeud")
            SubElement(_n, "numero").text = str(_noeud)
            SubElement(_n, "role").text = str(_reseau.R_graphe.nodes[_noeud]['role'])
            SubElement(_n, "batterie").text = str(_reseau.R_graphe.nodes[_noeud]['batterie'])
            SubElement(_n, "posx").text = str(_reseau.R_graphe.nodes[_noeud]['pos'][0])
            SubElement(_n, "posy").text = str(_reseau.R_graphe.nodes[_noeud]['pos'][1])


        _arcs = SubElement(_graphe, "arcs")
        for _arc in _reseau.R_graphe.edges:
            _a = SubElement(_arcs, "arc")
            _noeud1 = SubElement(_a, "noeud1")
            _noeud1.text = str(_arc[0])
            _noeud2 = SubElement(_a, "noeud2")
            _noeud2.text = str(_arc[1])

        _xml = tostring(_racine, 'utf-8')
        _xml = minidom.parseString(_xml)

        if len(_chemin.split(".")) > 1:
            _chemin = _chemin.split(".")[0]
        with open(_chemin + ".xml", 'w') as f:
            f.write(_xml.toprettyxml("  "))

    def FMchargerReseauDepuisXML(self, _chemin):
        from Controleur.ReseauControleur import ReseauControleur
        # try:
        _xml = ""
        _capteurs = []
        _arcs = []

        _racine = parse(_chemin)
        for _noeud in _racine.iter("noeud"):
            _num = int(next(_noeud.iter("numero")).text)
            _x = float(next(_noeud.iter("posx")).text)
            _y = float(next(_noeud.iter("posy")).text)
            _batterie = float(next(_noeud.iter("batterie")).text)
            _role = Roles(int(next(_noeud.iter("role")).text))
            if _role == Roles._PUIT:
                _capteurs.append(Puit((_x, _y)))
            else:
                _capteurs.append(Capteur((_x, _y), _batterie, _role))

        for _arc in _racine.iter("arc"):
            _noeud1 = int(next(_arc.iter("noeud1")).text)
            _noeud2 = int(next(_arc.iter("noeud2")).text)
            _arcs.append((_noeud1, _noeud2))

        _reseau = ReseauMoteur.RMcreerReseauAvecCapteursEtArcs(_capteurs, _arcs)
        _nbr_noeuds = 0

        _nbr_noeuds = int(next(_racine.iter("nbrnoeuds")).text)
        if _reseau.R_nbr_noeuds != _nbr_noeuds:
            ReseauControleur.RCmessageErreur("Le nombre de noeuds en meta et réél ne correspondent pas")
            return None
        return _reseau

        # except:
        #     ReseauControleur.RCmessageErreur("Le fichier est invalide ou corrompu")
        #     return None

    def FMsauvegarderLocal(self, _reseau):
        # Sauvegarde en HTML
        _chemin, _exist = self.FMobtenirCheminHTMLLocal()
        with open(_chemin, 'w') as f:
            f.write(ReseauMoteur.RMgenerationHTML(_reseau))
        # Sauvegarde en XML
        if not os.path.exists(self.FM_chemin_local):
            os.makedirs(self.FM_chemin_local)
        self.FMsauvegarderReseauVersXML(_reseau, self.FM_chemin_local + "//" + "local")

    def FMobtenirCheminXMLLocal(self):
        _exist = True
        _file = Path(self.FM_chemin_local + "\\" + "local.xml")
        if not _file.exists() or not _file.is_file():
            _exist = False
        return self.FM_chemin_local + "\\" + "local.xml", _exist

    def FMobtenirCheminHTMLLocal(self):
        _exist = True
        _file = Path(self.FM_chemin_local + "\\" + "local.html")
        if not _file.exists() or not _file.is_file():
            _exist = False
        return self.FM_chemin_local + "\\" + "local.html", _exist

    def FMobtenirCheminHTMLVide(self):
        _chemin = self.FM_chemin_local + "\\" + "pagevide.html"
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


class FileManager(Singleton):
    pass
