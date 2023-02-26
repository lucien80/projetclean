import os
import sys
import time
import glob
import subprocess

def analyze_usb():
    # Recherche de toutes les clés USB connectées
    devices = glob.glob('/media/*')
    print("Clés USB connectées :")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device} ({round(get_usb_size(device)/1024/1024/1024, 2)} GB)")
    print("")

    # Sélection de la clé USB à analyser
    selected_device = int(input("Choisissez la clé USB à analyser (entrez le numéro) : ")) - 1
    selected_device = devices[selected_device]

    # Demande si l'utilisateur souhaite monter la clé USB s'il n'est pas déjà monté
    if not selected_device.startswith('/media/'):
        mount_device = input(f"La clé USB {selected_device} n'est pas montée. Souhaitez-vous la monter automatiquement ? (o/n) : ")
        if mount_device.lower() == 'o':
            mount_point = '/media/' + selected_device.split('/')[-1]
            os.makedirs(mount_point, exist_ok=True)
            subprocess.run(['mount', selected_device, mount_point])
            selected_device = mount_point

    # Analyse de la clé USB avec ClamAV
    print(f"Analyse de la clé USB {selected_device} en cours...")
    result = subprocess.run(['clamscan', '-r', selected_device], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')

    # Affichage des résultats de l'analyse
    print(result)

def get_usb_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_usb_size(entry.path)
    return total

if __name__ == '__main__':
    analyze_usb()
