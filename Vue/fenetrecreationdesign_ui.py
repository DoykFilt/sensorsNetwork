# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fenetrecreationdesign.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 571)
        MainWindow.setMinimumSize(QtCore.QSize(600, 571))
        MainWindow.setMaximumSize(QtCore.QSize(600, 571))
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 581, 551))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.FCDlayout_principal = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.FCDlayout_principal.setContentsMargins(0, 0, 0, 0)
        self.FCDlayout_principal.setObjectName("FCDlayout_principal")
        self.FCDtitre = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCDtitre.setAlignment(QtCore.Qt.AlignCenter)
        self.FCDtitre.setWordWrap(False)
        self.FCDtitre.setObjectName("FCDtitre")
        self.FCDlayout_principal.addWidget(self.FCDtitre)
        self.FCDlayout_nbr_capteurs_1 = QtWidgets.QHBoxLayout()
        self.FCDlayout_nbr_capteurs_1.setObjectName("FCDlayout_nbr_capteurs_1")
        self.FCD_nbr_capteurs_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_nbr_capteurs_text.setObjectName("FCD_nbr_capteurs_text")
        self.FCDlayout_nbr_capteurs_1.addWidget(self.FCD_nbr_capteurs_text)
        self.FCD_nbr_capteurs_valeur = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_nbr_capteurs_valeur.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FCD_nbr_capteurs_valeur.setObjectName("FCD_nbr_capteurs_valeur")
        self.FCDlayout_nbr_capteurs_1.addWidget(self.FCD_nbr_capteurs_valeur)
        self.FCDlayout_principal.addLayout(self.FCDlayout_nbr_capteurs_1)
        self.FCDlayout_nbr_capteurs_2 = QtWidgets.QHBoxLayout()
        self.FCDlayout_nbr_capteurs_2.setObjectName("FCDlayout_nbr_capteurs_2")
        self.FCD_nbr_capteurs_min = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_nbr_capteurs_min.setObjectName("FCD_nbr_capteurs_min")
        self.FCDlayout_nbr_capteurs_2.addWidget(self.FCD_nbr_capteurs_min)
        self.FCD_nbr_capteurs_barre_choix = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.FCD_nbr_capteurs_barre_choix.setOrientation(QtCore.Qt.Horizontal)
        self.FCD_nbr_capteurs_barre_choix.setObjectName("FCD_nbr_capteurs_barre_choix")
        self.FCDlayout_nbr_capteurs_2.addWidget(self.FCD_nbr_capteurs_barre_choix)
        self.FCD_nbr_capteurs_max = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_nbr_capteurs_max.setObjectName("FCD_nbr_capteurs_max")
        self.FCDlayout_nbr_capteurs_2.addWidget(self.FCD_nbr_capteurs_max)
        self.FCDlayout_principal.addLayout(self.FCDlayout_nbr_capteurs_2)
        self.FCDlayout_cap_batterie_1 = QtWidgets.QHBoxLayout()
        self.FCDlayout_cap_batterie_1.setObjectName("FCDlayout_cap_batterie_1")
        self.FCD_cap_batterie_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_cap_batterie_text.setObjectName("FCD_cap_batterie_text")
        self.FCDlayout_cap_batterie_1.addWidget(self.FCD_cap_batterie_text)
        self.FCD_cap_batterie_valeur = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_cap_batterie_valeur.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FCD_cap_batterie_valeur.setObjectName("FCD_cap_batterie_valeur")
        self.FCDlayout_cap_batterie_1.addWidget(self.FCD_cap_batterie_valeur)
        self.FCDlayout_principal.addLayout(self.FCDlayout_cap_batterie_1)
        self.FCDlayout_cap_batterie_2 = QtWidgets.QHBoxLayout()
        self.FCDlayout_cap_batterie_2.setObjectName("FCDlayout_cap_batterie_2")
        self.FCD_cap_batterie_min = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_cap_batterie_min.setObjectName("FCD_cap_batterie_min")
        self.FCDlayout_cap_batterie_2.addWidget(self.FCD_cap_batterie_min)
        self.FCD_cap_batterie_barre_choix = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.FCD_cap_batterie_barre_choix.setOrientation(QtCore.Qt.Horizontal)
        self.FCD_cap_batterie_barre_choix.setObjectName("FCD_cap_batterie_barre_choix")
        self.FCDlayout_cap_batterie_2.addWidget(self.FCD_cap_batterie_barre_choix)
        self.FCD_cap_batterie_max = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_cap_batterie_max.setObjectName("FCD_cap_batterie_max")
        self.FCDlayout_cap_batterie_2.addWidget(self.FCD_cap_batterie_max)
        self.FCDlayout_principal.addLayout(self.FCDlayout_cap_batterie_2)
        self.FCDlayout_taille_max_1 = QtWidgets.QHBoxLayout()
        self.FCDlayout_taille_max_1.setObjectName("FCDlayout_taille_max_1")
        self.FCD_taille_max_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_taille_max_text.setObjectName("FCD_taille_max_text")
        self.FCDlayout_taille_max_1.addWidget(self.FCD_taille_max_text)
        self.FCD_taille_max_valeur = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_taille_max_valeur.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FCD_taille_max_valeur.setObjectName("FCD_taille_max_valeur")
        self.FCDlayout_taille_max_1.addWidget(self.FCD_taille_max_valeur)
        self.FCDlayout_principal.addLayout(self.FCDlayout_taille_max_1)
        self.FCDlayout_taille_max_2 = QtWidgets.QHBoxLayout()
        self.FCDlayout_taille_max_2.setObjectName("FCDlayout_taille_max_2")
        self.FCD_taille_max_min = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_taille_max_min.setObjectName("FCD_taille_max_min")
        self.FCDlayout_taille_max_2.addWidget(self.FCD_taille_max_min)
        self.FCD_taille_max_barre_choix = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.FCD_taille_max_barre_choix.setOrientation(QtCore.Qt.Horizontal)
        self.FCD_taille_max_barre_choix.setObjectName("FCD_taille_max_barre_choix")
        self.FCDlayout_taille_max_2.addWidget(self.FCD_taille_max_barre_choix)
        self.FCD_taille_max_max = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_taille_max_max.setObjectName("FCD_taille_max_max")
        self.FCDlayout_taille_max_2.addWidget(self.FCD_taille_max_max)
        self.FCDlayout_principal.addLayout(self.FCDlayout_taille_max_2)
        self.FCDlayout_distance_max_1 = QtWidgets.QHBoxLayout()
        self.FCDlayout_distance_max_1.setObjectName("FCDlayout_distance_max_1")
        self.FCD_distance_max_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_max_text.setObjectName("FCD_distance_max_text")
        self.FCDlayout_distance_max_1.addWidget(self.FCD_distance_max_text)
        self.FCD_distance_max_valeur = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_max_valeur.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FCD_distance_max_valeur.setObjectName("FCD_distance_max_valeur")
        self.FCDlayout_distance_max_1.addWidget(self.FCD_distance_max_valeur)
        self.FCDlayout_principal.addLayout(self.FCDlayout_distance_max_1)
        self.FCDlayout_distance_max_2 = QtWidgets.QHBoxLayout()
        self.FCDlayout_distance_max_2.setObjectName("FCDlayout_distance_max_2")
        self.FCD_distance_max_min = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_max_min.setObjectName("FCD_distance_max_min")
        self.FCDlayout_distance_max_2.addWidget(self.FCD_distance_max_min)
        self.FCD_distance_max_barre_choix = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.FCD_distance_max_barre_choix.setOrientation(QtCore.Qt.Horizontal)
        self.FCD_distance_max_barre_choix.setObjectName("FCD_distance_max_barre_choix")
        self.FCDlayout_distance_max_2.addWidget(self.FCD_distance_max_barre_choix)
        self.FCD_distance_max_max = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_max_max.setObjectName("FCD_distance_max_max")
        self.FCDlayout_distance_max_2.addWidget(self.FCD_distance_max_max)
        self.FCDlayout_principal.addLayout(self.FCDlayout_distance_max_2)
        self.FCDlayout_distance_min_1 = QtWidgets.QHBoxLayout()
        self.FCDlayout_distance_min_1.setObjectName("FCDlayout_distance_min_1")
        self.FCD_distance_min_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_min_text.setObjectName("FCD_distance_min_text")
        self.FCDlayout_distance_min_1.addWidget(self.FCD_distance_min_text)
        self.FCD_distance_min_valeur = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_min_valeur.setEnabled(True)
        self.FCD_distance_min_valeur.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.FCD_distance_min_valeur.setObjectName("FCD_distance_min_valeur")
        self.FCDlayout_distance_min_1.addWidget(self.FCD_distance_min_valeur)
        self.FCDlayout_principal.addLayout(self.FCDlayout_distance_min_1)
        self.FCDlayout_distance_min_2 = QtWidgets.QHBoxLayout()
        self.FCDlayout_distance_min_2.setObjectName("FCDlayout_distance_min_2")
        self.FCD_distance_min_min = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_min_min.setObjectName("FCD_distance_min_min")
        self.FCDlayout_distance_min_2.addWidget(self.FCD_distance_min_min)
        self.FCD_distance_min_barre_choix = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.FCD_distance_min_barre_choix.setOrientation(QtCore.Qt.Horizontal)
        self.FCD_distance_min_barre_choix.setObjectName("FCD_distance_min_barre_choix")
        self.FCDlayout_distance_min_2.addWidget(self.FCD_distance_min_barre_choix)
        self.FCD_distance_min_max = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.FCD_distance_min_max.setObjectName("FCD_distance_min_max")
        self.FCDlayout_distance_min_2.addWidget(self.FCD_distance_min_max)
        self.FCDlayout_principal.addLayout(self.FCDlayout_distance_min_2)
        self.FCDlayout_boutons = QtWidgets.QHBoxLayout()
        self.FCDlayout_boutons.setObjectName("FCDlayout_boutons")
        self.FCD_boutton_annuler = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.FCD_boutton_annuler.setObjectName("FCD_boutton_annuler")
        self.FCDlayout_boutons.addWidget(self.FCD_boutton_annuler)
        self.FCD_boutton_generer = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.FCD_boutton_generer.setObjectName("FCD_boutton_generer")
        self.FCDlayout_boutons.addWidget(self.FCD_boutton_generer)
        self.FCDlayout_principal.addLayout(self.FCDlayout_boutons)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.FCDtitre.setText(_translate("MainWindow", "Veuillez saisir les paramètres nécessaires"))
        self.FCD_nbr_capteurs_text.setText(_translate("MainWindow", "Nombre de capteurs sans fils à déployer :"))
        self.FCD_nbr_capteurs_valeur.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_nbr_capteurs_min.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_nbr_capteurs_max.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_cap_batterie_text.setText(_translate("MainWindow", "Capacité de la batterie des capteurs (Ampère.heure) :"))
        self.FCD_cap_batterie_valeur.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_cap_batterie_min.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_cap_batterie_max.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_taille_max_text.setText(_translate("MainWindow", "Largeur de la zone carrée à couvrir :"))
        self.FCD_taille_max_valeur.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_taille_max_min.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_taille_max_max.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_distance_max_text.setText(_translate("MainWindow", "Distance à partir de laquelle deux capteurs peuvent établir une connexion :"))
        self.FCD_distance_max_valeur.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_distance_max_min.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_distance_max_max.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_distance_min_text.setText(_translate("MainWindow", "Distance minimum à respecter entre deux capteurs :"))
        self.FCD_distance_min_valeur.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_distance_min_min.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_distance_min_max.setText(_translate("MainWindow", "TextLabel"))
        self.FCD_boutton_annuler.setText(_translate("MainWindow", "Annuler"))
        self.FCD_boutton_generer.setText(_translate("MainWindow", "Générer le réseau"))

