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

        self.piece_blanc_perdu = ""
        self.piece_noir_perdu = ""

        self.liste_mouvement_effectuer = []

        self.chiffres_rangees_inverse= ['8', '7', '6', '5', '4', '3', '2', '1']
        #self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


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


   # def changer_couleur_theme(self, type, couleur):
        #if type == 1:
            #self.couleur_1 = couleur
        #elif type == 2:
            #self.couleur_2 = couleur
        #self.delete('case')
        #self.dessiner_case()

        #self.dessiner_piece()



    def dessiner_piece(self):
        self.delete('piece')
        for position, type_piece in self.partie.echiquier.dictionnaire_pieces.items():

            coordonnee_y = (self.n_ligne - self.partie.echiquier.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2

            coordonnee_x = self.partie.echiquier.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2

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

        self.partie.echiquier.deplacer

        self.title("Échiquier")
        self.piece_selectionner = None

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        #self.affiche_liste_rangee = Label(self)
        #self.affiche_liste_rangee['text'] = "8\n\n\n7\n\n\n6\n\n\n5\n\n\n4\n\n\n3\n\n\n2\n\n\n1"
        #self.affiche_liste_rangee.grid(column= 0,row =0 )

        #self.affiche_liste_rangee = Label(self)
        #self.affiche_liste_rangee['text'] = "     a            b             c             d             e             f             g             h"
        #self.affiche_liste_rangee.grid(column= 1,row =1 )

        self.Canvas_echiquier = Canvas_echiquier(self, 60, self.partie)

        self.Canvas_echiquier.grid(sticky=NSEW,column = 1 ,row=0)

###########################################
        self.creation_frame_rangee()
        self.affiche_liste_rangee.grid(column= 0,row =0 )

        self.creation_frame_colonne()
        self.affiche_liste_colonne.grid(column= 1,row =1 )

        self.messages_joueur = Label(self)
        self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
        self.messages_joueur.grid(column = 1, row = 2)

        self.messages= Label(self)
        self.messages.grid( column= 1, row=3)

        self.messages_piece = Label(self)
        self.messages_piece['text'] = "Pièces qui on été manger:"
        self.messages_piece.grid(column= 1,row =4)

        self.messages_piece_blanc = Label(self)
        self.messages_piece_blanc['text'] = "Pièce blanc:"
        self.messages_piece_blanc.grid(column= 1, row=5)
        self.messages_piece_noir = Label(self)
        self.messages_piece_noir['text'] = "Pièce noir:"
        self.messages_piece_noir.grid(column= 1,row =6)


        self.creation_frame_droite()
        self.frame.grid(column = 2, row=0, rowspan=7, sticky = NSEW)


        self.Canvas_echiquier.bind('<Button-1>', self.selectionner_piece)
        self.Canvas_echiquier.bind('<Button-3>', self.deselectionner_piece)

        if self.Canvas_echiquier.partie.partie_terminee() == True:
            self.annoncer_partie_gagner()
        self.premier_menu()

    def creation_frame_rangee(self):
        self.affiche_liste_rangee = Frame(self, bg = "red")

        for element in self.Canvas_echiquier.chiffres_rangees_inverse:
            self.chiffre_rangee= Label(self.affiche_liste_rangee,height= (self.Canvas_echiquier.n_pixels_par_case//20))
            self.chiffre_rangee['text'] = element

            self.chiffre_rangee.grid(sticky= N)


    def creation_frame_colonne(self):
        self.affiche_liste_colonne = Frame(self, bg = "red", pady= 5)
        place_colonne = 0
        for element in self.partie.echiquier.lettres_colonnes:
            self.lettre_colonne= Label(self.affiche_liste_colonne,width= self.Canvas_echiquier.n_pixels_par_case//8)
            self.lettre_colonne['text'] = element

            self.lettre_colonne.grid(row= 0, column=place_colonne,sticky= N)
            place_colonne +=1


    def creation_frame_droite(self):

        self.frame = Frame(self, bg="red")


        self.messages_temps_jeu = Label(self.frame)
        self.messages_temps_jeu['text'] = "Temps de jeu"
        self.messages_temps_jeu.grid(column= 0,row=0 , columnspan= 2,padx= 10, pady= 10)

        self.messages_temps_jeu_blanc = Label(self.frame)
        self.messages_temps_jeu_blanc['text'] = "Pièce blanc:"
        self.messages_temps_jeu_blanc.grid(column= 0, row = 1)
        self.messages_temps_jeu_noir = Label(self.frame)
        self.messages_temps_jeu_noir['text'] = "Pièce noir:"
        self.messages_temps_jeu_noir.grid(column=0, row=2)

        self.temps_jeu_blanc = Label(self.frame)
        self.temps_jeu_blanc['text'] = "temps"
        self.temps_jeu_blanc.grid(column= 1, row = 1)
        self.temps_jeu_noir = Label(self.frame)
        self.temps_jeu_noir['text'] = "temps"
        self.temps_jeu_noir.grid(column=1, row=2)

        self.messages_mouvement = Label(self.frame)
        self.messages_mouvement['text'] = "Mouvement joué:"
        self.messages_mouvement.grid(column= 0,row=3 , columnspan= 2,padx= 100, pady= 15, sticky= N)

        self.creation_frame_mouvement()
        self.frame_mouvement.grid(column= 0,row=4, columnspan= 2,sticky= NSEW)

        self.bouton_annuler_dernier_coup = Button(self.frame, text="Annuler le\ndernier coup", command = None,width = 15)
        self.bouton_annuler_dernier_coup.grid(column = 0,columnspan = 2, row = 5, pady= 15)

    def creation_frame_mouvement(self):
        self.frame_mouvement = Frame(self.frame, bg="blue",width = 200,height= 450)



    def annoncer_partie_gagner(self):
        self.gagner = Toplevel()
        self.gagner.title("Partie Terminer")
        self.messages_gagner = Label(self.gagner)
        self.messages_gagner['text'] = "Félicitation! le {} à gagné la partie!\n Voulez-vous jouer une nouvelle partie?".format(self.partie.joueur_actif)
        self.messages_gagner.grid(columnspan = 2)

        self.bouton_nouvelle = Button(self.popup,text="Oui", command =lambda:self.nouvelle_partie(False),width = 10)
        self.bouton_quitter = Button(self.popup, text="Non, quitter", command = self.quit,width = 10)
        self.bouton_nouvelle.grid(column = 0, row = 1, pady= 10)
        self.bouton_quitter.grid(column = 1, row = 1, pady= 10)


    def deselectionner_piece(self):
        self.piece_selectionner = None
        self.Canvas_echiquier.supprimer_selection()
        self.messages['text'] = ' '

    def selectionner_piece(self, event):
        ligne = event.y // self.Canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.Canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.Canvas_echiquier.partie.echiquier.lettres_colonnes[colonne], int(self.Canvas_echiquier.partie.echiquier.chiffres_rangees[self.Canvas_echiquier.n_ligne- ligne - 1]))
        if self.piece_selectionner is None:
            try:
                piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_depart_selectionnee = position

                self.messages['foreground'] = 'blue'
                self.messages['text'] = 'Pièce séléctionné : {} à la position {}'.format(piece, self.position_depart_selectionnee)
                self.couleur_piece_selectionner = self.Canvas_echiquier.partie.echiquier.couleur_piece_a_position(position)
                if self.couleur_piece_selectionner != self.partie.joueur_actif:
                    self.messages['foreground'] = 'red'
                    self.messages['text'] = "Vous essayer de jouer une pièce de l'autre joueur TRICHEUR!"
                    return None
                self.piece_selectionner = piece
                self.Canvas_echiquier.changer_couleur_position(colonne, ligne)
                return position
            except KeyError:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'erreur aucune piece ici'


        else:
            self.selectionner_arriver(ligne, colonne)

    def selectionner_arriver(self, ligne, colonne):
        position = "{}{}".format(self.Canvas_echiquier.partie.echiquier.lettres_colonnes[colonne], int(self.Canvas_echiquier.partie.echiquier.chiffres_rangees[self.Canvas_echiquier.n_ligne- ligne - 1]))
        #piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
        #self.messages['text'] = 'Pièce séléctionné : {} à la position {}'.format(piece, self.position_depart_selectionnee)
        if self.Canvas_echiquier.partie.echiquier.recuperer_piece_a_position(position) is not None:
            if self.couleur_piece_selectionner == self.Canvas_echiquier.partie.echiquier.couleur_piece_a_position(position):
                piece = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.position_depart_selectionnee = position
                self.piece_selectionner = piece
                self.Canvas_echiquier.changer_couleur_position(colonne, ligne)

            #self.Canvas_echiquier.changer_couleur_position(colonne, ligne)
        self.position_arriver_selectionnee = position

        if self.partie.echiquier.deplacement_est_valide(self.position_depart_selectionnee,self.position_arriver_selectionnee) is True:

            self.piece_mange = self.Canvas_echiquier.partie.echiquier.recuperer_piece_a_position(self.position_arriver_selectionnee)

            if self.piece_mange is not None:
                piece_manger_str = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]
                self.ajouter_piece_manger(piece_manger_str)

            self.Canvas_echiquier.liste_mouvement_effectuer += [[self.piece_selectionner,self.position_depart_selectionnee,self.position_arriver_selectionnee, self.piece_mange]]

            print(self.Canvas_echiquier.liste_mouvement_effectuer)

            self.partie.echiquier.deplacer(self.position_depart_selectionnee,self.position_arriver_selectionnee)

            self.Canvas_echiquier.dessiner_piece()
            self.piece_selectionner = None
            self.messages['text'] = ' '
            self.Canvas_echiquier.supprimer_selection()
            self.joueur_actif = self.partie.joueur_suivant()
            self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
        else:
            return None

    def ajouter_piece_manger(self, piece_mange_str):
        if self.piece_mange.couleur == "blanc":
            self.Canvas_echiquier.piece_blanc_perdu  += str(piece_mange_str)
            self.messages_piece_blanc['text'] += self.Canvas_echiquier.piece_blanc_perdu

        elif self.piece_mange.couleur == "noir":
            self.Canvas_echiquier.piece_noir_perdu += str(piece_mange_str)
            self.messages_piece_noir['text'] += self.Canvas_echiquier.piece_noir_perdu

if __name__ == '__main__':
    f = fenetre()
    f.mainloop()