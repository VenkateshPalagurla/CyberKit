import requests
from bs4 import BeautifulSoup
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(Fore.CYAN + r"""
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
        OSINT Username Scanner
    """ + Style.RESET_ALL)

def check_github(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(Fore.GREEN + "[+] GitHub Found!")
        print(f"    Profile  : {data['html_url']}")
        print(f"    Name     : {data.get('name')}")
        print(f"    Bio      : {data.get('bio')}")
        print(f"    Public Repos : {data.get('public_repos')}")
        print(f"    Followers    : {data.get('followers')}")
    else:
        print(Fore.RED + "[-] GitHub Not Found")

def check_instagram(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and "content" in response.text:
        print(Fore.GREEN + "[+] Instagram Found!")
        print(f"    Profile : {url}")
    else:
        print(Fore.RED + "[-] Instagram Not Found")

def check_twitter(username):
    url = f"https://twitter.com/{username}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(Fore.GREEN + "[+] Twitter Found!")
        print(f"    Profile : {url}")
    else:
        print(Fore.RED + "[-] Twitter Not Found")

def main():
    banner()
    if len(sys.argv) != 2:
        print(Fore.YELLOW + f"Usage: python3 {sys.argv[0]} <username>")
        sys.exit(1)

    username = sys.argv[1]
    print(Fore.BLUE + f"\n[~] Scanning username: {username}\n")
    time.sleep(1)

    check_github(username)
    time.sleep(0.5)
    check_instagram(username)
    time.sleep(0.5)
    check_twitter(username)

if __name__ == "__main__":
    main()
