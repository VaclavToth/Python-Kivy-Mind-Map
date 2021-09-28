import pickle

import pomocne_funkce

def vlozit_default():
    # zakladni data do prazdnou databazi
    rodice_a_deti = []

    rodice_a_deti.append({'rodic': "Chci programovat!", 'deti':"Zaměstnání; Znalosti; Proč; Mám na to?"})
    rodice_a_deti.append({'rodic': "Proč", 'deti':"Pěkné peníze; Logické myšlení; Něco tvořím"})
    rodice_a_deti.append({'rodic': "Zaměstnání", 'deti':"Korporáty; StartUp; Fintech"})
    rodice_a_deti.append({'rodic': "Znalosti", 'deti':"Git; Databáze; Jazyky; Testování"})
    rodice_a_deti.append({'rodic': "Korporáty", 'deti':"Nechci, jebne mi"})
    rodice_a_deti.append({'rodic': "Něco tvořím", 'deti':"Malý projekt sám!; Nejlíp v týmu "})
    rodice_a_deti.append({'rodic': "Mám na to?", 'deti':"Výška; Udělám testy; Obekcám to"})
    rodice_a_deti.append({'rodic': "Jazyky", 'deti':"C#; Python; PHP"})

    pickle.dump(rodice_a_deti, open("data.dat","wb"))
    print("Data premazana na default!")

def novy_koren(rodic_vstup, dite_vstup):
    # Kdyz chci všechno smazat a mám definovaný nový kořen a aspoň jedno nové dítě
    rodice_a_deti = []
    rodice_a_deti.append({'rodic': rodic_vstup, 'deti':dite_vstup})
    pickle.dump(rodice_a_deti, open("data.dat","wb"))
    print("Novy kořen!")

def ukaz_data2():
    # Ukaze vsechny data po jednotlivych rodicich, neresi urovne
    nactena_data = pomocne_funkce.nacti_data()
    return nactena_data

def pridat_dite2(rodic_vstup):

    rodic = pomocne_funkce.vybrat_rodice_z_deti2(rodic_vstup)

    if rodic == "err: rodic nenalezen":
        return rodic
    else:
        return "ok"

def pridat_dite_pokracovani(rodic, nove_deti, nactena_data):
    # Uz tohoto rodice mame?
    c_rodice = pomocne_funkce.najdi_rodice(rodic, nactena_data)

    if not c_rodice == None:
        nactena_data[c_rodice]['deti'] = nactena_data[c_rodice]['deti'] + '; ' +  nove_deti
    else:
        nactena_data.append({'rodic': rodic, 'deti': nove_deti})

    pomocne_funkce.uloz_data(nactena_data)

def smazat_deti2(rodic, dite, nactena_data):
    
    c_rodice, deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(rodic, nactena_data)
    ma_deti = ""

    if dite == "":

        #Projdem vsechny jeho deti, jestli nemaji deti a smažem
        for dite in deti:
            c_ditete = pomocne_funkce.najdi_dite(dite, deti)
    
            #ceknu jesi dite nema svoje deti
            c_ditete_jako_rodice = pomocne_funkce.najdi_rodice(deti[c_ditete], nactena_data)

            if not c_ditete_jako_rodice == None:
                if ma_deti == "":
                    ma_deti = dite
                else:
                    ma_deti = ma_deti + " a " + dite
            
        return ma_deti
    else:
        c_ditete = pomocne_funkce.najdi_dite(dite, deti)

        if c_ditete == None:
            check = False
            return check

        #jeste ceknu jesi dite nema svoje deti - v tom pripade smazu i deti
        c_ditete_jako_rodice = pomocne_funkce.najdi_rodice(deti[c_ditete], nactena_data)

        if not c_ditete_jako_rodice == None:
            ma_deti = dite
        
        return ma_deti

def smazat_deti_od_deti(deti, nactena_data):
     for dite in deti:

            c_ditete = pomocne_funkce.najdi_dite(dite, deti)
            c_ditete_jako_rodice = pomocne_funkce.najdi_rodice(deti[c_ditete], nactena_data)
            #ceknu jesi dite nema svoje deti
            if c_ditete_jako_rodice == None:
                pass #Nema - jedu na dalsi
            else:
                # Ma - opakuju smycku pro jeho deti
                c_rodice, deti_od_deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(dite, nactena_data)
                smazat_deti_od_deti(deti_od_deti, nactena_data)

                #a na konci ho znova najdu (poradi se mohlo zmenit) a smazu
                c_rodice = pomocne_funkce.najdi_rodice(dite, nactena_data)

                del(nactena_data[c_rodice])


def deti_od_korene(nactena_data):

    #Uroven 0
    #Tady se definuji smery - zatím na pevno 4
    koren = nactena_data[0]['rodic']
    deti = pomocne_funkce.rozdel_deti(nactena_data[0]['deti'])

    pocet_deti_od_korene = 0

    for dite in deti:
        pocet_deti_od_korene +=1

        if pocet_deti_od_korene == 1: smer = "up"
        if pocet_deti_od_korene == 2: smer = "down"
        if pocet_deti_od_korene == 3: smer = "left"
        if pocet_deti_od_korene == 4: smer = "right"


        if pocet_deti_od_korene == 5:
            print("Vic jak 4 zakladni deti zatim neumim, nahravam zpatky defaultni databazi")
            vlozit_default()
            quit()

        myslenky = []
        myslenky.append({'poradi': pocet_deti_od_korene, 'text': dite, 'smer': smer, 'level': 1, })


     
    return koren, myslenky, pocet_deti_od_korene

def nacti_myslenky(nactena_data):

    myslenky = []
    koren = nactena_data[0]['rodic']
    
    cislo_myslenky = len(myslenky)
    #prvni bude myslenka otce
    myslenky.append({'text': koren, 'smer': None, 'level': 0, 'c rodice': None })
    

    c_rodice, deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(koren, nactena_data)
    myslenky = nacti_deti_od_deti(deti, nactena_data, myslenky, cislo_myslenky)

    return myslenky, koren

def nacti_deti_od_deti(deti, nactena_data, myslenky, cislo_myslenky_rodice):
    poradi_ditete = 0
    
    for dite in deti:
        poradi_ditete +=1
        cislo_myslenky = len(myslenky)
        
        if cislo_myslenky_rodice == 0:
            #Deti od kořene udávají směr
            if poradi_ditete == 1: smer = "up"
            if poradi_ditete == 2: smer = "down"
            if poradi_ditete == 3: smer = "left"
            if poradi_ditete == 4: smer = "right"

            if poradi_ditete == 5:
                print("Vic jak 4 zakladni deti zatim neumim, nahravam zpatky defaultni databazi")
                vlozit_default()
                quit()
            
            myslenky.append({'poradi': poradi_ditete, 'text': dite, 'smer': smer, 'level': 1, 'c rodice': cislo_myslenky_rodice })
        
        else:
            #Nejdříve načeteme myšlenku otce
            myslenka_otce = myslenky[cislo_myslenky_rodice]
          
            myslenky.append({'text': dite, 'smer': myslenka_otce['smer'], 'level': myslenka_otce['level']+1, 'poradi': poradi_ditete, 'c rodice': cislo_myslenky_rodice })

        c_ditete = pomocne_funkce.najdi_dite(dite, deti)
        c_ditete_jako_rodice = pomocne_funkce.najdi_rodice(deti[c_ditete], nactena_data)
        #ceknu jesi dite nema svoje deti
        if c_ditete_jako_rodice == None:
            pass #Nema - jedu na dalsi
        else:
            # Ma - opakuju smycku pro jeho deti
            c_ditete_jako_rodice, deti_od_deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(dite, nactena_data)
            nacti_deti_od_deti(deti_od_deti, nactena_data, myslenky, cislo_myslenky)
    return myslenky



def smazat_deti_pokracovani(rodic, dite, nactena_data):

    c_rodice, deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(rodic, nactena_data)

    if dite == "":
        #Smazu celeho rodice
        del(nactena_data[c_rodice])

        #A pak jeho deti
        smazat_deti_od_deti(deti, nactena_data)
            
    else:

        c_ditete = pomocne_funkce.najdi_dite(dite, deti)
        c_ditete_jako_rodice = pomocne_funkce.najdi_rodice(deti[c_ditete], nactena_data)
        #Smazu samotne dite pokud je rodicem
        
        if not c_ditete_jako_rodice == None:
            c_d_rodice, deti_od_deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(dite, nactena_data)
            del(nactena_data[c_ditete_jako_rodice])
            smazat_deti_od_deti(deti_od_deti, nactena_data)

        #Vymazu zaznam o tomto diteti u rodice
        c_ditete = pomocne_funkce.najdi_dite(dite, deti)
        del(deti[c_ditete])
        nove_deti = pomocne_funkce.spojeni_deti(deti)
        nactena_data[c_rodice]['deti'] = nove_deti

    # Na konec ulozime
    pomocne_funkce.uloz_data(nactena_data)

def upravit_dite_pokracovani(rodic, nactena_data):

    ma_deti = pomocne_funkce.najdi_rodice(rodic, nactena_data)
    
    if not ma_deti == None:
        c_rodice, deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(rodic, nactena_data)
        
        spojene_deti = pomocne_funkce.spojeni_deti(deti)

        return spojene_deti   

def upravit_dite_pokracovani2(rodic, dite, nactena_data):

    c_rodice, deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(rodic, nactena_data)
    c_ditete = pomocne_funkce.najdi_dite(dite, deti)
    
    if c_ditete == None:
        check = False
    else:
        check = True
    return check

def upravit_dite_pokracovani3(nove_jmeno, rodic, dite, nactena_data):

    c_rodice, deti = pomocne_funkce.najdi_rodice_a_jeho_deti2(rodic, nactena_data)
    c_ditete = pomocne_funkce.najdi_dite(dite, deti)

    #jeste ceknu jesi dite nema svoje deti - v tom pripade prejmenuju i rodice
    c_ditete_jako_rodice = pomocne_funkce.najdi_rodice(deti[c_ditete], nactena_data)

    if not c_ditete_jako_rodice == None:
        nactena_data[c_ditete_jako_rodice]['rodic'] = nove_jmeno   

    deti[c_ditete] = nove_jmeno
    nove_deti = pomocne_funkce.spojeni_deti(deti)
    nactena_data[c_rodice]['deti'] = nove_deti
    pomocne_funkce.uloz_data(nactena_data)