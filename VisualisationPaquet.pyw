from __future__ import annotations
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.colors import is_color_like
from matplotlib.patches import Rectangle

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from typing import List,Union
from AffichageGraphique import *

class Windows(ctk.CTk):
    def __init__(self,theme: str,tcolor: str,taille: str):
        """ fenètre de base de l'application """
        super().__init__()
        self.geometry(taille) #on definie la taille de la fenètre
        self.taille = taille 
        self.title('Visualisation de paquet d\'ondes') #on definie le titre de la fenètre
        self.protocol("WM_DELETE_WINDOW", self.quitw) #le protocol de fermeture de la fnètre
        self.wm_title("Visualisation de paquet d\'ondes") #on definie le titre de la fenètre tkinter
        try:
            self.iconbitmap('images\\icone.ico') #on définie l'icone de la fenètre
        except:
            pass # si une erreur survient lors de l'import de l'icone on ne change pas l'icone, ce sera celle de base
        self.framemain = MainTK(self) # on gènre les diférentes frames de notre application
        self.framegen = GenererTK(self)
        self.framelaby = LabyTK(self)
        self.framepara = Parametre(self)
        self.framemain.pack(fill='both', expand=True) #on affiche la fenètre principal framemain
        try : #lecture du fichier des préférences
            errors = 0
            f=open('preférences.config')
            lines=f.readlines()
            if len(lines[0].split(',')) >= 7 : #on lit le fichier preférences.config et on donne les valeurs contenue dans le fichier a un dictionnaire contenue dans la class Parametre
                colorsdict = {'3': None, '4': None, '5': None}
                for i in range(3,6):
                    if is_color_like(lines[0].split(',')[i]) and lines[0].split(',')[i] != 'None': # on verifie que les element sont des couleurs
                        colorsdict[str(i)] = lines[0].split(',')[i]
                    elif not is_color_like(lines[0].split(',')[i]):
                        errors += 1
                conversion = {'3':'nodes', '4':'edges', '5':'background'}
                for ncolors in conversion: #on convertie les element recu avec les valeur dans le dictionnaire
                    self.framepara.graphcolors[conversion[ncolors]] = colorsdict.get(ncolors, None)
                check = lines[0].split(',')[6]
                if check == 'True' : #on donne la valeur de la pondération 
                    self.framepara.graphcolors['pond'] = True
                else :
                    self.framepara.graphcolors['pond'] = False
            if len(lines[0].split(',')) < 7 or errors != 0: 

                with open('preférences.config','w') as file: #on lance le programe avec des valeurs par défaut
                        file.write(f"{theme},{tcolor},{taille}")
                        for elem in self.framepara.graphcolors.keys() :
                            file.write(',')
                            file.write(str(self.framepara.graphcolors.get(elem, None)))
        except: #si le code echoue on lance le programe avec des valeurs par défaut et on affiche une erreur
            messagebox.showerror('Erreur Préférences', 'Les valeurs du fichier config ne sont pas lisibles, elle on été remise par défault') 
            self.framepara.graphcolors = {'nodes': None, 'edges': None, 'background': None, 'pond': False}
            with open('preférences.config','w') as file:
                        file.write(f"{theme},{tcolor},{taille},None,None,None,False")
        

    def changeframe(self,frame):
        """fonction qui change la frame affichée"""
        self.framemain.pack_forget()
        self.framegen.pack_forget()
        self.framelaby.pack_forget()
        self.framepara.pack_forget()
        frame.pack(side="top", fill="both", expand=True)

    def changewithclear(self, frame):
     
        self.framemain.pack_forget()
        self.framegen.pack_forget()
        self.framelaby.pack_forget()
        self.framepara.pack_forget()
        for widgets in self.framelaby.winfo_children():
            widgets.destroy()
        frame.pack(side="top", fill="both", expand=True)

    def changewithclearall(self, frame):
        """fonction qui change la frame affichée en supprimant tout les element de toute les frames"""
        self.framemain.pack_forget()
        self.framegen.pack_forget()
        self.framelaby.pack_forget()
        self.framepara.pack_forget()
        for widgets in self.framemain.winfo_children():
            widgets.destroy()
        for widgets in self.framegen.winfo_children():
            widgets.destroy()
        for widgets in self.framepara.winfo_children():
            widgets.destroy()
        for widgets in self.framelaby.winfo_children():
            widgets.destroy()
        self.framemain.initialisation()
        self.framegen.initialisation()
        self.framepara.initialisation()
        frame.pack(side="top", fill="both", expand=True)
    
    def quitw(self):
        """méthode qui quitte le code"""
        plt.close('all') 
        plt.ioff()
        self.quit()
        self.destroy()
        quit()

class MainTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page principal"""
        super().__init__(parent)
        self.parent = parent
        self.initialisation()

    def initialisation(self):
        #affichage et assignations des éléments de la fenètre
        titre(self,'Visualisation de paquet d\'ondes')
        button(self,'Lancer une visualisation',lambda : self.parent.changeframe(self.parent.framegen))
        button(self,'Paramètres',lambda : self.parent.changeframe(self.parent.framepara))
        button(self,'Quitter',self.parent.quit)

        

    

class Parametre(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """Frame de la page des paramètre"""
        super().__init__(parent)
        self.parent = parent
        self.graphcolors = {'nodes': None, 'edges': None, 'background': None, 'pond': False} #on initilalise le dictionaire des valeurs
        self.graphcolorssave = {'nodes': None, 'edges': None, 'background': None, 'pond': False} #on initilalise le dictionaire des valeurs courantes
        self.initialisation()

    def initialisation(self):
        try : #on ouvre le fichier config pour recuperer les valeur de configuration de l'application
            f=open('preférences.config')
            lines=f.readlines()
            c1 = {"light":'Clair',"dark":'Sombre',"system":'Système'}
            c2 = {"blue":'Bleu',"dark-blue":'Bleu Sombre',"green":'Vert'}
            c3 = {'1920x1080':'1920x1080','1080x720':'1080x720','1020x760':'1020x760','855x620':'855x620'}
            selectthemedef = c1.get(lines[0].split(',')[0], 'Sombre')
            selectcolordef = c2.get(lines[0].split(',')[1], 'Bleu')
            selecttailledef = c3.get(lines[0].split(',')[2], '1080x720')
            check = lines[0].split(',')[6]
            if check == 'True' :
                check = True
            else :
                check = False
        except:
            selectthemedef = 'Sombre'
            selectcolordef = 'Bleu'
            selecttailledef = '1080x720'
            check = False
        #affichage et assignations des éléments de la fenètre
        titre(self,'Paramètres')
        selecttheme = selection(self,"Thème de l'application :", ['Clair','Sombre','Système'], selectthemedef)
        selectcolor = selection(self,'Couleur du Thème :', ['Bleu','Bleu Sombre','Vert'], selectcolordef)
        selecttaille = selection(self,'Taille de la fenètre :', ['1920x1080','1080x720','1020x760','855x620'], selecttailledef)
        multiple_button(self,2,['Menu Principal', 'Appliquer'],[self.menuprincipal, lambda: self.validation(selecttheme.get(),selectcolor.get(),selecttaille.get())])
        button(self,'Revenir aux paramètres par défaut', self.reset)
        text(self,"Visualisation de paquet d\'ondes \n Ahmed A, Marwa D, Maissa T, version 1.0", 11)
        
    
    def reset(self) :
        """méthode qui remet les paramètres par défault"""
        message = messagebox.askokcancel('Reset des paramètres !',"Vous êtes sur le point de réinitialiser vos paramètres voulez vous continuer ?")
        if message :
            self.graphcolors = {'nodes': None, 'edges': None, 'background': None, 'pond': False}
            self.validation('Sombre','Bleu','1080x720')

    def menuprincipal(self) :
        """méthode pour revenir au menu principal"""
        message = messagebox.askokcancel('retour au menu',"Toute modification non appliquée ne sera pas prise en compte, voulez vous continuer ?")
        if message :
            self.parent.changeframe(self.parent.framemain)

    def check(self, index: int, val: Union[str,int,float,None,bool]):
        """méthode appelé lors de la coche d'une case"""
        self.graphcolorssave[index] = val

    def validation(self,apmode: str,colormode: str, taillemode: str):
        """méthode qui valide et enregistre les paramètres"""
        self.graphcolors = self.graphcolorssave #on actualise le dictionnaire des paramètres
        c1 = {'Clair':"light",'Sombre':"dark",'Système':"system"}
        c2 = {'Bleu':"blue",'Bleu Sombre':"dark-blue",'Vert':"green"}
        c3 = {'1920x1080':'1920x1080','1080x720':'1080x720','1020x760':'1020x760','855x620':'855x620'}
        ctk.set_appearance_mode(c1.get(apmode, "dark")) #on change le thème
        ctk.set_default_color_theme(c2.get(colormode, "blue")) #on change le thème
        self.parent.geometry(taillemode) #on change la taille
        self.parent.taille = taillemode
        with open('preférences.config','w') as file:   #on ecrit le tout dans le fichier config
            file.write(c1.get(apmode, "dark"))
            file.write(',')
            file.write(c2.get(colormode, "blue"))
            file.write(',')
            file.write(c3.get(taillemode, "1080x720"))
            for elem in self.graphcolors.keys() :
                file.write(',')
                file.write(str(self.graphcolors.get(elem, None)))
        self.parent.changewithclearall(self.parent.framepara) #on actualise la fenetre
    
class GenererTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):
        """fenètre de génération"""
        super().__init__(parent)
        self.parent = parent
        self.initialisation()
    def initialisation(self):
        #affichage et assignations des éléments de la fenètre
        titre(self, 'Paramètres de simulation')
        text(self, 'Profondeur du puits (v0) : (par défaut -4000 eV)')
        self.e_profondeur = champ(self)
        self.e_profondeur.pack()
        text(self, 'Rapport E/v0 : (par défaut 5)')
        self.e_rapportE = champ(self)
        self.e_rapportE.pack()
        text(self, 'Etalement du paquet (sigma) : (par défaut 0.05 m)')
        self.e_etalement = champ(self)
        self.e_etalement.pack()
        text(self, 'Position initiale du paquet (xc) : (par défaut 0.6 m)')
        self.e_initialpose = champ(self)
        self.e_initialpose.pack()
        button(self, 'Générer', lambda: self.parent.framelaby.generer(self.e_profondeur.get(), self.e_rapportE.get(), self.e_etalement.get(), self.e_initialpose.get()))
        multiple_button(self,2, ['Menu Principal','Reset'], [lambda: self.parent.changeframe(self.parent.framemain), self.reset])

    def reset(self):
        """fonction qui reset la page"""
        for widgets in self.winfo_children():
            widgets.destroy()
        self.initialisation()
            
    
    
class LabyTK(ctk.CTkFrame):
    def __init__(self, parent: Windows):

        super().__init__(parent)
        self.parent = parent
        self.menu = False
        self.retourmenu = False
        self.ponder = False
        self.annim = False

    def menuprincipal(self):
        """méthodes qui retourne aux menu principal"""
        self.retourmenu = True
        plt.close('all') #on ferme les fenetre matplolib
        plt.ioff()
        self.parent.changewithclear(self.parent.framemain) #on change de frame

    def generer(self, Profondeurv0, RapportEv0, Etalementpaquetsigma, InitialPosexc):

        import numpy as np
        import math
        import matplotlib.animation as animation

        self.menu = False
        self.buttuns = multiple_button(self, 1, ['Menu principal'], [self.menuprincipal])

        try:
            Profondeurv0 = float(Profondeurv0) 
        except:
            Profondeurv0 = -4000
        try:
            RapportEv0 = float(RapportEv0)
        except:
            RapportEv0 = 5
        try:
            Etalementpaquetsigma = float(Etalementpaquetsigma)
        except:
            Etalementpaquetsigma = 0.05
        try:
            InitialPosexc = float(InitialPosexc)
        except:
            InitialPosexc = 0.6

        


        # Paramètres physiques et numériques
        dt = 1E-7
        dx = 0.001
        nx = int(1 / dx) * 2
        nt = 90000
        nd = int(nt / 1000) + 1
        n_frame = nd
        s = dt / (dx ** 2)
        xc = InitialPosexc
        sigma = Etalementpaquetsigma
        A = 1 / np.sqrt(np.sqrt(np.pi) * sigma)

        
        

        v0 = Profondeurv0
        e = RapportEv0
        E = e * v0
        k = math.sqrt(2 * abs(E))

        o = np.linspace(0, (nx - 1) * dx, nx)
        V = np.zeros(nx)
        V[(o >= 0.8) & (o <= 0.9)] = v0

        cpt = A * np.exp(1j * k * o - ((o - xc) ** 2) / (2 * (sigma ** 2)))
        densite = np.zeros((nt, nx))
        densite[0, :] = np.abs(cpt[:]) ** 2
        final_densite = np.zeros((n_frame, nx))
        re = np.real(cpt[:])
        im = np.imag(cpt[:])
        b = np.zeros(nx)

        it = 0
        for i in range(1, nt):
            if i % 2 != 0:
                b[1:-1] = im[1:-1]
                im[1:-1] = im[1:-1] + s * (re[2:] + re[:-2]) - 2 * re[1:-1] * (s + V[1:-1] * dt)
                densite[i, 1:-1] = re[1:-1] * re[1:-1] + im[1:-1] * b[1:-1]
            else:
                re[1:-1] = re[1:-1] - s * (im[2:] + im[:-2]) + 2 * im[1:-1] * (s + V[1:-1] * dt)

        for i in range(1, nt):
            if ((i - 1) % 1000 == 0):
                it += 1
                final_densite[it][:] = densite[i][:]

        x_trans = o > 0.9  # région après le puits
        densite_finale = final_densite[-1, :]
        T_E = np.sum(densite_finale[x_trans]) / np.sum(densite[0, :])

        # Création de la figure et de l'animation
        text(self, f"V0={v0} eV, E={E} eV, Position initiale: {xc} m, Etalement du paquet: {sigma} m, T = {T_E:.4f}")
        fig1 = Figure()
        ax1 = fig1.add_subplot()
        
        if ctk.get_appearance_mode() == "Light":
            fig1.set_facecolor('#DBDBDB')
            text_color = "black"
        else:
            fig1.set_facecolor('#2B2B2B')
            text_color = "white"

        line, = ax1.plot([], [], label="Densité")
        ax1.plot(o, V, label="Potentiel")
        ax1.set_ylim(0, 13)
        ax1.set_xlim(0, 2)
        ax1.set_xlabel("x", color=text_color)
        ax1.set_ylabel("Densité de probabilité de présence", color=text_color)
        ax1.set_title(f"Marche Ascendante avec E/Vo={e}", color=text_color)
        ax1.tick_params(axis='x', colors=text_color)
        ax1.tick_params(axis='y', colors=text_color)

        def init():
            line.set_data([], [])
            return line,

        def animate(j):
            line.set_data(o, final_densite[j, :])
            return line,

        canvas1 = FigureCanvasTkAgg(figure=fig1, master=self)
        canvas1.draw()
        toolbar1 = toolbarmatplotlib(canvas1, self)
        canvas1.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        toolbar1.pack(fill=tk.X)

        # Animation matplotlib dans tkinter
        self.ani = animation.FuncAnimation(
            fig1, animate, init_func=init, frames=n_frame, blit=False, interval=100, repeat=False
        )
        self.parent.changeframe(self.parent.framelaby)
        
        




if __name__ == "__main__":
    try :
        f=open('preférences.config') #on lit le fichier des préférences
        lines=f.readlines()
        theme = lines[0].split(',')[0]
        color = lines[0].split(',')[1]
        taille = lines[0].split(',')[2] #on verifie que ce sont des bonnes valeurs
        if theme in ["light","dark","system"] and color in ["blue","dark-blue","green"] and taille in ['1920x1080','1080x720','1020x760','855x620']:
            theme = lines[0].split(',')[0]
            color = lines[0].split(',')[1]
            taille = lines[0].split(',')[2]
        else :  #sinon on affiche une erreur et on lance le programme avec des valeurs par défault
            messagebox.showerror('Erreur Préférences', 'Le programme ce lance sur les valeurs de préférence par défault car il ne peut pas correctement lire le fichier config') 
            theme = "dark"
            color = "blue"
            taille = "1080x720"
            with open('preférences.config','w') as file:
                file.write("dark,blue,1080x720,None,None,None,False")
    except: #si le code echoue on lance le programme avec des valeurs par défault
        theme = 'dark'
        color = 'blue'
        taille = "1080x720"
    ctk.set_appearance_mode(theme) #on change le thème de l'application
    ctk.set_default_color_theme(color)  #on change la couleur du thème de l'application
    root = Windows(theme,color,taille) #on lance l'application
    root.mainloop() #on lance la boucle tkinter