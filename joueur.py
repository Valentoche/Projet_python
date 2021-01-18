# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
import random


def dummy_ai(laby_dico):
    """
    IA aléatoire mise par défaut sur les joueurs automatiques

    :param laby_dico: ce paramètre n'est pas utilisé
    :return: un ordre pour le joueur sous la forme d'une chaine de caractères
    """
    actions = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C']
    directions = ['E', 'O', 'S', 'N', 'X']
    positions = ['1', '3', '5']
    dir_peint = random.choice(directions)
    res = 'P' + dir_peint
    action = random.choice(actions)
    if action == 'D':
        direction = random.choice(directions[:-1])
        return res + action + direction
    if action == 'C':
        tourne = random.randint(0, 4)
        tournage = 'H' * tourne
        res += 'T' + tournage
        res += random.choice(directions)
        res += random.choice(positions)
        return res


def Joueur(nom, couleur, reserve_initiale=20, surface=0, type_joueur='O', objet=0, temps_restant=0, ia=dummy_ai):
    """
    creer un nouveau joueur portant le nom passé en paramètre.

    :param nom: une chaine de caractères donnant le nom du joueur
    :param couleur: une chaine de caractères donnant donnant la couleur du joueur
    :param reserve_initiale: un entier indiquant la réserve de peinture du joueur
    :param surface: un entier qui indique combien de case du labyrinthe sont peintes de la couleur du joueur
    :param type_joueur: un caractère 'H' pour humain 'O' pour ordinateur
    :param objet: un entier compris entre 0 et 3 indiquant l'objet possédé actuellement par le joueur (0 => pas d'objet)
    :param temps_restant: le nombre de tours restant avant que l'objet possédé par le joueur est encore valide
    :param ia:  une fonction indiquant quelle fonction appeler pour lancer l'IA associée à un joueur de type Ordinateur
    :return: le joueur possédant les caractéristiques passées en paramètre.
    """
    res = dict()
    res["nom"] = nom
    res["couleur"] = couleur
    res["reserve"] = reserve_initiale
    res["surface"] = surface
    res["type_joueur"] = type_joueur
    res["objet"] = objet
    res["temps_restant"] = temps_restant
    res["ia"] = ia
    return res

def ajouter_objet(joueur, objet, temps):
    """
    ajoute un objet au joueur et initialise le temps de validité de cet objet

    :param joueur: le joueur à modifier
    :param objet: un entier strictement positif indiquant l'objet attribué au joueur
    :param temps: le temps de validité de l'objet
    :return: la fonction ne retourne rien mais modifie le joueur
    """
    joueur["objet"] = objet
    joueur["temps_restant"] = temps
    return None

def mise_a_jour_temps(joueur):
    """
    enlève une unité de temps à la durée de vie de l'objet possédé par le joueur.
    Attention, si cette durée de vie passe à 0 il faut retirer l'objet du joueur

    :param joueur: le joueur à modifier
    :return: la fonction ne retourne rien mais modifie le joueur
    """
    if joueur["temps_restant"] > 0: joueur["temps_restant"] -= 1
    if get_temps_restant(joueur) == 0: ajouter_objet(joueur, 0, 0)


def set_type_joueur(joueur, type_joueur):
    """
    permet de "forcer" le type du joueur (humain ou ordinateur)

    :param joueur: le joueur à modifier
    :param type_joueur: un caractère 'H' pour humain 'O' pour ordinateur
    :return: la fonction ne retourne rien mais modifie le joueur
    """
    joueur["type_joueur"] = type_joueur
    return None


def get_type_joueur(joueur):
    """
    retourne le type du joueur

    :param joueur: le joueur
    :return: résultat un caratère 'H' pour humain et 'O' pour ordinateur
    """
    return joueur["type_joueur"]


def set_fonction_ia(joueur, la_fonction):
    """
    definit la fonction à appeler pour que ce joueur joue automatiquement

    :param joueur: le joueur
    :param la_fonction: une fonction qui prend en paramètre un dictionnaire donnant l'état du jeu
                        retourne l
    :return: la fonction ne retourne rien mais modifie le joueur
    """
    joueur["ia"] = la_fonction
    return None

def jouer_ia(joueur, etat_jeu):
    """
    appelle la fonction de l'ia associée au joueur et retourne son résultat

    :param joueur: le joueur
    :param etat_jeu: un dictionnaire donnant l'état du jeu
    :return: un ordre pour le joueur sous la forme d'une chaine de caractères
    """
    fonction = joueur['ia'](etat_jeu)
    return fonction


def set_surface(joueur, surface):
    """
    mis à jour la surface recouverte du joueur

    :param joueur: le joueur
    :param surface: un entier positif ou nul
    :return: la fonction ne retourne rien mais modifie le joueur
    """

    joueur["surface"] = surface


def get_surface(joueur):
    """
    retourne la surface recouverte du joueur

    :param joueur: le joueur
    :return: un entier positif ou nul
    """
    if type(joueur) == tuple:
        return joueur[1]['surface']
    return joueur["surface"]


def get_objet_joueur(joueur):
    """
    retourne l'objet possédé par le joueur

    :param joueur: le joueur
    :return: un entier positif ou nul (0 indique que le joueur ne possède pas d'objet)
    """
    if type(joueur) == tuple:
        return joueur[1]['objet']
    return joueur['objet']


def get_couleur_joueur(joueur):
    """
    retourne la couleur du joueur

    :param joueur: le joueur
    :return: une chaine de caractère indiquant la couleur du joueur
    """
    if type(joueur) == tuple:
        return joueur[1]['couleur']
    return joueur["couleur"]


def get_nom_joueur(joueur):
    """
    retourne le nom du joueur

    :param joueur: le joueur
    :return: une chaine de caractère indiquant le nom du joueur
    """
    if type(joueur) == tuple:
        return joueur[1]['nom']
    return joueur["nom"]


def get_reserve_peinture(joueur):
    """
    retourne le nombre de points du joueur

    :param joueur: le joueur
    :return: un entier indiquant le nombre d'unités de peintures possédé par le joueur
    """
    if type(joueur) == tuple:
        return joueur[1]['reserve']
    return joueur["reserve"]


def get_temps_restant(joueur):
    """
    retourne le temps restant pour l'objet que le joueur possède actuellement

    :param joueur: le joueur
    :return: un entier indiquant le temps restant pour l'objet que possède le joueur
             O si le joueur ne possède pas d'objet
    """
    return joueur["temps_restant"]


def ajouter_peinture(joueur, nb_unites):
    """
    ajoute ou enlève des unités de peintures dans la réserve du joueur
    ATTENTION la plus petite valeur pour la réserve est 0 et ne peut donc jamais devenir négative

    :param joueur: le joueur
    :param nb_unites:  un entier relatif (positif ou négatif)
    :return: la fonction ne retourne rien mais modifie le joueur
    """
    joueur["reserve"] += nb_unites
    if joueur["reserve"] <= 0 : joueur["reserve"] = 0


def comparer(joueur1, joueur2):
    """
    compare deux joueurs en fonction de la surface qu'il possède et en cas d'égalité, en fonction de la réserve

    :param joueur1: un joueur
    :param joueur2: un autre joueur
    :return: -1 si joueur1<joueur2, 1 si joueur1>joueur2 et 0 si les deux joueurs ont la même surface et la même réserve
    """
    if type(joueur1) == tuple:
        joueur1 = joueur1[1]
    if type(joueur2) == tuple:
        joueur2 = joueur2[1]
    if get_surface(joueur1) > get_surface(joueur2):
        return 1
    elif get_surface(joueur1) < get_surface(joueur2):
        return -1
    elif get_surface(joueur1) == get_surface(joueur2) :
        if joueur1["reserve"] >joueur2["reserve"]:
            return 1
        elif joueur1["reserve"] == joueur2["reserve"] :
            return 0
        else : return -1


