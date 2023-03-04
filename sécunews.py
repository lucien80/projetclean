import os
import subprocess

# Fonction pour afficher les informations sur les clés USB connectées
def display_usb_info():
    # Utilise la commande "lsblk" pour afficher les informations sur les périphériques de bloc
    output = subprocess.check_output(['lsblk', '-o', 'NAME,SIZE,MOUNTPOINT', '-J']).decode('utf-8')
    data = eval(output)['blockdevices']
    # Parcourt chaque périphérique de bloc pour afficher les informations sur les clés USB
    print("USB drives detected:")
    for device in data:
        if device['name'].startswith('sd'):
            # Vérifie si le périphérique est monté
            if 'mountpoint' in device:
                mount_point = device['mountpoint']
            else:
                mount_point = '(not mounted)'
            # Affiche le nom du périphérique, sa taille et son point de montage (s'il est monté)
            print(f"{device['name']} ({device['size']}B) - {mount_point}")
    print("")

# Fonction pour analyser une clé USB
def analyze_usb():
    # Utilise la commande "lsblk" pour trouver toutes les clés USB connectées
    output = subprocess.check_output(['lsblk', '-o', 'NAME', '-J']).decode('utf-8')
    data = eval(output)['blockdevices']
    usb_devices = [device['name'] for device in data if device['name'].startswith('sd')]
    if not usb_devices:
        print("No USB drives found.")
        return
    
    # Affiche les clés USB détectées et demande à l'utilisateur de choisir la clé à analyser
    print("Connected USB drives:")
    for i, device in enumerate(usb_devices):
        print(f"{i+1}. {device}")
    print("")
    selected_device = int(input("Choose the USB drive to analyze (enter the number): ")) - 1
    selected_device = usb_devices[selected_device]

    # Utilise la commande "df" pour trouver le point de montage de la clé USB sélectionnée
    output = subprocess.check_output(['df', '-P', selected_device]).decode('utf-8')
    selected_mount_point = output.split('\n')[1].split()[5]

    # Demande à l'utilisateur de choisir le répertoire de destination pour les fichiers non malveillants
    destination = input("Enter the destination directory for non-malicious files: ")

    # Analyse la clé USB sélectionnée avec ClamAV
    print(f"Analyzing USB drive {selected_device}...")
    subprocess.run(['clamscan', '-r', '--move=' + destination, selected_mount_point])
    print("Analysis complete.")

# Fonction pour mettre à jour la base de données de ClamAV
def update_clamav_database():
    print("Updating ClamAV database...")
    subprocess.run(['freshclam'])
    print("ClamAV database updated.")

if __name__ == '__main__':
    display_usb_info()
    analyze_usb()
    update_clamav_database()
