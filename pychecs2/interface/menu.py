from tkinter import *

def premier_menu(self):
        self.menu_bar= Menu()
        self.partie_menu = Menu(self.menu_bar, tearoff = 0)
        self.partie_menu.add_command(label= 'Nouvelle partie', command = lambda:self.quit)
        self.partie_menu.add_command(label= 'Ouvrir une partie', command = lambda:self.quit)
        self.partie_menu.add_command(label= 'Sauvegarder la partie', command = lambda:self.quit)
        self.partie_menu.add_command(label= 'Quitter', command = lambda:self.quit)


        self.affichage_menu = Menu(tearoff = 0)
        #################################
        self.affichage_menu.add_command(label= 'Modifier', command =lambda: self.canvas_echiquier.changer_couleur_1(1,'green'))
        self.affichage_menu.add_command(label= 'résolution',command = lambda:self.quit)


        self.aide_menu = Menu(tearoff= 0)
        self.aide_menu.add_command(label= 'Règle de jeu',command = lambda:self.quit)
        self.aide_menu.add_command(label= 'À propos',command = lambda:self.about())

        self.menu_bar.add_cascade(label= 'Partie', menu= self.partie_menu)
        self.menu_bar.add_cascade(label= 'Affichage', menu= self.affichage_menu)
        self.menu_bar.add_cascade(label= 'Aide', menu= self.aide_menu)
        self.config(menu = self.menu_bar)

def about(self):
        toplevel = Toplevel()
        label1 = Label(toplevel, text="Text", height=10, width=100)
        label1.grid()