# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
import copy

def Matrice(nb_lignes, nb_colonnes, valeur_par_defaut=0):
    """
    crée une matrice de nb_lignes lignes sur nb_colonnes colonnes en mettant valeur_par_defaut
    dans chacune des cases

    :param nb_lignes: un entier strictement positif qui indique le nombre de lignes
    :param nb_colonnes: un entier strictement positif qui indique le nombre de colonnes
    :param valeur_par_defaut: la valeur par défaut
    :return: la matrice ayant les bonnes propriétés
    """
    res = list()
    for i in range(nb_lignes):
        liste_temp = list()
        for j in range(nb_colonnes):
            liste_temp.append(valeur_par_defaut)
        res.append(liste_temp)
    return res

def get_nb_lignes(matrice):
    """
    retourne le nombre de lignes de la matrice

    :param matrice: la matrice considérée
    :return: un entier donnant le nombre de lignes
    """
    return len(matrice)


def get_nb_colonnes(matrice):
    """
    retourne le nombre de colonnes de la matrice

    :param matrice: la matrice considérée
    :return: un entier donnant le nombre de colonnes
    """
    return len(matrice[0])


def get_valeur(matrice, ligne, colonne):
    """
    retourne la valeur qui se trouve en (ligne,colonne) dans la matrice

    :param matrice: la matrice considérée
    :param ligne: le numéro de la ligne (en commençant par 0)
    :param colonne: le numéro de la colonne (en commençant par 0)
    :return: la valeur se trouvant (ligne,colonne) dans la matrice
    """
    return matrice[ligne][colonne]


def set_valeur(matrice, ligne, colonne, valeur):
    """
    met la valeur dans la case se trouve en (ligne,colonne) de la matrice
    :param matrice: la matrice considérée
    :param ligne: le numéro de la ligne (en commençant par 0)
    :param colonne: le numéro de la colonne (en commençant par 0)
    :param valeur: la valeur à stocker dans la matrice
    :return: cette fonction ne retourne rien mais modifie la matrice
    """
    matrice[ligne][colonne] = valeur


# ------------------------------------------
# decalages
# ------------------------------------------
def decalage_ligne_a_gauche(matrice, num_ligne, nouvelle_valeur=0):
    """
    permet de décaler une ligne vers la gauche en insérant une nouvelle
    valeur pour remplacer la premiere case à droite de cette ligne
    le fonction retourne la valeur qui a été éjectée

    :param matrice: la matrice considérée
    :param num_ligne: le numéro de la ligne à décaler
    :param nouvelle_valeur: la valeur à placer
    :return: la valeur qui a été ejectée lors du décalage
    """
    print(num_ligne)
    valeur_ejectee = get_valeur(matrice, num_ligne, 0)
    matrice_copy = copy.deepcopy(matrice)
    for i in range(get_nb_colonnes(matrice)):
        if i == get_nb_colonnes(matrice) - 1:
            set_valeur(matrice, num_ligne, i, nouvelle_valeur)
        else :
            set_valeur(matrice, num_ligne, i, get_valeur(matrice_copy, num_ligne, i+1))
    return valeur_ejectee
    

def decalage_ligne_a_droite(matrice, num_ligne, nouvelle_valeur=0):
    """
    decale la ligne num_ligne d'une case vers la droite en insérant une nouvelle
    valeur pour remplacer la premiere case à gauche de cette ligne

    :param matrice: la matrice considérée
    :param num_ligne: le numéro de la ligne à décaler
    :param nouvelle_valeur: la valeur à placer
    :return: la valeur qui a été ejectée lors du décalage
    """
    matrice_copy = copy.deepcopy(matrice)
    valeur_ejectee = get_valeur(matrice, num_ligne, get_nb_colonnes(matrice)-1)
    for i in range(get_nb_colonnes(matrice)):
        if i == 0:
            set_valeur(matrice, num_ligne, i, nouvelle_valeur)
        else :
            set_valeur(matrice, num_ligne, i, get_valeur(matrice_copy, num_ligne, i-1))
    return valeur_ejectee


def decalage_colonne_en_haut(matrice, num_colonne, nouvelle_valeur=0):
    """
    decale la colonne num_colonne d'une case vers le haut en insérant une nouvelle
    valeur pour remplacer la premiere case en bas de cette ligne

    :param matrice: la matrice considérée
    :param num_colonne: le numéro de la ligne à décaler
    :param nouvelle_valeur: la valeur à placer
    :return: la valeur qui a été ejectée lors du décalage
    """
    valeu_ejecte = get_valeur(matrice, 0, num_colonne)
    matrice_temp = copy.deepcopy(matrice)
    for i in range(len(matrice_temp)):
        if i == len(matrice)-1:
            set_valeur(matrice, i, num_colonne, nouvelle_valeur)
        else :
            set_valeur(matrice, i, num_colonne, get_valeur(matrice_temp, i+1, num_colonne))
    return valeu_ejecte


def decalage_colonne_en_bas(matrice, num_colonne, nouvelle_valeur=0):
    """
    decale la colonne num_colonne d'une case vers le bas en insérant une nouvelle
    valeur pour remplacer la premiere case en haut de cette ligne

    :param matrice: la matrice considérée
    :param num_colonne: le numéro de la ligne à décaler
    :param nouvelle_valeur: la valeur à placer
    :return: la valeur qui a été ejectée lors du décalage
    """
    valeu_ejecte = get_valeur(matrice, len(matrice)-1, num_colonne)
    matrice_temp = copy.deepcopy(matrice)
    for i in range(len(matrice_temp)):
        if i == 0:
            set_valeur(matrice, i, num_colonne, nouvelle_valeur)
        else :
            set_valeur(matrice, i, num_colonne, get_valeur(matrice_temp, i-1, num_colonne))
    return valeu_ejecte
