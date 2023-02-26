import os
import shutil
import subprocess
import sys
from tqdm import tqdm

# Chemin d'accès de ClamAV
CLAMAV_PATH = "/usr/bin/clamscan"

# Chemin d'accès du répertoire de destination des fichiers sains
DEST_DIR = "/media/usb_saine/"

def is_infected(file_path):
    """Vérifie si le fichier spécifié est infecté par un virus en utilisant ClamAV."""
    result = subprocess.run([CLAMAV_PATH, "-q", file_path], stdout=subprocess.PIPE)
    return result.returncode != 0

def main():
    # Recherche de toutes les clés USB connectées
    devices = [os.path.join("/dev", device) for device in os.listdir("/dev") if device.startswith("sd")]
    
    # Si aucune clé USB n'est trouvée, on quitte le script
    if not devices:
        print("Aucune clé USB n'a été trouvée.")
        sys.exit(0)
    
    # Sélectionne la première clé USB trouvée comme source de fichiers à analyser
    src_device = devices[0]
    print(f"Source device: {src_device}")
    
    # Montage de la clé USB source pour la lecture des fichiers
    src_mount_dir = "/mnt/src_usb"
    os.makedirs(src_mount_dir, exist_ok=True)
    subprocess.run(["sudo", "mount", "-t", "auto", src_device, src_mount_dir], check=True)
    print(f"Source mount point: {src_mount_dir}")
    
    # Recherche de tous les fichiers sur la clé USB source
    src_files = []
    for root, dirs, files in os.walk(src_mount_dir):
        for name in files:
            src_files.append(os.path.join(root, name))
    
    # Création du répertoire de destination des fichiers sains
    os.makedirs(DEST_DIR, exist_ok=True)
    print(f"Destination directory: {DEST_DIR}")
    
    # Analyse de chaque fichier et copie des fichiers sains vers la clé USB de destination
    for file_path in tqdm(src_files, desc="Analyzing files", unit="file"):
        if os.path.isfile(file_path):
            if is_infected(file_path):
                print(f"File {file_path} is infected")
            else:
                shutil.copy2(file_path, DEST_DIR)
    
    # Démontage de la clé USB source
    subprocess.run(["sudo", "umount", src_mount_dir], check=True)
    print(f"Source unmounted: {src_mount_dir}")
    
    # Affichage d'un résumé des résultats
    print("Summary:")
    print(f"Files analyzed: {len(src_files)}")
    print(f"Safe files copied: {len(os.listdir(DEST_DIR))}")
