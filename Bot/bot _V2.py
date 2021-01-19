from labyrinthe import *

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
    case_peint_precedent = None
    position = get_coordonnees_joueur(laby["Labyrinthe"], moi)
    for direction in 'NESO':
        if passage_plateau(laby["Labyrinthe"], position[0], position[1], direction) :
            (_, case_peint) = peindre_direction_couleur(laby["Labyrinthe"], position[0], position[1], direction, get_couleur_joueur(moi), get_reserve_peinture(moi), False, True)
            if case_peint_precedent is None or case_peint > case_peint_precedent :
                case_peint_precedent = case_peint
                direction_ok = direction
    
    res = res + 'P' + direction_ok + 'D' + direction_ok
    #################################################################
    return res
