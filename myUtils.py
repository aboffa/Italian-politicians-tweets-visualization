tweetterNames = [
    #M5S
    "matteorenzi",

    "luigidimaio",



    "DaniloToninelli",
    "AlfonsoBonafede",
    "GiuliaGrilloM5S",
    "carlosibilia",
    "PaolaTavernaM5S",
    #PD
    "CarloCalenda",

    "nzingaretti",
    "meb",
    "graziano_delrio",
    #Lega
    "matteosalvinimi",
    "zaiapresidente",
    "M_Fedriga",
    #Forza Italia
    "renatobrunetta",
    "gasparripdl",
    "msgelmini",
    "mara_carfagna",
    "berlusconi",
    #Fratelli d'Italia
    "DSantanche",
    "Ignazio_LaRussa",
    "GiorgiaMeloni",
    #Liberi e Uguali
    "PietroGrasso",
    "lauraboldrini",
    # + Europa
    "emmabonino",
    #Potere al Popolo
    "ViolaCarofalo",
    #Casa Pound
    "distefanoTW",
    #Popolo della famiglia
    "marioadinolfi"

]

politicians = {
    "Matteo Renzi":{
        "twetterName":"matteorenzi",
        "party": "PD",
        "color": "#FFA500",
        "photo": "https:\/\/it.wikipedia.org\/wiki\/Matteo_Renzi#\/media\/File:Matteo_Renzi_2015.jpeg"
    },
    "Luigi Di Maio":{
        "twetterName": "luigidimaio",
        "party": "M5S",
        "color": "#FFFF00",
        "photo": "https:\/\/it.wikipedia.org\/wiki\/Luigi_Di_Maio#\/media\/File:Di_Maio_2018.jpg"
    },
    "Matteo Salvini":{
        "twetterName": "matteosalvinimi",
        "party": "Lega",
        "color": "#08C318",
        "photo": "https:\/\/lmo.wikipedia.org\/wiki\/Matteo_Salvini#\/media\/File:Matteo_Salvini_Viminale_(cropped).jpg"
    }
}
notToConsider = [
    "essere|stare"
    "fa",
    "fare",
    "essere",
    "avere",
    "oggi",
    "RT",
    "rt",
    "essere",
    "due",
    "anni",
    "solo",
    "ora",
    "ecco",
    "dopo",
    "prima",
    "ieri",
    "no",
    "dire",
    "mai",
    "via",
    "ore",
    "così",
    "ogni",
    "cosa",
    "poi",
    "qualcuno",
    "me"
    "ancora",
    "certo",
    "d",
    "potere",
    "va",
    "tutto",
    "molto",
    "già",
    "quando",
    "parte",
    "senza",
    "dice",
    "bene",
    "meno",
    "dovere",
    "me",
    "stare",
    "volere",
    "andare",
    "sì",
    "anno",
    "minima|minimo"
    "fatto",
    "fatta"

]
topics = {
    "europ" : 0,
    "migra" : 0,
    "donna" : 0,
    "giovane" : 0,
    #"sicurezza" : 0,
    "mercato" : 0,
    "economi" : 0,
    "crescita" : 0,
    "pil" : 0,
    "debito" : 0,
    "scuola" : 0,
    "lavor" : 0,
    "web" : 0,
    "tecnologia":0,
    "pensione":0,
    "mafia":0,
    "salute" :0,
    "ambiente" :0,
    "famiglia":0,
    "sud" :0
}

notToConsiderLemma = [
    "grande",
    "minima|minimo"
    "bello"
]