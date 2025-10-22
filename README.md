# RF-Lookup 🔍

**Ransomfeed Advanced Domain Monitoring Tool**

RF-Lookup is an advanced tool for monitoring domains and onion sites, designed to detect DNS changes and possible seizures by law enforcement before they become public.
Originally based on [FBI_Watchdog](https://github.com/DarkWebInformer/FBI_Watchdog).

## Prerequisites

- Python 3.7 or higher
- Firefox (for automatic screenshots)
- Tor (optional, for onion site monitoring)
- Git (for cloning repositories)

## Key Features

- 🔍 **DNS Monitoring**: Checks changes in DNS records (A, AAAA, CNAME, MX, NS, SOA, TXT)
- 🌐 **Onion Support**: Monitors .onion sites through the Tor network
- 📸 **Automatic Screenshots**: Automatically captures screenshots of suspicious pages
- 📊 **HTML Reports**: Generates detailed reports in HTML format
- 💾 **Local Logging**: Saves all alerts in local JSON files
- 🔄 **Auto-Update**: Automatic update system from GitHub
- 📋 **CTI Integration**: Automatic extraction of domains from intelligence files [deepdarkCTI](https://github.com/fastfire/deepdarkCTI) - this project is a dependency from which to retrieve domain names to monitor.

## Installation

1. Clone the RF-Lookup repository:
```bash
git clone https://github.com/ransomfeed/RF-lookup.git
cd RF-lookup
```

2. Clone the CTI repository (external dependency):
```bash
git clone https://github.com/fastfire/deepdarkCTI.git
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Note**: The `deepdarkCTI` repository is an external dependency necessary for RF-Lookup to function. It contains intelligence files with domains to monitor.

4. Configure Tor (optional, for onion site monitoring):
```bash
# On macOS with Homebrew
brew install tor

# Start Tor
tor
```

## Usage

### Basic Start
```bash
python rf_lookup.py
```

### System Test
```bash
python test_rf_lookup.py
```

### CTI Domain Extraction Test
```bash
python test_cti_extraction.py
```

### Onion Seizure Detection Test
```bash
python test_onion_seizure.py
```

### Whitelist Functionality Test
```bash
python test_whitelist.py
```

## Configuration

### Automatic CTI Domain Extraction
RF-Lookup automatically extracts domains marked as "ONLINE" from files in the `deepdarkCTI/` folder:
- `markets.md` - Dark web markets
- `forum.md` - Forums and communities
- `ransomware_gang.md` - Ransomware groups

The system automatically analyzes these files at startup and monitors all found domains.

### Whitelist Configuration
RF-Lookup supports domain whitelisting to exclude specific domains from monitoring. Create a `whitelist.json` file:

```json
{
  "whitelist": {
    "description": "Domains to exclude from RF-Lookup monitoring",
    "clearnet_domains": [
      "example.com",
      "test-domain.org"
    ],
    "onion_domains": [
      "example.onion"
    ],
    "enabled": true
  },
  "settings": {
    "skip_whitelisted": true,
    "log_skipped_domains": true
  }
}
```

**Configuration Options:**
- `enabled`: Enable/disable whitelist functionality
- `skip_whitelisted`: Skip monitoring whitelisted domains
- `log_skipped_domains`: Log which domains are being skipped

### Custom Domains
If you want to add custom domains, modify the `extract_online_domains_from_cti()` function in the `rf_lookup.py` file:

## File Structure

```
RF-lookup/
├── rf_lookup.py              # Main script
├── test_rf_lookup.py         # Test script
├── test_whitelist.py         # Whitelist functionality test
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore file
├── deepdarkCTI/             # External CTI repository (cloned separately)
│   ├── markets.md
│   ├── forum.md
│   └── ransomware_gang.md
└── [Automatically generated files]
    ├── rf_lookup_logs/      # Log folder (created automatically)
    ├── rf_lookup_results.json # Previous DNS results
    ├── onion_lookup_results.json # Previous onion results
    └── screenshots/         # Screenshots of suspicious pages
```

## Monitoring Features

### DNS Monitoring
- Detects changes in DNS records
- Identifies possible seizures through suspicious NS records
- Saves change history

### Onion Monitoring
- Checks .onion site status
- Detects seizure pages
- Uses Tor proxy automatically

### Alert System
- Local logging in JSON format
- Interactive HTML reports
- Automatic screenshots of suspicious pages

## System Requirements

- **Python**: 3.7 or higher
- **Firefox**: For automatic screenshots of suspicious pages
- **Tor**: Optional, for onion site monitoring (port 9050)
- **Git**: For cloning necessary repositories
- **Operating System**: Windows, macOS, Linux

## Dependencies

- `dnspython` - DNS resolution
- `requests` - HTTP requests
- `selenium` - Browser automation
- `beautifulsoup4` - HTML parsing
- `rich` - Colored output
- `PySocks` - SOCKS proxy support

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## External Dependencies

- **[deepdarkCTI](https://github.com/fastfire/deepdarkCTI)**: Intelligence repository containing domains to monitor. Must be cloned separately in the project folder.

## Disclaimer

This tool is intended exclusively for educational and research purposes. Users are responsible for complying with local laws and applicable regulations.
