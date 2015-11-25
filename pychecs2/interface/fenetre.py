from tkinter import Canvas,Tk, Label, NSEW, Menu, Button
import time
from pychecs2.interface.menu import *
from pychecs2.echecs.echiquier import *

class canvas_echiquier(Canvas):

    def __init__(self, parent, n_pixels_par_case):

        self.n_ligne = 8
        self.n_colonne = 8
        self.n_pixels_par_case = n_pixels_par_case
        self.couleur_1 = 'white'
        self.couleur_2 = 'gray'

        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        self.piece = {
            'a1': 'TB', 'b1': 'CB', 'c1': 'FB', 'd1': 'DB', 'e1': 'RB', 'f1': 'FB', 'g1': 'CB', 'h1': 'TB',
            'a2': 'PB', 'b2': 'PB', 'c2': 'PB', 'd2': 'PB', 'e2': 'PB', 'f2': 'PB', 'g2': 'PB', 'h2': 'PB',
            'a7': 'PN', 'b7': 'PN', 'c7': 'PN', 'd7': 'PN', 'e7': 'PN', 'f7': 'PN', 'g7': 'PN', 'h7': 'PN',
            'a8': 'TN', 'b8': 'CN', 'c8': 'FN', 'd8': 'DN', 'e8': 'RN', 'f8': 'FN', 'g8': 'CN', 'h8': 'TN',
        }


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

    def changer_couleur_1(self, type, couleur):
        if type == 1:
            self.couleur_1 = couleur
        elif type == 2:
            self.couleur_2 = couleur
        self.delete('case')
        self.dessiner_case()

        self.delete('piece')
        self.dessiner_piece()

    def dessiner_piece(self):

        caracteres_pieces = {'PB': '\u2659',
                             'PN': '\u265f',
                             'TB': '\u2656',
                             'TN': '\u265c',
                             'CB': '\u2658',
                             'CN': '\u265e',
                             'FB': '\u2657',
                             'FN': '\u265d',
                             'RB': '\u2654',
                             'RN': '\u265a',
                             'DB': '\u2655',
                             'DN': '\u265b'
                             }

        for position, type_piece in self.piece.items():

            coordonnee_y = (self.n_ligne - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            self.create_text(coordonnee_x, coordonnee_y, text=caracteres_pieces[type_piece],
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

class fenetre(Tk,menu_global):

    def __init__(self):
        super().__init__()
        #self.background( colour = 'red')



        self.title("Échiquier")
        self.position_selectionnee = None

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.canvas_echiquier = canvas_echiquier(self,60)
        self.canvas_echiquier.grid(sticky=NSEW)

        self.messages = Label(self)
        self.messages.grid()
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)

        self.premier_menu()

    def selectionner(self,event):
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_ligne- ligne - 1]))

        try:
            piece = self.canvas_echiquier.piece[position]
            self.position_selectionnee = position
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce séléctionné : {} à la position {}'.format(piece, self.position_selectionnee)
        except KeyError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'erreur aucune piece ici'


if __name__ == '__main__':
    f = fenetre()
    f.mainloop()