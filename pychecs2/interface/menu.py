from tkinter import *
from pychecs2.echecs import echiquier

class menu_global():
    def premier_menu(self):
        self.menu_bar= Menu()
        self.partie_menu = Menu(self.menu_bar, tearoff = 0)
        self.partie_menu.add_command(label= 'Nouvelle partie', command = lambda:self.nouvelle_partie())
        self.partie_menu.add_command(label= 'Ouvrir une partie', command = lambda:self.quit)
        self.partie_menu.add_command(label= 'Sauvegarder la partie', command = lambda:self.menu_enregistrer())
        self.partie_menu.add_command(label= 'Quitter', command = lambda:self.quitter())


        self.affichage_menu = Menu(tearoff = 0)
        #################################
        self.affichage_menu.add_command(label= 'Modifier', command =lambda: self.canvas_echiquier.changer_couleur_theme(2,'green'))
        self.affichage_menu.add_command(label= 'résolution',command = lambda:self.quit)


        self.aide_menu = Menu(tearoff= 0)
        self.aide_menu.add_command(label= 'Règle de jeu',command = lambda:self.fenetre_popup('Règle du jeu'))
        self.aide_menu.add_command(label= 'À propos',command = lambda:self.quit)

        self.menu_bar.add_cascade(label= 'Partie', menu= self.partie_menu)
        self.menu_bar.add_cascade(label= 'Affichage', menu= self.affichage_menu)
        self.menu_bar.add_cascade(label= 'Aide', menu= self.aide_menu)
        self.config(menu = self.menu_bar)

    def fenetre_popup(self, titre):
        self.popup = Toplevel()
        self.popup.title(titre)
        contenu_text = Label(self.popup, text="Text", height=10, width=50)
        contenu_text.grid()

    def menu_enregistrer(self):
        self.popup = Toplevel()
        self.popup.title("Enregistrer la partie")
        self.messages_sauvegarde = Label(self.popup)
        self.messages_sauvegarde['text'] = "Entrez le nom du ficher pour la partie à enregistrer"
        self.messages_sauvegarde.grid(column = 0, columnspan = 2, row = 0, pady= 10, padx = 15)
        self.entree = Entry(self.popup,width=40)
        self.entree.grid(column = 0,columnspan = 2, row = 1, pady= 5)

        self.entree.insert(0, "partie_echec")

        self.bouton_sauvegarder = Button(self.popup,text="Sauvegarder", command =lambda:self.sauvegarder_partie(self.entree.get()))
        self.bouton_annuler = Button(self.popup, text="Annuler", command = self.popup.destroy)
        self.bouton_sauvegarder.grid(column = 0, row = 2, pady= 10)
        self.bouton_annuler.grid(column = 1, row = 2)


    def sauvegarder_partie(self, nom_fichier):
        fichier_ecriture = open(nom_fichier, 'w',encoding="utf-8")
        #echiquier.Echiquier.initialiser_echiquier_depart.dictionnaire_pieces
        dictionaire = self.canvas_echiquier.piece
        for element in dictionaire:
            piece = str("{} {}".format(element, dictionaire[element]))
            fichier_ecriture.write(piece)

        #On fait un retour de chariot dans le fichier de sortie pour séparer les entiers chiffrés dans le fichier.
            fichier_ecriture.write("\n")
        fichier_ecriture.close()
        self.popup.destroy()
        self.confirmation()

    def confirmation(self):
        self.confirme = Toplevel()
        self.confirme.title("Enregistrer la partie")
        self.messages_confirme = Label(self.confirme)
        self.messages_confirme['text'] = "La sauvegarde à été éffectué avec succès!"
        self.messages_confirme.grid(padx= 10, pady= 10)
        self.bouton_ok = Button(self.confirme,text="ok",width=10, command =self.confirme.destroy)
        self.bouton_ok.grid(pady= 10)

    def nouvelle_partie(self):
        self.popup=Toplevel()
        self.popup.title("Nouvelle Partie")
        self.messages_nouvelle = Label(self.popup)
        self.messages_nouvelle['text'] = "Voulez-vous commencer une nouvelle partie?"
        self.messages_nouvelle.grid(column = 0, columnspan = 2, row = 0, pady= 10, padx = 15)
        self.entree = Entry(self.popup,width=40)



        self.bouton_nouvelle = Button(self.popup,text="Nouvelle Partie", command =lambda:self.supprimer_partie(self.entree.get()))
        self.bouton_annuler = Button(self.popup, text="Annuler", command = self.popup.destroy)
        self.bouton_nouvelle.grid(column = 0, row = 2, pady= 10)
        self.bouton_annuler.grid(column = 1, row = 2)

    #def supprimer_partie(self):
        #self.delete('case')
        #self.dessiner_case()
        #self.delete('piece')
        #self.dessiner_piece()

    def quitter(self):
        self.popup=Toplevel()
        self.popup.title("Quitter Partie")
        self.messages_nouvelle = Label(self.popup)
        self.messages_nouvelle['text'] = "Voulez-vous sauvegarder la partie avant de quitter?"
        self.messages_nouvelle.grid(column = 0, columnspan = 2, row = 0, pady= 10, padx = 15)
        self.entree = Entry(self.popup,width=40)
        self.entree.grid(column = 0,columnspan = 2, row = 1, pady= 5)

        self.entree.insert(0, "partie_echec")

        self.bouton_sauvegarder = Button(self.popup,text="Sauvegarder", command =lambda:self.sauvegarder_partie(self.entree.get()))
        self.bouton_quitter = Button(self.popup, text="Quitter", command = self.popup.destroy)
        self.bouton_sauvegarder.grid(column = 0, row = 2, pady= 10)
        self.bouton_quitter.grid(column = 1, row = 2)








