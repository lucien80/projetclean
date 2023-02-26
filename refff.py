import os
import shutil
import sys
import subprocess
import time

# Définition des chemins des ports USB
USB_SOURCE = "/dev/sda"
USB_DEST = "/dev/sdb"

# Liste des extensions à filtrer
FILTER_EXTS = [".exe", ".bat", ".sh"]

# Définition de la fonction pour nettoyer un fichier
def clean_file(file_path):
    # Vérification de la signature du virus avec ClamAV
    result = subprocess.run(["clamscan", "-i", file_path], capture_output=True, text=True)
    if "Infected files: 1" in result.stdout:
        print(f"{file_path} est infecté !")
        return False

    # Renommage des fichiers pour indiquer qu'ils ont été traités
    new_file_path = file_path + ".ok"
    os.rename(file_path, new_file_path)
    print(f"{file_path} a été nettoyé !")

    # Copie des fichiers nettoyés vers la clé USB saine
    shutil.copy2(new_file_path, USB_DEST)

    return True

# Définition de la fonction pour nettoyer une clé USB
def clean_usb():
    print("Recherche d'une clé USB infectée...")
    while True:
        # Recherche d'un périphérique USB branché
        devices = os.listdir("/dev")
        usb_devices = [d for d in devices if d.startswith("sd") and d != "sda"]
        if not usb_devices:
            print("Pas de clé USB trouvée, veuillez en brancher une.")
            time.sleep(1)
            continue

        # Analyse de chaque fichier sur la clé USB
        for device in usb_devices:
            print(f"Analyse de {device}...")
            mount_path = f"/mnt/{device}"
            os.makedirs(mount_path, exist_ok=True)

            # Montage du périphérique USB
            subprocess.run(["sudo", "mount", f"/dev/{device}", mount_path])

            # Nettoyage de chaque fichier
            for root, dirs, files in os.walk(mount_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file_path)[1].lower()

                    # Vérification de l'extension pour les fichiers exécutables
                    if file_ext in FILTER_EXTS:
                        # Modification des permissions pour empêcher l'exécution
                        os.chmod(file_path, 0o644)
                        if not clean_file(file_path):
                            # Fichier infecté, indiquer l'erreur et passer au suivant
                            continue

                    # Vérification de la signature pour les fichiers PDF
                    if file_ext == ".pdf":
                        result = subprocess.run(["pdfid.py", file_path], capture_output=True, text=True)
                        if "JS" in result.stdout:
                            print(f"{file_path} contient un script malveillant !")
                            continue

                    # Copie des fichiers non infectés sur la clé USB saine
                    shutil.copy2(file_path, USB_DEST)

            # Démontage du périphérique USB
            subprocess.run(["sudo", "umount", mount_path])
            os.rmdir(mount_path)

        print("Tous les périphériques USB ont été analysés.")
        break

# Exécution du script
if __name__ == "__main__":
    clean_usb()
