import os
import sys
import time
import math

def clear():
    os.system('clear' if os.name=='posix' else 'cls')

def progress_bar(percent, width=50):
    left = math.floor(width * percent)
    right = width - left
    print('\r[' + '#' * left + ' ' * right + '] {:.2%}'.format(percent), end='')

def main():
    print("Détection des disques durs et des clés USB...")

    # Liste de tous les disques durs et clés USB connectés
    drives = []
    for drive in os.listdir('/dev'):
        if 'sd' in drive or 'mmcblk' in drive:
            drives.append('/dev/' + drive)

    if len(drives) == 0:
        print("Aucun disque dur ou clé USB détecté.")
        return

    while True:
        clear()
        print("Sélectionnez le disque dur ou la clé USB à effacer:")
        for i, drive in enumerate(drives):
            print("{}) {}".format(i+1, drive))

        choice = input("Entrez le numéro de disque dur ou clé USB à effacer, ou 'q' pour quitter: ")

        if choice == 'q':
            break

        try:
            choice = int(choice)
            if choice < 1 or choice > len(drives):
                raise ValueError
        except ValueError:
            print("Valeur invalide. Veuillez sélectionner un disque dur ou une clé USB valide.")
            time.sleep(2)
            continue

        drive = drives[choice - 1]

        print("Effacement du disque dur ou de la clé USB: {}".format(drive))
        print("Taille du disque dur ou de la clé USB: {:.2f} Go".format(os.path.getsize(drive) / 1024**3))

        confirmation = input("Êtes-vous sûr de vouloir effacer ce disque dur ou cette clé USB ? (y/n): ")

        if confirmation != 'y':
            print("Opération annulée.")
            time.sleep(2)
            continue

        # Effacement du disque dur ou de la clé USB
        print("Effacement en cours...")
        start_time = time.time()

        with open(drive, 'wb') as f:
            total_size = os.path.getsize(drive)
            bytes_written = 0
            chunk_size = 1024 * 1024 * 10  # Écrire 10 Mo à la fois

            while True:
                chunk = b'\x00' * chunk_size
                f.write(chunk)
                bytes_written += chunk_size

                if bytes_written >= total_size:
                    break

                progress_bar(bytes_written / total_size)

        print("\nEffacement terminé en {:.2f} secondes.".format(time.time() - start_time))
        time.sleep(2)

if __name__ == "__main__":
    main()