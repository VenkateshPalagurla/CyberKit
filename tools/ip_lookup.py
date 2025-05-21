import sys
import requests
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
    IP Address Geolocation & Info Lookup
    """ + Style.RESET_ALL)

def get_ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(Fore.RED + f"[!] Request error: {e}")
        return None

def print_ip_info(data):
    print(Fore.GREEN + "\n[!] IP Information\n")
    def print_kv(key, val):
        if val:
            print(f"{Fore.YELLOW}{key:<12}:{Style.RESET_ALL} {val}")
    
    print_kv("IP", data.get("ip"))
    print_kv("Hostname", data.get("hostname"))
    print_kv("City", data.get("city"))
    print_kv("Region", data.get("region"))
    print_kv("Country", data.get("country"))
    print_kv("Location", data.get("loc"))
    print_kv("Organization", data.get("org"))
    print_kv("Postal", data.get("postal"))
    print_kv("Timezone", data.get("timezone"))

    # ASN Info if available
    if "asn" in data:
        asn = data["asn"]
        print(Fore.MAGENTA + "\n[!] ASN Info")
        print_kv("ASN", asn.get("asn"))
        print_kv("Name", asn.get("name"))
        print_kv("Route", asn.get("route"))
        print_kv("Domain", asn.get("domain"))
        print_kv("Country", asn.get("country"))

def main():
    banner()
    if len(sys.argv) != 2:
        print(Fore.YELLOW + f"Usage: python3 {sys.argv[0]} <ip_address>")
        print(Fore.YELLOW + "Example: python3 ip_lookup.py 8.8.8.8")
        sys.exit(1)
    
    ip = sys.argv[1].strip()
    data = get_ip_info(ip)
    if data:
        print_ip_info(data)
    else:
        print(Fore.RED + "[!] Failed to retrieve IP info.")

if __name__ == "__main__":
    main()
