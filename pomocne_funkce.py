import pickle

def nacti_data():
    nactena_data = pickle.load(open("data.dat","rb"))
    return nactena_data

def uloz_data(upravena_data):
    pickle.dump(upravena_data, open("data.dat","wb"))

def mozni_rodice2():
    # ukaze koren a unikatni deti - vsechny mozne rodice
    nactena_data = nacti_data()

    koren = nactena_data[0]['rodic']
    
    vsechny_deti = []

    vsechny_deti.append(koren)

    for line in nactena_data:
            deti = line['deti'].split("; ")

            for dite in deti:
                vsechny_deti.append(dite)

    vsechny_deti = list(dict.fromkeys(vsechny_deti))

    return vsechny_deti

def vybrat_rodice_z_deti2(rodic):
    moznosti = mozni_rodice2()

    mame_rodice = False

    for dite in moznosti:
        if rodic == dite:
            mame_rodice = True

    return mame_rodice

def najdi_rodice(vybrany_rodic, nactena_data):

     for index, stary_rodic in enumerate(nactena_data):
        if vybrany_rodic == stary_rodic['rodic']:
            return index

def nacti_rodice(nactena_data):

    rodice = []

    for line in nactena_data:
        rodice.append(line['rodic'])

    return rodice

def rozdel_deti(deti):
    deti = deti.split("; ")
    return deti

def najdi_dite(vybrane_dite, deti):
    c_ditete = None

    for index, dite in enumerate(deti):
            if dite == vybrane_dite:
                c_ditete = index

    return c_ditete

def najdi_rodice_a_jeho_deti2(rodic, nactena_data):

    c_rodice = najdi_rodice(rodic, nactena_data)   

    deti = rozdel_deti(nactena_data[c_rodice]['deti'])

    return c_rodice, deti

def spojeni_deti(deti):
    #Všechno se odjíví od středníku ;
    nove_deti = ""
    for dite in deti:
        if nove_deti == "":
            nove_deti = dite
        else:
            nove_deti = nove_deti + "; " + dite
    return nove_deti

