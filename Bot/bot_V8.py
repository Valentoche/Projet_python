from labyrinthe import *
import math

def le_plus_proche(coordO,coordMoi,plateau):
    mini=None
    coord_mini=None
    for i in range(len(coordO)):
        if accessible(plateau,coordMoi[0],coordMoi[1],coordO[i][0],coordO[i][1]):
            if mini==None or mini > math.sqrt(((coordO[i][0]-coordMoi[0])**2+(coordO[i][1]-coordMoi[1])**2)):
                mini = math.sqrt(((coordO[i][0]-coordMoi[0])**2+(coordO[i][1]-coordMoi[1])**2))
                coord_mini = (coordO[i][0],coordO[i][1])
    return coord_mini



def get_coordonnees_objet(plateau,ia):
    res=[]
    for num_ligne in range(get_nb_lignes(plateau)):
        for num_colonne in range(get_nb_colonnes(plateau)):
            if get_valeur(plateau,num_ligne,num_colonne)['objet']!=0:
                res.append([num_ligne, num_colonne])
    return le_plus_proche(res,ia,plateau)



def carte_selon_direction(plateau, direction, lig, col):
    if direction == 'N' and lig-1>=0:
        return get_valeur(plateau, lig-1, col)
    elif direction == 'S' and lig+1<= get_nb_lignes(plateau):
        return get_valeur(plateau, lig+1, col)
    elif direction == 'E' and col+1<= get_nb_colonnes(plateau):
        return get_valeur(plateau, lig, col+1)
    elif direction == 'O' and col-1>= 0:
        return get_valeur(plateau, lig, col-1)

def donne_direction(liste, position):
    print(liste)
    if liste.count(liste[0]) > 1:
        liste.remove(liste[0])
        i = liste.index(position)
    else :
        i = 0
    if liste[i][0] > liste[i+1][0]:
        return 'N'
    elif liste[i][0] < liste[i+1][0]:
        return 'S'
    elif liste[i][1] > liste[i+1][1]:
        return 'O'
    elif liste[i][1] < liste[i+1][1]:
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
            return donne_direction(history, (lig_depart, col_depart))

def aleatoire():
    res = ''
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
    return res

def choix_tirer(laby, moi, position):
    direction_ok='X'

    if get_objet_joueur(moi)==2:
        traverser_mur=True
    else :
        traverser_mur=False
    case_peint_precedent_peint=None
    ennemi_touche=0
    for direction in 'NESO':
        if passage_plateau(laby["Labyrinthe"], position[0], position[1], direction) :
            (liste_ennemi_touche, case_peint) = peindre_direction_couleur(laby["Labyrinthe"], position[0], position[1], direction, get_couleur_joueur(moi), get_reserve_peinture(moi), traverser_mur, True)
            if len(liste_ennemi_touche)>ennemi_touche:
                case_peint_precedent_peint=case_peint
                direction_ok = direction
                ennemi_touche= len(liste_ennemi_touche)
            elif case_peint_precedent_peint is None or case_peint > case_peint_precedent_peint:
                case_peint_precedent_peint = case_peint
                direction_ok = direction

    res='P'+ direction_ok
    return res


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
    position = get_coordonnees_joueur(laby["Labyrinthe"], moi)
    position_obj = get_coordonnees_objet(laby['Labyrinthe'], get_coordonnees_joueur(laby["Labyrinthe"], moi))
    
    ###################################################################################
    
    
    ###################################################################################

    print(res)
    # print(position_obj)
    # input()
    print(position_obj)
    if position_obj != None:
        print(position_obj)
        chemin_possible = chemin(laby['Labyrinthe'], position[0], position[1], position_obj[0], position_obj[1])
        print(chemin_possible)
        if chemin_possible != None :
            res += 'P' + chemin_possible
            res += 'D' + chemin_possible
        else :
            res += choix_tirer(laby,moi, position)
            res += aleatoire()

    else :
        res += choix_tirer(laby,moi, position)
        res += aleatoire()

    print(res)


    #################################################################
    return res
