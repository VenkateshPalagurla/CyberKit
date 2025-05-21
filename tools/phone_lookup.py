import requests
import sys
from colorama import Fore, Style, init
import re

init(autoreset=True)

API_URL = "http://apilayer.net/api/validate"
API_KEY = ""  # Masukkan API key Numverify kamu di sini

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
    Phone Number HLR Lookup - Numverify API
    """ + Style.RESET_ALL)

def validate_phone(phone):
    # cek format nomor minimal + dan 7-15 digit angka
    pattern = re.compile(r"^\+\d{7,15}$")
    if not pattern.match(phone):
        return False
    return True

def lookup_phone(phone):
    params = {
        'access_key': API_KEY,
        'number': phone,
        'format': 1
    }
    print(Fore.BLUE + f"[~] Looking up phone number: {phone}\n")
    try:
        resp = requests.get(API_URL, params=params, timeout=15)
        data = resp.json()
        if resp.status_code != 200 or 'success' in data and not data['success']:
            print(Fore.RED + f"[!] API Error: {data.get('error', {}).get('info', 'Unknown error')}")
            return

        # Hasil validasi
        if not data.get('valid', False):
            print(Fore.YELLOW + "[!] Number is invalid or not recognized.")
            return

        print(Fore.GREEN + "[!] Phone Number Information:")
        print(f"  Number      : {data.get('number')}")
        print(f"  Local Format: {data.get('local_format')}")
        print(f"  International Format: {data.get('international_format')}")
        print(f"  Country Name: {data.get('country_name')}")
        print(f"  Country Code: {data.get('country_code')}")
        print(f"  Location    : {data.get('location') or 'N/A'}")
        print(f"  Carrier     : {data.get('carrier') or 'N/A'}")
        print(f"  Line Type   : {data.get('line_type') or 'N/A'}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] Request failed: {e}")

def main():
    banner()
    if len(sys.argv) != 2:
        print(Fore.YELLOW + f"Usage: python3 {sys.argv[0]} <phone_number>")
        print(Fore.YELLOW + "Example: python3 phone_lookup.py +6281234567890")
        sys.exit(1)

    phone = sys.argv[1].strip()
    if not validate_phone(phone):
        print(Fore.RED + "[!] Invalid phone number format. Use E.164 format, e.g., +6281234567890")
        sys.exit(1)

    lookup_phone(phone)

if __name__ == "__main__":
    main()
