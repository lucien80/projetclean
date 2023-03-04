import os
import subprocess

def unmount_and_remove(mount_point):
    subprocess.call(["umount", mount_point])
    os.rmdir(mount_point)

def main():
    media_dir = "/media/"
    for item in os.listdir(media_dir):
        if item.startswith("sd"):
            mount_point = os.path.join(media_dir, item)
            unmount_and_remove(mount_point)
    print("Démontage et suppression des points de montage USB terminés.")

if __name__ == "__main__":
    main()