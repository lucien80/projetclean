import os
from tkinter import *
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

# fonction pour effacer les données
def effacer_donnees():
    os.system("nwipe --autonuke")

# fonction pour sécuriser les clés USB
def securiser_cles_usb():
    os.system("chemin/vers/votre/fichier")

# créer la fenêtre principale
root = Tk()
root.title("Département de la Marne")

# créer le logo en ASCII
logo = """
______                      _                            _         _        _        ___  ___                      
|  _  \                    | |                          | |       | |      | |       |  \/  |                      
| | | |___ _ __   __ _ _ __| |_ ___ _ __ ___   ___ _ __ | |_    __| | ___  | | __ _  | .  . | __ _ _ __ _ __   ___ 
| | | / _ \ '_ \ / _` | '__| __/ _ \ '_ ` _ \ / _ \ '_ \| __|  / _` |/ _ \ | |/ _` | | |\/| |/ _` | '__| '_ \ / _ \
| |/ /  __/ |_) | (_| | |  | ||  __/ | | | | |  __/ | | | |_  | (_| |  __/ | | (_| | | |  | | (_| | |  | | | |  __/
|___/ \___| .__/ \__,_|_|   \__\___|_| |_| |_|\___|_| |_|\__|  \__,_|\___| |_|\__,_| \_|  |_/\__,_|_|  |_| |_|\___|
          | |                                                                                                      
          |_|                                                                                                      
                                 
"""

# créer un widget Label pour afficher le logo
logo_label = Label(root, text=logo, font=("Courier", 14))
logo_label.pack()

# créer un widget Label pour afficher le texte du menu
menu_label = Label(root, text="Que souhaitez-vous faire?", font=("Courier", 12))
menu_label.pack(pady=10)

# créer un widget Button pour effacer les données
effacer_button = Button(root, text="Effacer les données", font=("Courier", 12), command=effacer_donnees)
effacer_button.pack(pady=10)

# créer un widget Button pour sécuriser les clés USB
securiser_button = Button(root, text="Sécuriser les clés USB", font=("Courier", 12), command=securiser_cles_usb)
securiser_button.pack(pady=10)

# lancer la boucle principale de la fenêtre
root.mainloop()
