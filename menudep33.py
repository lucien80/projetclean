#!/usr/bin/env python

# ASCII art logo
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

# Display the logo
print(logo)

# Options menu
print("Choisissez une option :")
print("1 - Exécuter le fichier 'script1.py'")
print("2 - Exécuter le fichier 'script2.py'")

# User input
choice = input("> ")

# Execute the selected script
if choice == "1":
    exec(open("effacement.py").read())
elif choice == "2":
    exec(open("script2.py").read())
else:
    print("Option invalide.")