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
    actions = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'C']
    directions = ['E', 'O', 'S', 'N', 'X']
    positions = ['1', '3', '5']
    dir_peint = random.choice(directions)
    res = 'P' + dir_peint
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
