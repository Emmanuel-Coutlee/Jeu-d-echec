from tkinter import *
from time import strftime, localtime
from pychecs2.echecs.partie import Partie
import pickle
import os
from random import randrange


class menu_global():
    # Méthode qui crée la barre menu du jeu
    def premier_menu(self):
        self.menu_bar= Menu()
        self.partie_menu = Menu(self.menu_bar, tearoff = 0)
        self.partie_menu.add_command(label= 'Nouvelle partie', command = lambda:self.menu_nouvelle_partie())
        self.partie_menu.add_command(label= 'Charger une partie', command = lambda:self.menu_charger())
        self.partie_menu.add_command(label= 'Sauvegarder la partie', command = lambda:self.menu_enregistrer(False,False))
        self.partie_menu.add_command(label= 'Quitter', command = lambda:self.menu_quitter())


        self.affichage_menu = Menu(tearoff = 0)
        #self.affichage_menu.add_command(label= 'Modifier', command =lambda: self.canvas_echiquier.changer_couleur_theme(2,'green'))
        self.affichage_menu.add_command(label= 'Modifier', command =lambda: self.menu_modifier())


        self.aide_menu = Menu(tearoff= 0)
        self.aide_menu.add_command(label= 'Règle de jeu',command = lambda:self.menu_regle_du_jeu())
        self.aide_menu.add_command(label= 'Aide',command = lambda:self.menu_fonction())

        self.menu_bar.add_cascade(label= 'Partie', menu= self.partie_menu)
        self.menu_bar.add_cascade(label= 'Affichage', menu= self.affichage_menu)
        self.menu_bar.add_cascade(label= 'Aide', menu= self.aide_menu)
        self.config(menu = self.menu_bar)


    # Méthode qui crée un menu pour enregistrer un partie
    def menu_enregistrer(self,nouvelle_partie,quitter):
        self.popup_enregister = Toplevel()
        self.popup_enregister.title("Enregistrer la partie")
        self.messages_sauvegarde = Label(self.popup_enregister)
        self.messages_sauvegarde['text'] = "Entrez le nom du ficher pour la partie à enregistrer"
        self.messages_sauvegarde.grid(column = 0, columnspan = 2, row = 0, pady= 10, padx = 15)
        self.entree = Entry(self.popup_enregister,width=40)
        self.entree.grid(column = 0,columnspan = 2, row = 1, pady= 5)
        self.entree.insert(0, "partie_echec[{}]".format(strftime("%d,%m,%Y", localtime())))

        self.bouton_sauvegarder = Button(self.popup_enregister,text="Sauvegarder", command =lambda:self.sauvegarder_partie(self.entree.get(),nouvelle_partie,quitter))
        self.bouton_annuler = Button(self.popup_enregister, text="Annuler", command = self.popup_enregister.destroy)
        self.bouton_sauvegarder.grid(column = 0, row = 2, pady= 10)
        self.bouton_annuler.grid(column = 1, row = 2)

    # Méthode qui crée un menu pour charger une partie sauvegardée
    def menu_charger(self):
        self.popup_charger = Toplevel()
        self.popup_charger.title("Charger une partie")

        try:
            if os.stat("liste_partie").st_size ==0:
                self.messages_charger = Label(self.popup_charger)
                self.messages_charger['text'] = "Il n'y a aucune partie sauvegardé."
                self.messages_charger.grid(column = 0, row = 0, pady= 10, padx = 15)
                self.bouton_ok = Button(self.popup_charger,text="ok",width=10, command =self.popup_charger.destroy)
                self.bouton_ok.grid(pady= 10)
                return None


            fichier_liste_partie = open("liste_partie", 'r',encoding="utf-8") # ouverture des partie pour pouvoir les supprimer ou charger
            self.messages_charger = Label(self.popup_charger)
            self.messages_charger['text'] = "Choissez une partie à charger ou supprimer."
            self.messages_charger.grid(column = 0, columnspan = 3, row = 0, pady= 10, padx = 15)

            self.nom_partie = StringVar()
            ligne_bouton = 2
            frame_nom_partie = Frame(self.popup_charger)
            frame_nom_partie.grid()
            for partie in fichier_liste_partie:
                choisir_partie = Radiobutton(self.popup_charger, text= partie.rstrip(),variable = self.nom_partie,value = partie.rstrip(),indicatoron=0)
                choisir_partie.grid(column = 0,columnspan = 3,padx= 10, pady= 10)
                ligne_bouton += 1
            self.bouton_charger = Button(self.popup_charger,text="Charger", command =lambda:self.charger_partie(self.nom_partie.get()))
            self.bouton_suprimer = Button(self.popup_charger,text="suprimer", command =lambda:self.suprimer_partie(self.nom_partie.get()))
            self.bouton_annuler = Button(self.popup_charger, text="Annuler", command = self.popup_charger.destroy)
            self.bouton_charger.grid(column = 0,row = ligne_bouton, pady= 10, sticky = S)
            self.bouton_suprimer.grid(column = 1,row = ligne_bouton, pady= 10, sticky = S)
            self.bouton_annuler.grid(column = 2,row = ligne_bouton, pady = 10, sticky = S )
        except FileNotFoundError: #Erreur si le joueur veut ouvrir partie, mais aucune n'a été sauvegardée
            self.messages_charger = Label(self.popup_charger)
            self.messages_charger['text'] = "Il n'y a aucune partie sauvegardé."
            self.messages_charger.grid(column = 0, row = 0, pady= 10, padx = 15)
            self.bouton_ok = Button(self.popup_charger,text="ok",width=10, command =self.popup_charger.destroy)
            self.bouton_ok.grid(pady= 10)

    # Méthode qui permet de supprimer une partie sauvegardé
    def suprimer_partie (self, nom_partie):
        try:
            os.remove(nom_partie+".p")
            liste_partie = open("liste_partie", "r+")
            nom_liste_partie = liste_partie.readlines()
            liste_partie.seek(0,0)
            for line in nom_liste_partie:
                if line != nom_partie+"\n":
                    liste_partie.write(line)
            liste_partie.truncate()
            liste_partie.close()
            self.popup_charger.destroy()
            self.menu_charger()
        except FileNotFoundError: #Erreur si le joueur sélectionne aucune partie à supprimer
            self.messages_charger['text'] = "***ATTENTION!***\nVous n'avez sélectionné aucune partie.\nVeuillez choisir une partie."


    # Méthode qui crée un menu pour nouvelle partie
    def menu_nouvelle_partie(self):
        self.popup_nouvelle = Toplevel()
        self.popup_nouvelle.title("Nouvelle partie")
        self.messages_nouvelle = Label(self.popup_nouvelle)
        self.messages_nouvelle['text'] = "Vous allez commencer une nouvelle partie.Voulez-vous enregistrer la partie en cour?"
        self.messages_nouvelle.grid(column = 0, columnspan = 3, row = 0, pady= 10, padx = 20)
        self.bouton_oui = Button(self.popup_nouvelle,text="Oui", command =lambda:self.menu_enregistrer(True,False),width = 10)
        self.bouton_non = Button(self.popup_nouvelle,text="Non", command =lambda:self.nouvelle_partie(),width = 10)
        self.bouton_annuler = Button(self.popup_nouvelle, text="Annuler", command = self.popup_nouvelle.destroy,width = 10)
        self.bouton_oui.grid(column = 0,row = 1, pady= 15)
        self.bouton_non.grid(column = 1, row = 1, pady= 15)
        self.bouton_annuler.grid(column = 2, row = 1, pady = 15)


    # Méthode qui permet de créer une nouvelle partie, et de la sauvegarder avant.
    def nouvelle_partie(self):

        self.Canvas_echiquier.partie.echiquier.initialiser_echiquier_depart()
        self.Canvas_echiquier.dessiner_piece()
        self.Canvas_echiquier.partie.joueur_actif = "blanc"
        self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)

        self.messages_piece_blanc['text'] = "Pièce blanc:"
        self.messages_piece_noir['text'] = "Pièce noir:"
        self.Canvas_echiquier.piece_blanc_perdu = ""
        self.Canvas_echiquier.piece_noir_perdu = ""
        self.deselectionner_piece(None)
        self.Canvas_echiquier.liste_mouvement_effectuer = []
        self.listbox_mouvement.delete(0,END)
        try:
            self.popup_gagner.destroy()
        #la fenetre n'existe pas donc on ne ferme rien
        except AttributeError:
            pass
        try:
            self.confirme.destroy()
        except AttributeError:
            pass
        try:
            self.popup_nouvelle.destroy()
        #la fenetre n'existe pas donc on ne ferme rien
        except AttributeError:
            pass

    # Méthode qui crée un menu pour quitter
    def menu_quitter(self):

        self.popup_quitter=Toplevel()
        self.popup_quitter.title("Quitter Partie")
        self.messages_nouvelle = Label(self.popup_quitter)
        self.messages_nouvelle['text'] = "Voulez-vous sauvegarder la partie avant de quitter?"
        self.messages_nouvelle.grid(column = 0, columnspan = 3, row = 0, pady= 10, padx = 15)

        self.bouton_sauvegarder = Button(self.popup_quitter,text="Oui", command =lambda:self.menu_enregistrer(False,True),width = 10)
        self.bouton_quitter = Button(self.popup_quitter, text="Non", command = self.quit,width = 10)
        self.bouton_annuler = Button(self.popup_quitter, text="Annuler", command = self.popup_quitter.destroy,width = 10)
        self.bouton_sauvegarder.grid(column = 0, row = 2, pady= 10)
        self.bouton_quitter.grid(column = 1, row = 2, pady= 10)
        self.bouton_annuler.grid(column = 2, row = 2)

    # Méthode qui crée un menu pour modifier les couleurs des cases de l'échiquier.
    def menu_modifier(self):
        self.popup_modifier=Toplevel()
        self.popup_modifier.title("modifier")
        self.messages_modifier = Label(self.popup_modifier)
        self.messages_modifier['text'] = "Choisisez un thème et cliquez sur OK "
        self.messages_modifier.grid(column = 0, columnspan = 2, row = 0, pady= 10, padx = 15)


        self.messages_modifier_0 = Button(self.popup_modifier,text="Thème normal", command =lambda :self.Canvas_echiquier.changer_couleur_theme("white","gray"),width = 15)
        self.messages_modifier_0.grid(column = 0, row = 1, pady= 10)

        #todo rajouter autant de bouton avec des thème changer les couleur
        self.messages_modifier_1 = Button(self.popup_modifier,text="Thème noël", command =lambda :self.Canvas_echiquier.changer_couleur_theme("red","green"),width = 15)
        self.messages_modifier_1.grid(column = 1, row = 1, pady= 10)

        self.messages_modifier_1 = Button(self.popup_modifier,text="Thème Feu", command =lambda :self.Canvas_echiquier.changer_couleur_theme("red","Darkorange1"),width = 15)
        self.messages_modifier_1.grid(column = 2, row = 1, pady= 10)

        self.messages_modifier_1 = Button(self.popup_modifier,text="Thème St-Valentin", command =lambda :self.Canvas_echiquier.changer_couleur_theme("deep pink","red"),width = 15)
        self.messages_modifier_1.grid(column = 3, row = 1, pady= 10)


        self.bouton_ok = Button(self.popup_modifier, text="Ok", command = self.popup_modifier.destroy,width = 10)
        self.bouton_ok.grid(column = 0, columnspan = 1, row = 2)

    #Méthode pour sauvegarder une partie jouée
    def sauvegarder_partie(self, nom_fichier,nouvelle_partie,quitter):

        if os.path.exists(nom_fichier+".p"): # si la partie existe déjà, demander à l'utilisateur d'écraser la partie existante
            self.menu_ecraser_partie(nom_fichier,nouvelle_partie, quitter)
            return None

        if not os.path.exists("liste_partie"): # si la partie n'existe pas ouvrir le fichier liste partie pour pouvoir sauvegarder la partie
            fichier_liste_partie = open("liste_partie", 'w',encoding="utf-8")
        else:
            fichier_liste_partie = open("liste_partie", 'a',encoding="utf-8")
        fichier_liste_partie.writelines("{}\n".format(nom_fichier))

        dictionaire = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces

        joueur_actif = self.Canvas_echiquier.partie.joueur_actif

        liste_mouvement = self.Canvas_echiquier.liste_mouvement_effectuer

        piece_blanc_perdu = self.Canvas_echiquier.piece_blanc_perdu

        piece_noir_perdu = self.Canvas_echiquier.piece_noir_perdu

        pickle.dump((joueur_actif,dictionaire,liste_mouvement), open(nom_fichier+".p",'wb'))

        self.confirmation(nouvelle_partie,quitter)

    #Méthode qui va créer un button pour supprimer une partie existante au même nom.
    def menu_ecraser_partie(self,nom_fichier,nouvelle_partie,quitter):
        self.popup_ecraser=Toplevel()
        self.popup_ecraser.title("Écraser une partie")
        self.messages_modifier = Label(self.popup_ecraser)
        self.messages_modifier['text'] = "Une partie avec ce nom existe déjà. Voulez-vous l'écraser ou choisir un nouveau nom?"
        self.messages_modifier.grid(column = 0, columnspan = 2,pady= 10, padx = 10)
        self.bouton_sauvegarder = Button(self.popup_ecraser,text="Écraser", command =lambda:self.ecraser_partie(nom_fichier,nouvelle_partie,quitter),width = 10)
        self.bouton_annuler = Button(self.popup_ecraser, text="Changer le nom", command = self.popup_ecraser.destroy,width = 15)
        self.bouton_sauvegarder.grid(column = 0, row = 1, pady= 10)
        self.bouton_annuler.grid(column = 1, row = 1)

        #Méthode qui permet supprimer la partie existante au nom donné pour la partie voulant être sauvegarder.
    def ecraser_partie(self,nom_fichier,nouvelle_partie, quitter):
        dictionaire = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces
        liste_mouvement = self.Canvas_echiquier.liste_mouvement_effectuer
        joueur_actif = self.Canvas_echiquier.partie.joueur_actif

        pickle.dump((joueur_actif,dictionaire, liste_mouvement), open(nom_fichier+".p",'wb'))
        self.popup_ecraser.destroy()
        self.confirmation(nouvelle_partie,quitter)

    #Méthode qui permet de sélectionner une partie qui a été sauvegardée
    def charger_partie(self, nom_partie):
        #lire le ficher partie_echec
        try:

            (joueur_actif,dictionaire, liste_mouvement ) = pickle.load(open(nom_partie+".p","rb"))
            self.Canvas_echiquier.partie.joueur_actif = joueur_actif
            self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces = dictionaire
            self.Canvas_echiquier.liste_mouvement_effectuer = liste_mouvement

            self.listbox_mouvement.delete(0,END)
            self.Canvas_echiquier.piece_blanc_perdu = ""
            self.Canvas_echiquier.piece_noir_perdu = ""

            self.nombre_déplacement = 0

            for mouvement in liste_mouvement:
                self.message_mouvement(mouvement)

            self.Canvas_echiquier.dernier_mouvement_effectuer = self.Canvas_echiquier.liste_mouvement_effectuer[-1]

            self.listbox_mouvement.see(END)

            self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
            self.messages['text'] = ""
            self.Canvas_echiquier.dessiner_case()
            self.Canvas_echiquier.dessiner_piece()
            self.popup_charger.destroy()
        except FileNotFoundError:
            self.messages_charger['text'] = "***ATTENTION!***\nVous n'avez sélectionné aucune partie.\nVeuillez choisir une partie."

    #Méthode qui crée un POPUP pour avertir les joueurs que la partie a bien été sauvegarder.
    def confirmation(self,nouvelle_partie,quitter):
        self.popup_enregister.destroy()
        self.confirme = Toplevel()
        self.confirme.title("Enregistrer la partie")
        self.messages_confirme = Label(self.confirme)
        self.messages_confirme['text'] = "La sauvegarde à été éffectué avec succès!"
        self.messages_confirme.grid(padx= 10, pady= 10)
        if nouvelle_partie is True: # Si nouvelle partie est sélectioner, utilise la méthode nouvelle partie
            self.bouton_ok = Button(self.confirme,text="ok",width=10, command =self.nouvelle_partie)
            self.bouton_ok.grid(pady= 10)
        elif quitter is True: # sinon si quitter est sélectionner, utiliser la méthode quitter partie
            self.bouton_ok = Button(self.confirme,text="ok",width=10, command =self.quit)
            self.bouton_ok.grid(pady= 10)
        else:
            self.bouton_ok = Button(self.confirme,text="ok",width=10, command =self.confirme.destroy)
            self.bouton_ok.grid(pady= 10)

    def menu_fonction(self):
        self.popup_fonction = Toplevel()
        self.popup_fonction.title("Fonctionalité du programe")
        self.messages_fonction = Label(self.popup_fonction)
        self.messages_fonction['text'] = "Voici les règle du jeu d'échec pour cette version du programme"
        self.messages_fonction.grid()
        self.fonction_programe = Label(self.popup_fonction)

        ####################todo remplir ce texte
        self.texte_fonction_programe = "1) Manger la pièce Roi adverse pour pouvoir gagner la partie." "\n" "2) Vous pouvez annuler le dernier coup joué si besoin.""\n""3) Vous pouvez voir votre dernier coup joué si besoin."

        self.fonction_programe['text'] = self.texte_fonction_programe
        self.fonction_programe.grid()

        self.bouton_ok = Button(self.popup_fonction,text="ok",width=10, command =self.popup_fonction.destroy)
        self.bouton_ok.grid(pady= 10)

    # Méthode qui crée un menu pour savoir les rêgle du jeu échec .
    def menu_regle_du_jeu(self):
        self.popup_regle = Toplevel()
        self.popup_regle.title("Règle du jeu")
        self.messages_regle = Label(self.popup_regle)
        self.messages_regle['text'] = "Voici les les fonction pour cette version du programme"
        self.messages_regle.grid()
        self.regle_du_jeu = Label(self.popup_regle)


        ############################todo remplir ce texte
        self.texte_regle_du_jeu = "Le jeu d'échecs se joue à deux joueurs qui font évoluer seize pièces chacun, respectivement blanches et noires, sur un échiquier de 64 cases en alternance blanches et noires." "\n" "Pour parler des adversaires, on dit « les Blancs » et « les Noirs »""\n\n""Pour gagner la partie, il faut vous manger la pièce Roi adverse.""\n\n""Le pion se déplace droit devant lui (vers la 8e rangée pour les Blancs et la 1re rangée pour les Noirs) d'une seule case à chaque coup et sans jamais pouvoir reculer.""\n\n"" Cependant, lors de son tout premier déplacement, chaque pion peut avancer d'une ou de deux cases à la fois, au choix du joueur (au premier coup, on ne peut pas déplacer à la fois deux pions d'une case).""\n\n""Le cavalier est la seule pièce sauteuse (sa case d'arrivée doit être soit inoccupée, soit occupée par une pièce adverse, il n'y a pas d'interception possible comme pour les pièces de ligne).""\n\n"" Son mouvement combiné correspond à deux cases dans une direction comme une Tour puis une case dans une direction perpendiculaire toujours comme une Tour.""\n\n""La tour, le fou et la dame sont des pièces à longue portée, cela signifie qu'elles peuvent se déplacer de plusieurs cases en un seul coup, en ligne droite, tant qu'elles ne sont pas limitées par l'obstacle infranchissable que constitue toute autre pièce, adverse ou non.""\n\n""Pour plus d'information, voici le site web des rêglements du jeu: https://fr.wikipedia.org/wiki/R%C3%A8gles_du_jeu_d%27%C3%A9checs                                                "

        self.regle_du_jeu['text'] = self.texte_regle_du_jeu
        self.regle_du_jeu.grid()

        self.bouton_ok = Button(self.popup_regle,text="ok",width=10, command =self.popup_regle.destroy)
        self.bouton_ok.grid(pady= 10)