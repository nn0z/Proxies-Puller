# Proxies Puller
import concurrent.futures
import socket
import requests
import sys
import os

PROXY_SOURCES = {
    "http": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http/data.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-list/master/proxies.txt",
        "https://raw.githubusercontent.com/roosterkid/open-proxies/main/HTTPS_RAW.txt",
        "https://api.openproxylist.xyz/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxyscan.io/download?type=http",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1220/Free-Proxy-List/main/http.txt",
        "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt"
    ],
    "socks4": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/roosterkid/open-proxies/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks4/data.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://www.proxyscan.io/download?type=socks4",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks4.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1220/Free-Proxy-List/main/socks4.txt"
    ],
    "socks5": [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks5/data.txt",
        "https://raw.githubusercontent.com/roosterkid/open-proxies/main/SOCKS5_RAW.txt",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://www.proxyscan.io/download?type=socks5",
        "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/socks5.txt",
        "https://raw.githubusercontent.com/Anonym0usWork1220/Free-Proxy-List/main/socks5.txt"
    ]
}

TIMEOUT_SEC = 2

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def banner():
    asc_banner = r"""
    ██████╗  ██╗   ██╗ ██╗      ██╗      ███████╗ ██████╗ 
    ██╔══██╗ ██║   ██║ ██║      ██║      ██╔════╝ ██╔══██╗
    ██████╔╝ ██║   ██║ ██║      ██║      █████╗   ██████╔╝
    ██╔═══╝  ██║   ██║ ██║      ██║      ██╔══╝   ██╔══██╗
    ██║      ╚██████╔╝ ███████╗ ███████╗ ███████╗ ██║  ██║
    ╚═╝       ╚═════╝  ╚══════╝ ╚══════╝ ╚══════╝ ╚═╝  ╚═╝
             [ Advanced Proxies Puller Tool ]
    """
    print("\033[1;35m" + asc_banner + "\033[0m")
    print("\033[1;30m" + "=" * 65 + "\033[0m")

def fetch_source(url):
    try:
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            return [l.strip() for l in res.text.splitlines() if ":" in l]
    except:
        pass
    return []

def get_proxies(selected_types):
    print(f"{Colors.BLUE}[*] Fetching proxies from expanded sources...{Colors.ENDC}")
    urls = []
    for t in selected_types:
        if t in PROXY_SOURCES:
            urls.extend(PROXY_SOURCES[t])

    all_proxies = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = executor.map(fetch_source, urls)
        for p_list in results:
            all_proxies.update(p_list)

    print(f"{Colors.GREEN}[+] Total Unique Proxies Collected: {len(all_proxies)}{Colors.ENDC}")
    return list(all_proxies)

def test_proxy(proxy):
    try:
        ip, port = proxy.split(":")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT_SEC)
        res = s.connect_ex((ip, int(port)))
        s.close()
        if res == 0:
            return proxy
    except:
        pass
    return None

def check_proxies(proxies):
    print(f"{Colors.WARNING}[*] Testing proxies in real-time...{Colors.ENDC}")
    valid = []
    total = len(proxies)
    checked = 0
    working_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
        futures = {executor.submit(test_proxy, p): p for p in proxies}
        for future in concurrent.futures.as_completed(futures):
            checked += 1
            res = future.result()
            if res:
                working_count += 1
                valid.append(res)

            sys.stdout.write(
                f"\r{Colors.CYAN}[Checking: {checked}/{total}] {Colors.GREEN}[Working Found: {working_count}]{Colors.ENDC}   ")
            sys.stdout.flush()

    print("\n")
    return valid

if __name__ == "__main__":
    banner()
    print(f"{Colors.BOLD}{Colors.HEADER}┌────────────────────────────────────────┐{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}│{Colors.ENDC} {Colors.CYAN}Select Proxy Type:{Colors.ENDC}                     {Colors.BOLD}{Colors.HEADER}│{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}├────────────────────────────────────────┤{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}│{Colors.ENDC} {Colors.GREEN}[1]{Colors.ENDC} HTTP                               {Colors.BOLD}{Colors.HEADER}│{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}│{Colors.ENDC} {Colors.GREEN}[2]{Colors.ENDC} SOCKS4                             {Colors.BOLD}{Colors.HEADER}│{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}│{Colors.ENDC} {Colors.GREEN}[3]{Colors.ENDC} SOCKS5                             {Colors.BOLD}{Colors.HEADER}│{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}│{Colors.ENDC} {Colors.GREEN}[4]{Colors.ENDC} All Protocols                      {Colors.BOLD}{Colors.HEADER}│{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}└────────────────────────────────────────┘{Colors.ENDC}")

    choice = input(f"{Colors.BLUE}┌──({Colors.ENDC}{Colors.GREEN}Puller{Colors.ENDC}{Colors.BLUE})-[{Colors.ENDC}{Colors.CYAN}Select{Colors.ENDC}{Colors.BLUE}]\n└─$ {Colors.ENDC}").strip()

    mapping = {"1": ["http"], "2": ["socks4"], "3": ["socks5"], "4": ["http", "socks4", "socks5"]}
    selected = mapping.get(choice, ["http", "socks4", "socks5"])

    proxies = get_proxies(selected)

    if not proxies:
        print(f"{Colors.FAIL}[-] No proxies found.{Colors.ENDC}")
    else:
        working = check_proxies(proxies)
        print(f"{Colors.GREEN}[+] Scan Complete! Total Working Proxies Found: {len(working)}{Colors.ENDC}")

        if working:
            filename = input(f"{Colors.BLUE}Enter output filename : {Colors.ENDC}").strip()
            if not filename:
                filename = "proxies.txt"

            existing_proxies = set()
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    existing_proxies = set(line.strip() for line in f if line.strip())

            total_before_dedup = len(existing_proxies) + len(working)
            total_combined = existing_proxies.union(set(working))
            duplicates_removed = total_before_dedup - len(total_combined)

            with open(filename, "w") as f:
                for p in sorted(total_combined):
                    f.write(f"{p}\n")

            print(
                f"{Colors.BOLD}[*] Successfully merged and saved proxies into: {filename} (Total proxies inside file: {len(total_combined)}){Colors.ENDC}")
            print(f"{Colors.WARNING}[*] Duplicates removed : {duplicates_removed}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}[-] No active proxies found at this moment .{Colors.ENDC}")
