import os
import shutil
import subprocess
import sys
from pathlib import Path
from tqdm import tqdm

# Chemin du dossier de destination pour les fichiers sains
dest_dir = "CLEAN"

# Vérification si le dossier de destination existe, sinon le créer
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Vérification des fichiers dans tous les périphériques de stockage connectés
dev_list = []
for device in Path("/dev").glob("sd*"):
    dev_list.append(str(device))

if not dev_list:
    print("Aucun périphérique de stockage détecté")
    sys.exit(1)

# Itération à travers la liste de périphériques de stockage
for device in dev_list:
    print(f"Analyse de {device}")
    
    # Montage du périphérique
    try:
        mount_dir = subprocess.check_output(["sudo", "mkdir", "-p", "/mnt/tmp && sudo mount -o rw,uid=1000,gid=1000", f"{device}1", "/mnt/tmp"], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du montage de {device}: {e.output.decode()}")
        continue

    # Analyse du périphérique avec ClamAV
    try:
        proc = subprocess.Popen(["sudo", "clamscan", "-r", "-i", "--exclude-dir=/mnt/tmp", "/mnt/tmp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = proc.communicate()
        if error:
            print(f"Erreur lors de l'analyse de {device}: {error.decode()}")
            continue
    except Exception as e:
        print(f"Erreur lors de l'analyse de {device}: {e}")
        continue

    # Parcours des résultats de l'analyse de ClamAV
    for line in output.decode().splitlines():
        if "Infected files" in line:
            infected_files = int(line.split(":")[1].strip())
            if infected_files > 0:
                print(f"{infected_files} fichier(s) infecté(s) sur {device}")
        elif "SCAN SUMMARY" in line:
            break
        elif " OK" in line:
            src_file = line.split(" ")[-1]
            dest_file = os.path.join(dest_dir, os.path.relpath(src_file, "/mnt/tmp"))
            dest_file = dest_file[:-4] + ".txt" if dest_file.endswith(".pdf") else dest_file
            dest_folder = os.path.dirname(dest_file)

            # Vérification de l'existence du dossier de destination, sinon le créer
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            # Copie du fichier de source vers le dossier de destination
            shutil.copy2(src_file, dest_file)

            # Modification des permissions et des propriétaires du fichier de destination
            os.chown(dest_file, os.getuid(), os.getgid())
            os.chmod(dest_file, 0o664)

            # Suppression de l'exécution des fichiers .exe, .bat et shell
            if dest_file.endswith((".exe", ".bat", ".sh")):
                os.chmod(dest_file, 0o644)

    # Démontage du périphérique
    subprocess.run(["sudo", "umount", "/mnt/tmp"])
    subprocess.run(["sudo", "rmdir", "/mnt/tmp"])
