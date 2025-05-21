import sys
import socket
import concurrent.futures
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + """
   +--------------+
   |.------------.|
   ||            ||
   ||            ||
   ||            ||
   ||            ||
   |+------------+|
   +-..--------..-+
   .--------------.
  / /============\ \
 / /==============\ \
/____________________\
\____________________/
   TCP Port Scanner - Fast & Reliable
    """ + Style.RESET_ALL)

def scan_port(target, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            return port, (result == 0)  # True if open
    except Exception as e:
        return port, False

def parse_ports(port_str):
    ports = set()
    for part in port_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.update(range(int(start), int(end)+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def main():
    banner()
    if len(sys.argv) != 3:
        print(Fore.YELLOW + f"Usage: python3 {sys.argv[0]} <target> <ports>")
        print(Fore.YELLOW + "Example:")
        print(Fore.YELLOW + "  python3 port_scanner.py 192.168.1.1 22,80,443")
        print(Fore.YELLOW + "  python3 port_scanner.py scanme.nmap.org 1-1024")
        sys.exit(1)

    target = sys.argv[1]
    ports_input = sys.argv[2]

    try:
        ports = parse_ports(ports_input)
    except Exception:
        print(Fore.RED + "[!] Invalid port format. Use comma-separated ports or ranges, e.g. 22,80,443 or 1-1024")
        sys.exit(1)

    print(Fore.GREEN + f"\n[+] Starting scan on target: {target}")
    print(Fore.GREEN + f"[+] Ports to scan: {ports_input}\n")

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(Fore.GREEN + f"[OPEN] Port {port}")
                open_ports.append(port)
            else:
                print(Fore.RED + f"[CLOSED] Port {port}")

    print(Fore.CYAN + "\nScan completed.")
    if open_ports:
        print(Fore.GREEN + f"Open ports: {', '.join(str(p) for p in open_ports)}")
    else:
        print(Fore.YELLOW + "No open ports found.")

if __name__ == "__main__":
    main()
