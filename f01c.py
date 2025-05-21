#!/usr/bin/env python3

import os

def banner():
    print("""
╔════════════════════════════════════╗
║        F01C - Cyber Toolkit        ║
║     For OSINT, Recon, and Scan     ║
╚════════════════════════════════════╝
""")

def menu():
    print("""
[1] OSINT - Cek Username
[2] Email Leak Checker
[3] Phone HLR Lookup
[4] IP Address Info
[5] Domain Whois Info
[6] Port Scanner
[0] Exit
""")

def main():
    banner()
    while True:
        menu()
        choice = input("Pilih opsi > ")

        if choice == '1':
            os.system("python3 tools/osint.py")
        elif choice == '2':
            os.system("python3 tools/email_leak.py")
        elif choice == '3':
            os.system("python3 tools/phone_lookup.py")
        elif choice == '4':
            os.system("python3 tools/ip_lookup.py")
        elif choice == '5':
            os.system("python3 tools/domain_info.py")
        elif choice == '6':
            os.system("python3 tools/port_scan.py")
        elif choice == '0':
            print("Keluar...")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
