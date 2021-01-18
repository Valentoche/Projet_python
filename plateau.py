# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
from carte import *
from participants import *
from matrice import *
from random import *


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
    shuffle(carte)
    return carte

def poser_les_objets(plateau, nb_joueurs, nb_objets):
    """
    cette fonction va poser de manière aléatoire les objets sur le plateau, il y aura un objet de chaque types par joueur

    :param plateau: le plateau
    :param nb_joueurs: un entier indiquant le nombre de joueurs participant à la partie
    :param nb_objets: un entier le nombre de type d'objets différents
    :return: cette fonction ne retourne rien mais modifie le plateau
    """
    for i in range(nb_objets+1):
        for j in range(nb_joueurs):
            lig, col = randint(0, 6), randint(0, 6)
            while get_objet(get_valeur(plateau, lig, col)) > 0 :
                lig, col = randint(0, 6), randint(0, 6)
            poser_objet(get_valeur(plateau, lig, col), i)

    

def get_coordonnees_joueur(plateau, joueur):
    """
    retourne les coordonnées sous la forme (lig,col) du joueur passé en paramètre

    :param plateau: le plateau considéré
    :param joueur: le joueur à trouver
    :return: un couple d'entiers donnant les coordonnées du joueur ou None si le joueur n'est pas sur le plateau
    """
    for i in range(get_nb_lignes(plateau)) :
        for j in range(get_nb_colonnes(plateau)):
            if possede_joueur(get_valeur(plateau, i, j), joueur) :
                return (i,j)
    

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
    if direction == 'N' and lig > 0:
        if passage_nord(get_valeur(plateau, lig, col), get_valeur(plateau, lig-1, col)) :
            return (lig-1, col)
    elif direction == 'S' and lig < get_nb_lignes(plateau)-1 :
        if passage_sud(get_valeur(plateau, lig, col), get_valeur(plateau, lig+1, col)) :
            return (lig+1, col)
    elif direction == 'O' and col > 0 :
        if passage_ouest(get_valeur(plateau, lig, col), get_valeur(plateau, lig, col-1)) :
            return (lig, col-1)
    elif direction == 'E' and col < get_nb_colonnes(plateau)-1 :
        if passage_est(get_valeur(plateau, lig, col), get_valeur(plateau, lig, col+1)) :
            return (lig, col+1)
    else :
        return None


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
    act = (lig_depart, col_depart)
    tested = [act]
    history = [act]
    directions = []

    # on établit les priorités de directions
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
        next = None
        i = 0
        while i < len(directions) and (next is None or next in tested): # on tente de trouver une case non testé autour de notre case
            next = passage_plateau(plateau, act[0], act[1], directions[i])
            i += 1
        if not next is None: # si on a trouvé quelque chose alors on remplace notre position par celle trouvé
            act = next
            tested.append(act)
            history.append(act)
        elif next is None and act == (lig_depart, col_depart): # si nous n avons rien trouvé en étant retourné au debut on retourne False
            return False
        else: # sinon on revient en arrière
            act = history.pop(-1)
        
        if act == (lig_arrivee, col_arrivee): # si nous nous trouvons là où nous souhaitions arrivé on retourne True
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
    :param tester: booléen indiquant si on souhaite vraiment peindre les cases ou juste tester combien on peut en peindre
    :return: un couple contenant la liste des joueurs touchés lors de l'action de peindre et le nombre de cases peintes
    """
    
    (ligne,colonne) = (lig,col)
    possible = (lig, col)
    liste_joueurs_touchees = list()
    case_couleur = 0
    while possible != None and reserve_peinture >0 :
        reserve_peinture -= 1
        case_couleur +=1
        if tester == False:
            set_couleur(get_valeur(plateau, ligne, colonne), couleur)
        if get_liste_joueurs(get_valeur(plateau, ligne, colonne)) != list():
            joueur = get_liste_joueurs(get_valeur(plateau, ligne, colonne))
            for nom in joueur :
                liste_joueurs_touchees.append(nom)
        possible = passage_plateau(plateau, ligne, colonne, direction)
        if possible != None :
            ligne,colonne = possible
        if possible == None and traverser_mur == True :
            if direction == 'S' and ligne+1 < get_nb_lignes(plateau):
                possible=(ligne+1, colonne)
            else : 
                ligne = 0
                possible=(ligne, colonne)
            if direction == 'N' and ligne-1 > 0:
                possible(ligne-1, colonne)
            else : 
                ligne = get_nb_lignes(plateau)-1
                possible=(ligne, colonne)
            if direction == 'E' and colonne+1 < get_nb_colonnes(plateau):
                possible=(ligne, colonne+1)
            else : 
                colonne = 0
                possible=(ligne, colonne)
            if direction == 'O' and colonne-1 > 0:
                possible=(ligne, colonne-1)
            else : 
                colonne = get_nb_colonnes(plateau)-1
                possible=(ligne, colonne)
            traverser_mur = False
    

    return (liste_joueurs_touchees, case_couleur)


def nb_cartes_par_couleur(plateau):
    """
    calcule le nombre de cartes coloriées pour chaque couleur

    :param plateau: le plateau
    :return: un dictionnaire contenant pour chaque couleur présente sur le plateau le nombre de carte de cette couleur
    """
    res = dict()
    for i in range(get_nb_lignes(plateau)):
        for j in range(get_nb_colonnes(plateau)):
            if get_couleur(get_valeur(plateau, i, j)) in res.keys():
                res[get_couleur(get_valeur(plateau, i, j))] += 1
            else :
                res[get_couleur(get_valeur(plateau, i, j))] = 1
    if None in res.keys():
        res.pop(None)
    if 'aucune' in res.keys():
        res.pop('aucune')
        
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


# plat = Plateau(['moi'])
# print(creer_cartes_amovibles())
# print(plat)
