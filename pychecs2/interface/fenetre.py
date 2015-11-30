from tkinter import Canvas,Tk, Label, NSEW, Menu, Button
import time
from pychecs2.interface.menu import *
from pychecs2.echecs.partie import Partie

class Canvas_echiquier(Canvas):


    def __init__(self, parent, n_pixels_par_case, la_partie):

        self.n_ligne = 8
        self.n_colonne = 8
        self.n_pixels_par_case = n_pixels_par_case
        self.couleur_1 = 'white'
        self.couleur_2 = 'gray'
        self.partie = la_partie

        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


        super().__init__(parent, width = self.n_ligne*self.n_pixels_par_case,
                     height = self.n_colonne*self.n_pixels_par_case)
        self.bind('<Configure>', self.redimensionner)

    def dessiner_case(self):

        for i in range(self.n_ligne):
            for j in range(self.n_colonne):
                x_coin_superieur_gauche = i*self.n_pixels_par_case
                y_coin_superieur_gauche = j*self.n_pixels_par_case
                x_coin_inferieur_droit = i*self.n_pixels_par_case + self.n_pixels_par_case
                y_coin_inferieur_droit = j*self.n_pixels_par_case + self.n_pixels_par_case

                if (i+j) % 2 == 0:
                    couleur = self.couleur_1

                else:
                    couleur = self.couleur_2

                self.create_rectangle(x_coin_superieur_gauche, y_coin_superieur_gauche,
                                      x_coin_inferieur_droit, y_coin_inferieur_droit, fill = couleur, tag = 'case')

    def changer_couleur_position(self, colonne, ligne):
        self.delete('selection')
        x_coin_superieur_gauche = colonne*self.n_pixels_par_case
        y_coin_superieur_gauche = ligne*self.n_pixels_par_case
        x_coin_inferieur_droit = colonne*self.n_pixels_par_case + self.n_pixels_par_case
        y_coin_inferieur_droit = ligne*self.n_pixels_par_case + self.n_pixels_par_case


        self.create_rectangle(x_coin_superieur_gauche, y_coin_superieur_gauche,
                            x_coin_inferieur_droit, y_coin_inferieur_droit, fill = 'yellow', tag = 'selection')

        self.dessiner_piece()

    def supprimer_selection(self):
        self.delete('selection')


    def changer_couleur_theme(self, type, couleur):
        if type == 1:
            self.couleur_1 = couleur
        elif type == 2:
            self.couleur_2 = couleur
        self.delete('case')
        self.dessiner_case()

        self.dessiner_piece()



    def dessiner_piece(self):
        self.delete('piece')
        for position, type_piece in self.partie.echiquier.dictionnaire_pieces.items():

            coordonnee_y = (self.n_ligne - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            self.create_text(coordonnee_x, coordonnee_y, text=type_piece,
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
            nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
            self.n_pixels_par_case = nouvelle_taille // self.n_ligne

        # On supprime les anciennes cases et on ajoute les nouvelles.
            self.delete('case')
            self.dessiner_case()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
            self.delete('piece')
            self.dessiner_piece()
        #if position_selectionner:


class fenetre(Tk,menu_global):

    def __init__(self):
        super().__init__()
        #self.background( colour = 'red')

        self.partie = Partie()

        self.partie.echiquier.deplacer('a2','a4')

        self.joueur_actif = 'blanc'

        self.title("Échiquier")
        self.piece_selectionner = None

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.Canvas_echiquier = Canvas_echiquier(self, 60, self.partie)
        self.Canvas_echiquier.grid(sticky=NSEW)

        self.messages = Label(self)
        self.messages.grid()
        self.Canvas_echiquier.bind('<Button-1>', self.selectionner_piece)
        self.Canvas_echiquier.bind('<Button-3>', self.deselectionner_piece)

        self.premier_menu()

    def deselectionner_piece(self, event):
        self.piece_selectionner = None
        self.Canvas_echiquier.supprimer_selection()
        self.messages['text'] = ' '

    def selectionner_piece(self, event):
        ligne = event.y // self.Canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.Canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.Canvas_echiquier.lettres_colonnes[colonne], int(self.Canvas_echiquier.chiffres_rangees[self.Canvas_echiquier.n_ligne- ligne - 1]))
        if self.piece_selectionner is None:
            try:
                piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_depart_selectionnee = position
                self.messages['foreground'] = 'blue'
                self.messages['text'] = 'Pièce séléctionné : {} à la position {}'.format(piece, self.position_depart_selectionnee)
                self.piece_selectionner = piece
                self.Canvas_echiquier.changer_couleur_position(colonne, ligne)
                return position
            except KeyError:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'erreur aucune piece ici'
                return None

        else:
            if self.Canvas_echiquier.partie.echiquier.recuperer_piece_a_position(position) is not None:
                piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_depart_selectionnee = position
                self.messages['foreground'] = 'blue'
                self.messages['text'] = 'Pièce séléctionné : {} à la position {}'.format(piece, self.position_depart_selectionnee)
                self.piece_selectionner = piece
                self.Canvas_echiquier.changer_couleur_position(colonne, ligne)
            else:
                self.Canvas_echiquier.changer_couleur_position(colonne, ligne)
                self.position_arriver_selectionnee = position
                self.partie.echiquier.deplacer(self.position_depart_selectionnee,self.position_arriver_selectionnee)
                self.Canvas_echiquier.dessiner_piece()
                self.piece_selectionner = None
                self.messages['text'] = ' '
                self.Canvas_echiquier.supprimer_selection()
                self.partie.joueur_suivant()


    def selectionner_arriver(self, event):
        ligne = event.y // self.Canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.Canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.Canvas_echiquier.lettres_colonnes[colonne], int(self.Canvas_echiquier.chiffres_rangees[self.Canvas_echiquier.n_ligne- ligne - 1]))
        return position

if __name__ == '__main__':
    f = fenetre()
    f.mainloop()