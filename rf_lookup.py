import re
import glob
import sys
import os
import subprocess
import time
import json
import signal
import random
import socks
import socket
from datetime import datetime, timezone, timedelta
import dns.resolver
import requests
import platform
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from rich.console import Console
from rich.padding import Padding

console = Console()

def extract_online_domains_from_cti():
    """Extract domains marked as ONLINE from deepdarkCTI files."""
    cti_files = [
        "deepdarkCTI/markets.md",
        "deepdarkCTI/forum.md", 
        "deepdarkCTI/ransomware_gang.md"
    ]
    
    online_domains = []
    onion_sites = []
    
    for file_path in cti_files:
        if not os.path.exists(file_path):
            console.print(Padding(f"[yellow]→ CTI file not found: {file_path}[/yellow]", (0, 0, 0, 4)))
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content into lines and process each line
            lines = content.split('\n')
            
            for line in lines:
                # Skip header lines and empty lines
                if not line.strip() or line.startswith('|Name|') or line.startswith('| ------ |'):
                    continue
                
                # Extract domains from markdown table format
                # Pattern: |[Name](URL)| STATUS | Description |
                match = re.search(r'\|\[.*?\]\((https?://[^)]+)\)\|\s*ONLINE\s*\|', line)
                if match:
                    url = match.group(1)
                    # Extract domain from URL
                    domain_match = re.search(r'https?://([^/]+)', url)
                    if domain_match:
                        domain = domain_match.group(1)
                        # Remove port numbers if present
                        domain = domain.split(':')[0]
                        
                        if domain.endswith('.onion'):
                            onion_sites.append(domain)
                        else:
                            online_domains.append(domain)
                
                # Also check for onion domains in different formats
                onion_match = re.search(r'\|\[.*?\]\((http://[^)]+\.onion[^)]*)\)\|\s*ONLINE\s*\|', line)
                if onion_match:
                    onion_url = onion_match.group(1)
                    onion_domain = re.search(r'http://([^/]+)', onion_url)
                    if onion_domain:
                        domain = onion_domain.group(1)
                        onion_sites.append(domain)
            
            console.print(Padding(f"[green]→ Processed {file_path}: {len([d for d in online_domains if not d.endswith('.onion')])} clearnet domains, {len([d for d in online_domains + onion_sites if d.endswith('.onion')])} onion sites[/green]", (0, 0, 0, 4)))
            
        except Exception as e:
            console.print(Padding(f"[red]→ Error processing {file_path}: {e}[/red]", (0, 0, 0, 4)))
    
    # Remove duplicates while preserving order
    online_domains = list(dict.fromkeys(online_domains))
    onion_sites = list(dict.fromkeys(onion_sites))
    
    console.print(Padding(f"[bold green]→ Total extracted: {len(online_domains)} clearnet domains, {len(onion_sites)} onion sites[/bold green]", (0, 0, 0, 4)))
    
    return online_domains, onion_sites

def watchdog_update():
    """Checks for updates from GitHub and asks for confirmation before applying."""
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    python_executable = sys.executable
    script_path = os.path.abspath(__file__)

    try:
        # Return changes from remote without applying them yet
        subprocess.run(
            ["git", "-C", repo_dir, "fetch", "origin", "main"],
            capture_output=True, text=True
        )

        # Check if updates are available
        diff_result = subprocess.run(
            ["git", "-C", repo_dir, "diff", "HEAD..origin/main"],
            capture_output=True, text=True
        )

        if not diff_result.stdout:
            console.print("")
            console.print(Padding("[bold green]→ No updates found. Running the script normally...[/bold green]", (0, 0, 0, 4)))
            return

        # Show changes before updating
        console.print("")
        console.print(Padding("[bold yellow]→ Updates are available! Here are the changes:[/bold yellow]", (0, 0, 0, 4)))
        console.print(Padding(diff_result.stdout, (0, 0, 0, 4)))

        # Confirm first
        user_input = input("\n[?] Apply these updates? (y/n): ").strip().lower()
        if user_input != "y":
            console.print("")
            console.print(Padding("[bold cyan]→ Update skipped. Running the current version.[/bold cyan]", (0, 0, 0, 4)))
            return

        # Apply the update
        update_result = subprocess.run(
            ["git", "-C", repo_dir, "pull", "origin", "main"],
            capture_output=True, text=True
        )

        console.print("")
        console.print(Padding("[bold yellow]→ Update applied! Restarting script in 3 seconds...[/bold yellow]", (0, 0, 0, 4)))
        time.sleep(3)

        # Restart the script
        subprocess.Popen([python_executable, script_path] + sys.argv[1:])
        sys.exit(0)

    except Exception as e:
        console.print("")
        console.print(Padding(f"[bold red]→ Couldn't update from GitHub. Error: {e}[/bold red]", (0, 0, 0, 4)))

# Run auto-update first
watchdog_update()

def clear_screen():
    try:
        time.sleep(3)
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
    except KeyboardInterrupt:
        console.print("")
        console.print(Padding("[bold red]\n[!] Script interrupted by user. Exiting cleanly...[/bold red]", (0, 0, 0, 4)))
        sys.exit(0)

load_dotenv()

clear_screen()

ascii_banner = r"""
██████╗ ███████╗    ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗██╔════╝    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
██████╔╝█████╗      ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
██╔══██╗██╔══╝      ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ 
██║  ██║██╗         ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     
╚═╝  ╚═╝╚═╝         ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                                        
    🔍  ╭─────────────────────────────────────────╮  🔍
    🔍  │  RF-Lookup: Advanced Domain Monitoring  │  🔍
    🔍  │  Detecting seizures before they happen  │  🔍
    🔍  │  Monitoring DNS changes & onion sites   │  🔍
    🔍  ╰─────────────────────────────────────────╯  🔍
                                                                        
[bold blue]RF-Lookup v1.0.0 by [link=https://ransomfeed.it]Ransomfeed Team[/link][/bold blue]
"""

console.print(Padding(f"[bold blue]{ascii_banner}[/bold blue]", (0, 0, 0, 4)))

# Extract domains from CTI files
console.print(Padding("[bold cyan]→ Extracting domains from deepdarkCTI files...[/bold cyan]", (0, 0, 0, 4)))
cti_domains, cti_onion_sites = extract_online_domains_from_cti()

# Domain list to monitor for seizure banners and DNS changes
domains = cti_domains

onion_sites = cti_onion_sites

# DNS records that will be checked for changes
dnsRecords = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]

# Local logging configuration - no external services required
log_directory = "rf_lookup_logs"
os.makedirs(log_directory, exist_ok=True)

# File to store previous DNS results
state_file = "rf_lookup_results.json"
previous_results = {}

def log_alert(alert_type, domain, record_type, records, previous_records, seizure_capture=None):
    """Log alerts to local JSON file instead of sending external notifications."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    alert_data = {
        "timestamp": timestamp,
        "alert_type": alert_type,
        "domain": domain,
        "record_type": record_type,
        "records": records if isinstance(records, list) else [],
        "previous_records": previous_records if isinstance(previous_records, list) else [],
        "seizure_capture": seizure_capture,
        "status": "detected"
    }
    
    # Save to daily log file
    log_filename = f"{log_directory}/alerts_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    try:
        # Load existing alerts for today
        if os.path.exists(log_filename):
            with open(log_filename, 'r', encoding='utf-8') as f:
                daily_alerts = json.load(f)
        else:
            daily_alerts = []
        
        # Add new alert
        daily_alerts.append(alert_data)
        
        # Save updated alerts
        with open(log_filename, 'w', encoding='utf-8') as f:
            json.dump(daily_alerts, f, indent=2, ensure_ascii=False)
        
        console.print(Padding(f"[bold green]→ Alert logged to: {log_filename}[/bold green]", (0, 0, 0, 4)))
        
        # Also save to summary file
        summary_filename = f"{log_directory}/alert_summary.json"
        if os.path.exists(summary_filename):
            with open(summary_filename, 'r', encoding='utf-8') as f:
                summary = json.load(f)
        else:
            summary = {"total_alerts": 0, "domains_monitored": [], "last_alert": None}
        
        summary["total_alerts"] += 1
        summary["last_alert"] = timestamp
        if domain not in summary["domains_monitored"]:
            summary["domains_monitored"].append(domain)
        
        with open(summary_filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        console.print(Padding(f"[red]→ Error logging alert: {e}[/red]", (0, 0, 0, 4)))

def generate_html_report():
    """Generate an HTML report of all alerts."""
    try:
        # Collect all alerts from daily files
        all_alerts = []
        for filename in os.listdir(log_directory):
            if filename.startswith("alerts_") and filename.endswith(".json"):
                filepath = os.path.join(log_directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    daily_alerts = json.load(f)
                    all_alerts.extend(daily_alerts)
        
        # Sort by timestamp (newest first)
        all_alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Generate HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RF-Lookup - Alert Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .alert {{ border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 5px; background: #fafafa; }}
        .alert.seizure {{ border-left: 5px solid #dc3545; background: #fff5f5; }}
        .alert.dns {{ border-left: 5px solid #007bff; background: #f0f8ff; }}
        .alert.onion {{ border-left: 5px solid #6f42c1; background: #f8f5ff; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
        .domain {{ font-weight: bold; color: #333; }}
        .records {{ margin: 10px 0; }}
        .record {{ background: #e9ecef; padding: 5px; margin: 2px 0; border-radius: 3px; font-family: monospace; }}
        .screenshot {{ margin-top: 10px; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 5px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; padding: 20px; background: #e9ecef; border-radius: 5px; }}
        .stat {{ text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
        .stat-label {{ color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 RF-Lookup - Alert Report</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(all_alerts)}</div>
                <div class="stat-label">Total Alerts</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(set(alert['domain'] for alert in all_alerts))}</div>
                <div class="stat-label">Domains Monitored</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len([a for a in all_alerts if 'seizure' in a['alert_type'].lower()])}</div>
                <div class="stat-label">Seizure Detections</div>
            </div>
        </div>
"""
        
        # Add alerts
        for alert in all_alerts:
            alert_class = "seizure" if "seizure" in alert['alert_type'].lower() else "onion" if "onion" in alert['alert_type'].lower() else "dns"
            
            html_content += f"""
        <div class="alert {alert_class}">
            <div class="timestamp">{alert['timestamp']}</div>
            <div class="domain">{alert['domain']}</div>
            <div><strong>Type:</strong> {alert['alert_type']}</div>
            <div><strong>Record Type:</strong> {alert['record_type']}</div>
            
            <div class="records">
                <strong>Previous Records:</strong>
                {''.join(f'<div class="record">{record}</div>' for record in alert['previous_records']) if alert['previous_records'] else '<div class="record">None</div>'}
            </div>
            
            <div class="records">
                <strong>New Records:</strong>
                {''.join(f'<div class="record">{record}</div>' for record in alert['records']) if alert['records'] else '<div class="record">None</div>'}
            </div>
"""
            
            if alert['seizure_capture'] and os.path.exists(alert['seizure_capture']):
                html_content += f"""
            <div class="screenshot">
                <strong>Screenshot:</strong><br>
                <img src="{alert['seizure_capture']}" alt="Seizure Screenshot">
            </div>
"""
            
            html_content += "        </div>\n"
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # Save HTML report
        report_filename = f"{log_directory}/alert_report.html"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        console.print(Padding(f"[bold green]→ HTML report generated: {report_filename}[/bold green]", (0, 0, 0, 4)))
        return report_filename
        
    except Exception as e:
        console.print(Padding(f"[red]→ Error generating HTML report: {e}[/red]", (0, 0, 0, 4)))
        return None

def send_request(url, data=None, use_tor=False):
    """Send a request using Tor only for .onion sites, normal internet uses direct connection."""
    
    # ✅ Default: No proxy (use normal internet)
    proxies = None  

    # ✅ Use Tor proxy ONLY for .onion sites
    if use_tor:
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }

    try:
        if data:
            response = requests.post(url, json=data, proxies=proxies, timeout=15)
        else:
            response = requests.get(url, proxies=proxies, timeout=15)

        response.raise_for_status()
        return response.text

    except requests.exceptions.ProxyError:
        console.print(Padding(f"[red]→ Proxy Error! Check if you're trying to route normal traffic through Tor.[/red]", (0, 0, 0, 4)))
        return None

    except requests.exceptions.RequestException as e:
        console.print(Padding(f"[red]→ Request failed: {e}[/red]", (0, 0, 0, 4)))
        return None

# Local notification functions (replacing Telegram/Discord)
def local_notify_dns_change(domain, record_type, records, previous_records, seizure_capture=None):
    """Log DNS changes locally instead of sending external notifications."""
    console.print(Padding(f"[bold yellow]→ DNS Change Detected: {domain} ({record_type})[/bold yellow]", (0, 0, 0, 4)))
    
    # Log the alert
    log_alert("DNS Change", domain, record_type, records, previous_records, seizure_capture)
    
    # Generate HTML report after each alert
    generate_html_report()

def local_notify_seizure(domain, seizure_type, seizure_capture=None):
    """Log seizure detection locally instead of sending external notifications."""
    console.print(Padding(f"[bold red]→ SEIZURE DETECTED: {domain} ({seizure_type})[/bold red]", (0, 0, 0, 4)))
    
    # Log the alert
    log_alert(f"Seizure - {seizure_type}", domain, "N/A", ["Seized"], ["Active"], seizure_capture)
    
    # Generate HTML report after each alert
    generate_html_report()


def capture_seizure_image(domain, use_tor=False):
    """Capture a screenshot of a suspected seizure page using Firefox.
    
    - Uses **Tor (Firefox proxy settings)** for `.onion` sites.
    - Uses **Direct connection** for clearnet sites.
    """
    
    screenshot_filename = f"screenshots/{domain}_image.png"
    os.makedirs("screenshots", exist_ok=True)

    console.print(Padding(f"→ Capturing likely LEA seizure {domain}...", (0, 0, 0, 4)))

    try:
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=2560,1440")  
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-web-security")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Automatically detect OS and set Firefox binary location
        if platform.system() == "Windows":
            options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        elif platform.system() == "Linux":
            options.binary_location = "/usr/bin/firefox"
        elif platform.system() == "Darwin":  # macOS
            options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
        else:
            raise Exception("Unsupported operating system: Cannot determine Firefox binary path.")

        if use_tor:
            console.print(Padding(f"→ Routing traffic through Tor for {domain}...", (0, 0, 0, 4)))

            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.socks", "127.0.0.1")
            options.set_preference("network.proxy.socks_port", 9050)
            options.set_preference("network.proxy.socks_remote_dns", True)  # 🛠 Ensures Tor resolves .onion domains
            options.set_preference("network.http.referer.spoofSource", True)
            options.set_preference("privacy.resistFingerprinting", True)
            options.set_preference("network.dns.disableIPv6", True)  # 🔴 Prevents DNS leaks

        # ✅ Automatically download & update Geckodriver
        service = FirefoxService(GeckoDriverManager().install())  # Automatically finds & installs Geckodriver
        driver = webdriver.Firefox(service=service, options=options)

        try:
            url = f"http://{domain}" if not domain.startswith("http") else domain
            console.print(Padding(f"→ Attempting to load {url} via Selenium...", (0, 0, 0, 4)))

            driver.get(url)
            time.sleep(10)  # Wait for page to fully load

            # ✅ Print the page title for debugging
            console.print(Padding(f"→ Page Title: {driver.title}", (0, 0, 0, 4)))

        except Exception as e:
            console.print(Padding(f"→ Failed to access {domain}: {e}", (0, 0, 0, 4)))
            driver.quit()
            return None

        driver.save_screenshot(screenshot_filename)
        driver.quit()
        console.print(Padding(f"→ Seizure screenshot saved: {screenshot_filename}", (0, 0, 0, 4)))
        return screenshot_filename

    except Exception as e:
        console.print(Padding(f"→ Unable to save seizure screenshot. {domain}: {e}", (0, 0, 0, 4)))
        return None

onion_state_file = "onion_lookup_results.json"
onion_results = {}  # Store `.onion` site statuses separately

def load_onion_results():
    """Load previous onion site results from a separate file at script startup."""
    global onion_results
    try:
        if os.path.exists(onion_state_file):
            with open(onion_state_file, "r", encoding="utf-8") as file:
                onion_results = json.load(file)
            console.print(Padding(f"[bold green]→ Loaded previous onion scan results.[/bold green]", (0, 0, 0, 4)))
        else:
            onion_results = {}
            console.print(Padding(f"[bold yellow]→ No previous onion scan results found, starting fresh.[/bold yellow]", (0, 0, 0, 4)))
    except Exception as e:
        console.print(Padding(f"[red]→ Error loading onion results: {e}[/red]", (0, 0, 0, 4)))
        onion_results = {}

def save_onion_results():
    """Save onion site results to a separate file to ensure persistence."""
    try:
        with open(onion_state_file, "w", encoding="utf-8") as file:
            json.dump(onion_results, file, indent=4, ensure_ascii=False)
        console.print(Padding(f"[bold green]→ Onion scan results saved successfully.[/bold green]", (0, 0, 0, 4)))
    except Exception as e:
        console.print(Padding(f"[red]→ Error saving onion results: {e}[/red]", (0, 0, 0, 4)))

def load_previous_results():
    global previous_results
    state_file = "rf_lookup_results.json"
    try:
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as file:
                previous_results = json.load(file)
        else:
            previous_results = {}
    except Exception as e:
        console.print(Padding(f"[red]→ Error loading previous results: {e}[/red]", (0, 0, 0, 4)))
        previous_results = {}

# Save DNS scan results to JSON
def save_previous_results():
    state_file = "rf_lookup_results.json"
    try:
        with open(state_file, "w", encoding="utf-8") as file:
            json.dump(previous_results, file, indent=4, ensure_ascii=False)
        console.print(Padding(f"[bold green]→ All results have been successfully saved.[/bold green]", (0, 0, 0, 4)))
    except Exception as e:
        console.print("")
        console.print(Padding(f"[red]→ Error saving results: {e}[/red]", (0, 0, 0, 4)))

exit_flag = False

def signal_handler(sig, frame):
    global exit_flag
    if exit_flag:
        console.print("")
        console.print(Padding("[red]→ Force stopping...[/red]", (0, 0, 0, 4)))
        os._exit(1)
    exit_flag = True
    sys.stdout.write("\033[2K\r")
    sys.stdout.flush()
    console.print("")
    console.print(Padding("[red]→ Safely shutting down...[/red]", (0, 0, 0, 4)))
    save_previous_results()
    
    # Generate final HTML report
    console.print(Padding("[bold cyan]→ Generating final HTML report...[/bold cyan]", (0, 0, 0, 4)))
    report_path = generate_html_report()
    if report_path:
        console.print(Padding(f"[bold green]→ Final report saved: {report_path}[/bold green]", (0, 0, 0, 4)))
    
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

tor_status = True  # Global variable to store Tor connection status

def is_tor_running():
    """Checks if Tor is running and correctly routing traffic."""
    global tor_status

    # ✅ If tor_status is already True, don't check again
    if tor_status:
        return True  

    tor_ports = [9050, 9150]  # Check both common Tor ports

    for tor_port in tor_ports:
        try:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", tor_port)
            socket.socket = socks.socksocket  # Redirect all sockets through Tor

            # ✅ First check: Try HTTPS version of Tor check page
            proxies = {"http": f"socks5h://127.0.0.1:{tor_port}", "https": f"socks5h://127.0.0.1:{tor_port}"}
            response = requests.get("https://check.torproject.org/", proxies=proxies, timeout=10)

            # ✅ Parse HTML to extract text properly
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find("h1", class_="not") and "Congratulations" in soup.find("h1", class_="not").text:
                tor_status = True
                console.print("")
                console.print(Padding(f"[bold green]→ Tor is running and routing traffic on port {tor_port}![/bold green]", (0, 0, 0, 4)))
                console.print("")
                return True
                
        except requests.exceptions.RequestException:
            console.print(Padding(f"[yellow]→ Tor check failed on port {tor_port}. Trying next port...[/yellow]", (0, 0, 0, 4)))
            continue  # Try the next port

    # ❌ If both checks fail, mark Tor as unavailable and log it
    tor_status = False
    console.print("")
    console.print(Padding("[bold red]→ Tor is NOT running or misconfigured! Skipping .onion scans.[/bold red]", (0, 0, 0, 4)))
    console.print("")
    return False

def check_onion_status(onion_url):
    """Check if a .onion site is seized by scanning for known seizure text in HTML."""
    global onion_results

    if not is_tor_running():  
        console.print(Padding(f"[red]→ Skipping {onion_url}: Tor is not running![/red]", (0, 0, 0, 4)))
        return False

    tor_proxy = "socks5h://127.0.0.1:9050"
    proxies = {"http": tor_proxy, "https": tor_proxy}

    last_status = onion_results.get(onion_url, {}).get("status", "unknown")

    try:
        response = requests.get(f"http://{onion_url}", proxies=proxies, timeout=30)
        html_content = response.text.lower()
        
        # Debug: Show page title and first 200 chars
        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.find("title")
        title_text = page_title.get_text().strip() if page_title else "No title"
        
        console.print(Padding(f"[cyan]→ Checking {onion_url} - Title: '{title_text}'[/cyan]", (0, 0, 0, 4)))
        
        # More specific seizure keywords
        seizure_keywords = [
            "this hidden site has been seized",
            "this domain has been seized", 
            "this site has been seized",
            "this website has been seized",
            "seized by law enforcement",
            "seized by the fbi",
            "seized by europol",
            "seized by interpol",
            "seized by nca",
            "operation onymous",
            "operation bayonet",
            "law enforcement seizure",
            "federal bureau of investigation",
            "department of justice seizure",
            "site seized",
            "domain seized",
            "website seized",
            "seized pursuant to",
            "seized under warrant",
            "seized by",
            "has been seized",
            "was seized",
            "seized site",
            "seized domain",
            "seized website"
        ]
        
        # Check for seizure indicators
        found_keywords = [keyword for keyword in seizure_keywords if keyword in html_content]
        
        # Additional checks for common seizure page patterns
        seizure_indicators = [
            "seized" in html_content and ("fbi" in html_content or "law enforcement" in html_content),
            "operation" in html_content and ("seized" in html_content or "takedown" in html_content),
            "warrant" in html_content and "seized" in html_content,
            "court order" in html_content and "seized" in html_content
        ]
        
        is_seized = len(found_keywords) > 0 or any(seizure_indicators)
        
        if found_keywords:
            console.print(Padding(f"[yellow]→ Found seizure keywords: {found_keywords}[/yellow]", (0, 0, 0, 4)))
        
        new_status = "seized" if is_seized else "active"

        if last_status == new_status:
            console.print(Padding(f"[cyan]→ No change detected for {onion_url}, skipping.[/cyan]", (0, 0, 0, 4)))
            return False

        if is_seized:
            console.print(Padding(f"[bold red]→ SEIZURE DETECTED: {onion_url}[/bold red]", (0, 0, 0, 4)))
            console.print(Padding(f"[red]→ Keywords found: {found_keywords}[/red]", (0, 0, 0, 4)))
            seizure_capture = capture_seizure_image(onion_url, use_tor=True)

            onion_results[onion_url] = {"status": "seized", "last_checked": datetime.now(timezone.utc).isoformat(), "keywords": found_keywords}
            save_onion_results()

            local_notify_seizure(onion_url, "Onion Seized", seizure_capture)

        else:
            console.print(Padding(f"[green]→ {onion_url} is active (no seizure indicators found)[/green]", (0, 0, 0, 4)))
            onion_results[onion_url] = {"status": "active", "last_checked": datetime.now(timezone.utc).isoformat()}
            save_onion_results()

        return is_seized

    except requests.exceptions.ConnectionError:
        console.print(Padding(f"[yellow]→ {onion_url} is unreachable. Connection refused.[/yellow]", (0, 0, 0, 4)))
        new_status = "unreachable"
    except requests.exceptions.Timeout:
        console.print(Padding(f"[yellow]→ {onion_url} timed out. Likely offline or slow.[/yellow]", (0, 0, 0, 4)))
        new_status = "unreachable"
    except requests.exceptions.RequestException as e:
        console.print(Padding(f"[yellow]→ {onion_url} is unreachable. Error: {e}[/yellow]", (0, 0, 0, 4)))
        new_status = "unreachable"

    if last_status == new_status:
        console.print(Padding(f"[cyan]→ No change detected for {onion_url}, skipping.[/cyan]", (0, 0, 0, 4)))
        return False

    onion_results[onion_url] = {"status": new_status, "last_checked": datetime.now(timezone.utc).isoformat()}
    save_onion_results()

    return False

def check_all_onion_sites():
    """Iterate through all .onion sites and check their status using a single Tor check."""
    global tor_status

    if not is_tor_running():
        console.print(Padding("[bold red]→ Skipping all .onion scans: Tor is not running![/bold red]", (0, 0, 0, 4)))
        return

    for onion_site in onion_sites:
        check_onion_status(onion_site)

    # ✅ Save results after all `.onion` sites are scanned
    save_onion_results()

    console.print(Padding("[bold green]→ Onion scan complete. Snoozing for 60 seconds...[/bold green]\n", (0, 0, 0, 4)))


# Monitor domains for DNS changes and possible seizures and send alerts when needed
def watch_dog():
    global exit_flag
    try:
        while not exit_flag:
            for i, domain in enumerate(domains, start=1):
                if exit_flag:
                    break
                console.print("")

                if i < len(domains):
                    console.print(Padding(f"[bold green]→ {(i / len(domains)) * 100:.0f}% complete[/bold green]", (0, 0, 0, 4)))

                for record_type in dnsRecords:
                    if exit_flag:
                        break
                    console.print(Padding(f"[bold cyan]→ Scanning {record_type:<5} records for {domain[:25]:<25}[/bold cyan]", (0, 0, 0, 4)))

                    # Check the DNS records for the current domain
                    try:
                        answers = dns.resolver.resolve(domain, record_type, lifetime=5)
                        records = [r.to_text() for r in answers]
                    except dns.resolver.NXDOMAIN:
                        continue
                    except dns.resolver.Timeout:
                        console.print(Padding(f"[red]→ DNS check timed out for {domain}[/red]", (0, 0, 0, 4)))
                        continue
                    except:
                        records = []

                    sorted_records = sorted(records)
                    prev_entry = previous_results.get(domain, {}).get(record_type, {"records": []})

                    # Ensure prev_entry is a dictionary before accessing keys
                    if not isinstance(prev_entry, dict):
                        prev_entry = {"records": []}

                    prev_sorted_records = sorted(prev_entry["records"])

                    if domain not in previous_results:
                        previous_results[domain] = {}

                    # Load history of previous record sets for this domain/record type
                    history = previous_results[domain].get(record_type, {}).get("history", [])

                    if sorted_records in history or exit_flag:
                        continue

                    console.print("")
                    console.print(Padding(f"→ Change detected: {domain} ({record_type})", (0, 0, 0, 4)))

                    formatted_previous = "\n".join(f"   - {entry}" for entry in history[-1]) if history else "   - None"
                    formatted_new = "\n".join(f"   - {entry}" for entry in sorted_records) or "   - None"

                    console.print("")
                    console.print(Padding(f"[yellow]→ Previous Records:[/yellow]\n[yellow]{formatted_previous}[/yellow]", (0, 0, 0, 4)))
                    console.print("")
                    console.print(Padding(f"[green]→ New Records:[/green]\n[green]{formatted_new}[/green]", (0, 0, 0, 4)))
                    console.print("")

                    seizure_capture = None
                    if record_type == "NS" and any(ns in sorted_records for ns in [
                        "ns1.fbi.seized.gov.", "ns2.fbi.seized.gov.",
                        "jocelyn.ns.cloudflare.com.", "plato.ns.cloudflare.com.",
                        "ns1.usssdomainseizure.com", "ns2.usssdomainseizure.com"
                    ]):
                        console.print(Padding(f"→ Taking seizure screenshot for {domain} (FBI Seized NS Detected)", (0, 0, 0, 4)))
                        seizure_capture = capture_seizure_image(domain)

                    local_notify_dns_change(domain, record_type, sorted_records, history[-1] if history else [], seizure_capture)

                    # Update stored results and append to history
                    history.append(sorted_records)
                    previous_results[domain][record_type] = {
                        "records": sorted_records,
                        "history": history[-10:]  # limit history to last 10 changes
                    }

            # ✅ Show this once after all domains are processed
            console.print(Padding("[bold green]→ 100% complete[/bold green]", (0, 0, 0, 4)))

            if is_tor_running():
                console.print("")
                console.print(Padding(f"→ Configuring Firefox to route traffic through Tor...", (0, 0, 0, 4)))
                console.print(Padding("[bold cyan]→ Checking .onion sites for seizures...[/bold cyan]", (0, 0, 0, 4)))
                console.print("")

                for onion_site in onion_sites:
                    check_onion_status(onion_site)

                console.print("")
                console.print(Padding("[bold green]→ Onion scan complete. Snoozing for 60 seconds...[/bold green]\n", (0, 0, 0, 4)))

            if not exit_flag:
                save_previous_results()
                console.print(Padding("[bold green]→ RF-Lookup shift complete. Snoozing for 60 seconds...[/bold green]\n", (0, 0, 0, 4)))
                time.sleep(15)

    except KeyboardInterrupt:
        exit_flag = True
        console.print(Padding("[bold red]→ Monitoring interrupted by user. Exiting...[/bold red]", (0, 0, 0, 4)))
        save_previous_results()
        
        # Generate final HTML report
        console.print(Padding("[bold cyan]→ Generating final HTML report...[/bold cyan]", (0, 0, 0, 4)))
        report_path = generate_html_report()
        if report_path:
            console.print(Padding(f"[bold green]→ Final report saved: {report_path}[/bold green]", (0, 0, 0, 4)))
        
        console.print(Padding("[bold green]→ RF-Lookup Results saved successfully.[/bold green]", (0, 0, 0, 4)))
        exit(0)

if __name__ == "__main__":
    load_previous_results()  # ✅ Loads clearnet sites
    load_onion_results()  # ✅ Loads onion sites

    console.print(Padding("[bold cyan]→ Loading previous RF-Lookup results...[/bold cyan]", (0, 0, 0, 4)))
    time.sleep(random.uniform(0.5, 1.2))

    console.print(Padding("[bold green]→ Previous RF-Lookup results were successfully loaded...[/bold green]", (0, 0, 0, 4)))
    time.sleep(random.uniform(1.0, 2.0))

    console.print(Padding("[bold yellow]→ RF-Lookup is starting to sniff for seizure records...[/bold yellow]\n", (0, 0, 0, 4)))
    time.sleep(random.uniform(1.5, 2.5))

    watch_dog()