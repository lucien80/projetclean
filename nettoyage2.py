import os
import shutil
import subprocess
import sys

# Chemin de la clé USB à scanner
usb_path = '/media/user/usb'

# Chemin de la clé USB de destination
dst_path = '/media/user/usb_clean'

# Liste des extensions de fichiers exécutables à filtrer
executable_extensions = ['.exe', '.bat', '.sh']

# Liste des extensions de fichiers PDF à vérifier
pdf_extensions = ['.pdf']

# Commande pour lancer ClamAV
clamav_cmd = ['clamscan', '-r', '--max-filesize=50M', '--exclude-dir=System Volume Information']

# Fonction pour afficher la progression du scan
def progress_callback(progress):
    sys.stdout.write('\r%d%%' % progress)
    sys.stdout.flush()

# Fonction pour filtrer les extensions de fichiers exécutables
def is_executable(filename):
    _, extension = os.path.splitext(filename)
    return extension.lower() in executable_extensions

# Fonction pour filtrer les extensions de fichiers PDF
def is_pdf(filename):
    _, extension = os.path.splitext(filename)
    return extension.lower() in pdf_extensions

# Création du dossier de destination
if not os.path.exists(dst_path):
    os.makedirs(dst_path)

# Scan de la clé USB avec ClamAV
print('Scanning USB...')
infected_files = []
total_files = 0
for dirpath, dirnames, filenames in os.walk(usb_path):
    for filename in filenames:
        total_files += 1
clamav_process = subprocess.Popen(clamav_cmd + [usb_path], stdout=subprocess.PIPE)
progress = 0
for line in iter(clamav_process.stdout.readline, b''):
    line = line.decode('utf-8').strip()
    if line.startswith(usb_path):
        if 'FOUND' in line:
            infected_files.append(line.split()[0])
        progress = int(clamav_process.stdout.tell() * 100 / total_files)
        progress_callback(progress)
clamav_process.stdout.close()
clamav_process.wait()
sys.stdout.write('\n')

# Nettoyage des fichiers infectés
print('Cleaning infected files...')
for filename in infected_files:
    print('Removing %s' % filename)
    os.remove(filename)

# Copie des fichiers non infectés dans la clé USB de destination
print('Copying clean files...')
for dirpath, dirnames, filenames in os.walk(usb_path):
    rel_dirpath = os.path.relpath(dirpath, usb_path)
    dst_dirpath = os.path.join(dst_path, rel_dirpath)
    for filename in filenames:
        src_path = os.path.join(dirpath, filename)
        dst_path = os.path.join(dst_dirpath, filename)
        if not os.path.exists(dst_dirpath):
            os.makedirs(dst_dirpath)
        if not is_executable(filename) and not is_pdf(filename):
            print('Copying %s' % src_path)
            shutil.copy2(src_path, dst_path)
        else:
            print('Skipping %s' % src_path)
