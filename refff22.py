import os
import shutil
import subprocess
import time

# Définir les extensions de fichiers à traiter
extensions = ['.txt', '.docx', '.pdf', '.jpg', '.png']

# Définir les chemins d'entrée et de sortie
input_path = '/media/'
output_path = '/home/user/clean/'

# Trouver les noms des clés USB
usb_names = []
for root, dirs, files in os.walk('/media'):
    for name in dirs:
        if 'usb' in name.lower():
            usb_names.append(name)

# Traiter chaque clé USB
for usb_name in usb_names:
    print('Traitement de la clé USB :', usb_name)

    # Vérifier si la clé USB est montée en lecture seule
    is_read_only = False
    with open('/proc/mounts', 'r') as f:
        for line in f:
            if usb_name in line and 'ro,' in line:
                is_read_only = True
                break

    # Analyser chaque fichier
    files_processed = 0
    files_infected = 0
    for root, dirs, files in os.walk(os.path.join(input_path, usb_name)):
        for file in files:
            # Vérifier si l'extension est dans la liste des extensions à traiter
            if any(file.endswith(ext) for ext in extensions):
                # Chemin d'entrée et de sortie
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_path, file)

                # Vérifier la signature du fichier avec ClamAV
                cmd = ['clamscan', '--no-summary', '--quiet', input_file_path]
                result = subprocess.run(cmd, capture_output=True)
                if result.returncode == 0:
                    # Copier le fichier dans le dossier de sortie
                    shutil.copy2(input_file_path, output_file_path)

                    # Changer le format des fichiers exécutables
                    if file.endswith('.exe') or file.endswith('.bat') or file.endswith('.sh'):
                        os.chmod(output_file_path, 0o644)

                    # Incrémenter le nombre de fichiers traités
                    files_processed += 1
                else:
                    # Incrémenter le nombre de fichiers infectés
                    files_infected += 1

                    # Afficher le chemin du fichier infecté
                    print('Fichier infecté :', input_file_path)

    # Afficher le résultat du traitement
    print('Fichiers traités :', files_processed)
    print('Fichiers infectés :', files_infected)

    # Afficher "OK" pour indiquer que le traitement est terminé
    for root, dirs, files in os.walk(os.path.join(output_path)):
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, 'OK - ' + file)
            os.rename(old_file_path, new_file_path)

    # Copier tous les fichiers traités dans le dossier racine de la clé USB
    for root, dirs, files in os.walk(os.path.join(output_path)):
        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(input_path, usb_name, file))

    # Attendre quelques secondes avant de passer à la clé USB suivante
    time.sleep(5)
