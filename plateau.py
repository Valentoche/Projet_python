# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
from carte import *
from participants import *
from matrice import *


def Plateau(les_joueurs, taille=7, nb_objets=3):
    """
    créer un nouveau plateau contenant les joueurs passés en paramètres

    :param les_joueurs: la liste des joueurs participant à la partie
    :param taille: un entier qqui donne la taille du labyrinthe
    :param nb_objets: un entier qui indique combien d'objets différents existent
    :return: un couple contenant
              * une matrice de taille taillextaill représentant un plateau de labyrinthe où les cartes
                ont été placée de manière aléatoire
              * la carte amovible qui n'a pas été placée sur le plateau
    """
    plateau = Matrice(taille, taille)

    # Ligne 1
    set_valeur(plateau, 0, 0, Carte(True, False, False, True))
    set_valeur(plateau, 0, 6, Carte(True, True, False, False))
    set_valeur(plateau, 0, 2, Carte(True, False, False, False))
    set_valeur(plateau, 0, 4, Carte(True, False, False, False))

    # Ligne 3
    set_valeur(plateau, 2, 0, Carte(False, False, False, True))
    set_valeur(plateau, 2, 2, Carte(False, False, False, True))
    set_valeur(plateau, 2, 4, Carte(True, False, False, False))
    set_valeur(plateau, 2, 6, Carte(False, True, False, False))

    # Ligne 5
    set_valeur(plateau, 4, 0, Carte(False, False, False, True))
    set_valeur(plateau, 4, 2, Carte(False, False, True, False))
    set_valeur(plateau, 4, 4, Carte(False, True, False, False))
    set_valeur(plateau, 4, 6, Carte(False, True, False, False))

    # Ligne 7
    set_valeur(plateau, 6, 0, Carte(False, False, True, True))
    set_valeur(plateau, 6, 6, Carte(False, True, True, False))
    set_valeur(plateau, 6, 2, Carte(False, False, True, False))
    set_valeur(plateau, 6, 4, Carte(False, False, True, False))
    
    # Mise en place des cartes amovibles
    carte_amovible = creer_cartes_amovibles()
    indice = 0

    for i in range(taille):
        for j in range(taille) :
            if get_valeur(plateau, i, j) == 0:
                set_valeur(plateau, i, j, carte_amovible[indice])
                indice += 1

    # Mise en place des joueurs
    if get_nb_joueurs(les_joueurs) == 1 :
        poser_joueur(get_valeur(plateau, 0, 0), les_joueurs['Joueurs'][0][1])
    if get_nb_joueurs(les_joueurs) == 2 :
        poser_joueur(get_valeur(plateau, 0, 0), les_joueurs['Joueurs'][0][1])
        poser_joueur(get_valeur(plateau, 0, 6), les_joueurs['Joueurs'][1][1])
    if get_nb_joueurs(les_joueurs) == 3 :
        poser_joueur(get_valeur(plateau, 0, 0), les_joueurs['Joueurs'][0][1])
        poser_joueur(get_valeur(plateau, 0, 6), les_joueurs['Joueurs'][1][1])
        poser_joueur(get_valeur(plateau, 6, 0), les_joueurs['Joueurs'][2][1])
    if get_nb_joueurs(les_joueurs) == 4 :
        poser_joueur(get_valeur(plateau, 0, 0), les_joueurs['Joueurs'][0][1])
        poser_joueur(get_valeur(plateau, 0, 6), les_joueurs['Joueurs'][1][1])
        poser_joueur(get_valeur(plateau, 6, 0), les_joueurs['Joueurs'][2][1])
        poser_joueur(get_valeur(plateau, 6, 6), les_joueurs['Joueurs'][3][1])

    poser_les_objets(plateau, get_nb_joueurs(les_joueurs) , nb_objets)    
    
    return (plateau, carte_amovible[indice]) 

def creer_cartes_amovibles():
    """
    fonction utilitaire qui permet de créer les cartes amovibles du jeu 
    la fonction retourne la liste, mélangée aléatoirement, des cartes ainsi créées

    :return: la liste mélangée aléatoirement des cartes amovibles créees
    """
    carte = list()
    for i in range(16) :
        variable_carte = Carte(True, False, False, True)
        tourner_aleatoire(variable_carte)
        carte.append(variable_carte)
    
    for i in range(6):
        variable_carte = Carte(False, False, True, False)
        tourner_aleatoire(variable_carte)
        carte.append(variable_carte)

    for i in range(12):
        variable_carte = Carte(True, False, True, False)
        tourner_aleatoire(variable_carte)
        carte.append(variable_carte)
    random.shuffle(carte)
    return carte


def poser_les_objets(plateau, nb_joueurs, nb_objets):
    """
    cette fonction va poser de manière aléatoire les objets sur le plateau, il y aura un objet de chaque types par
    joueur

    :param plateau: le plateau
    :param nb_joueurs: un entier indiquant le nombre de joueurs participant à la partie
    :param nb_objets: un entier le nombre de type d'objets différents
    :return: cette fonction ne retourne rien mais modifie le plateau
    """
    for objet in range(nb_objets):
        for _ in range(nb_joueurs):
            carte = None
            while carte is None or get_objet(carte) != 0:
                carte = get_valeur(plateau, random.randint(1, get_nb_lignes(plateau) - 2),
                                   random.randint(1, get_nb_colonnes(plateau) - 2))
            poser_objet(carte, objet + 1)


def get_coordonnees_joueur(plateau, joueur):
    """
    retourne les coordonnées sous la forme (lig,col) du joueur passé en paramètre

    :param plateau: le plateau considéré
    :param joueur: le joueur à trouver
    :return: un couple d'entiers donnant les coordonnées du joueur ou None si le joueur n'est pas sur le plateau
    """
    res = None
    for ligne in range(get_nb_lignes(plateau)):
        for colonne in range(get_nb_colonnes(plateau)):
            carte = get_valeur(plateau, ligne, colonne)
            for j_liste in get_liste_joueurs(carte) :
                if get_nom_joueur(joueur) == get_nom_joueur(j_liste):
                    res = (ligne, colonne)
    return res


def passage_plateau(plateau, lig, col, direction):
    """
    indique si il y a bien un passage dans le direction passée en paramètre à partir de la position
    lig,col sur le plateau. La fonction retourne None si il n'y a pas de passage ou les coordonnées
    de la case où on arrive en prenant le passage s'il y en a un

    :param plateau: le plateau
    :param lig: un entier donnant le numéro de la ligne
    :param col: un entier donnant le numéro de la colonne
    :param direction: un caractère 'N', 'S', 'O' ou 'E' indiquant la direction où on veut aller
    :return: None s'il n'y a pas de passage possible
             (x,y) les coordonnées où on arrive en prenant le passage s'il existe (un couple d'entiers)
    """
    res = None
    if direction == "N" and 0 <= lig - 1 and passage_nord(get_valeur(plateau, lig, col),
                                                          get_valeur(plateau, lig - 1, col)):
        res = (lig - 1, col)
    elif direction == "E" and get_nb_colonnes(plateau) > col + 1 and passage_est(get_valeur(plateau, lig, col),
                                                                                 get_valeur(plateau, lig, col + 1)):
        res = (lig, col + 1)
    elif direction == "S" and get_nb_lignes(plateau) > lig + 1 and passage_sud(get_valeur(plateau, lig, col),
                                                                               get_valeur(plateau, lig + 1, col)):
        res = (lig + 1, col)
    elif direction == "O" and 0 <= col + 1 and passage_ouest(get_valeur(plateau, lig, col),
                                                             get_valeur(plateau, lig, col - 1)):
        res = (lig, col - 1)
    return res


def accessible(plateau, lig_depart, col_depart, lig_arrivee, col_arrivee):
    """
    indique si il y a un chemin entre la case lig_depart,col_depart et la case lig_arrivee,col_arrivee du labyrinthe

    :param plateau: le plateau considéré
    :param lig_depart: la ligne de la case de départ
    :param col_depart: la colonne de la case de départ
    :param lig_arrivee: la ligne de la case d'arrivée
    :param col_arrivee: la colonne de la case d'arrivée
    :return: un boolean indiquant s'il existe un chemin entre la case de départ
              et la case d'arrivée
    """
    chemin = (lig_depart, col_depart)
    test = [chemin]
    historique = [chemin]
    directions = []

    if lig_depart < lig_arrivee:
        directions.append("S")
        if col_depart < col_arrivee:
            directions.append("E")
            directions.append("O")
        else:
            directions.append("O")
            directions.append("E")
        directions.append("N")
    else:
        directions.append("N")
        if col_depart < col_arrivee:
            directions.append("E")
            directions.append("O")
        else:
            directions.append("O")
            directions.append("E")
        directions.append("S")

    while True:
        suivant = None
        i = 0
        while i < len(directions) and (suivant is None or suivant in test):
            suivant = passage_plateau(plateau, chemin[0], chemin[1], directions[i])
            i += 1
        if not suivant is None:
            chemin = suivant
            test.append(chemin)
            historique.append(chemin)
        elif suivant is None and chemin == (lig_depart, col_depart):
            return False
        else:
            chemin = historique.pop(-1)

        if chemin == (lig_arrivee, col_arrivee):
            return True


def peindre_direction_couleur(plateau, lig, col, direction, couleur, reserve_peinture, traverser_mur, tester=False):
    """
    Permet de peindre d'un couleur les cases accessibles à partir de lig,col dans la direction direction avec la reserve
    de peinture disponible.
    La fonction retourne la liste des joueurs touchés et le nombre de cases peintes.
    Attention si le paramètre tester est à True les cases ne sont pas réellement peintes (on teste juste combien de
    cases seraient peintes)

    :param plateau: un plateau
    :param lig: ligne de départ
    :param col: colonne de départ
    :param direction: un caractère valeur 'N','E','S' ou 'O'
    :param couleur: une couleur de peinture
    :param reserve_peinture: le nombre maximum de cases pouvant être peinte
    :param traverser_mur: booléen permettant de traverser une fois un mur (pouvoir du pistolet)
    :param tester: booléen indiquant si on souhaite vraiment peindre les cases ou juste tester combien on peut en
    peindre
    :return: un couple contenant la liste des joueurs touchés lors de l'action de peindre et le nombre de cases peintes
    """
    nombre = 0
    joueurs = []
    suivant = (lig, col)
    while suivant is not None:
        carte = get_valeur(plateau, suivant[0], suivant[1])
        if nombre < reserve_peinture:
            if not tester:
                set_couleur(carte, couleur)
            nombre += 1
        for joueur in get_liste_joueurs(carte):
            joueurs.append(joueur)
        if direction == "N" and suivant[0] - 1 >= 0:
            if passage_nord(get_valeur(plateau, suivant[0], suivant[1]),
                            get_valeur(plateau, suivant[0] - 1, suivant[1])):
                suivant = (suivant[0] - 1, suivant[1])
            elif traverser_mur:
                suivant = (suivant[0] - 1, suivant[1])
                traverser_mur = False
            else:
                suivant = None
        elif direction == "E" and suivant[1] + 1 < get_nb_colonnes(plateau):
            if passage_est(get_valeur(plateau, suivant[0], suivant[1]),
                           get_valeur(plateau, suivant[0], suivant[1] + 1)):
                suivant = (suivant[0], suivant[1] + 1)
            elif traverser_mur:
                suivant = (suivant[0], suivant[1] + 1)
                traverser_mur = False
            else:
                suivant = None
        elif direction == "S" and suivant[0] + 1 < get_nb_lignes(plateau):
            if passage_sud(get_valeur(plateau, suivant[0], suivant[1]),
                           get_valeur(plateau, suivant[0] + 1, suivant[1])):
                suivant = (suivant[0] + 1, suivant[1])
            elif traverser_mur:
                suivant = (suivant[0] + 1, suivant[1])
                traverser_mur = False
            else:
                suivant = None
        elif direction == "O" and suivant[1] - 1 >= 0:
            if passage_ouest(get_valeur(plateau, suivant[0], suivant[1]),
                             get_valeur(plateau, suivant[0], suivant[1] - 1)):
                suivant = (suivant[0], suivant[1] - 1)
            elif traverser_mur:
                suivant = (suivant[0], suivant[1] - 1)
                traverser_mur = False
            else:
                suivant = None
        else:
            suivant = None
    return joueurs, nombre


def nb_cartes_par_couleur(plateau):
    """
    calcule le nombre de cartes coloriées pour chaque couleur

    :param plateau: le plateau
    :return: un dictionnaire contenant pour chaque couleur présente sur le plateau le nombre de carte de cette couleur
    """
    res = dict()
    for i in range(get_nb_lignes(plateau)):
        for j in range(get_nb_colonnes(plateau)):
            carte = get_valeur(plateau, i, j)
            couleur = get_couleur(carte)
            if not couleur == "aucune":
                if couleur not in res.keys():
                    res[couleur] = 1
                else:
                    res[couleur] += 1
    return res


def affiche_plateau(plateau):
    """
    affichage redimentaire d'un plateau

    :param plateau: le plateau
    :return: rien mais affiche le plateau
    """
    remplissage = ' ' * 30
    print(remplissage, end='')
    for i in range(1, 7, 2):
        print(" " + str(i), sep='', end='')
    print()
    for i in range(get_nb_lignes(plateau)):
        print(remplissage, end='')
        if i % 2 == 0:
            print(' ', sep='', end='')
        else:
            print(str(i), sep='', end='')
        for j in range(get_nb_colonnes(plateau)):
            print(to_char(get_valeur(plateau, i, j)), end='')
        if i % 2 == 0:
            print(' ', sep='', end='')
        else:
            print(str(i), sep='', end='')
        print()
    print(' ', sep='', end='')
    print(remplissage, end='')
    for i in range(1, 7, 2):
        print(" " + str(i), sep='', end='')
    print()
