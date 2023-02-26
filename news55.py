import os
import sys
import time
import glob
import shutil
import subprocess

def analyze_usb():
    # Recherche de toutes les clés USB connectées
    devices = glob.glob('/dev/sd*')
    if not devices:
        print("Aucune clé USB n'est connectée.")
        sys.exit()
        
    print("Clés USB connectées :")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device}")
    print("")

    # Sélection de la clé USB à analyser
    selected_device = int(input("Choisissez la clé USB à analyser (entrez le numéro) : ")) - 1
    if selected_device < 0 or selected_device >= len(devices):
        print("Sélection de clé USB non valide.")
        sys.exit()
    selected_device = devices[selected_device]

    # Monter la clé USB si elle n'est pas déjà montée
    mount_point = '/media/' + selected_device.split('/')[-1]
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['mount', selected_device, mount_point], check=True)
    selected_device = mount_point

    # Analyse de la clé USB avec ClamAV
    print(f"Analyse de la clé USB {selected_device} en cours...")
    process = subprocess.Popen(['clamscan', '-r', selected_device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
        time.sleep(0.1)
    print("Analyse terminée.")

    # Sélection de la clé USB de destination
    dest_device = int(input("Choisissez la clé USB de destination pour les fichiers scannés (entrez le numéro) : ")) - 1
    if dest_device < 0 or dest_device >= len(devices):
        print("Sélection de clé USB non valide.")
        sys.exit()
    dest_device = devices[dest_device]

    # Monter la clé USB de destination si elle n'est pas déjà montée
    dest_mount_point = '/media/' + dest_device.split('/')[-1]
    os.makedirs(dest_mount_point, exist_ok=True)
    subprocess.run(['mount', dest_device, dest_mount_point], check=True)
    dest_device = dest_mount_point

    # Copie des fichiers scannés sur la clé USB de destination
    for dirpath, dirnames, filenames in os.walk(selected_device):
        for filename in filenames:
            src_path = os.path.join(dirpath, filename)
            dest_path = os.path.join(dest_device, dirpath.replace(selected_device, ''), 'vérifié_' + filename)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)

if __name__ == '__main__':
    analyze_usb()

