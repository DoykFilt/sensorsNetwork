from Modele.Reseau import Reseau
from Vue.FenetrePrincipale import FenetrePrincipale

# TODO : Tkinter : option charger ou sauvegarder un réseau

def main():

    # reseau = Reseau(100)
    # nx.draw(reseau.R_graphe)
    # plt.show()

    _max_size = 100
    _marge = 5
    _nbr_capteurs = 3
    _max_distance = 5
    _min_distance = 0

    print("Génération du réseau..")
    reseau = Reseau(_nbr_capteurs, _max_size, _marge, _max_distance, _min_distance)
    # nx.draw(reseau.R_graphe)
    # plt.show()
    print("Calcul de l'affichage..")
    FPFenetrePrincipale = FenetrePrincipale()
    FPFenetrePrincipale.FPafficherReseau(reseau, "networkx")


if __name__ == "__main__":
    main()
