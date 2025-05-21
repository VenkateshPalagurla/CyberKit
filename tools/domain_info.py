import whois
import sys
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
    Domain WHOIS Info Lookup
    """ + Style.RESET_ALL)

def print_whois_info(domain, data):
    print(Fore.GREEN + f"\n[!] WHOIS Information for: {domain}\n")
    
    def safe_print(key, value):
        if value:
            if isinstance(value, list):
                value = ', '.join(map(str, value))
            print(f"{Fore.YELLOW}{key:<20}:{Style.RESET_ALL} {value}")

    safe_print("Registrar", data.registrar)
    safe_print("Registrant", getattr(data, 'name', None) or getattr(data, 'org', None))
    safe_print("Registrar Email", getattr(data, 'emails', None))
    safe_print("Creation Date", data.creation_date)
    safe_print("Expiration Date", data.expiration_date)
    safe_print("Updated Date", data.updated_date)
    safe_print("Status", data.status)
    safe_print("Nameservers", data.name_servers)
    safe_print("DNSSEC", data.dnssec)

def main():
    banner()
    if len(sys.argv) != 2:
        print(Fore.YELLOW + f"Usage: python3 {sys.argv[0]} <domain>")
        print(Fore.YELLOW + "Example: python3 domain_info.py google.com")
        sys.exit(1)
    
    domain = sys.argv[1].strip()
    try:
        w = whois.whois(domain)
        if not w.domain_name:
            print(Fore.RED + f"[!] No WHOIS data found for {domain}. Possibly invalid domain.")
            sys.exit(1)
        print_whois_info(domain, w)
    except Exception as e:
        print(Fore.RED + f"[!] Error fetching WHOIS data: {e}")

if __name__ == "__main__":
    main()
