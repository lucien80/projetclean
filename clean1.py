import os
import sys
import time
import glob
import subprocess
import shutil
import tqdm

def analyze_usb():
    # Find all connected USB drives
    devices = glob.glob('/dev/sd*')
    if not devices:
        print("No USB drive found.")
        sys.exit()
        
    print("Connected USB drives:")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device}")
    print("")

    # Select the USB drive to analyze
    selected_device = int(input("Choose the USB drive to analyze (enter the number): ")) - 1
    selected_device = devices[selected_device]

    # Mount the USB drive if it's not already mounted
    mount_point = '/media/' + selected_device.split('/')[-1]
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['mount', selected_device, mount_point])
    selected_device = mount_point

    # Choose the destination USB drive to copy the files to
    destination_device = int(input("Choose the destination USB drive (enter the number): ")) - 1
    destination_device = devices[destination_device]

    # Mount the destination USB drive if it's not already mounted
    mount_point = '/media/' + destination_device.split('/')[-1]
    os.makedirs(mount_point, exist_ok=True)
    subprocess.run(['mount', destination_device, mount_point])
    destination_device = mount_point

    # Ask if a detailed report should be generated
    generate_report = input("Generate a detailed report (y/n): ").lower() == 'y'

    # Ask if malicious files should be removed
    remove_malicious = input("Remove malicious files (y/n): ").lower() == 'y'

    # Analyze the USB drive with ClamAV
    clamscan_command = ['clamscan', '-r', selected_device]
    if remove_malicious:
        clamscan_command.append('--remove')
    print(f"Analyzing USB drive {selected_device}...")
    report = []
    process = subprocess.Popen(clamscan_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            if generate_report:
                report.append(output.strip())
        time.sleep(0.1)
    print("Analysis complete.")

    # Copy the non-malicious files to the destination USB drive
    for dirpath, dirnames, filenames in os.walk(selected_device):
        for filename in filenames:
            src = os.path.join(dirpath, filename)
            dst = os.path.join(destination_device, os.path.relpath(src, selected_device))
            # Check if the file
            result = subprocess.run(['clamscan', '-i', src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if "Infected files: 0" in result.stdout.decode('utf-8'):
                # Copy the non-malicious file
                shutil.copy2(src, dst)
                file_size = os.path.getsize(src)
                with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc=os.path.basename(src)) as pbar:
                    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                        while True:
                            buf = fsrc.read(4096)
                            if not buf:
                                break
                            fdst.write(buf)
                            pbar.update(len(buf))
                
    # Save the report on the destination USB drive
    if generate_report:
        report_file = f"{selected_device.split('/')[-1]}_report.txt"
        report_file = os.path.join(destination_device, report_file)
        with open(report_file, 'w') as f:
            f.write('\n'.join(report))

def unmount_devices(devices):
    for device in devices:
        mount_point = '/media/' + device.split('/')[-1]
        subprocess.run(['umount', mount_point])
        print(f"USB drive {device} has been unmounted.")

def update_clamav_database():
    print("Updating ClamAV database...")
    result = subprocess.run(['freshclam'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode('utf-8'))
    print("ClamAV database updated.")

if __name__ == '__main__':
    devices = glob.glob('/dev/sd*')
    analyze_usb()
    unmount_devices(devices)
    update_clamav_database()
    print("All USB drives have been successfully unmounted.")
