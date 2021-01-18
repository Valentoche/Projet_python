#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
                           Projet Splaby'O
        Projet Python 2020-2021 de 1ere année et AS DUT Informatique Orléans

"""
import os
import signal
import argparse

import pygame

from labyrinthe import *


class IaTimeout(Exception):
    pass


class iatimeout:
    def __init__(self, seconds, error_message=None):
        if error_message is None:
            error_message = 'ordre non reçu après {}s.'.format(seconds)
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise IaTimeout(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


class LabyrintheGraphique(object):
    """Classe simple d'affichage et d'interaction pour le labyrinthe."""

    def __init__(self, labyrinthe, titre="Splaby'O", size=(1000, 800), couleur=(209, 238, 238),
                 prefixe_image="./images", mode_concours=False):
        """Method docstring."""
        self.noms = ["aucune", "chimie", "gea", "gmp", "gte", "info", "qlio"]
        self.message_info = None
        self.img_info = None
        self.mode_concours = mode_concours
        self.labyrinthe = labyrinthe
        self.fini = False
        self.couleur_texte = couleur
        self.la_matrice = get_plateau(labyrinthe)
        self.nb_colonnes = get_nb_colonnes(self.la_matrice)
        self.nb_lignes = get_nb_lignes(self.la_matrice)
        self.les_joueurs = get_participants(labyrinthe)
        self.interactif = get_type_joueur(get_joueur_courant(self.les_joueurs)) == 'H'
        self.phase = 1
        self.titre = titre
        self.images_cartes = {}
        self.images_pions = {}
        self.images_objets = {}
        self.icone = None
        self.hauteur = 0
        self.largeur = 0
        self.deltah = 0
        self.deltal = 0
        self.finh = 0
        self.finl = 0
        self.taille_font = 0
        self.get_images(prefixe_image)
        pygame.init()
        pygame.display.set_icon(self.icone)
        pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.maj_parametres()
        self.affiche_jeu()

    def get_images(self, prefixe_image="./images"):

        for nom in self.noms:
            self.images_cartes[nom] = []
            # lecture des différentes cartes dans les fichiers nommés Cartexxx.jpeg où xxx va de 1 à 12
            for i in range(16):
                if os.path.isfile(os.path.join(prefixe_image + "/" + nom, 'Carte' + str(i) + '.jpeg')):
                    s = pygame.image.load(os.path.join(prefixe_image + "/" + nom, 'Carte' + str(i) + '.jpeg'))
                else:
                    s = None
                self.images_cartes[nom].append(s)

        # lecture des différents pions

        for nom in self.noms[1:]:
            s = pygame.image.load(os.path.join(prefixe_image + "/" + nom, 'pion.png'))
            self.images_pions[nom] = s

        # lecture des différents objets dans les fichiers de la forme objetxxx.png où xxx va de 0 à 3
        i = 1
        while os.path.isfile(os.path.join(prefixe_image, 'objet' + str(i) + '.png')):
            s = pygame.image.load(os.path.join(prefixe_image, 'objet' + str(i) + '.png'))
            self.images_objets[i] = s
            i += 1

        # lecture du logo de l'IUT'O
        icone_img = pygame.image.load(os.path.join(prefixe_image, 'logo.jpeg'))
        self.icone = pygame.transform.smoothscale(icone_img, (50, 50))

    def maj_parametres(self):
        """
        permet de mettre à jour les paramètre d'affichage en cas de redimensionnement de la fenêtre
        """
        self.surface = pygame.display.get_surface()
        self.hauteur = self.surface.get_height() * 2 // 3
        self.largeur = self.hauteur
        self.deltah = self.hauteur // (self.nb_lignes + 2)
        self.deltal = self.largeur // (self.nb_colonnes + 2)
        self.finh = self.deltah * (self.nb_lignes + 2)
        self.finl = self.deltal * (self.nb_colonnes + 2)
        self.taille_font = min(self.deltah, self.deltal) * 2 // 3

    def surface_carte(self, carte):
        """
        transforme une carte en une surface (image 2D) avec les pions et trésor associés
        """
        objet = get_objet(carte)
        pions = get_liste_joueurs(carte)
        couleur = get_couleur(carte)
        img = self.images_cartes[couleur][coder_murs(carte)]
        if img is None:
            return None

        surf_carte = pygame.transform.smoothscale(img, (self.deltal, self.deltah))
        dist = 5
        coord = [(dist, dist), (dist, self.deltah - (self.deltah // 2 + dist)),
                 (self.deltal - (self.deltal // 2 + dist), self.deltah - (self.deltah // 2 + dist)),
                 (self.deltal - (self.deltal // 2 + dist), dist)]
        for pion in pions:
            surf_pion = pygame.transform.smoothscale(
                self.surface_pion(pion, True),
                (self.deltal // 2, self.deltah // 2))
            surf_carte.blit(surf_pion, coord.pop(0))
        if get_objet(carte) != 0:
            surf_objet = pygame.transform.smoothscale(self.images_objets[get_objet(carte)],
                                                      (self.deltal // 4, self.deltah // 4))
            surf_carte.blit(surf_objet, (self.deltah // 4 + dist, self.deltah // 4 + dist))
        return surf_carte

    def surface_fleche(self, direction='O', couleur=(209, 238, 238)):
        """
        transforme une direction en une image de flèche qui sera affichée sur l'écran
        """
        res = pygame.Surface((self.deltal, self.deltah))
        pygame.draw.polygon(res, couleur,
                            [(self.deltal // 2, self.deltah // 3), (self.deltal - self.deltal // 8, self.deltah // 2),
                             (self.deltal // 2, self.deltah * 2 // 3)], 0)
        if direction == 'N':
            res = pygame.transform.rotate(res, -90.0)
        elif direction == 'E':
            res = pygame.transform.rotate(res, 180.0)
        elif direction == 'S':
            res = pygame.transform.rotate(res, 90.0)
        return res

    def surface_pion(self, joueur, affiche_objet=False):
        """
        transforme un numéro de pion en son image
        """
        couleur = get_couleur_joueur(joueur)
        objet = get_objet_joueur(joueur)
        res = pygame.Surface((self.deltal, self.deltah), pygame.SRCALPHA)
        surf_pion = pygame.transform.smoothscale(self.images_pions[couleur], (self.deltal // 2, self.deltah // 2))
        res.blit(surf_pion, (self.deltal // 4, self.deltah // 4))
        if affiche_objet and objet != 0:
            surf_objet = pygame.transform.smoothscale(self.images_objets[objet],
                                                      (self.deltal // 5, self.deltah // 5))
            res.blit(surf_objet, (self.deltal // 5, self.deltah // 5))
        return res

    def surface_objet(self, objet):
        """
        produit l'image de l'objet dont le numéro est passé en paramètre
        """
        res = pygame.Surface((self.deltal, self.deltah))
        surf_objet = pygame.transform.smoothscale(self.images_objets[objet], (self.deltal // 2, self.deltah // 2))
        res.blit(surf_objet, (self.deltal // 4, self.deltah // 4))
        return res

    def affiche_message(self, ligne, texte, images=[], couleur=None):
        """
        affiche un message en mode graphique à l'écran
        """
        font = pygame.font.Font(None, self.taille_font)
        if couleur is None:
            couleur = self.couleur_texte
        posy = self.finh + self.deltah * (ligne - 1)
        posx = self.deltal // 3

        liste_textes = texte.split('@img@')
        for msg in liste_textes:
            if msg != '':
                texte = font.render(msg, True, couleur)
                textpos = texte.get_rect()
                textpos.y = posy
                textpos.x = posx
                self.surface.blit(texte, textpos)
                posx += textpos.width
            if images != []:
                surface = images.pop(0)
                debuty = posy - (self.deltah // 3)
                self.surface.blit(surface, (posx, debuty))
                posx += surface.get_width()

    def affiche_joueurs(self, couleur=None):
        font = pygame.font.Font(None, self.taille_font)
        if couleur is None:
            couleur = self.couleur_texte
        posx = self.finl + self.deltal // 3
        posy = self.deltah
        classement = classement_joueurs(self.les_joueurs)
        for joueur in classement:
            nom = get_nom_joueur(joueur)
            surface = get_surface(joueur)
            points = get_reserve_peinture(joueur)
            contenu = "{} {:.2%} ({})"
            surfp = self.surface_pion(joueur)
            objet = get_objet_joueur(joueur)
            if objet != 0:
                surfo = self.surface_objet(objet)
            else:
                surfo = pygame.Surface((self.deltal // 4, self.deltal // 4))
            self.surface.blit(surfp, (posx, posy - self.deltah // 3))
            texte = font.render(contenu.format(nom[:12], (surface / (self.nb_colonnes * self.nb_lignes)), points), True,
                                couleur)
            textpos = texte.get_rect()
            textpos.y = posy
            textpos.x = posx + surfp.get_width()
            self.surface.blit(texte, textpos)
            textpos.x += texte.get_width()
            textpos.y = posy - self.deltah // 3
            self.surface.blit(surfo, textpos)
            posy += texte.get_height() * 2

    def affiche_message_info(self, num_ligne=4):
        """
        affiche un message d'information aux joueurs
        """
        if self.message_info is not None:
            self.affiche_message(num_ligne, self.message_info, self.img_info)
        self.message_info = None
        self.img_info = None

    def affiche_carte_a_jouer(self):
        """
        affiche la carte à jouer
        """
        self.surface.blit(self.surface_carte(get_carte_a_jouer(self.labyrinthe)),
                          (self.finl + self.deltal // 2, self.finh // 2))

    def dessine_grille(self, couleur=(255, 0, 0)):
        """
        dessine la grille sur laquelle on va afficher le labyrinthe (avec les flèches notamment)
        """
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(None, self.taille_font)
        fleche_ouest = self.surface_fleche('O')
        fleche_est = self.surface_fleche('E')
        fleche_nord = self.surface_fleche('N')
        fleche_sud = self.surface_fleche('S')
        for i in range(1, self.nb_lignes, 2):
            self.surface.blit(fleche_ouest, (0, (i + 1) * self.deltah))
            self.surface.blit(fleche_est, (self.deltal * (self.nb_colonnes + 1), (i + 1) * self.deltah))

        for i in range(1, self.nb_colonnes, 2):
            self.surface.blit(fleche_nord, ((i + 1) * self.deltal, 0))
            self.surface.blit(fleche_sud, ((i + 1) * self.deltah, self.deltah * (self.nb_lignes + 1)))

    def affiche_grille(self):
        """
        affiche le labyrinthe
        """
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                try:
                    carte = get_valeur(self.la_matrice, i, j)
                    s = self.surface_carte(carte)
                    if s is None:
                        self.surface.fill((0, 0, 0),
                                          ((j + 1) * self.deltal, (i + 1) * self.deltah, self.deltal, self.deltah))
                    else:
                        self.surface.blit(s, ((j + 1) * self.deltal, (i + 1) * self.deltah))
                except Exception as ex:
                    print(ex, i, j)
                    pass

    def get_case(self, pos):
        """
        transforme une position de souris en coordonnées de case de labyrinthe. 
        Si on clique sur la carte à jouer la fonction retourne ('T','T'), 
        Si on clique hors du labyrinthe la fonction retourne (-1,-1)
        Si on clique sur une flèche de direction la fonction retourne la direction et le numéro de la colonne
        si on clique sur une carte de labyrinthe la fonction retourne les coordonnées x,y de la carte
        """
        if self.finl + self.deltal // 2 <= pos[0] <= self.finl + self.deltal // 2 + self.deltal and self.finh // 2 <= \
                pos[1] <= self.finh // 2 + self.deltah:
            return ('T', 'T')
        if pos[0] < 0 or pos[0] > self.finl or pos[1] < 0 or pos[1] > self.finh:
            return (-1, -1)

        x = pos[1] // self.deltah
        y = pos[0] // self.deltal
        if x == 0 and y in [2, 4, 6]:
            return ('N', y - 1)
        if x == self.nb_colonnes + 1 and y in [2, 4, 6]:
            return ('S', y - 1)
        if y == 0 and x in [2, 4, 6]:
            return ('O', x - 1)
        if y == self.nb_lignes + 1 and x in [2, 4, 6]:
            return ('E', x - 1)
        if x == 0 or x == self.nb_colonnes + 1 or y == 0 or y == self.nb_lignes + 1:
            return (-1, -1)
        return (x - 1, y - 1)

    def affiche_jeu(self):
        """
        affiche l'ensemble du jeu du labyrinthe
        """
        self.dessine_grille()
        self.affiche_grille()
        if self.fini:
            self.affiche_message(2, "La partie est terminée")
        else:
            self.affiche_message(2, "C'est au joueur @img@ de jouer",
                                 [self.surface_pion(get_joueur_courant(self.les_joueurs))])
        nb_tours = get_nb_tours_restants(self.labyrinthe)
        pluriel = "s"
        if nb_tours <= 1:
            pluriel = ""
        self.affiche_message(3, "il reste " + str(nb_tours) + " tour" + pluriel + " de jeu", [])
        self.affiche_carte_a_jouer()
        self.affiche_joueurs()
        pygame.display.flip()

    def demarrer(self):
        """
        démarre l'environnement graphique et la boucle d'écoute des événements
        """
        pygame.time.set_timer(pygame.USEREVENT + 1, 200)
        clock = pygame.time.Clock()
        while (True):
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break

            if ev.type == pygame.USEREVENT + 1:
                if self.fini:
                    self.affiche_jeu()
                    continue
                if self.interactif:
                    continue
                jc = get_joueur_courant(self.les_joueurs)
                ordre = ""
                try:
                    with iatimeout(1):
                        if self.mode_concours:
                            ordre = bot.calculer_action(labyrinthe_2_dico(self.labyrinthe))
                        else:
                            ordre = jouer_ia(jc, "")
                except Exception as e:
                    print(e)
                    self.affiche_message(4, "Ordre non reçu", [])

                interpreter_ordre(self.labyrinthe, ordre)
                finir_tour(self.labyrinthe)
                self.interactif = get_type_joueur(get_joueur_courant(self.les_joueurs)) == 'H'
                self.affiche_jeu()
            if ev.type == pygame.VIDEORESIZE:
                fenetre = pygame.display.set_mode(ev.size, pygame.RESIZABLE | pygame.DOUBLEBUF)
                self.maj_parametres()
                self.affiche_jeu()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                (gauche, milieu, droite) = pygame.mouse.get_pressed()
                if self.fini or not self.interactif:
                    continue
                if self.phase == 1 and gauche:
                    continue
                if self.phase == 2 and droite:
                    continue

                (x, y) = self.get_case(ev.pos)
                if x == 'T':
                    tourner_carte(self.labyrinthe, 'H')
                elif x in ['N', 'S', 'E', 'O']:
                    jouer_carte(self.labyrinthe, x, y)
                    finir_tour(self.labyrinthe)
                    self.phase = 1
                    self.interactif = get_type_joueur(get_joueur_courant(self.les_joueurs)) == 'H'
                elif x != (-1, -1):
                    ligne_cour, col_cour = get_coordonnees_joueur_courant(self.labyrinthe)
                    d_x = x - ligne_cour
                    d_y = y - col_cour
                    if d_x == 0:
                        if d_y < 0:
                            direction = 'O'
                        elif d_y > 0:
                            direction = 'E'
                        else:
                            direction = 'X'  # le joueur a cliqué sur la case ou il se situe
                    elif d_y == 0:
                        if d_x < 0:
                            direction = 'N'
                        else:
                            direction = 'S'
                    else:
                        direction = '_'
                    if direction != '_':
                        if gauche:
                            deplacer(self.labyrinthe, direction)
                            finir_tour(self.labyrinthe)
                            self.interactif = get_type_joueur(get_joueur_courant(self.les_joueurs)) == 'H'
                            self.phase = 1
                        elif droite:
                            peindre(self.labyrinthe, direction)
                            self.phase = 2

                self.affiche_jeu()
            self.fini = get_nb_tours_restants(self.labyrinthe) == 0
        pygame.quit()


# ------------------------------
# programme principal
# ------------------------------

if __name__ == '__main__':
    print("Bienvenue dans le jeu du Splaby'O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode_concours", help="Indique si on doit utiliser l'IA du concours ou l'IA par défaut",
                        action="store_true")
    args = parser.parse_args()
    # saisie des joueurs
    liste_joueurs = ["joueur1", "joueur2", "joueur3", "joueur4"]
    liste_couleurs = ["info", "gmp", "chimie", "gte"]
    # initialisation du labyrinthe
    l = Labyrinthe(liste_joueurs, liste_couleurs, True, 100, 10)
    if args.mode_concours:
        import bot

    # initialisation de l'affichage
    g = LabyrintheGraphique(l, mode_concours=args.mode_concours)

    # démarrage de la partie
    g.demarrer()
