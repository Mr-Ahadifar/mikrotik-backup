import paramiko
import os
from datetime import date
import subprocess

print("Please Wait a Moment ...")

username="Enter Username"
password="Enter Password"

today = date.today()
backup_dir = f'./Backup/{today.year}/{today.month:02d}/{today.day:02d}'

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def offline_device(ip_address):
    proc = subprocess.Popen(["ping", "-n", "2", "-4", ip_address], stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode()
    return "Request timed out" in output



with open('devices.txt') as f:
    for line in f:
        devices, port = line.strip().split(':')

        offline_devices = []

        for ip_address in devices.split(','): 
            if offline_device(ip_address):
                offline_devices.append(ip_address)
                ofline = (ip_address)

        if len(offline_devices) > 0:
            with open(f"{backup_dir}/Troubled_Devices.txt", 'a') as f: 
                f.write(f"\nOffline_Devices {ofline}\n")
        else:
            for ip_address in devices.split(','): 
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(ip_address,port,username,password)

                    stdin, stdout, stderr = client.exec_command('/export compact')
                    backup_text = stdout.read().decode()

                    stdin, stdout, stderr = client.exec_command(':put [ /system identity get name ]')
                    identity = stdout.read().decode().strip()
                    backup_filename = f'{identity}.rsc'

                    with open(f'{backup_dir}/{backup_filename}', 'w') as f:
                        f.write(backup_text)

                    client.close()
                except paramiko.ssh_exception.NoValidConnectionsError as e:
                    with open(f"{backup_dir}/Troubled_Devices.txt", 'a') as d: 
                        d.write(f"\nUnable to connect to port {port} on {ip_address}")
                    continue

                except Exception as e:
                    print(f"Error: {str(e)}")
                    continue

    with open(f"{backup_dir}/Troubled_Devices.txt", 'a') as d: 
        d.write(f"\n\n\n         --- Powerd by @Mr_AhadiFar ---")

    print("Backups Completed Successfully.")

    print(f"""

    --- Powerd by @Mr_AhadiFar ---
    """)

        


#   --- Powerd by @Mr_AhadiFar ---   #