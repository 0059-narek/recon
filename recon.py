import os
import subprocess
import sys
import time

# color
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[0m"

# 0059 RECON 
def show_banner():
    os.system('clear')
    banner = f"""{B}
  ██████   ██████  ███████  █████      ██████  ███████  ██████  ██████  ███    ██ 
 ███  ███ ███  ███ ██      ██   ██     ██   ██ ██      ██      ██    ██ ████   ██ 
 ███  ███ ███  ███ ███████  ██████     ██████  █████   ██      ██    ██ ██ ██  ██ 
 ███  ███ ███  ███      ██      ██     ██   ██ ██      ██      ██    ██ ██  ██ ██ 
  ██████   ██████  ███████      ██     ██   ██ ███████  ██████  ██████  ██   ████ 
                                                                                  
                          {Y}v1.0 - Created by Narek0059{C}
    """
    print(banner)

show_banner()

def run_silent(command, description):
    print(f"{Y}[*] {description}...{C}", end="\r")
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{G}[+] {description} DONE!    {C}")

# help text
help_message = """
Usage: python3 recon.py -d <domain>

Options:
  -d    Target domain (e.g., google.com)
  -h    Show this help message
"""
# file
subfinder = "subfinder.txt"
assetfinder = "assetfinder.txt"
sublist3r = "sublist3r.txt"

if "-d" not in sys.argv or len(sys.argv) < 3:
    print("[!] Error: Missing target domain.")
    print(help_message)
    sys.exit()

if "-h" in sys.argv:
	print(f"{help_message}")
	sys.exit()

target = sys.argv[2]

# file subfinder
if os.path.exists(subfinder):
	pat = input(f"File subfinder.txt already exists. Use it? (y/n): ")
	if pat.lower() == "y":
		print("Continuing with existing file.")
	else:
		subfinder = input("Enter a new filename for results (e.g., custom.txt): ")
		print(f"Continuing recon with file:")

# subfinder
subfinderr = f"subfinder -d {target} -all -recursive > {subfinder}"
run_silent(subfinderr, "Running Subfinder enumeration")

# file Assetfinder
if os.path.exists(assetfinder):
	pat = input(f"{assetfinder} File already exists. Continue using it? (y/n): ")
	if pat.lower() == "y":
		print("Continuing...")
	else:
		assetfinder = input("Enter filename in .txt format: ")


# assetfinder
assetfinderr = f"assetfinder -subs-only {target} > {assetfinder}"
run_silent(assetfinderr, "Running Assetfinder enumeration")

# file sublist3r
if os.path.exists(sublist3r):
	pat = input(f"{sublist3r} File already exists. Continue using it? (y/n): ")
	if pat.lower() == "y":
		print("Continuing...")
	else:
		sublist3r = input("Enter filename in .txt format: ")

# sublist3r
sublist3rr = f"sublist3r -d {target} > {sublist3r}"
run_silent(sublist3rr, "Running Sublist3r enumeration")

# sort
sort = f"cat {subfinder} {assetfinder} {sublist3r} | sort -u > sort.txt"
run_silent(sort, "Merging and sorting subdomains")

# del
os.remove(subfinder)
os.remove(assetfinder)
os.remove(sublist3r)

# httpx 
httpx = f"cat sort.txt | httpx -sc -title -td -t 20 -o live.txt"
run_silent(httpx, "Checking live domains with HTTPX")

# sort
cat200 = f"""cat live.txt | cut -d ' ' -f1 | grep "20" > 2xx.txt"""
cat300 = f"""cat live.txt | cut -d ' ' -f1 | grep "30" > 3xx.txt"""
cat400 = f"""cat live.txt | cut -d ' ' -f1 | grep "40" > 4xx.txt"""
cat500 = f"""cat live.txt | cut -d ' ' -f1 | grep "50" > 5xx.txt"""

run_silent(cat200, "Filtering 2xx status codes")
run_silent(cat300, "Filtering 3xx status codes")
run_silent(cat400, "Filtering 4xx status codes")
run_silent(cat500, "Filtering 5xx status codes")




print(f"[!] Recon complete! Results are sorted. Run 'ls' to see the files.")
