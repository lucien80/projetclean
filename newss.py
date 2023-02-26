import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Fonction pour analyser une clé USB avec ClamAV
def scan_usb(path, progress):
    result = subprocess.run(['clamscan', '-r', '--bell', path], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    progress['value'] = 100
    if 'Infected files: 0' in output:
        messagebox.showinfo('Résultat de l\'analyse', 'Aucun virus ou logiciel malveillant détecté.')
    else:
        messagebox.showwarning('Résultat de l\'analyse', 'Virus ou logiciel malveillant détecté!\n\n' + output)

# Fonction pour obtenir la liste des clés USB connectées
def get_usb_list():
    drives = []
    bitmask = subprocess.check_output(['lsblk', '-n', '-o', 'NAME,SIZE,TYPE']).decode('utf-8')
    lines = bitmask.split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) == 3 and parts[2] == 'part':
            drives.append(parts[0] + ' (' + parts[1] + ')')
    return drives

# Interface graphique pour choisir une clé USB et démarrer l'analyse
def main():
    root = tk.Tk()
    root.title('Analyseur de Clés USB')
    root.geometry('400x200')

    label = tk.Label(root, text='Sélectionnez une clé USB à analyser:')
    label.pack(pady=10)

    usb_list = get_usb_list()
    if not usb_list:
        messagebox.showerror('Erreur', 'Aucune clé USB connectée.')
        sys.exit(1)

    selected_usb = tk.StringVar()
    selected_usb.set(usb_list[0])
    dropdown = ttk.OptionMenu(root, selected_usb, *usb_list)
    dropdown.pack(pady=10)

    progress = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress.pack(pady=10)

    scan_button = tk.Button(root, text='Analyser', command=lambda: scan_usb('/dev/' + selected_usb.get().split()[0], progress))
    scan_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
