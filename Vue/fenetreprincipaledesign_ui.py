"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Compilation du .ui éponyme issu de QT Creator
    Created by: PyQt5 UI code generator 5.11.3
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 741)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 741))
        self.FPD_widget_principal = QtWidgets.QWidget(MainWindow)
        self.FPD_widget_principal.setMinimumSize(QtCore.QSize(1200, 700))
        self.FPD_widget_principal.setMaximumSize(QtCore.QSize(1200, 700))
        self.FPD_widget_principal.setObjectName("FPD_widget_principal")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.FPD_widget_principal)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1181, 691))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.FPD_layout_principale = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.FPD_layout_principale.setContentsMargins(0, 0, 0, 0)
        self.FPD_layout_principale.setObjectName("FPD_layout_principale")
        self.FPD_layout_gauche = QtWidgets.QVBoxLayout()
        self.FPD_layout_gauche.setObjectName("FPD_layout_gauche")
        self.FPD_layout_gauche_haut = QtWidgets.QVBoxLayout()
        self.FPD_layout_gauche_haut.setObjectName("FPD_layout_gauche_haut")
        self.FPD_layout_gauche.addLayout(self.FPD_layout_gauche_haut)
        self.FPD_layout_barre_temporelle = QtWidgets.QHBoxLayout()
        self.FPD_layout_barre_temporelle.setObjectName("FPD_layout_barre_temporelle")
        self.FPD_barre_temporelle = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.FPD_barre_temporelle.setEnabled(True)
        self.FPD_barre_temporelle.setOrientation(QtCore.Qt.Horizontal)
        self.FPD_barre_temporelle.setObjectName("FPD_barre_temporelle")
        self.FPD_layout_barre_temporelle.addWidget(self.FPD_barre_temporelle)
        self.FPD_layout_gauche.addLayout(self.FPD_layout_barre_temporelle)
        self.FPD_layout_control_resultat = QtWidgets.QHBoxLayout()
        self.FPD_layout_control_resultat.setObjectName("FPD_layout_control_resultat")
        self.FPD_boutton_saut_arriere = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.FPD_boutton_saut_arriere.setEnabled(True)
        self.FPD_boutton_saut_arriere.setObjectName("FPD_boutton_saut_arriere")
        self.FPD_layout_control_resultat.addWidget(self.FPD_boutton_saut_arriere)
        self.FPD_boutton_arrire = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.FPD_boutton_arrire.setObjectName("FPD_boutton_arrire")
        self.FPD_layout_control_resultat.addWidget(self.FPD_boutton_arrire)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.FPD_layout_control_resultat.addItem(spacerItem)
        self.FPD_label_selection = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.FPD_label_selection.setObjectName("FPD_label_selection")
        self.FPD_layout_control_resultat.addWidget(self.FPD_label_selection)
        self.FPD_selection_barre_temporelle = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.FPD_selection_barre_temporelle.setObjectName("FPD_selection_barre_temporelle")
        self.FPD_layout_control_resultat.addWidget(self.FPD_selection_barre_temporelle)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.FPD_layout_control_resultat.addItem(spacerItem1)
        self.FPD_boutton_avant = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.FPD_boutton_avant.setObjectName("FPD_boutton_avant")
        self.FPD_layout_control_resultat.addWidget(self.FPD_boutton_avant)
        self.FPD_boutton_saut_avant = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.FPD_boutton_saut_avant.setEnabled(True)
        self.FPD_boutton_saut_avant.setObjectName("FPD_boutton_saut_avant")
        self.FPD_layout_control_resultat.addWidget(self.FPD_boutton_saut_avant)
        self.FPD_layout_gauche.addLayout(self.FPD_layout_control_resultat)
        self.FPD_layout_gauche_bas = QtWidgets.QHBoxLayout()
        self.FPD_layout_gauche_bas.setObjectName("FPD_layout_gauche_bas")
        self.FPD_bouton_generer_reseau = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.FPD_bouton_generer_reseau.setObjectName("FPD_bouton_generer_reseau")
        self.FPD_layout_gauche_bas.addWidget(self.FPD_bouton_generer_reseau)
        self.FPD_bouton_lancer_simulation = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.FPD_bouton_lancer_simulation.setEnabled(True)
        self.FPD_bouton_lancer_simulation.setObjectName("FPD_bouton_lancer_simulation")
        self.FPD_layout_gauche_bas.addWidget(self.FPD_bouton_lancer_simulation)
        self.FPD_check_box = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.FPD_check_box.setChecked(True)
        self.FPD_check_box.setObjectName("FPD_check_box")
        self.FPD_layout_gauche_bas.addWidget(self.FPD_check_box)
        self.FPD_layout_gauche.addLayout(self.FPD_layout_gauche_bas)
        self.FPD_layout_principale.addLayout(self.FPD_layout_gauche)
        self.FPD_layout_droit = QtWidgets.QVBoxLayout()
        self.FPD_layout_droit.setObjectName("FPD_layout_droit")
        self.FPD_layout_graphiques = QtWidgets.QVBoxLayout()
        self.FPD_layout_graphiques.setObjectName("FPD_layout_graphiques")
        self.FPD_layout_droit.addLayout(self.FPD_layout_graphiques)
        self.FPD_aire_informations = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.FPD_aire_informations.setFrameShape(QtWidgets.QFrame.Box)
        self.FPD_aire_informations.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.FPD_aire_informations.setLineWidth(1)
        self.FPD_aire_informations.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.FPD_aire_informations.setObjectName("FPD_aire_informations")
        self.FPD_layout_droit.addWidget(self.FPD_aire_informations)
        self.FPD_layout_principale.addLayout(self.FPD_layout_droit)
        MainWindow.setCentralWidget(self.FPD_widget_principal)
        self.FPD_barre_menu = QtWidgets.QMenuBar(MainWindow)
        self.FPD_barre_menu.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.FPD_barre_menu.setObjectName("FPD_barre_menu")
        self.FPD_menu_reseau = QtWidgets.QMenu(self.FPD_barre_menu)
        self.FPD_menu_reseau.setObjectName("FPD_menu_reseau")
        self.FPD_menu_exporter = QtWidgets.QMenu(self.FPD_menu_reseau)
        self.FPD_menu_exporter.setObjectName("FPD_menu_exporter")
        self.FPD_menu_charger = QtWidgets.QMenu(self.FPD_menu_reseau)
        self.FPD_menu_charger.setObjectName("FPD_menu_charger")
        MainWindow.setMenuBar(self.FPD_barre_menu)
        self.FPD_barre_status = QtWidgets.QStatusBar(MainWindow)
        self.FPD_barre_status.setObjectName("FPD_barre_status")
        MainWindow.setStatusBar(self.FPD_barre_status)
        self.FPDActionSauvegarder = QtWidgets.QAction(MainWindow)
        self.FPDActionSauvegarder.setEnabled(True)
        self.FPDActionSauvegarder.setObjectName("FPDActionSauvegarder")
        self.FPDActionExporterReseau = QtWidgets.QAction(MainWindow)
        self.FPDActionExporterReseau.setObjectName("FPDActionExporterReseau")
        self.FDPActionExporterSimulation = QtWidgets.QAction(MainWindow)
        self.FDPActionExporterSimulation.setEnabled(True)
        self.FDPActionExporterSimulation.setObjectName("FDPActionExporterSimulation")
        self.FPDActionChargerReseau = QtWidgets.QAction(MainWindow)
        self.FPDActionChargerReseau.setObjectName("FPDActionChargerReseau")
        self.FPDActionChargerResultats = QtWidgets.QAction(MainWindow)
        self.FPDActionChargerResultats.setEnabled(True)
        self.FPDActionChargerResultats.setObjectName("FPDActionChargerResultats")
        self.action_le_r_seau_HTML = QtWidgets.QAction(MainWindow)
        self.action_le_r_seau_HTML.setObjectName("action_le_r_seau_HTML")
        self.FPD_menu_exporter.addAction(self.FPDActionExporterReseau)
        self.FPD_menu_exporter.addAction(self.FDPActionExporterSimulation)
        self.FPD_menu_charger.addAction(self.FPDActionChargerReseau)
        self.FPD_menu_charger.addAction(self.FPDActionChargerResultats)
        self.FPD_menu_reseau.addAction(self.FPD_menu_exporter.menuAction())
        self.FPD_menu_reseau.addSeparator()
        self.FPD_menu_reseau.addAction(self.FPD_menu_charger.menuAction())
        self.FPD_barre_menu.addAction(self.FPD_menu_reseau.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.FPD_boutton_saut_arriere.setText(_translate("MainWindow", "<<"))
        self.FPD_boutton_arrire.setText(_translate("MainWindow", "<"))
        self.FPD_label_selection.setText(_translate("MainWindow", "Sélection :"))
        self.FPD_selection_barre_temporelle.setText(_translate("MainWindow", "Selection / Total"))
        self.FPD_boutton_avant.setText(_translate("MainWindow", ">"))
        self.FPD_boutton_saut_avant.setText(_translate("MainWindow", ">>"))
        self.FPD_bouton_generer_reseau.setText(_translate("MainWindow", "Générer un réseau"))
        self.FPD_bouton_lancer_simulation.setText(_translate("MainWindow", "Lancer la simulation"))
        self.FPD_check_box.setText(_translate("MainWindow", "Voir l\'évolution (plus lent)"))
        self.FPD_aire_informations.setText(_translate("MainWindow", "Informations relatives au résultats de la simulation"))
        self.FPD_menu_reseau.setTitle(_translate("MainWindow", "Réseau"))
        self.FPD_menu_exporter.setTitle(_translate("MainWindow", "Exporter .."))
        self.FPD_menu_charger.setTitle(_translate("MainWindow", "Importer .."))
        self.FPDActionSauvegarder.setText(_translate("MainWindow", "Sauvegarder"))
        self.FPDActionExporterReseau.setText(_translate("MainWindow", ".. le réseau affiché (.XML)"))
        self.FDPActionExporterSimulation.setText(_translate("MainWindow", ".. le résultat de la simulation (Dossier complet)"))
        self.FPDActionChargerReseau.setText(_translate("MainWindow", ".. un réseau en tant qu\'état initial (.XML)"))
        self.FPDActionChargerResultats.setText(_translate("MainWindow", ".. un résultat de simulation (Dossier complet)"))
        self.action_le_r_seau_HTML.setText(_translate("MainWindow", ".. le réseau (.HTML)"))

