import curses

# Logo ASCII
logo = r"""
______                      _                            _         _        _        ___  ___                      
|  _  \                    | |                          | |       | |      | |       |  \/  |                      
| | | |___ _ __   __ _ _ __| |_ ___ _ __ ___   ___ _ __ | |_    __| | ___  | | __ _  | .  . | __ _ _ __ _ __   ___ 
| | | / _ \ '_ \ / _` | '__| __/ _ \ '_ ` _ \ / _ \ '_ \| __|  / _` |/ _ \ | |/ _` | | |\/| |/ _` | '__| '_ \ / _ \
| |/ /  __/ |_) | (_| | |  | ||  __/ | | | | |  __/ | | | |_  | (_| |  __/ | | (_| | | |  | | (_| | |  | | | |  __/
|___/ \___| .__/ \__,_|_|   \__\___|_| |_| |_|\___|_| |_|\__|  \__,_|\___| |_|\__,_| \_|  |_/\__,_|_|  |_| |_|\___|
          | |                                                                                                      
          |_|
"""

# Fonction pour afficher le menu
def afficher_menu(stdscr, choix):
    stdscr.clear()
    hauteur, largeur = stdscr.getmaxyx()

    # Affichage du logo
    x = largeur // 2 - len(logo.split("\n")[0]) // 2
    for i, ligne in enumerate(logo.split("\n")):
        stdscr.addstr(i, x, ligne)

    # Affichage des options
    texte_options = ["(1) Option 1", "(2) Option 2"]
    y = hauteur // 2
    for i, option in enumerate(texte_options):
        x = largeur // 2 - len(option) // 2
        if choix == i:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, option)
        y += 1

    stdscr.refresh()

# Initialisation de la bibliothèque curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

# Variables pour le menu
choix = 0
nombre_options = 2

# Boucle principale pour afficher le menu et gérer les entrées utilisateur
while True:
    afficher_menu(stdscr, choix)

    # Lecture de la touche entrée
    touche = stdscr.getch()

    # Déplacement vers le haut si la touche haut est pressée
    if touche == curses.KEY_UP:
        choix = (choix - 1) % nombre_options
    # Déplacement vers le bas si la touche bas est pressée
    elif touche == curses.KEY_DOWN:
        choix = (choix + 1) % nombre_options
    # Sortie du programme si la touche q est pressée
    elif touche == ord('q'):
        break
    # Exécution de l'option sélectionnée si la touche entrée est pressée
    elif touche == curses.KEY_ENTER or touche == 10:
        if choix == 0:
            exec(open("fichier1.py").read())
        elif choix == 1:
            exec(open("fichier2.py").read())

# Fermeture de la bibliothèque curses
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()