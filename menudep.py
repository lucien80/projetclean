import os
import shutil
import subprocess
import sys
import time

# ASCII art logo
LOGO = """

______                      _                            _         _        _        ___  ___                      
|  _  \                    | |                          | |       | |      | |       |  \/  |                      
| | | |___ _ __   __ _ _ __| |_ ___ _ __ ___   ___ _ __ | |_    __| | ___  | | __ _  | .  . | __ _ _ __ _ __   ___ 
| | | / _ \ '_ \ / _` | '__| __/ _ \ '_ ` _ \ / _ \ '_ \| __|  / _` |/ _ \ | |/ _` | | |\/| |/ _` | '__| '_ \ / _ \
| |/ /  __/ |_) | (_| | |  | ||  __/ | | | | |  __/ | | | |_  | (_| |  __/ | | (_| | | |  | | (_| | |  | | | |  __/
|___/ \___| .__/ \__,_|_|   \__\___|_| |_| |_|\___|_| |_|\__|  \__,_|\___| |_|\__,_| \_|  |_/\__,_|_|  |_| |_|\___|
          | |                                                                                                      
          |_|                                                                                                      


"""

# menu principal
def menu_principal():
    while True:
        print(LOGO)
        print("Bienvenue dans le Département de la Marne !\n")
        print("1. Sécurisé Clés USB")
        print("2. Effacer les données")
        print("3. Quitter")

        choix = input("\nEntrez le numéro de votre choix : ")
        if choix == "1":
            securiser_cles_usb()
        elif choix == "2":
            effacer_donnees()
        elif choix == "3":
            sys.exit()
        else:
            print("Choix invalide. Veuillez réessayer.\n")

# sécurité des clés USB
def securiser_cles_usb():
    print("\nSécurisation des clés USB\n")
    
    # liste des extensions à convertir
    extensions_convertir = [".exe", ".bat", ".sh"]
    
    # signature des virus
    signature_virus = "c86bdf7df53c1d53797f41460b0ec8d7"
    
    # répertoire de la clé USB source
    source = input("Entrez le chemin de la clé USB source : ")
    while not os.path.isdir(source):
        print("Le chemin entré n'est pas valide. Veuillez réessayer.")
        source = input("Entrez le chemin de la clé USB source : ")
    
    # répertoire de la clé USB cible
    cible = input("Entrez le chemin de la clé USB cible : ")
    while not os.path.isdir(cible):
        print("Le chemin entré n'est pas valide. Veuillez réessayer.")
        cible = input("Entrez le chemin de la clé USB cible : ")
    
    # progress bar
    total = sum(len(f) for _, _, files in