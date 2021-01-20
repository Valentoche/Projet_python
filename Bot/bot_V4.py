from labyrinthe import *

def coordonnee_objet(plateau, objet) :
    for ligne in range(get_nb_lignes(plateau)):
        for colonne in range(get_nb_colonnes(plateau)):
            if get_objet(get_valeur(plateau, ligne, colonne)) == objet:
                return (ligne, colonne)
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
    for direction in 'NESO':
        if passage_plateau(laby["Labyrinthe"], position[0], position[1], direction) :
            (_, case_peint) = peindre_direction_couleur(laby["Labyrinthe"], position[0], position[1], direction, get_couleur_joueur(moi), get_reserve_peinture(moi), False, True)
            if case_peint_precedent is None or case_peint > case_peint_precedent and get_couleur(carte_selon_direction(laby['Labyrinthe'], direction_ok, position[0], position[1])) != get_couleur_joueur(moi) :
                case_peint_precedent = case_peint
                direction_ok = direction
    
    if direction_ok is None:
        res += 'PX'
    else :
        res += 'P' + direction_ok


    # res = 'PX'
    actions = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C']
    directions = ['E', 'O', 'S', 'N', 'X']
    positions = ['1', '3', '5']
    action = random.choice(actions)
    if action == 'D':
        direction = random.choice(directions[:-1])
        res += action + direction
    elif action == 'C':
        tourne = random.randint(0, 4)
        tournage = 'H' * tourne
        res += 'T' + tournage
        res += random.choice(directions)
        res += random.choice(positions)




    #################################################################
    return res
