# -*- coding: utf-8 -*-
"""Ce module contient une classe contenant les informations sur une partie d'échecs,
dont un objet échiquier (une instance de la classe Echiquier).

"""
from pychecs.echiquier import Echiquier


class Partie:
    """La classe Partie contient les informations sur une partie d'échecs, c'est à dire un échiquier, puis
    un joueur actif (blanc ou noir). Des méthodes sont disponibles pour faire avancer la partie et interagir
    avec l'utilisateur.

    Attributes:
        joueur_actif (str): La couleur du joueur actif, 'blanc' ou 'noir'.
        echiquier (Echiquier): L'échiquier sur lequel se déroule la partie.

    """
    def __init__(self):
        # Le joueur débutant une partie d'échecs est le joueur blanc.
        self.joueur_actif = 'blanc'

        # Création d'une instance de la classe Echiquier, qui sera manipulée dans les méthodes de la classe.
        self.echiquier = Echiquier()

    def determiner_gagnant(self):
        """Détermine la couleur du joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        le roi de la couleur adverse doit être absente de l'échiquier.

        Returns:
            str: 'blanc' si le joueur blanc a gagné, 'noir' si c'est plutôt le joueur noir, et 'aucun' si aucun
                joueur n'a encore gagné.

        """
        #Cas où le roi noir est absent de l'échiquier.
        if not self.echiquier.roi_de_couleur_est_dans_echiquier('noir'):
            return 'blanc'

        #Cas où le roi blanc est absent de l'échiquier.
        if not self.echiquier.roi_de_couleur_est_dans_echiquier('blanc'):
            return 'noir'

        #Cas où les deux rois sont sur l'échiquier.
        return 'aucun'

    def partie_terminee(self):
        """Vérifie si la partie est terminée. Une partie est terminée si un gagnant peut être déclaré.

        Returns:
            bool: True si la partie est terminée, et False autrement.

        """
        #Cas où le joueur blanc ou le joueur noir est le gagnant.
        if self.determiner_gagnant() == 'blanc' or self.determiner_gagnant() == 'noir':
            return True

        #Cas où il n'y a encore aucun gagnant.
        return False

    def piece_position_depart(self,position_depart):
        """
        Détermine si la position de départ donner par l'utilisateur est sur l'échiquier.
        On vérifie qu'il y a bien une pièce du joueur actif sur cette case.
        S'il n'y a pas de pièce ou que c'est la pièce d'un autre joueur on retourne un message d'erreur.
        :param position_depart:
            str: Une chaine de charactère qui représente une position à évaluer.
        :return:
            bool: True si le la position est valide et a une pièce du joueur actif, et False autrement.
        """
        #On redemande la position de départ tant que la position n'est pas valide.
        if not self.echiquier.position_est_valide(position_depart):
            return False

        #Tant qu'il n'y a pas de pièces on informe le joueur qu'il ne peux pas choisir cette case de départ et on redemande la position de départ
        if self.echiquier.recuperer_piece_a_position(position_depart) is None:
            print("Il n'y a pas de pièce sur cette case")
            return False
        #Tant que ce n'est pas une de ses pièces on informe le joueur qu'il ne peut pas jouer cette pièce et on redemande la position de départ.
        if self.echiquier.couleur_piece_a_position(position_depart) != self.joueur_actif:
            print("Vous jouer les pieces de l'autre joueur, TRICHEUR!")
            return False
        # Si c'est une bonne position, avec un pièce du joueur actif on retourne true.
        return True

    def demander_positions(self):
        """Demande à l'utilisateur d'entrer les positions de départ et d'arrivée pour faire un déplacement. Si les
        positions entrées sont valides (si le déplacement est valide), on retourne les deux positions. On doit
        redemander tant que l'utilisateur ne donne pas des positions valides.

        Returns:
            str, str: Deux chaînes de caractères représentant les deux positions valides fournies par l'utilisateurs.

        """
        #On demande la position de départ au joueur.
        position_depart = str(input("Entrez la position départ:"))

        #On redemande la position de départ tant que la position n'est pas une position avec une pièce du joueur.
        while not self.piece_position_depart(position_depart):
                    position_depart = str(input("Entrez la position départ:"))

        #On demande la position d'arriver au joueur.
        position_arrive = str(input("Entrez la position arrivé:"))

        #On redemande la position d'arriver tant que la position n'est pas valide.
        while not self.echiquier.position_est_valide(position_arrive):
            position_arrive = str(input("Entrez la position arrivé:"))

        #retourne les positions de départ et d'arriver.
        return position_depart, position_arrive

    def joueur_suivant(self):
        """Change le joueur actif: passe de blanc à noir, ou de noir à blanc, selon la couleur du joueur actif.

        """
        # Si le joueur actif est blanc on le change en noir
        if self.joueur_actif == 'blanc':
            self.joueur_actif = 'noir'

        #Si le joueur actif est noir on le change en blanc
        elif self.joueur_actif == 'noir':
            self.joueur_actif = 'blanc'

    def jouer(self):
        """Tant que la partie n'est pas terminée, joue la partie. À chaque tour :
            - On affiche l'échiquier.
            - On demande les deux positions.
            - On fait le déplacement sur l'échiquier.
            - On passe au joueur suivant.

        Une fois la partie terminée, on félicite le joueur gagnant!

        """

        partie_est_terminer = False

        #On forme une boucle de jeu qui va continuer tant que la partie n'est pas terminer.
        while not partie_est_terminer:

            #On affiche l'échiquier.
            print(self.echiquier)

            #On informe quel est la couleur du joueur actif.
            print("C'est au tour du joueur:",self.joueur_actif)

            deplacement_valide = False

            #On forme une seconde boucle qui va continuer tant qu'on n'entre pas un déplacement valide.
            while not deplacement_valide:

                #On demande à l'utilisateur les positions de départ et d'arriver du déplacement.
                position_depart, position_arrive = self.demander_positions()

                #Maintenant qu'on a une position de départ et d'arriver,on vérifie que c'est un déplacement valide.
                deplacement_valide = self.echiquier.deplacer(position_depart,position_arrive)

            #On verifie si la partie est terminé.
            partie_est_terminer = self.partie_terminee()
            #Si c'est le cas on félicite le joueur gagnant.
            if partie_est_terminer:
                print("Bravo joueur", self.joueur_actif,"vous avez gagné!")

            #S'il n'y a pas de gagnant, la partie n'est pas fini, on change de joueur actif.
            else:
                self.joueur_suivant()