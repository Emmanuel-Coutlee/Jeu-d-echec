from tkinter import *
from time import strftime, localtime
from pychecs2.echecs.partie import Partie
import pickle
import os
from random import randrange


class menu_global():
    def premier_menu(self):
        self.menu_bar= Menu()
        self.partie_menu = Menu(self.menu_bar, tearoff = 0)
        self.partie_menu.add_command(label= 'Nouvelle partie', command = lambda:self.menu_nouvelle_partie())
        self.partie_menu.add_command(label= 'Charger une partie', command = lambda:self.menu_charger())
        self.partie_menu.add_command(label= 'Sauvegarder la partie', command = lambda:self.menu_enregistrer(False,False))
        self.partie_menu.add_command(label= 'Quitter', command = lambda:self.menu_quitter())


        self.affichage_menu = Menu(tearoff = 0)
        #################################
        #self.affichage_menu.add_command(label= 'Modifier', command =lambda: self.canvas_echiquier.changer_couleur_theme(2,'green'))
        self.affichage_menu.add_command(label= 'Modifier', command =lambda: self.menu_modifier())


        self.aide_menu = Menu(tearoff= 0)
        self.aide_menu.add_command(label= 'Règle de jeu',command = lambda:self.menu_regle_du_jeu())
        self.aide_menu.add_command(label= 'Aide',command = lambda:self.menu_fonction())

        self.menu_bar.add_cascade(label= 'Partie', menu= self.partie_menu)
        self.menu_bar.add_cascade(label= 'Affichage', menu= self.affichage_menu)
        self.menu_bar.add_cascade(label= 'Aide', menu= self.aide_menu)
        self.config(menu = self.menu_bar)

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


            fichier_liste_partie = open("liste_partie", 'r',encoding="utf-8")
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
        except FileNotFoundError:
            self.messages_charger = Label(self.popup_charger)
            self.messages_charger['text'] = "Il n'y a aucune partie sauvegardé."
            self.messages_charger.grid(column = 0, row = 0, pady= 10, padx = 15)
            self.bouton_ok = Button(self.popup_charger,text="ok",width=10, command =self.popup_charger.destroy)
            self.bouton_ok.grid(pady= 10)

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
        except FileNotFoundError:
            self.messages_charger['text'] = "***ATTENTION!***\nVous n'avez sélectionné aucune partie.\nVeuillez choisir une partie."



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


    def nouvelle_partie(self):

        self.Canvas_echiquier.partie.echiquier.initialiser_echiquier_depart()
        self.Canvas_echiquier.dessiner_piece()
        self.Canvas_echiquier.partie.joueur_actif = "blanc"
        self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)

        self.messages_piece_blanc['text'] = "Pièce blanc:"
        self.messages_piece_noir['text'] = "Pièce noir:"
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

    def menu_modifier(self):
        self.popup=Toplevel()
        self.popup.title("modifier")
        self.messages_modifier = Label(self.popup)
        self.messages_modifier['text'] = "Changez les couleurs des cases à votre goût "
        self.messages_modifier.grid(column = 0, columnspan = 2, row = 0, pady= 10, padx = 15)
        self.messages_modifier_2 = Label(self.popup)
        self.messages_modifier_3 = Button(self.popup,text="Autre thême", command =self.changer_theme(True),width = 10)
        self.messages_modifier_3.grid(column = 1, row = 2, pady= 10)

    def changer_couleur_theme(self, type, couleur):
        if type == 1:
            self.couleur_1 = couleur

        self.delete('case')
        self.dessiner_case()

        self.dessiner_piece()

    def changer_theme (self):
        if self.changer_couleur_theme is True:

            for couleur in self.changer_couleur_theme:

                liste_couleur =['purple','cyan','maroon','green','red','blue','orange','yellow']
                c = randrange(8) # => génère un nombre aléatoire de 0 à 7
                self.changer_couleur_theme = liste_couleur[c]

    def sauvegarder_partie(self, nom_fichier,nouvelle_partie,quitter):

        if os.path.exists(nom_fichier+".p"):
            self.menu_ecraser_partie(nom_fichier,nouvelle_partie, quitter)
            return None

        if not os.path.exists("liste_partie"):
            fichier_liste_partie = open("liste_partie", 'w',encoding="utf-8")
        else:
            fichier_liste_partie = open("liste_partie", 'a',encoding="utf-8")
        fichier_liste_partie.writelines("{}\n".format(nom_fichier))

        dictionaire = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces

        joueur_actif = self.Canvas_echiquier.partie.joueur_actif

        pickle.dump((joueur_actif,dictionaire), open(nom_fichier+".p",'wb'))

        #ecriture_csv = csv.writer(fichier_ecriture)

        #echiquier.Echiquier.initialiser_echiquier_depart.dictionnaire_pieces
        #dictionaire = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces
        #for cle, valeur in dictionaire.items():
            #ecriture_csv.writerow([cle,valeur])
            # piece = str("{} {}".format(cle, dictionaire[valeur]))
            #fichier_ecriture.write(piece)

        #On fait un retour de chariot dans le fichier de sortie pour séparer les entiers chiffrés dans le fichier.
            #fichier_ecriture.write("\n")
        #fichier_ecriture.close()

        self.confirmation(nouvelle_partie,quitter)

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

    def ecraser_partie(self,nom_fichier,nouvelle_partie, quitter):
        dictionaire = self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces

        joueur_actif = self.Canvas_echiquier.partie.joueur_actif

        pickle.dump((joueur_actif,dictionaire), open(nom_fichier+".p",'wb'))
        self.popup_ecraser.destroy()
        self.confirmation(nouvelle_partie,quitter)

    def charger_partie(self, nom_partie):
        #lire le ficher partie_echec
        try:
            #fichier_lecture = open(nom_partie,'r',encoding="utf-8")

            (self.Canvas_echiquier.partie.joueur_actif,self.Canvas_echiquier.partie.echiquier.dictionnaire_pieces) = pickle.load(open(nom_partie+".p","rb"))

            #for cle, valeur in csv.reader(fichier_lecture):
                #self.dictionnaire_pieces[cle]= eval(valeur)
            #fichier_lecture.close()
            self.messages_joueur['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
            self.Canvas_echiquier.dessiner_piece()
            self.popup_charger.destroy()
        except FileNotFoundError:
            self.messages_charger['text'] = "***ATTENTION!***\nVous n'avez sélectionné aucune partie.\nVeuillez choisir une partie."

    def confirmation(self,nouvelle_partie,quitter):
        self.popup_enregister.destroy()
        self.confirme = Toplevel()
        self.confirme.title("Enregistrer la partie")
        self.messages_confirme = Label(self.confirme)
        self.messages_confirme['text'] = "La sauvegarde à été éffectué avec succès!"
        self.messages_confirme.grid(padx= 10, pady= 10)
        if nouvelle_partie is True:
            self.bouton_ok = Button(self.confirme,text="ok",width=10, command =self.nouvelle_partie)
            self.bouton_ok.grid(pady= 10)
        elif quitter is True:
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

        #todo remplir ce texte
        self.texte_fonction_programe = "entrez les fonction ici et crédit"

        self.fonction_programe['text'] = self.texte_fonction_programe
        self.fonction_programe.grid()

        self.bouton_ok = Button(self.popup_fonction,text="ok",width=10, command =self.popup_fonction.destroy)
        self.bouton_ok.grid(pady= 10)

    def menu_regle_du_jeu(self):
        self.popup_regle = Toplevel()
        self.popup_regle.title("Règle du jeu")
        self.messages_regle = Label(self.popup_regle)
        self.messages_regle['text'] = "Voici les les fonction pour cette version du programme"
        self.messages_regle.grid()
        self.regle_du_jeu = Label(self.popup_regle)


        #todo remplir ce texte
        self.texte_regle_du_jeu = "entrez les regle ici"

        self.regle_du_jeu['text'] = self.texte_regle_du_jeu
        self.regle_du_jeu.grid()

        self.bouton_ok = Button(self.popup_regle,text="ok",width=10, command =self.popup_regle.destroy)
        self.bouton_ok.grid(pady= 10)