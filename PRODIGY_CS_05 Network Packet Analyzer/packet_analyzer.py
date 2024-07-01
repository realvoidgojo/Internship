import scapy.all as scapy
import os

LOG_FILE = "net_packet_log.txt"

def is_admin():
    if os.name == 'nt':
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            print(f"\033[91mError checking admin status: {e}\033[0m")
            return False
    elif os.name == 'posix':
        return os.geteuid() == 0
    else:
        return False

def packet_callback(packet):
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        protocol_num = packet[scapy.IP].proto
        protocol = ''
        if protocol_num == 6:
            protocol = 'TCP'
        elif protocol_num == 17:
            protocol = 'UDP'

        log_message = f"\nSource IP: {src_ip} --> Destination IP: {dst_ip} | Protocol: {protocol} \n"
        print(log_message)

        if packet.haslayer(scapy.TCP):
            try:
                payload = packet[scapy.Raw].load if packet.haslayer(scapy.Raw) else b""
                log_message += f"\nTCP Payload : { str(payload) }\n"
            except Exception as e:
                log_message += f"\nError decoding TCP payload: {e}\n"
        
        elif packet.haslayer(scapy.UDP):
            try:
                payload = packet[scapy.Raw].load if packet.haslayer(scapy.Raw) else b""
                log_message += f"\nUDP Payload : { str(payload) }\n"
            except Exception as e:
                log_message += f"\nError decoding UDP payload: {e}\n"
               
        log_message += ( '='*80 )

        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_message)
        print("PAYLOAD data stored in net_packet_log.txt")

def start_sniffing():
    print("\033[92m[+] Starting packet sniffing...\033[0m")
    print("\033[92mStoring in Text file called 'net_packet_log.txt'  in current directory\033[0m")
    try:
        scapy.sniff(store=False, prn=packet_callback)
    except KeyboardInterrupt:
        print("\033[91m[+] Quitting...\033[0m")
    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")

ascii = """\033[91m
    ____  ___   ________ __ ____________   ___    _   _____    ____  _______   __________ 
   / __ \\/   | / ____/ //_// ____/_  __/  /   |  / | / /   |  / /\\ \\/ /__  /  / ____/ __ \\
  / /_/ / /| |/ /   / ,<  / __/   / /    / /| | /  |/ / /| | / /  \\  /  / /  / __/ / /_/ /
 / ____/ ___ / /___/ /| |/ /___  / /    / ___ |/ /|  / ___ |/ /___/ /  / /__/ /___/ _, _/ 
/_/   /_/  |_\\____/_/ |_/_____/ /_/    /_/  |_/_/ |_/_/  |_/_____/_/  /____/_____/_/ |_|  
                                                                                          
\033[0m"""
print(ascii)

if not is_admin():
    print("\033[91mThis script needs to be run as an admin on Windows or with root (sudo) privileges on Linux.\033[0m")
else:
    start_sniffing()
