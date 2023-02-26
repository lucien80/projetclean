import os
import shutil
import subprocess
import sys
import time

# Chemin des clés USB
usb_top_path = '/dev/sda'
usb_bottom_path = '/dev/sdb'

# Liste des extensions de fichiers à renommer
executable_extensions = ['.exe', '.bat', '.sh']

# Commande pour vérifier les fichiers avec ClamAV
clamav_command = 'clamscan --detect-pua --infected --no-summary --recursive --stdout'

# Fonction pour vérifier si une clé USB est connectée
def is_usb_connected(usb_path):
    return os.path.exists(usb_path)

# Fonction pour renommer un fichier
def rename_file(file_path):
    file_dirname = os.path.dirname(file_path)
    file_basename = os.path.basename(file_path)
    file_root, file_extension = os.path.splitext(file_basename)

    if file_extension in executable_extensions:
        new_extension = file_extension + '.renamed'
        new_file_name = file_root + new_extension
        new_file_path = os.path.join(file_dirname, new_file_name)
        os.rename(file_path, new_file_path)
        return new_file_path
    else:
        return file_path

# Fonction pour copier les fichiers sains dans la clé USB saine
def copy_safe_files(src_path, dst_path):
    for root, dirs, files in os.walk(src_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                new_file_path = rename_file(file_path)
                if new_file_path == file_path:
                    shutil.copy2(file_path, dst_path)
                    os.rename(file_path, file_path + '.OK')

# Fonction pour analyser les fichiers avec ClamAV
def analyze_files(files, progress_bar):
    nb_files = len(files)
    for i, file in enumerate(files):
        progress_bar.update(i / nb_files)
        result = subprocess.run([clamav_command, file], stdout=subprocess.PIPE)
        if result.returncode == 1:
            print('Le fichier {} est infecté !'.format(file))
            with open('infected_files.txt', 'a') as f:
                f.write(file + '\n')

# Fonction pour vérifier si un fichier est un PDF
def is_pdf(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(4)
        return header == b'%PDF'

# Fonction principale
def main():
    # Initialisation de la barre de progression
    progress_bar = tqdm(total=1, desc='Analyse en cours...')

    # Attente de la connexion de la clé USB à analyser
    while not is_usb_connected(usb_top_path):
        time.sleep(1)

    # Analyse des fichiers avec ClamAV
    files_to_analyze = []
    for root, dirs, files in os.walk(usb_top_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and not is_pdf(file_path):
                files_to_analyze.append(file_path)
    analyze_files(files_to_analyze, progress_bar)

    # Copie des fichiers sains dans la clé USB saine
    if is_usb_connected(usb_bottom_path):
        copy_safe_files(usb_top_path, usb_bottom_path)

    # Nettoyage de la barre de progression
    progress_bar.close()

if __name__ == '__main__':
    main()
