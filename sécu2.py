import os
import sys
import time
import glob
import subprocess
import psutil
import shutil
from tqdm import tqdm

def analyze_usb():
    # Search for all connected USB drives
    devices = psutil.disk_partitions()
    devices = [device for device in devices if device.fstype == 'vfat']
    if not devices:
        print("No USB drive is connected.")
        sys.exit()
        
    print("Connected USB drives:")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device.mountpoint} ({device.device})")
    print("")

    # Select the USB drive to analyze
    selected_device = int(input("Choose the USB drive to analyze (enter the number): ")) - 1
    selected_device = devices[selected_device].device
    print(f"The selected drive for analysis is: {selected_device}")

    # Choose the destination USB drive
    destination_device = int(input("Choose the destination USB drive (enter the number): ")) - 1
    destination_device = devices[destination_device].device
    print(f"The selected destination drive is: {destination_device}")

    # Ask if the report should be generated
    generate_report = input("Generate a detailed report (o/n): ").lower() == 'o'

    # Analyze the USB drive with ClamAV
    print("Analyzing the USB drive...")
    report = []
    for root, dirs, files in os.walk(selected_device):
        for file in tqdm(files, desc="Analyzing files"):
            src = os.path.join(root, file)
            # Check if the file is malicious
            result = subprocess.run(['clamscan', '-i', src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if "Infected files: 0" in result.stdout.decode('utf-8'):
                # Copy the non-malicious file
                dst = os.path.join(destination_device, os.path.relpath(src, selected_device))
                shutil.copy2(src, dst)

    # Save the report on the destination USB drive
    if generate_report:
        report_file = f"{selected_device.split('/')[-1]}_report.txt"
        report_file = os.path.join(destination_device, report_file)
        with open(report_file, 'w') as f:
            f.write('\n'.join(report))

    # Unmount the USB drives
    subprocess.run(['umount', selected_device])
    subprocess.run(['umount', destination_device])

if __name__ == '__main__':
    analyze_usb()