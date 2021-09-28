#Tohle je hlavni část Appky - určuje obrazovky a co se na nich bude dít a obsahuje veškerou logiku pro Mind mapu

#Ostatni kody - jedtnolive funkce
from kivy.core import window
import hlavni_funkce
import pomocne_funkce

#Kivy
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

#Pro mapu
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.uix.scatter import Scatter

def aktualizuj_data():
    #Pokaždé, kdyz udělám nějakou změnu a taky na začátku chci aktualizovat data - načíst znovu rodiče a děti
    global nactena_data
    global seznam_text

    nactena_data = hlavni_funkce.ukaz_data2()

    seznam_text = ""

    for line in nactena_data:
        seznam_text = seznam_text + "\n" + line['rodic'] +": " + line['deti']
 

#Zacatek - co se stane při spuštění:
aktualizuj_data()
prepinac_nalezen = 0 #Přepínač slouží k tomu, aby se na Edit obrazovce šlo dál pouze v případě, že podmínky jsou splněny - máme vybraného rodiče případně děti
rodic = ""
dite = ""

class Menu(Screen):
    #viz Kivi
    def btn_ukaz_graf(self):
        pass

class Sc_ukaz_data(Screen):
    #Pouze ukazani aktualnich dat po řádcích
    def btn_ukaz_data(self):
        self.ids.seznam.text = seznam_text

    def btn_do_menu(self):
        pass

class Sc_mapa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Hlavni cil teto appky - poskládání myšlenkové mapy z uložených dat
        nactena_data = hlavni_funkce.ukaz_data2()
        self._myslenky = []
        global id
        id = -1

        def vytvor_krouzek(self, myslenka, x,y, myslenka_otce):
            #Tady se tvoří na určítých pozicích kroužek a vepisuje se text, pozice kroužku se určuje podle podle úrovně a taky kolik jich je
            #Text dovnitř se pak snaží trefit
            
            global id
            
            text_myslenky = myslenka['text']
            self.text_do_krouzku = CoreLabel(text = text_myslenky)
            self.text_do_krouzku.refresh()

            stred_x = Window.width/2
            strex_y = Window.height/2
            self.txtkrouzek = Rectangle(texture= self.text_do_krouzku.texture, pos= (stred_x + x - round(self.text_do_krouzku.texture.size[0]/2,0) , strex_y + y), size = self.text_do_krouzku.texture.size)

            zvetseni_w = self.txtkrouzek.size[0]*0.55 + 20
            txt1_w = self.txtkrouzek.size[0]+zvetseni_w
            txt1_h = self.txtkrouzek.size[1]
            txt1_x = self.txtkrouzek.pos[0] - zvetseni_w/2
            txt1_y = self.txtkrouzek.pos[1]
            self.krouzek = Rectangle(pos= (txt1_x, txt1_y- 20), size = (txt1_w, txt1_h + 40), source = "krouzek.png")

            self.canvas.add(self.krouzek)
            self.canvas.add(self.txtkrouzek)

            #Sipka - TODO zatim nefugnuje rotace, tak neřeším ani pozici
            # if not myslenka_otce == None:
            #     #Pouze pro myšlenky, které mají nějakou nadařazou - ne pro střed

            #     with self.canvas:
            #         pass

            #     sipka_w = 10
            #     sipka_h = myslenka_otce['y']
            #     sipka_x = txt1_x

            #     sipka_y = txt1_y

            #     novy_scatter = Scatter(do_rotation=False, do_scale=False, do_translation=False, rotation = 0)

            #     nova_sipka = Rectangle(pos = (sipka_x, sipka_y), size = (sipka_w, sipka_h), source = "sipka.png")

            #     novy_scatter.canvas.add(nova_sipka)

            #     print("pos textu: " + str(txt1_x))
            #     print ("pos sipky: " + str(nova_sipka.pos))

            #     self.scat_pro_sipku = self.add_widget(novy_scatter)

            # else:
            #     pass

            self._myslenky.append(self.krouzek)

            id += 1

            return id

        vytvorene_myslenky = []
        koren =[]

        # Načteme všechny myšlenky
        # Zatím máme jen 4 základní směry, ať je to jednodušší, do budoucna ještě relativně jednoduše půjde 8, ale více už bude horší vzhledem k souřadnicm
        myslenky, koren_text = hlavni_funkce.nacti_myslenky(nactena_data)

        koren.append({'text': str(koren_text)})

        vytvor_krouzek(self, koren[0], 0,0, None)
        vytvorene_myslenky.append({'x': 0,'y': 0})

        for myslenka in myslenky:
            # Koren uz mame
            if myslenka['level'] == 0:
                myslenka['x'] = 0
                myslenka['y'] = 0
                continue

            if myslenka['level'] == 1:
                otec = 0
            else:
                otec = myslenka['c rodice']     

            if myslenka['smer'] == "up":
                x = vytvorene_myslenky[otec]['x']
                y = vytvorene_myslenky[otec]['y']+100

            if myslenka['smer'] == "down":
                x = vytvorene_myslenky[otec]['x']
                y = vytvorene_myslenky[otec]['y']-100

            if myslenka['smer'] == "left":
                x = vytvorene_myslenky[otec]['x']-100
                y = vytvorene_myslenky[otec]['y']

            if myslenka['smer'] == "right":
                x = vytvorene_myslenky[otec]['x']+100
                y = vytvorene_myslenky[otec]['y']

            if myslenka['level'] == 1 or  myslenka['poradi'] == 1:
                zarovnani = 0
            else:                 
                dalsi_v_poradi = myslenka['poradi']-1 #Další v pořadí počítáme od 2. místa jako první

                #Sudé se pro výpočet počítají -1
                if (dalsi_v_poradi % 2) == 0:
                    zaklad_pro_vypocet = dalsi_v_poradi -1
                else:
                    zaklad_pro_vypocet = dalsi_v_poradi

                zarovnani = zaklad_pro_vypocet *100 - (zaklad_pro_vypocet -1)/2 *100

                #Sude další v pořadí je posunuté vlevo/dolů místo vpravo/nahoru
                if (dalsi_v_poradi % 2) == 0:
                    zarovnani = zarovnani*(-1)

            if myslenka['smer'] == "up" or myslenka['smer'] == "down":
                x = x + zarovnani
            if myslenka['smer'] == "left" or myslenka['smer'] == "right":
                y = y + zarovnani   
                
            myslenka['x'] = x
            myslenka['y'] = y
            myslenka = vytvor_krouzek(self, myslenka, x,y, vytvorene_myslenky[otec])
            vytvorene_myslenky.append({'x': x,'y': y})

    def btn_do_menu(self):
        pass

class Sipka(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        source = "sipka.png"


class Sc_edit(Screen):
    #Tohle je obrazovka pro veškeré změny - přidání, úprava, smazání, vzhledem k podobné struktuře je jedna

    def btn_pridat(self):
        global edit_akce
        self.ids.pridani_hint.text = "Přidání: vyber si jedno z dětí níže a napiš ho tady:"
        self.ids.seznam.text = seznam_text
        edit_akce = "pridat"

    def btn_upravit(self):
        global edit_akce
        self.ids.pridani_hint.text = "Úprava: Nejdříve si vyber RODIČE, kterému chceš upravit dítě a napiš ho tady:"
        self.ids.seznam.text = seznam_text
        edit_akce = "upravit"

    def btn_smazat(self):
        global edit_akce
        self.ids.pridani_hint.text = "Smazání: Nejdříve si vyber RODIČE, kterému chceš smazat dítě/děti a napiš ho tady:"
        self.ids.seznam.text = seznam_text
        edit_akce = "smazat"

    def btn_smazat_vse(self):
        global edit_akce
        self.ids.pridani_hint.text = "Smazat vše: Napiš si nový kořen (střed myšlenkové mapy):"
        self.ids.seznam.text = ""
        edit_akce = "smazat_vse"

    def btn_default(self):
        global edit_akce
        self.ids.pridani_hint.text = "Nahrát původní data: Pokud opravdu chceš nahrát původní data, klikni na pokračovat"
        self.ids.seznam.text = ""
        edit_akce = "default"

    def btn_pokracovat(self):
        #Pokračování už je specifické pro každou akci, Hinty dost přesně popisují, co se děje :)
        
        global prepinac_nalezen
        global rodic
        global dite

        if edit_akce == "pridat":
            if prepinac_nalezen == 0:

                rodic = self.ids.rodic_input.text
                check_rodic_nalezen = pomocne_funkce.vybrat_rodice_z_deti2(rodic)

                if check_rodic_nalezen:
                    self.ids.pridani_hint.text = "Napiš nové děti. Oddělte je středníkem (;):"
                    self.ids.seznam.text = "Vybraný rodič: " + self.ids.rodic_input.text
                    self.ids.rodic_input.text = ""
                    prepinac_nalezen = 1
                else:
                    self.ids.pridani_hint.text = "Rodič nenalezen. Zkus to znovu. Vyber si jedno z dětí níže a napiš ho tady:"

            else:

                deti = self.ids.rodic_input.text

                if not deti == "":
                    hlavni_funkce.pridat_dite_pokracovani(rodic, deti, nactena_data)

                    self.ids.pridani_hint.text = "Děti přidany. Můžeš přidat další \nVyber si jedno z dětí níže a napiš ho tady:"
                    aktualizuj_data()
                    self.ids.seznam.text = seznam_text
                    self.ids.rodic_input.text = ""
                    prepinac_nalezen = 0

        if edit_akce == "upravit":
            if prepinac_nalezen == 0:
                rodic = self.ids.rodic_input.text
                mame_rodice = pomocne_funkce.najdi_rodice(rodic, nactena_data)

                if not mame_rodice == None:
                    self.ids.pridani_hint.text = "Vyber si z dětí níže:"
                    deti = hlavni_funkce.upravit_dite_pokracovani(rodic, nactena_data)
                    self.ids.seznam.text = "Rodič " + rodic + " má tyto děti: " + deti
                    self.ids.rodic_input.text = ""
                    prepinac_nalezen = 1
                else:
                    self.ids.pridani_hint.text = "Rodič nenalezen. Zkus to znovu. Úprava: vyber si jedno z dětí níže a napiš ho tady:"
            else:
                if prepinac_nalezen == 1:
                    dite = self.ids.rodic_input.text
                    check_dite_nalezeno = hlavni_funkce.upravit_dite_pokracovani2(rodic, dite, nactena_data)

                    if not check_dite_nalezeno == False:
                        self.ids.pridani_hint.text = "Napiš nové jméno pro toto dítě:"
                        self.ids.seznam.text = "Vybrané dítě: " + dite
                        self.ids.rodic_input.text = ""
                        prepinac_nalezen = 2
                    else:
                        self.ids.pridani_hint.text = "Dítě nenalezeno. Zkus to znovu. Úprava: vyber si jedno z dětí níže a napiš ho tady:"

                else:
                    nove_jmeno = self.ids.rodic_input.text

                    if not nove_jmeno == "":
                        hlavni_funkce.upravit_dite_pokracovani3(nove_jmeno, rodic, dite, nactena_data)
                        self.ids.pridani_hint.text = "Dítě upraveno. Můžeš upravit další \nVyber si jedno z dětí níže a napiš ho tady:"
                        aktualizuj_data()
                        self.ids.seznam.text = seznam_text
                        self.ids.rodic_input.text = ""
                        prepinac_nalezen = 0

        if edit_akce == "smazat":
            if prepinac_nalezen == 0:
                rodic = self.ids.rodic_input.text
                check_rodic_nalezen = pomocne_funkce.vybrat_rodice_z_deti2(rodic)

                if check_rodic_nalezen:
                    self.ids.pridani_hint.text = "Pokud chceš smazat jenom jedno dítě, vyber si z dětí níže. Pokud všechny, nech prázndé"
                    deti = hlavni_funkce.upravit_dite_pokracovani(rodic, nactena_data)
                    self.ids.seznam.text = "Rodič " + rodic + " má tyto děti: " + deti
                    self.ids.rodic_input.text = ""
                    prepinac_nalezen = 1
                else:
                    self.ids.pridani_hint.text = "Rodič nenalezen. Zkus to znovu."

            else:
                if prepinac_nalezen == 1:
                    dite = self.ids.rodic_input.text

                    ma_deti = hlavni_funkce.smazat_deti2(rodic, dite, nactena_data)

                    if dite == "":
                        if ma_deti == "":
                            self.ids.pridani_hint.text = "Zmáčkni ještě jednou pro smazání"
                            self.ids.seznam.text = "Smazat všechny děti od rodiče " + rodic
                            prepinac_nalezen = 2
                        else:
                            self.ids.pridani_hint.text = "Zmáčkni ještě jednou pro smazání"
                            self.ids.seznam.text = "Smazat všechny děti od rodiče " + rodic +"\nPozor deti od " + ma_deti + " budou smazány taky"
                            prepinac_nalezen = 2
                    else:
                        if ma_deti == False:
                            self.ids.pridani_hint.text = "Dítě nenalezeno. Zkus to znovu."
                        else:
                            if ma_deti == "":
                                self.ids.pridani_hint.text = "Zmáčkni ještě jednou pro smazání"
                                self.ids.seznam.text = "Smazat dítě: " + dite
                                self.ids.rodic_input.text = ""
                                prepinac_nalezen = 2
                            else:
                                self.ids.pridani_hint.text = "Zmáčkni ještě jednou pro smazání"
                                self.ids.seznam.text = "Smazat dítě: " + dite + " i jeho děti"
                                self.ids.rodic_input.text = ""
                                prepinac_nalezen = 2
                else:
                    hlavni_funkce.smazat_deti_pokracovani(rodic, dite, nactena_data)
                    self.ids.pridani_hint.text = "Dítě smazáno. Můžeš další"
                    aktualizuj_data()
                    self.ids.seznam.text = seznam_text
                    self.ids.rodic_input.text = ""
                    prepinac_nalezen = 0

        if edit_akce == "smazat_vse":
            if prepinac_nalezen == 0:
                rodic = self.ids.rodic_input.text
                if rodic == "":
                    self.ids.pridani_hint.text = "Nový střed nebyl zadán, Napiš si nový kořen (střed myšlenkové mapy):"
                else:
                    self.ids.rodic_input.text = ""
                    prepinac_nalezen = 1
            if prepinac_nalezen == 1:
                dite_input = self.ids.rodic_input.text
                if dite_input == "":
                    self.ids.pridani_hint.text = "Musí být zadáno alespoň první dítě, může být i více, odděl středníkem:"
                else:
                    hlavni_funkce.novy_koren(rodic, dite_input)
                    aktualizuj_data()
                    self.ids.pridani_hint.text = "Všechna data smazána, Nový střed : " + rodic + ": a první děti: " + dite_input
                    prepinac_nalezen = 0
                    self.ids.rodic_input.text = ""

        if edit_akce == "default":
            hlavni_funkce.vlozit_default()
            aktualizuj_data()
            self.ids.pridani_hint.text = "Data přemazána na původní."
            
            




    def btn_do_menu(self):
        global prepinac_nalezen
        prepinac_nalezen = 0

class Spravce(ScreenManager):
    pass

class MindMapApp(App):
    pass

if __name__=='__main__':
    MindMapApp().run()
