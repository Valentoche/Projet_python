# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
from plateau import *

# dictionnaire qui gère le nombre d'unités de peinture gagnées ou perdues en fonction des actions
POINTS = {"objet": 5, "couleur_joueur": 2, "couleur_neutre": -1, "couleur_adversaire": -2, "peindre_adversaire": 3,
          "ordre_errone": -1, }
# constantes indiquant les différents objets disponibles
BOMBE = 1
PISTOLET = 2
BOUCLIER = 3


def Labyrinthe(noms_joueurs, couleurs_joueurs, humain=False, nb_tours=100, duree_objet=10):
    """
    permet de créer un labyrinthe avec nbJoueurs joueurs, nb_tresors trésors
    chacun des joueurs aura au plus nb_tresors_max à trouver
    si ce dernier paramètre est à 0, on distribuera le maximum de trésors possible
    à chaque joueur en restant équitable
    un joueur courant est choisi et la phase est initialisée

    :param noms_joueurs: la liste des noms des joueurs participant à la partie
    :param couleurs_joueurs: la liste des couleurs choisies par chacun des joueurs
    :param humain: un caractère valant 'H' ou 'O' qui indique si le joueur 1 est humain ou ordinateur
    :param nb_tours: un entier indiquant le nombre de tours de la partie
    :param duree_objet: un entier indiquant la durée de validité d'un objet pris par un joueur
    :return: le labyrinthe crée
    """
    participants = Participants(noms_joueurs, couleurs_joueurs, humain)
    plateau = Plateau(participants, 7, 3)
    return {"Labyrinthe":plateau[0], "Carte_sup" : plateau[1], 'participants':participants, 'nb_tour': nb_tours, 'duree_objet':duree_objet, 'rangee_interdite':[1,3,5], 'direction_interdite':None}
    

def initialiser_labyrinthe(participants, plateau, carte_supplementaire, nb_tours, rangee_interdite, direction_interdite, duree_objet):
    """
    Cette fonction permet d'initialiser un labyrinthe avec des valeurs bien précises (permettant de charger une partie
    en cours)

    :param participants: les participants à la partie
    :param plateau: le plateau dans son état actuel
    :param carte_supplementaire: la carte amovible qui est à l'extérieur du plateau
    :param nb_tours: le nombre de tours restants
    :param rangee_interdite: la rangée interdite pour la carte amovible
    :param direction_interdite: la colonne interdite pour la carte amovible
    :param duree_objet: la durée de vie des objets possédés par un joueur
    :return: retourne le labyrinthe avec les caractéristiques passées en paramètre
    """
    return {"Labyrinthe":(plateau,carte_supplementaire), 'participants':participants, 'nb_tour': nb_tours, 'duree_objet':duree_objet, 'rangee_interdite':rangee_interdite, 'direction_interdite':direction_interdite}


def get_nb_tours_restants(labyrinthe):
    """
    donne le nombre de tours restants dans la partie

    :param labyrinthe: un labyrinthe
    :return: un entier donnant le nombre de tours restants
    """
    return labyrinthe['nb_tour'] - labyrinthe['participants']["Tour"]


def get_plateau(labyrinthe):
    """
    retourne la matrice représentant le plateau de jeu

    :param labyrinthe: labyrinthe le labyrinthe considéré
    :return: la matrice représentant le plateau de ce labyrinthe
    """
    return labyrinthe['Labyrinthe']


def get_coordonnees_joueur_courant(labyrinthe):
    """
    donne les coordonnées du joueur courant sur le plateau

    :param labyrinthe: le labyrinthe considéré
    :return: les coordonnées du joueur courant ou None si celui-ci n'est pas sur le plateau
    """
    joueur_courant = get_joueur_courant(labyrinthe['participants'])
    return get_coordonnees_joueur(labyrinthe['Labyrinthe'], joueur_courant)


def prendre_joueur_courant(labyrinthe, lig, col):
    """
    enlève le joueur courant de la carte qui se trouve sur la case lin,col du plateau
    si le joueur ne s'y trouve pas la fonction ne fait rien

    :param labyrinthe: le labyrinthe considéré
    :param lig: la ligne où se trouve la carte
    :param col: la colonne où se trouve la carte
    :return: la fonction ne retourne rien mais modifie le labyrinthe
    """
    joueur_courant = get_joueur_courant(labyrinthe['participants'])
    carte = get_valeur(labyrinthe['Labyrinthe'], lig, col)
    prendre_joueur(carte, joueur_courant)


def poser_joueur_courant(labyrinthe, lig, col):
    """
    pose le joueur courant sur la case lin,col du plateau

    :param labyrinthe: le labyrinthe considéré
    :param lig: la ligne où se trouve la carte
    :param col: la colonne où se trouve la carte
    :return: la fonction ne retourne rien mais modifie le labyrinthe
    """
    joueur_courant = get_joueur_courant(labyrinthe['participants'])
    carte = get_valeur(labyrinthe['Labyrinthe'], lig, col)
    poser_joueur(carte, joueur_courant)


def get_participants(labyrinthe):
    """
    retourne la liste des participants (structure créée dans participants.py

    :param labyrinthe: le labyrinthe considéré
    :return: les joueurs sous la forme de la structure implémentée dans participants.py
    """
    return labyrinthe['participants']


def get_carte_a_jouer(labyrinthe):
    """
    donne la carte à jouer celle qui est hors du plateau

    :param labyrinthe: le labyrinthe considéré
    :return: la carte à jouer
    """
    return labyrinthe['Carte_sup']


def get_duree_objet(labyrinthe):
    """
    permet de connaitre la durée de validité des objets quand ils sont pris par un joueur

    :param labyrinthe: le labyrinthe considéré
    :return: un entier indiquant la durée de validité des objets
    """
    return labyrinthe['duree_objet']


def get_rangee_interdite(labyrinthe):
    """
    retourne le numéro de la rangée interdite

    :param labyrinthe: le labyrinthe considéré
    :return: un entier indiquant la rangée interdite
    """
    return labyrinthe['rangee_interdite']


def get_direction_interdite(labyrinthe):
    """
    retourne le numéro de la direction interdite

    :param labyrinthe: le labyrinthe considéré
    :return: un entier indiquant la direction interdite
    """
    return labyrinthe['direction_interdite']


def coup_interdit(labyrinthe, direction, rangee):
    """
    retourne True si le coup proposé correspond au coup interdit elle retourne False sinon

    :param labyrinthe: le labyrinthe considéré
    :param direction: un caractère 'N', 'E', 'S' ou 'O' indiquant la direction choisie
    :param rangee: un entier indiquant la colonne ou la ligne choisie
    :return: un booléen indiquant si le coup est interdit ou non
    """
    if get_rangee_interdite(labyrinthe) == rangee or get_direction_interdite(labyrinthe) == direction:
        return False
    return True


def lave_et_transfert_joueurs(carte_a_jouer, carte_inseree):
    """
    Permet de laver la carte à jouer (enlever la couleur) et de transférer la liste des joueurs
    qui se trouvent sur la carte_a_jouer vers la carte_inseree

    :param carte_a_jouer: la carte qui vient d'être expulsée du plateau
    :param carte_inseree: la carte qui vient d'être remuise sur le plateau
    :return: cette fonction ne retourne rien
    """
    liste_joueur = get_liste_joueurs(carte_a_jouer)
    set_liste_joueurs(carte_a_jouer, list())
    set_couleur(carte_a_jouer, 'aucune')
    set_liste_joueurs(carte_inseree, liste_joueur)


def jouer_carte(labyrinthe, direction, rangee):
    """
    fonction qui joue la carte amovible dans la direction et sur la rangée passées
    en paramètres. Cette fonction
       - met à jour le plateau du labyrinthe
       - met à jour la carte à jouer
       - met à jour la nouvelle direction interdite

    :param labyrinthe: le labyrinthe
    :param direction: un caractère qui indique la direction choisie ('N','S','E','O')
    :param rangee:  le numéro de la ligne ou de la colonne choisie
    :return: None si tout s'est bien passé ou une chaine de caractères indiquants le problème survenu.
    Voici les messages possibles
        * Carte insérée!
        * Rangée invalide
        * Direction invalide
        * Coup interdit
    """
    if coup_interdit(labyrinthe, direction, rangee) == False :
        return "Coup interdit"
    else :
        if direction == 'N' :
            carte_enlevee = decalage_colonne_en_bas(labyrinthe['Labyrinthe'], rangee, labyrinthe['Carte_sup'])
            lave_et_transfert_joueurs(carte_enlevee, get_valeur(labyrinthe['Labyrinthe'], 0, rangee))
            labyrinthe['Carte_sup'] = carte_enlevee
            return "Carte insérée !"

        if direction == 'S' :
            carte_enlevee = decalage_colonne_en_haut(labyrinthe['Labyrinthe'], rangee, labyrinthe['Carte_sup'])
            lave_et_transfert_joueurs(carte_enlevee, get_valeur(labyrinthe['Labyrinthe'], get_nb_lignes(labyrinthe['Labyrinthe'])-1, rangee))
            labyrinthe['Carte_sup'] = carte_enlevee
            return "Carte insérée !"
        
        if direction == 'E' :
            carte_enlevee = decalage_ligne_a_droite(labyrinthe['Labyrinthe'], rangee, labyrinthe['Carte_sup'])
            lave_et_transfert_joueurs(carte_enlevee, get_valeur(labyrinthe['Labyrinthe'], rangee, 0))
            labyrinthe['Carte_sup'] = carte_enlevee
            return "Carte insérée !"

        if direction == 'O' :
            carte_enlevee = decalage_ligne_a_gauche(labyrinthe['Labyrinthe'], rangee, labyrinthe['Carte_sup'])
            lave_et_transfert_joueurs(carte_enlevee, get_valeur(labyrinthe['Labyrinthe'], rangee, get_nb_colonnes(labyrinthe['Labyrinthe'])-1))
            labyrinthe['Carte_sup'] = carte_enlevee
            return "Carte insérée !"

    return "Direction invalide"

        

def tourner_carte(labyrinthe, sens='H'):
    """
    Tourne la carte à jouer dans le sens indiqué en paramètre (H horaire A antihoraire)

    :param labyrinthe:  le labyrinthe considéré
    :param sens: un caractère indiquant le sens dans lequel tourner la carte ('A' ou 'H')
    :return: un chaine de caractères indiquant ce qui s'est passé
        * Carte tournée!
        * Ordre pour tourner la carte inconnu
    """
    if sens == 'H' :
        tourner_horaire(labyrinthe['Carte_sup'])
        return "Carte tournée!"
    elif sens == 'A':
        tourner_antihoraire(labyrinthe['Carte_sup'])
        return "Carte tournée!"
    else :
        return "Ordre pour tourner la carte inconnu"

def peindre(labyrinthe, direction):
    """
    Permet de peindre de la couleur du joueur courant toutes les cases atteignables dans la direction choisie.
    Si direction vaut 'X' la fonction ne fait rien (le joueur courant ne veut pas peindre)
    Cette fonction va donc
        * peindre toutes les cartes atteignables à partir de la position du joueur courant dans la direction choisie
        * enlever au joueur courant le nombre d'unités de peinture correspond au nombre de cases peintes
        * enlever aux joueurs ne possedant pas de bouclier et touchés par le jet de peinture le nombre d'unités
          prévu par POINTS["peindre_adversaire"]
        * ajouter au joueur courant le nombre d'unités de peinture enlevés aux adversaires
    De plus si le joueur courant possède un pistolet son jet de peinture doit traverser un mur et si il possède une
    bombe le jet de peinture doit aller dans toutes les directions en commençant par direction et en allant dans le
    sens des aiguilles d'une montre

    :param labyrinthe: le labyrinthe considéré
    :param direction: un caractère qui indique la direction choisie ('X', 'N','S','E','O')
    :return: un chaine de caractères indiquant ce qui s'est passé
        * Le joueur ne veut pas peindre
        * Le joueur a peint dans la direction ...
        * Direction inconnue
    """
    if direction == 'X':
        return "Le joueur ne veut pas peindre"
    if direction not in 'NSEO' :
        return "Direction inconnue"

    coordonnee_joueur = get_coordonnees_joueur_courant(labyrinthe)
    if coordonnee_joueur != None :
        joueur_courant = get_joueur_courant(labyrinthe['participants'])
        liste_joueur_touchees = list()

        if get_objet_joueur(joueur_courant) == 2 :
            peindre = peindre_direction_couleur(labyrinthe['Labyrinthe'], coordonnee_joueur[0], coordonnee_joueur[1], direction, get_couleur_joueur(joueur_courant), get_reserve_peinture(joueur_courant), True, False)
            liste_joueur_touchees.append(peindre[0])
            ajouter_peinture(joueur_courant, -peindre[1])
        
        elif get_objet_joueur(joueur_courant) == 1:
            if direction == 'N' :
                sens = 'NESO'
            elif direction == 'E' :
                sens = 'ESON'
            elif direction == 'S' :
                sens = 'SONE'
            else :
                sens = 'ONES'

            for dire in sens :
                peindre = peindre_direction_couleur(labyrinthe['Labyrinthe'], coordonnee_joueur[0], coordonnee_joueur[1], dire, get_couleur_joueur(joueur_courant), get_reserve_peinture(joueur_courant), False, False)
                liste_joueur_touchees.append(peindre[0])
                ajouter_peinture(joueur_courant, -peindre[1])

        else :
            peindre = peindre_direction_couleur(labyrinthe['Labyrinthe'], coordonnee_joueur[0], coordonnee_joueur[1], direction, get_couleur_joueur(joueur_courant), get_reserve_peinture(joueur_courant), False, False)
            liste_joueur_touchees.append(peindre[0])
            ajouter_peinture(joueur_courant, -peindre[1])
        
        for sous_liste_joueur in liste_joueur_touchees :
            for joueur in sous_liste_joueur :
                if get_objet_joueur(joueur) != 3:
                    ajouter_peinture(joueur, -POINTS["peindre_adversaire"])
                    ajouter_peinture(joueur_courant, POINTS["peindre_adversaire"])
        
        couleur = nb_cartes_par_couleur(labyrinthe['Labyrinthe'])
        mise_a_jour_surface(labyrinthe["participants"], couleur)
        
        
        return "Le joueur a peint dans la direction "

def deplacer(labyrinthe, direction):
    """
    Déplace le joueur courant dans la direction souhaitée si c'est possible. Cette fonction va notamment:
    * verifier que le déplacement est possible
    * déplacer le joueur
    * donner au joueur courant l'objet qu'il y a sur la carte d'arrivée (si elle possède un objet) en augmentant
      la réserve de peinture du joueur de POINTS["objet"]
    * mettre à jour la réserve de peinture du joueur en fonction de la couleur de la case d'arrivée
      (POINTS["couleur_joueur"], POINTS["couleur_neutre"] ou POINTS["couleur_adversaire"]
    Si le joueur donne un ordre erroné ou un déplacement impossible il perd POINTS["ordre_errone"] unité de peinture

    :param labyrinthe: le labyrinthe considéré
    :param direction: un caractère qui indique la direction choisie ('N','S','E','O')
    :return: un chaine de caractères indiquant ce qui s'est passé
        * La direction est inconnue
        * Le déplacement est impossible
        * Le joueur s'est déplacé vers ...
        * Le joueur s'est déplacé vers ... et un trouvé un objet
    """
    joueur = get_joueur_courant(labyrinthe['participants'])

    if direction not in 'NESO':
        ajouter_peinture(joueur, POINTS["ordre_errone"])
        return "La direction est inconnue"

    position = get_coordonnees_joueur_courant(labyrinthe)
    if position != None :
        passage = passage_plateau(labyrinthe['Labyrinthe'], position[0], position[1], direction)

        if passage != None :
            prendre_joueur_courant(labyrinthe, position[0], position[1])
            poser_joueur_courant(labyrinthe, passage[0], passage[1])

            if get_couleur(get_valeur(labyrinthe['Labyrinthe'], passage[0], passage[1])) == get_couleur_joueur(joueur):
                ajouter_peinture(joueur, POINTS["couleur_joueur"])
            elif get_couleur(get_valeur(labyrinthe['Labyrinthe'], passage[0], passage[1])) == None :
                ajouter_peinture(joueur, POINTS["couleur_neutre"])
            else :
                ajouter_peinture(joueur, POINTS["couleur_adversaire"])
            
            carte = get_valeur(labyrinthe['Labyrinthe'], passage[0], passage[1])
            objet = get_objet(carte)
            if objet != 0 :
                prendre_objet(carte)
                ajouter_objet(joueur, objet, labyrinthe['duree_objet'])
                ajouter_peinture(joueur, POINTS["objet"])
                return ("Le joueur s'est déplacé vers " + str(direction) + "et un trouvé un objet")
            
            return ("Le joueur s'est déplacé vers " + str(direction))
        else :
            ajouter_peinture(joueur, POINTS["ordre_errone"])
            return "Le déplacement est impossible"

    
def interpreter_ordre(labyrinthe, ordre):
    """
    Cette fonction executes les ordres fournie sous la forme d'une chaine de caractères commençant par l'ordre de
    peinture puis l'ordre de déplacement ou l'ordre de modification du labyrinthe. Tous les ordres commencent par un P
    suivi d'une des lettre X N O S ou E indiquant la direction où peindre (X indiquant que le joueur ne souhaite pas
    peindre) . La seconde partie de l'ordre est
        * soit un D (pour déplacement) suivi d'une des lettres N O S ou E
        * soit un T (pour tourner) suivi d'une suite de H ou de A suivi une des lettres N O S ou E suivi d'un chiffre
    Par exemple:
        * "PODE" indique que le joueur peint vers l'ouest et se déplace vers l'est
        * "PXTAAN3" indique que le joueur ne souhaite pas peindre et qu'il tourne la carte amovible deux fois dans le
            sens antihoraire puis insère la carte amovible au nord dans la colonne 3

    :param labyrinthe: le labyrinthe considéré
    :param ordre: un chaine de caractère comme indiquée ci-dessus
    :return: une chaine de caractères indiquant ce qui s'est passé
    """
    peinture = peindre(labyrinthe, ordre[1])

    if ordre[2] == 'D' :
        deplacement = deplacer(labyrinthe, ordre[3])
        return (peinture)

    elif ordre[2] == 'T' :
        for i in range(3, len(ordre)):
            if ordre[i] == 'A' or ordre[i] == 'H':

                tourner = tourner_carte(labyrinthe, ordre[i])
            elif ordre[i] in 'NESO':
                inseree = jouer_carte(labyrinthe, ordre[i], int(ordre[i+1]))
                return (peinture)
    
def finir_tour(labyrinthe):
    """
     met a jour les différentes informations sur les joueurs
     * le temps restant de l'objet du joueur courant
     * la surface couverte par chaque joueur
     change le joueur courant (et met à jour le compteur de tour si nécessaire
    vérifie si la partie est terminée, si ce n'est pas le cas passe au joueur suivant

    :param labyrinthe: labyrinthe considéré
    :return: Cette fonction retourne rien mais elle modifie le labyrinthe
    """
    
    retour_premier_joueur = changer_joueur_courant(labyrinthe['participants'])

    if retour_premier_joueur :
        labyrinthe['participants']['Tour'] += 1
    
    couleur = nb_cartes_par_couleur(labyrinthe['Labyrinthe'])
    mise_a_jour_surface(labyrinthe["participants"], couleur)


###################################################
### Fonctions utilitaires qui permettent de transmettre l'état du labyrinthe à une intelligence artificielle
###################################################

def joueur_2_dico(joueur):
    return {
        "nom": get_nom_joueur(joueur), "objet": get_objet_joueur(joueur), "couleur": get_couleur_joueur(joueur),
        "reserve_peinture": get_reserve_peinture(joueur), "surface": get_surface(joueur),
        "type_joueur": get_type_joueur(joueur), "temps_restant": get_temps_restant(joueur)
    }


def participants_2_dico(participants):
    nb_participants = get_nb_joueurs(participants)
    liste_joueurs = [joueur_2_dico(get_joueur_par_num(participants, i)) for i in range(1, nb_participants + 1)]
    return {"liste_joueurs": liste_joueurs, "joueur_courant": get_num_joueur_courant(participants),
            "premier_joueur": get_num_premier_joueur(participants)
            }


def carte_2_dico(carte):
    return {"murs": coder_murs(carte), "pions": [get_nom_joueur(joueur) for joueur in get_liste_joueurs(carte)],
            "objet": get_objet(carte), "couleur": get_couleur(carte)}


def matrice_2_dico(matrice):
    nb_lig = get_nb_lignes(matrice)
    nb_col = get_nb_colonnes(matrice)
    res = {"nb_lignes": nb_lig, "nb_colonnes": nb_col,
           "les_valeurs": [carte_2_dico(get_valeur(matrice, i, j)) for i in range(nb_lig) for j in range(nb_col)]}
    return res


def labyrinthe_2_dico(labyrinthe):
    return {
        "les_joueurs": participants_2_dico(get_participants(labyrinthe)),
        "plateau": matrice_2_dico(get_plateau(labyrinthe)),
        "carte": carte_2_dico(get_carte_a_jouer(labyrinthe)),
        "nb_tours": get_nb_tours_restants(labyrinthe),
        "rangee_interdite": get_rangee_interdite(labyrinthe),
        "direction_interdite": get_direction_interdite(labyrinthe),
        "duree_objet": get_duree_objet(labyrinthe)
    }


def labyrinthe_from_dico(dico_lab):
    participants = Participants([], [])
    for dico_joueur in dico_lab["les_joueurs"]["liste_joueurs"]:
        joueur = Joueur(dico_joueur["nom"], dico_joueur["couleur"], dico_joueur["reserve_peinture"],
                        dico_joueur["surface"], dico_joueur["type_joueur"],dico_joueur["objet"],
                        dico_joueur["temps_restant"])
        ajouter_joueur(participants, joueur)
    init_premier_joueur(participants, dico_lab["les_joueurs"]["premier_joueur"])
    set_joueur_courant(participants, dico_lab["les_joueurs"]["joueur_courant"])
    nb_lig = dico_lab["plateau"]["nb_lignes"]
    nb_col = dico_lab["plateau"]["nb_colonnes"]
    plateau = Matrice(nb_lig, nb_col)
    for i in range(nb_lig * nb_col):
        carte_dico = dico_lab["plateau"]["les_valeurs"][i]
        carte = Carte(True, True, True, True)
        decoder_murs(carte, carte_dico["murs"])
        poser_objet(carte, carte_dico["objet"])
        set_couleur(carte, carte_dico["couleur"])
        pions = [get_joueur_par_nom(participants, nom) for nom in carte_dico["pions"]]
        set_liste_joueurs(carte, pions)
        set_valeur(plateau,i//nb_col,i%nb_col,carte)
    carte = Carte(True, True, True, True)
    decoder_murs(carte, dico_lab["carte"]["murs"])
    poser_objet(carte, dico_lab["carte"]["objet"])
    return initialiser_labyrinthe(participants, plateau, carte, dico_lab["nb_tours"], dico_lab["rangee_interdite"],
                                  dico_lab["direction_interdite"], dico_lab["duree_objet"])


