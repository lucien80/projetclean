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

# Options menu
def show_menu():
    print("\n" + logo)
    print("Choisissez une option :")
    print("1 - Exécuter le fichier 'script1.py'")
    print("2 - Exécuter le fichier 'script2.py'")

# Execute the selected script
def execute_script(choice):
    if choice.lower() == "script1":
        print("\nExécution de 'script1.py'...")
        exec(open("script1.py").read())
    elif choice.lower() == "script2":
        print("\nExécution de 'script2.py'...")
        exec(open("script2.py").read())
    else:
        print("\nOption invalide. Veuillez sélectionner une option valide.")

# Main loop
while True:
    show_menu()
    choice = input("\n> ").strip().lower()
    if not choice:
        continue
    execute_script(choice)
