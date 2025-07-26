from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

import os
import sqlite3
from time import strftime
#Mettre les page a jours

#for Page in [file for file in os.listdir("Pages") if os.path.isfile(os.path.join("Pages",file))]:
 #   Builder.load_file(f"Pages/{Page}")
Builder.load_file("Pages/Page1.kv")
Builder.load_file("Pages/Page2.kv")
Builder.load_file("Pages/Page3.kv")
Builder.load_file("Pages/Page4.kv")
Builder.load_file("Pages/Page5.kv") #Cotisation
Builder.load_file("Pages/Page6.kv") #Total

class Page1(MDScreen):
    pass

class Page2(MDScreen):
    pass

class Page3(MDScreen):
    pass

class Page4(MDScreen):
    pass

class Page5(MDScreen):
    pass

class Page6(MDScreen):
    pass

#Le main
class CAF(MDApp):
    def build(self):
        self.cr = MDScreenManager()
        Liste = [Page1,Page2,Page3,Page4,Page5,Page6]
        for elmt in Liste:
                self.cr.add_widget(elmt())
        
        return self.cr
    
#------------------ Page6 ------------------
    def Page_Transition2(self):
        Liste = ["Total sur somme","Inventaire sur cotisation"]
        
        Box = MDBoxLayout(orientation = "vertical",spacing = 10,adaptive_height=True,padding=10,pos_hint = {"center_x":.5,"center_y":.5})
        for elmt in Liste:
            But = MDRaisedButton(
                text = elmt,
                pos_hint = {"center_x":.5},
                on_release = self.Appui_Page6
            )
            Box.add_widget(But)

        self.Popup = Popup(
            title = "Compte total",
            content = Box,
            size_hint = (.5,.4),
        )
        self.Popup.open()
    
    def Appui_Page6(self,instance):
        self.Popup.dismiss()
        dic = {"Total sur somme":self.Total,"Inventaire sur cotisation":self.Inven}
        do = dic.get(instance.text)
        do()
    
    def Inven(self):
        #(Name,Mise,Date,Heur,Nbre_de_mise,Payer_with,Remise
        LISTE = []
        for elmt in self.Lire(self.IDENT,self.PASS):
            In = False
            for elmt2 in LISTE:
                if elmt2[0] == elmt[0] and elmt2[1] == elmt[1]:
                    elmt2[2] = str(int(elmt2[2]) + int(elmt[4]))
                    elmt2[3] = str(int(elmt2[2])*int(elmt2[1]))
                    In = True
            if not In:
                LISTE.append([elmt[0],elmt[1],elmt[4],str(int(elmt[1])*int(elmt[4]))])
        
        for i,elmt in enumerate(LISTE):
            elmt.insert(0,i+1)
        self.Next(6)
        pge = self.root.current_screen.ids.Data_Page6
        pge.clear_widgets()
        MD = MDDataTable(
            pos_hint = {"center_x":.5,"center_y":.5},
            size_hint = (.93,.85),
            use_pagination = True,
            column_data = [("ID",10),("Name",20),("Mise",30),("Total de mise",30),('Total',40)],
            row_data = LISTE,
        )
        pge.add_widget(MD)

    def Total(self):
        Liste = set()
        for elmt in self.Lire(self.IDENT,self.PASS):
            Liste.add(elmt[1])
        #Mise , Nombre de personne , Total
        LISTE = []
        TOTAL = 0 #Pour le grand total des argents
        PERSO = 0 #Pour le grand total des person
        for i,emt in enumerate(Liste):
            Total , perso = 0,[]
            for elmt in self.Lire(self.IDENT,self.PASS):
                if elmt[1] == emt:
                    if elmt[0] not in perso:
                        perso.append(elmt[0])
                    Total += int(elmt[1])*int(elmt[4])
            LISTE.append([i+1,emt,len(perso),Total])
            TOTAL += Total
            PERSO += len(perso)
        
        LISTE.append([len(LISTE)+1,"Tous Les mises",PERSO,TOTAL])
        self.Next(6)
        pge = self.root.current_screen.ids.Data_Page6
        pge.clear_widgets()
        MD = MDDataTable(
            pos_hint = {"center_x":.5,"center_y":.5},
            size_hint = (.93,.85),
            use_pagination = True,
            column_data = [("ID",10),("Mise",20),("Nombre de personne",40),('Total',40)],
            row_data = LISTE,
        )
        pge.add_widget(MD)
#-------------------------------------------
    def change_theme(self,instance):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def change_color(self,instance):
        Liste = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        #self.theme_cls.primary_palette = "Rose"
        
        Item = []
        for col in Liste:
            Item.append({
                "text":col,
                "viewclass":"OneLineListItem",
                "on_release":lambda x = col:self.Change(x)
            })
        
        self.Drop = MDDropdownMenu(
            items = Item,
            caller = instance,
            width_mult=4,
        )

        self.Drop.open()
    
    def Change(self,col):
        self.theme_cls.primary_palette = col
        self.Drop.dismiss()
    
    def Close(self,instance):
        self.MDD = self.show(State = "Q",text = "Voulez vous quitter ?",rep = ["Oui","Non"],fonct = [self.stop,self.Error3])

    def Menu_1(self,instance):
        self.Page_Transition1()
    
    def Menu_2(self,instance):
        self.Page_Transition2()

    def on_start(self):
        self.con = sqlite3.connect("base.db")
        But = self.root.current_screen.ids.But_Page1
        self.Cligner = self.Alter(But,self.Net,self.Flou,1)
    
    def on_close(self):
        self.con.close()
         
    def Alter(self,But,font1,font2,duree = 2):
        def Go1():
            font1(But)
            self.Cligner = Clock.schedule_once(lambda dt:Go2() , duree)
        def Go2():
            font2(But)
            self.Cligner = Clock.schedule_once(lambda dt:Go1(),duree)
        
        Go2()
    
    def New_Compte(self,instance):
        #self.Next()
        self.root.current_screen.ids.cr.current = "Page2"

    def Valider_Page2(self, instance,Ident,Pass):
        #try:
            # Accès simplifié avec les nouveaux IDs
            Error = False
            for elmt in [Ident,Pass]:
                if elmt.text == "": 
                    elmt.error = True
                    Error = True

            if not Error:
                Ident,Pass = Ident.text,Pass.text
                
                if self.existes(Ident, Pass):
                    self.IDENT,self.PASS = Ident,Pass
                    self.MD = self.show(text=f"Bienvenue collecteur {Ident}", State="I", fonct=self.Ok_page2)
                else:
                    self.MD = self.show(text="Compte introuvable", State="I", fonct=self.Error)
                
    def Send_page_2(self,instance,ident,pass1,pass2):
        Error = False
        for elmt in [ident,pass1,pass2]:
            if elmt.text == "":
                elmt.error = True
                Error = True
        if not Error:
            if pass1.text != pass2.text:
                #Error = True
                self.MD = self.show(text = "Echec de Verification des mots de passe",fonct = self.Error)
            elif f"{ident.text}_{pass1.text}" in self.return_liste_table():
                self.MD = self.show(text = "Compte invalid !",fonct = self.Error)
            else:
                self.Page2_Ident,self.Page2_passs = ident.text,pass1.text
                INFO = f"Identifiant : {ident.text}\nMot de passe : {pass1.text}"
                self.MD = self.show(text = f"{INFO}\n\nConfirner ?",rep = ["[b]Oui[/b]","[b]Non[/b]"],fonct = [self.Oui_page2,self.Non_page2],State = "Q")
    
    def Oui_page2(self,instance):
        try:
            self.MD.dismiss()
            self.add_in_table(self.Page2_Ident,self.Page2_passs)
            self.MD = self.show(text = "Creation reussi !",fonct =self.Back_Home_1)
        except:
            self.MD = self.show(text = "Echec !\nVotre nom contient des caratere indesirable",fonct = self.Error)

    def Back_Home_1(self,instance):
        self.MD.dismiss()
        self.root.current_screen.ids.cr.current = "Page1"
    
    
    def Non_page2(self,instance):
        self.MD.dismiss()

    def Ok_page2(self,instance):
        self.MD.dismiss()
        self.Page_Transition1()
    
    def Page_Transition1(self):
        self.Li  = ["Histoire des Cotisations","Cotisations","Compte total","Ajouter un membre"]
        #List_but = []
        Box = MDBoxLayout(orientation = 'vertical', spacing = 10,adaptive_height = True,pos_hint = {"center_y":.5})
        for elmt in self.Li:
            MD = MDRaisedButton(
                text =f"[b]{elmt}[/b]",
                elevation = 3,
                pos_hint = {'center_x': 0.5},
                on_release= self.appui,
            )
            #List_but.append(MD)
            Box.add_widget(MD)
            
        self.Op = Popup(
            title = "Page de Tansistion",
            #text = "Veuillez choisir une operation",
            #type = "confirmation",
            content = Box,
            size_hint = (.5,.5),
        )
        self.Op.open()
    
    def appui(self,instance):
        val = instance.text[3:-4]
        self.Op.dismiss()
        #print(val)
        dic = {}
        for elmt1,elmt2 in zip(self.Li,[self.History,self.Cotisation,self.Compte_total,self.Member]):
            dic[elmt1] = elmt2
        do = dic.get(val)
        do()
    
    def New_member(self,instance,mise,name):
        Tous = self.Lire(self.IDENT,self.PASS)
        Error = False
        for elmt in [mise,name]:
            if elmt.text == "":
                elmt.error = True
                Error = True
        
        if not Error:
            In = False
            for elmt in Tous:
                if elmt[0] == name.text and elmt[1] == mise.text:
                    self.show(text=f"{name.text} existe déjà dans la mise {mise.text}",fonct = self.Error)
                    In = True
            if not In:
                Liste = [name.text,mise.text,strftime("%D"),strftime('%T'),0,0,0]
                self.add_item_in_table(self.IDENT,self.PASS,Liste)

    def Compte_total(self):
        self.Page_Transition2()
    
    def Member(self):
        self.Next(4)
        self.Next_de_la_page(3)

    def Cotisation(self):
        Tous = self.Lire(self.IDENT,self.PASS)
        if not Tous:
            self.MD = self.show(text = "Pas de Mise",fonct = self.Error)
        else:
            Mise = set()
            for elmt in Tous:
                Mise.add(elmt[1])
            self.Next(5)
            self.Next_de_la_page(1)
            Pge = self.root.current_screen.ids.Les_Mises_Page5
            Pge.clear_widgets()
            for elmt in Mise:
                BUT = MDRaisedButton(
                    text = elmt,
                    on_release = self.Appui_Mise_cotise
                )
                Pge.add_widget(BUT)

    
    def Appui_Mise_cotise(self,instance):
        self.MISE = instance.text

        Tous = self.Lire(self.IDENT,self.PASS)
        Liste = set()
        for elmt in Tous:
            if elmt[1] == self.MISE:
                Liste.add(elmt[0])
        
        self.Next(5)
        self.Next_de_la_page(2)
        Pge = self.root.current_screen.ids.Les_Names_Page5
        Pge.clear_widgets()
        
        for elmt in Liste:
            BUT = MDRaisedButton(
                text = elmt,
                on_release = lambda x , Elmt = self.MISE : self.Appui_Name_cotise(x,Elmt)
            )
            Pge.add_widget(BUT)

    
    def Appui_Name_cotise(self,instance,Mise):
        self.Next_de_la_page(3)

        cur = self.root.current_screen.ids
        MISE,NAME,NBRE,TOTAL,PAYER,REMISE = cur.Mise_Page5,cur.Name_Page5,cur.Cotise_Page5,cur.Total_Page5,cur.Payer_Page5,cur.Remise_Page5
        
        #Mettre tous a Zero
        for elmt in [MISE,NAME,NBRE,TOTAL,PAYER,REMISE]:
            elmt.text = ""

        NAME.text = instance.text
        MISE.text = Mise

        self.Remplie_moi_les_choses(NAME,MISE,NBRE,TOTAL,PAYER,REMISE)

    def Remplie_moi_les_choses(self,NAME,MISE,NBRE,TOTAL,PAYER,REMISE):
        
        try:
            Nbr = int(NBRE.text)
            TOTAL.text = str(int(MISE.text)*Nbr)
            if PAYER.text == "" or int(PAYER.text) < int(TOTAL.text):
                PAYER.error = True
                REMISE.text = "Error"
            else:
                REMISE.text = str(int(PAYER.text) - int(TOTAL.text))
        except:
            pass
        
        #print(1)
        self.Remplissement = Clock.schedule_once(lambda dt : self.Remplie_moi_les_choses(NAME,MISE,NBRE,TOTAL,PAYER,REMISE),.1)
    
    def Cotisation_Page5(self,instance,NAME,MISE,NBRE,TOTAL,PAYER,REMISE):#Button pour arreter le page5
        Clock.unschedule(self.Remplissement)
        Error = False
        self.LISTE_PAGE5 = [NAME,MISE,NBRE,TOTAL,PAYER,REMISE]

        for elmt in self.LISTE_PAGE5[2:]:
            if elmt.text == "" or elmt.text =="Error":
                Error = True
        
        if Error:
            self.MDD = self.show(text = "Impossible de soumettre",fonct = self.Error3)
            self.Back_petit_et_grand()
        
        else:
            Table = f"Mise : {MISE.text}\nMise Total : {NBRE.text}\nTotal : {TOTAL.text}"
            self.MDD2 = self.show(text = f"{Table}\n\nConfirmer ?",rep = ["Oui","Non"],fonct = [self.Ok_page5,self.Non_page5],State = "Q")
    
    def Error3(self,instance):
        self.MDD.dismiss()
    
    def Non_page5(self,instance):
        self.MDD2.dismiss()

    def Ok_page5(self,instance):
        #(Name,Mise,Date,Heur,Nbre_de_mise,Payer_with,Remise)
        Date,Heur = strftime("%D"),strftime("%T")
        
        Liste = [elmt.text for elmt in self.LISTE_PAGE5[:2]] + [Date,Heur] + [elmt.text for elmt in self.LISTE_PAGE5[3:]]
        self.MDD2.dismiss()
        
        self.add_item_in_table2(self.IDENT,self.PASS,Liste)
    
    def add_item_in_table2(self,Iden,Pass,Liste):
        cur = self.con.cursor()
        Table = f"{Iden}_{Pass}"
        if self.existes(Iden,Pass):
            cur.execute(f"Insert into {Table} (Name,Mise,Date,Heur,Nbre_de_mise,Payer_with,Remise) values  (?,?,?,?,?,?,?)",tuple(Liste))
            self.con.commit()
            self.Ajouter = self.show(text = "Ajout effectué avec success !",fonct = self.Ajouter_But)
        else:
            self.MDD = self.show(text = "Compte invalide !",fonct = self.Error3)
    
    def Ajouter_But(self,instance):
        self.Ajouter.dismiss()
        self.Back_petit_et_grand()

    #def Obtenir(self,)
    def History(self):
        Tous = self.Lire(self.IDENT,self.PASS)
        if not Tous:
            self.MD = self.show(text = "Pas de Mise",fonct = self.Error)
        else:
            Mise = set()
            for elmt in Tous:
                Mise.add(elmt[1])
            self.Next(3)
            Pge = self.root.current_screen.ids.Les_Mises
            Pge.clear_widgets()
            for elmt in Mise:
                BUT = MDRaisedButton(
                    text = elmt,
                    on_release = self.Appui_Mise
                )
                Pge.add_widget(BUT)
            #self.Next()
            self.root.current_screen.ids.cr.current = "Page1"
            
    def Appui_Mise(self,instance): #Page3
        Mise = instance.text
        Tous = self.Lire(self.IDENT,self.PASS)
        Liste = set()
        for elmt in Tous:
            if elmt[1] == Mise:
                Liste.add(elmt[0])
        
        self.Next_de_la_page(2)
        Pge = self.root.current_screen.ids.Les_Clients
        Pge.clear_widgets()
        self.root.current_screen.ids.Title.text = f"[b]Les Clients de la mise  {Mise}[/b]"
        for elmt in Liste:
            BUT = MDRaisedButton(
                text = elmt,
                on_release = lambda x , Elmt = Mise : self.Appui_Name(x,Elmt)
            )
            Pge.add_widget(BUT)
    
    def Appui_Name(self,instance,Elmt):
        Name = instance.text
        self.Next_de_la_page(3)
        Tous = self.Lire(self.IDENT,self.PASS)
        Liste = []
        i = 1
        for elmt in Tous:
            if elmt[1] == Elmt and elmt[0] == Name:
                Liste.append([i] + list(elmt))
                i+=1
        
        Pge = self.root.current_screen.ids.Data
        Data = MDDataTable(
                    size_hint = (0.93,0.85),
                    pos_hint = {"center_x":.5,"center_y":.5},
                    use_pagination=True,
                    column_data=[("ID", 10),("Nom",30),("Mise",20),("Date", 30),("Heur", 30),("Mise Total", 30),("Prix Total", 30),("Remise", 30)],
                    row_data = Liste,)
        Pge.clear_widgets()
        Pge.add_widget(Data)


    def Error(self,instance):
        self.MD.dismiss()
        
    def show(self,text,State = "I",rep = None,fonct = None):
        def info():
            MD = MDDialog(text = text,buttons = [MDFlatButton(text = "Ok",on_release = fonct)])
            return MD
        
        def Question():
            But = []
            for elmt,elmt1 in zip(rep,fonct):
                but = MDFlatButton(
                    text = elmt,
                    on_release = elmt1,
                )
                But.append(but)
            MD = MDDialog(text = text,buttons = But)
            return MD
        
        dic = {"I":info , "Q":Question}
         
        val = dic.get(State)()
        val.open()
        return val
    
    #def New_Compte(self,instance):

    
    def Lire(self, Ident, passs):
        if self.existes(Ident, passs):
            cur = self.con.cursor()
            Table = f"{Ident}_{passs}"
            Tous = cur.execute(f"SELECT * FROM {Table}")
            return [elmt for elmt in Tous]
        return []

    def add_in_table(self,Iden,Pass):
        cur = self.con.cursor()
        Table = f"{Iden}_{Pass}"
        #Date;;;Heurs;;;Nbre_de_mise;;;Payer_avec;;;remise
        cur.execute(f"CREATE TABLE {Table} (Name TEXT,Mise TEXT,Date TEXT, Heur TEXT, Nbre_de_mise TEXT, Payer_with TEXT, Remise TEXT)")
        self.con.commit()
    
    def add_item_in_table(self,Iden,Pass,Liste):
        cur = self.con.cursor()
        Table = f"{Iden}_{Pass}"
        if self.existes(Iden,Pass):
            cur.execute(f"Insert into {Table} (Name,Mise,Date,Heur,Nbre_de_mise,Payer_with,Remise) values  (?,?,?,?,?,?,?)",tuple(Liste))
            self.con.commit()
            self.Ajouter = self.show(text = "Ajout effectué avec success !\n\nAjouter encore ?",rep = ["[b]Oui[/b]","[b]Non[/b]"],fonct = [self.Ok_ajouter,self.Non_Ajouter],State="Q")
        else:
            self.MD = self.show(text = "Compte invalide !",fonct = self.Error2)
    
    def Ok_ajouter(self,instance):
        self.Ajouter.dismiss()

    def Non_Ajouter(self,instance):
        self.Page_Transition1()
        self.Ajouter.dismiss()

    def Error2(self,instance):
        self.MD.dismiss()

    def Back_de_la_page(self,val = None):
        Pge = self.root.current_screen.ids.cr.current
        self.root.current_screen.ids.cr.current = f'Page{str(int(Pge.split("e")[-1])-1) if not val else str(val)}'

    def Next_de_la_page(self,val = None):
        Pge = self.root.current_screen.ids.cr.current
        self.root.current_screen.ids.cr.current = f'Page{str(int(Pge.split("e")[-1])+1) if not val else str(val)}'
    
    def Back_de_la_page(self,val = None,val2 = None):
        Pge = self.root.current_screen.ids.cr.current
        if val:
            self.Next(val)
        self.root.current_screen.ids.cr.current = f'Page{str(int(Pge.split("e")[-1])-1) if not val2 else str(val2)}'
    
    def return_liste_table(self):
        cur = self.con.cursor()
        listes = cur.execute("SELECT name FROM sqlite_master  WHERE type = 'table'")
        return [liste[0] for liste in listes]

    def existes(self,ident,passs):
        if f"{ident}_{passs}" in self.return_liste_table():
            return True
        return False
    
    def Commancer(self,instance):
        Clock.unschedule(self.Cligner)
        self.Next()

    def Next(self,val = None,val2 = None):
        Pge = self.cr.current.split("e")
        self.cr.current = f"Page{str(int(Pge[-1])+1) if not val else str(val)}"
        try:
            self.Next_de_la_page(1 if not val2 else val2)
        except:
            pass
    
    def Back(self,val = None):
        Pge = self.cr.current.split("e")
        self.cr.current = f"Page{str(int(Pge[-1])-1) if not val else str(val)}"
    
    def Back_button(self,instance,val= None):
        self.Back(val)
    
    def Back_petit_et_grand(self,val = None,val2 = None):
        try:
            self.Back_de_la_page(val,val2)
        except:
            #self.Back(val)
            pass
    
    def Back_petit_et_grand_Button(self,instance,val = None,val2 = None):
        self.Back_petit_et_grand(val,val2)

    def Net(self,Wedget):
        Wedget.opacity = 1
    
    def Flou(self,Wedget,visi = .5):
         Wedget.opacity = visi
CAF().run()