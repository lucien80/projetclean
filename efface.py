import os
import sys
import time
import platform

def clear_disk(disk_path, rewrite_with_zeros):
    disk_size = os.path.getsize(disk_path)
    block_size = 1024 * 1024
    blocks = disk_size // block_size
    blocks_written = 0

    if rewrite_with_zeros:
        with open(disk_path, 'wb') as f:
            while blocks_written < blocks:
                f.write(b'\x00' * block_size)
                blocks_written += 1
                progress = int(blocks_written / blocks * 100)
                print(f'\rProgress: {progress}%', end='')
    else:
        with open(disk_path, 'wb') as f:
            while blocks_written < blocks:
                f.write(os.urandom(block_size))
                blocks_written += 1
                progress = int(blocks_written / blocks * 100)
                print(f'\rProgress: {progress}%', end='')
    print('\nDisk cleared successfully!')

def format_disk(disk_path):
    if platform.system() == 'Linux':
        os.system(f'sudo mkfs.ext4 {disk_path}')
        print(f'Disk at {disk_path} formatted successfully!')
    else:
        print(f'Formatting is not supported on {platform.system()}')

def main():
    print('Select an option:')
    print('1. Clear disk with zeros')
    print('2. Clear disk with random data')
    print('3. Format disk')
    print('4. Clear and format disk')
    option = int(input('Enter your choice: '))

    print('Detected disks:')
    disks = ['/dev/sda', '/dev/sdb', '/dev/sdc']
    for i, disk in enumerate(disks):
        print(f'{i + 1}. {disk}')
    disk_index = int(input('Select a disk: ')) - 1

    disk_path = disks[disk_index]
    print(f'Selected disk: {disk_path}')

    if option == 1:
        clear_disk(disk_path, True)
    elif option == 2:
        clear_disk(disk_path, False)
    elif option == 3:
        format_disk(disk_path)
    elif option == 4:
        clear_disk(disk_path, True)
        format_disk(disk_path)

if __name__ == '__main__':
    main()