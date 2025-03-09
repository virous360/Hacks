import requests 
import re
import wget
import os 

url = 'https://www.schoolmouv.fr/cours/combinatoire-et-denombrement/fiche-de-cours'
headers = {
    'Host': 'www.schoolmouv.fr',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/x-component',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Next-Action': '4f5f3f09f5e6791522c31545174e107d5302c629',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://www.schoolmouv.fr',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=4',
}

DEBUG = True

def debug(*arg) -> None:
    if DEBUG : print(arg)

def get_pdf_link(cour : str) -> str: 
    response = requests.post(url, headers=headers, data=f'["{cour}","fiche-de-cours"]', verify=True)
    filters = re.findall("https://pdf-schoolmouv.+.pdf",response.text)
    if len(filters) == 0 :
        debug("Error: regex returned an empty list (no pdf found)")
        return "" 
    return filters[0]

def filter_name(name : str) -> str:
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if not all(char not in name for char in invalid_chars):
        debug(f"The folder name '{name}' is invalid.")
    for char in invalid_chars:
        name = name.replace(char," ")
    return name

def create_folder(chapitre : str ,matiere : str,classe : str) -> str:
    sanitized_classe = filter_name(classe)
    sanitized_matiere = sanitized_classe + "/" + filter_name(matiere)
    sanitized_name = sanitized_matiere +"/"+ filter_name(chapitre)
    # create classe folder
    if os.path.exists(classe):
        debug(f"The folder for the '{sanitized_classe}' class already exists.")
    else :
        os.makedirs(sanitized_classe)
        debug(f"The folder '{sanitized_classe}' has been created.")
    # create matiere folder
    if os.path.exists(sanitized_matiere):
        debug(f"The folder for the '{sanitized_matiere}' matiere already exists.")
    else :
        os.makedirs(sanitized_matiere)
        debug(f"The folder '{sanitized_matiere}' has been created.")
    # create folder
    if os.path.exists(sanitized_name):
        debug(f"The folder for the '{sanitized_name}' already exists.")
    else :
        os.makedirs(sanitized_name)
        debug(f"The folder '{sanitized_name}' has been created.")
    return sanitized_name + "/"

def download_pdf(cour_file : str, matiere : str, chapitre : str, classe : str) -> None : 
    loc = create_folder(classe=classe,matiere=matiere,chapitre=chapitre)    
    pdf_link = get_pdf_link(cour_file)
    if pdf_link == "" : 
        print(f"skipping download of cour, no links returned : {cour_file}")
        return
    wget.download(pdf_link,loc)

# wget.download("https://www.schoolmouv.fr/eleves/histoire")
matiere = "mathematiques"
classe="terminale"
leak = {
  "Algèbre et géométrie": [
    "combinatoire-et-denombrement",
    "droites-plans-et-vecteurs-de-l-espace",
    "manipulation-des-vecteurs-des-droites-et-des-plans-de-l-espace",
    "orthogonalite-et-distances-dans-l-espace",
    "representations-parametriques-et-equations-cartesiennes"
  ],
  "Analyse": [
    "raisonnement-par-recurrence",
    "suites",
    "limites-des-fonctions",
    "complements-sur-la-derivation-2",
    "fonctions-convexes-1",
    "continuite-des-fonctions-d-une-variable-reelle",
    "fonction-logarithme",
    "etude-de-la-fonction-logarithme-neperien",
    "fonctions-sinus-et-cosinus",
    "primitives-equations-differentielles",
    "calcul-integral"
  ],
  "Probabilités": [
    "succession-d-epreuves-independantes-schema-de-bernoulli",
    "sommes-de-variables-aleatoires",
    "concentration-loi-des-grands-nombres"
  ],
  "Option mathématiques expertes : Nombres complexes": [
    "nombres-complexes-point-de-vue-algebrique",
    "nombres-complexes-point-de-vue-geometrique",
    "nombres-complexes-et-trigonometrie",
    "equations-polynomiales",
    "utilisation-des-nombres-complexes-en-geometrie"
  ],
  "Option mathématiques expertes : Arithmétique": [
    "arithmetique",
    "pgcd-theoremes-de-bezout-et-de-gauss",
    "nombres-premiers-et-petit-theoreme-de-fermat"
  ],
  "Option mathématiques expertes : Graphes et matrices": [
    "calcul-matriciel-1",
    "graphes-et-matrices",
    "suites-de-matrices-colonnes",
    "chaines-de-markov"
  ],
  "Option mathématiques complémentaires : Analyse": [
    "suites-numeriques-modeles-discrets",
    "fonctions-continuite-derivabilite-limites-representation-graphique",
    "continuite-de-fonctions",
    "fonction-logarithme-neperien-ln-",
    "complements-sur-la-derivation-3",
    "fonctions-convexes",
    "primitives-et-equations-differentielles",
    "integration-2"
  ],
  "Option mathématiques complémentaires : Probabilités et statistique": [
    "lois-discretes",
    "lois-a-densite-2",
    "statistique-a-deux-variables-quantitatives"
  ]
}

for chapitre in leak : 
    list_of_cours = leak[chapitre]
    for cour in list_of_cours : 
        download_pdf(cour_file=cour,matiere=matiere,chapitre=chapitre,classe=classe)
    

# download_pdf(cour_file="representations-parametriques-et-equations-cartesiennes",matiere="mathematiques",chapitre="Algèbre et géométrie",classe="terminale")

# print(create_folder(chapitre="Algèbre et géométrie",matiere="mathematiques",classe="terminale"))