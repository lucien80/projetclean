import os
import sys
import time
import glob
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
    selected_device = devices[selected_device]

    # Monter la clé USB si elle n'est pas déjà montée
    mount_point = '/media/' + selected_device.split('/')[-1]
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['mount', selected_device, mount_point])
    selected_device = mount_point

    # Demander si le rapport doit être généré
    generate_report = input("Générer un rapport détaillé (o/n) : ").lower() == 'o'

    # Demander si les fichiers malveillants doivent être supprimés
    remove_malicious = input("Supprimer les fichiers malveillants (o/n) : ").lower() == 'o'

    # Analyse de la clé USB avec ClamAV
    clamscan_command = ['clamscan', '-r', selected_device]
    if remove_malicious:
        clamscan_command.append('--remove')
    print(f"Analyse de la clé USB {selected_device} en cours...")
    report = []
    process = subprocess.Popen(clamscan_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            if generate_report:
                report.append(output.strip())
        time.sleep(0.1)
    print("Analyse terminée.")

    # Enregistrement du rapport
    if generate_report:
        report_file = f"{selected_device.replace('/', '_')}_report.txt"
        with open(report_file, 'w') as f:
            f.write('\n'.join(report))
        print(f"Rapport enregistré dans {report_file}")

if __name__ == '__main__':
    analyze_usb()
