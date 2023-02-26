import os
import sys
import time
import glob
import shutil
import subprocess

def analyze_and_clean_usb():
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
    selected_device = devices[selected_device]

    # Monter la clé USB si elle n'est pas déjà montée
    mount_point = '/media/' + selected_device.split('/')[-1]
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['mount', selected_device, mount_point])
    selected_device = mount_point

    # Analyse de la clé USB avec ClamAV
    print(f"Analyse de la clé USB {selected_device} en cours...")
    infected_files = []
    process = subprocess.Popen(['clamscan', '-r', selected_device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            if "FOUND" in output:
                file_name = output.split()[0]
                infected_files.append(file_name)
            print(output.strip())
        time.sleep(0.1)
    print("Analyse terminée.")

    # Suppression en toute sécurité des fichiers infectés
    if infected_files:
        print("Fichiers infectés détectés :")
        for file in infected_files:
            print(f"- {file}")
        answer = input("Voulez-vous supprimer les fichiers infectés ? (o/n)")
        if answer.lower() == 'o':
            for file in infected_files:
                file_path = os.path.join(selected_device, file)
                shutil.move(file_path, "/tmp/infected_files")
            print("Les fichiers infectés ont été déplacés dans le dossier /tmp/infected_files pour une analyse ultérieure.")
    else:
        print("Aucun fichier infecté détecté.")

if __name__ == '__main__':
    analyze_and_clean_usb()
