from labyrinthe import *
import math

def le_plus_proche(coordO,coordMoi,plateau):
    coo = None
    for i in range(len(coordO)):
        if accessible(plateau, coordMoi[0], coordMoi[1], coordO[i][0], coordO[i][1]) :
            return (coordO[i][0], coordO[i][1])
    return coo



def get_coordonnees_objet(plateau,ia):
    res=[]
    for num_ligne in range(get_nb_lignes(plateau)):
        for num_colonne in range(get_nb_colonnes(plateau)):
            if get_objet(get_valeur(plateau,num_ligne,num_colonne))!=0 and accessible(plateau, ia[0], ia[1], num_ligne, num_colonne):
                return (num_ligne, num_colonne)
    return None



def carte_selon_direction(plateau, direction, lig, col):
    if direction == 'N' and lig-1>=0:
        return get_valeur(plateau, lig-1, col)
    elif direction == 'S' and lig+1<= get_nb_lignes(plateau):
        return get_valeur(plateau, lig+1, col)
    elif direction == 'E' and col+1<= get_nb_colonnes(plateau):
        return get_valeur(plateau, lig, col+1)
    elif direction == 'O' and col-1>= 0:
        return get_valeur(plateau, lig, col-1)

def donne_direction(liste):
    print(liste)
    if liste[0][0] > liste[1][0]:
        return 'N'
    elif liste[0][0] < liste[1][0]:
        return 'S'
    elif liste[0][1] > liste[1][1]:
        return 'O'
    elif liste[0][1] < liste[1][1]:
        return 'E'


def chemin(plateau, lig_depart, col_depart, lig_arrivee, col_arrivee):
    act = (lig_depart, col_depart)
    tested = [act]
    history = [act]
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
    
    for i in range(7*7):
        next = None
        i = 0
        while i < len(directions) and (next is None or next in tested): 
            next = passage_plateau(plateau, act[0], act[1], directions[i])
            i += 1
        if not next is None: 
            act = next
            tested.append(act)
            history.append(act)
        elif next is None and act == (lig_depart, col_depart): 
            return False
        else:
            if history != list():
                act = history.pop(-1)
        
        if act == (lig_arrivee, col_arrivee):
            return donne_direction(history)


def calculer_action(labyrinthe_dico):
    """
    :param labyrinthe_dico: un dictionnaire qui permet de reconstruire le jeu suivant votre représentation
           grâce à la fonction labyrinthe_from_dico
    :return: un ordre sous la forme d'une chaîne de caractères (voir docstring de interpreter_ordre)
    """
    laby = labyrinthe_from_dico(labyrinthe_dico)  # récupération du labyrinthe
    moi = get_joueur_courant(get_participants(laby))  # le joueur qui joue cette IA
    res = ''
    #################################################################
    # Remplacer cela par votre IA
    direction = 'NESO'
    case_peint_precedent = None
    direction_ok = None
    position = get_coordonnees_joueur(laby["Labyrinthe"], moi)
    position_obj = get_coordonnees_objet(laby['Labyrinthe'], get_coordonnees_joueur(laby["Labyrinthe"], moi))
    
    ###################################################################################
    for direction in 'NESO':
        if passage_plateau(laby["Labyrinthe"], position[0], position[1], direction) :
            (_, case_peint) = peindre_direction_couleur(laby["Labyrinthe"], position[0], position[1], direction, get_couleur_joueur(moi), get_reserve_peinture(moi), False, True)
            if case_peint_precedent is None or case_peint > case_peint_precedent :
                case_peint_precedent = case_peint
                direction_ok = direction
    
    ###################################################################################

    if direction_ok is None or get_couleur(carte_selon_direction(laby['Labyrinthe'], direction_ok, position[0], position[1])) == get_couleur_joueur(moi):
        res += 'PX'
    else :
        res += 'P' + direction_ok
    print(res)
    # print(position_obj)
    input()
    # res = 'PX'
    actions = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C']
    directions = ['E', 'O', 'S', 'N', 'X']
    positions = ['1', '3', '5']
    action = 'D'
    print(position_obj)
    if position_obj != None:
        print(position_obj)
        chemin_possible = chemin(laby['Labyrinthe'], position[0], position[1], position_obj[0], position_obj[1])
        print(chemin_possible)
        if chemin_possible != None :
            res += 'D' + chemin_possible
        else :
            res += 'D' + 'N'
        # if position[0] > position_obj[0] and passage_plateau(laby['Labyrinthe'], position[0], position[1], 'E'):
        #     res += 'DE'
        # elif position[0] < position_obj[0] and passage_plateau(laby['Labyrinthe'], position[0], position[1], 'O'):
        #     res += 'DO'
        # elif position[1] < position_obj[1] and passage_plateau(laby['Labyrinthe'], position[0], position[1], 'S') :
        #     res += 'DS'
        # elif position[1] > position_obj[1] and passage_plateau(laby['Labyrinthe'], position[0], position[1], 'N') :
        #     res += 'DN'
    else :
        # direction = random.choice(directions[:-1])
         res += 'D' + 'N'


        # tourne = random.randint(0, 4)
        # tournage = 'H' * tourne
        # res += 'T' + tournage
        # res += random.choice(directions)
        # res += random.choice(positions)

    print(res)
    # print(get_coordonnees_objet(laby["Labyrinthe"], get_coordonnees_joueur(laby["Labyrinthe"], moi)))

    #################################################################
    return res
