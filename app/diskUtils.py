import subprocess
from app.pwManager import getPw

def get_mounted_diskss():
    """Get a list of mounted disks."""
    output = subprocess.run(['mount'], capture_output=True, text=True)
    return [line.split()[0] for line in output.stdout.splitlines()]

def get_mounted_disks():
    """Get a list of all disks excluding 'sr0' and disks starting with 'sda'."""
    with open('/proc/mounts', 'r') as f:
        lines = f.readlines()
        all_disks = [line.split(" ")[0] for line in lines]
        return [disk for disk in all_disks]

def get_all_disks():
    """Get a list of all disks excluding 'sr0' and disks starting with 'sda'."""
    with open('/proc/partitions', 'r') as f:
        lines = f.readlines()[2:]  # Skip header lines
        all_disks = [line.split()[-1] for line in lines]
        all_disks_sizes = [line.split()[-2] for line in lines]
        disks = [[all_disks[i], all_disks_sizes[i]] for i in range(len(all_disks))]
        return [disk for disk in disks if 'sda' not in disk[0] and disk[0] != 'sr0' and disk[0] != "dm-0"]

def not_in(disk, mounted_disks):
    disks = [disk.split("/")[-1] for disk in mounted_disks]
    return disk[0] not in disks

def get_unmounted_disks():
    """Get a list of unmounted disks."""
    mounted_disks = get_mounted_disks()
    all_disks = get_all_disks()
    return [disk for disk in all_disks if not_in(disk,mounted_disks)]

def mount(disk, mount_path):
    """Mount a disk."""
    disk_path = f"/dev/{disk}"

    # Define the sudo command you want to execute
    sudo_command = "sudo mount " + disk_path + " " + mount_path
    # Define the password
    password = getPw()
    # Encode the password as bytes
    password_bytes = password.encode('utf-8')
    # Run the sudo command using subprocess
    process = subprocess.Popen(['sudo', '-S'] + sudo_command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=password_bytes)

def unmount(mount_path):
    """Unmount a disk."""
    # Define the sudo command you want to execute
    sudo_command = "sudo umount " + mount_path
    # Define the password
    password = getPw()

    # Encode the password as bytes
    password_bytes = password.encode('utf-8')
    # Run the sudo command using subprocess
    process = subprocess.Popen(['sudo', '-S'] + sudo_command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=password_bytes)

def get_disk_usage(mount_path):
        #return the usage and the total size of the disk in the given path
    try:
        # Run df command to get disk usage information
        df_output = subprocess.check_output(["df", "-BG", mount_path])
        
        # Split the output lines and extract the relevant information
        lines = df_output.decode().split('\n')
        if len(lines) > 1:
            # Extract total size and used size from the second line
            total_size_raw, used_size_raw = lines[1].split()[1:3]
            # Remove 'M' from sizes and convert to integers
            total_size = int(total_size_raw[:-1])
            used_size = int(used_size_raw[:-1])
            return total_size, used_size
        else:
            return None, None
    except subprocess.CalledProcessError:
        # Handle error if df command fails
        print("Error: Unable to get disk usage.")
        return None, None

def isMounted(mount_point):
    # Run the mount command
    result = subprocess.run(['mount'], capture_output=True, text=True)
    # Check if the command was successful
    if result.returncode == 0:
        # Split the output by lines and iterate through each line
        for line in result.stdout.split('\n'):
            # Check if the line contains the desired mount point
            if mount_point in line:
                line = line.strip()  # Return the line containing the mount point
                print("Disk exists")
                return True
    else:
        print("Error executing the command.")
    print("Disk does not exist")
    # Return None if the mount point is not found
    return False

