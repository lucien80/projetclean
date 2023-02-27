import os
import time
import sys

def menu():
    print("Sélectionnez l'option souhaitée :")
    print("1. Effacer complètement le disque dur")
    print("2. Formater le disque dur")
    print("3. Effacer et formater le disque dur")
    choice = int(input("Entrez votre choix : "))
    return choice

def erase_disk(disk):
    size = os.popen("lsblk -b | grep " + disk + " | awk '{print $4}'").read()
    size = int(size)
    blocks = size / 1024 / 1024
    print("Taille du disque : " + str(size / 1024 / 1024 / 1024) + " GB")
    print("Effacement en cours...")
    for i in range(int(blocks)):
        sys.stdout.write("\r%d%%" % (i / blocks * 100))
        sys.stdout.flush()
        with open(disk, "wb") as f:
            f.write(os.urandom(1024 * 1024))
    print("\nEffacement terminé")

def format_disk(disk):
    print("Formatage en cours...")
    os.system("mkfs.ext4 " + disk)
    print("Formatage terminé")

def main():
    print("Détection des disques durs...")
    disks = os.popen("lsblk -o NAME,TYPE | grep disk | awk '{print $1}'").read()
    disks = disks.splitlines()
    for i, disk in enumerate(disks):
        print(str(i + 1) + ". " + disk)
    disk_choice = int(input("Entrez le numéro du disque à effacer : "))
    disk = "/dev/" + disks[disk_choice - 1]
    choice = menu()
    if choice == 1:
        erase_disk(disk)
    elif choice == 2:
        format_disk(disk)
    else:
        erase_disk(disk)
        format_disk(disk)

if __name__ == "__main__":
    main()