import requests
import sys
from colorama import Fore, Style, init
import time

init(autoreset=True)

API_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"
# Masukkan API key HIBP kamu di sini (daftar gratis di https://haveibeenpwned.com/API/Key)
API_KEY = ""  # Isi dengan API key mu jika ada

HEADERS = {
    "User-Agent": "F01C - OSINT Email Leak Checker",
    "hibp-api-key": API_KEY,
    "Accept": "application/json"
}

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
    Email Leak Checker - Have I Been Pwned API
    """ + Style.RESET_ALL)

def check_email_leak(email):
    print(Fore.BLUE + f"[~] Checking breaches for: {email}\n")
    url = API_URL + email
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            breaches = response.json()
            print(Fore.GREEN + f"[!] Found {len(breaches)} breach(es) for {email}!\n")
            for b in breaches:
                print(Fore.YELLOW + f"== Breach: {b['Title']} ==")
                print(f"Domain      : {b['Domain']}")
                print(f"Breach date : {b['BreachDate']}")
                print(f"PwnCount    : {b['PwnCount']:,}")
                print(f"Description : {b['Description'][:200].replace('<br>', ' ').replace('&quot;', '\"')}...")
                print(f"Data leaked : {', '.join(b['DataClasses'])}")
                print("-" * 50)
        elif response.status_code == 404:
            print(Fore.GREEN + f"[+] Good news — no breaches found for {email}!")
        elif response.status_code == 401:
            print(Fore.RED + "[!] Unauthorized — check your API key!")
        elif response.status_code == 429:
            print(Fore.RED + "[!] Rate limit exceeded — slow down!")
        else:
            print(Fore.RED + f"[!] Unexpected error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] Request failed: {e}")

def main():
    banner()
    if len(sys.argv) != 2:
        print(Fore.YELLOW + f"Usage: python3 {sys.argv[0]} <email>")
        sys.exit(1)

    email = sys.argv[1].strip()
    if "@" not in email:
        print(Fore.RED + "[!] Invalid email address format.")
        sys.exit(1)

    check_email_leak(email)

if __name__ == "__main__":
    main()
