# RF-Lookup 🔍

**Ransomfeed Advanced Domain Monitoring Tool**

RF-Lookup è uno strumento avanzato per il monitoraggio di domini e siti onion, progettato per rilevare cambiamenti DNS e possibili sequestri da parte delle forze dell'ordine prima che diventino pubblici.

## Prerequisiti

- Python 3.7 o superiore
- Firefox (per gli screenshot automatici)
- Tor (opzionale, per il monitoraggio dei siti onion)
- Git (per clonare i repository)

## Caratteristiche Principali

- 🔍 **Monitoraggio DNS**: Controlla cambiamenti nei record DNS (A, AAAA, CNAME, MX, NS, SOA, TXT)
- 🌐 **Supporto Onion**: Monitora siti .onion attraverso la rete Tor
- 📸 **Screenshot Automatici**: Cattura automaticamente screenshot di pagine sospette
- 📊 **Report HTML**: Genera report dettagliati in formato HTML
- 💾 **Logging Locale**: Salva tutti gli alert in file JSON locali
- 🔄 **Auto-Update**: Sistema di aggiornamento automatico da GitHub
- 📋 **CTI Integration**: Estrazione automatica di domini dai file di intelligence [deepdarkCTI](https://github.com/fastfire/deepdarkCTI) - questo progetto è una dipendenza dalla quale reperire i nomi dei domini da monitorare.

## Installazione

1. Clona il repository RF-Lookup:
```bash
git clone https://github.com/yourusername/RF-lookup.git
cd RF-lookup
```

2. Clona il repository CTI (dipendenza esterna):
```bash
git clone https://github.com/fastfire/deepdarkCTI.git
```

3. Installa le dipendenze Python:
```bash
pip install -r requirements.txt
```

**Nota**: Il repository `deepdarkCTI` è una dipendenza esterna necessaria per il funzionamento di RF-Lookup. Contiene i file di intelligence con i domini da monitorare.

4. Configura Tor (opzionale, per il monitoraggio dei siti onion):
```bash
# Su macOS con Homebrew
brew install tor

# Avvia Tor
tor
```

## Utilizzo

### Avvio Base
```bash
python rf_lookup.py
```

### Test del Sistema
```bash
python test_rf_lookup.py
```

### Test Estrazione Domini CTI
```bash
python test_cti_extraction.py
```

## Configurazione

### Estrazione Automatica Domini CTI
RF-Lookup estrae automaticamente i domini marcati come "ONLINE" dai file nella cartella `deepdarkCTI/`:
- `markets.md` - Mercati dark web
- `forum.md` - Forum e comunità
- `ransomware_gang.md` - Gruppi ransomware

Il sistema analizza automaticamente questi file all'avvio e monitora tutti i domini trovati.

### Domini Personalizzati
Se vuoi aggiungere domini personalizzati, modifica la funzione `extract_online_domains_from_cti()` nel file `rf_lookup.py`:

## Struttura dei File

```
RF-lookup/
├── rf_lookup.py              # Script principale
├── test_rf_lookup.py         # Script di test
├── test_cti_extraction.py    # Test estrazione domini CTI
├── requirements.txt          # Dipendenze Python
├── README.md                 # Documentazione
├── LICENSE                   # Licenza MIT
├── .gitignore               # File Git ignore
├── deepdarkCTI/             # Repository CTI esterno (clonato separatamente)
│   ├── markets.md
│   ├── forum.md
│   └── ransomware_gang.md
└── [File generati automaticamente]
    ├── rf_lookup_logs/      # Cartella dei log (creata automaticamente)
    ├── rf_lookup_results.json # Risultati DNS precedenti
    ├── onion_lookup_results.json # Risultati onion precedenti
    └── screenshots/         # Screenshot delle pagine sospette
```

## Funzionalità di Monitoraggio

### DNS Monitoring
- Rileva cambiamenti nei record DNS
- Identifica possibili sequestri tramite NS records sospetti
- Salva cronologia delle modifiche

### Onion Monitoring
- Controlla lo stato dei siti .onion
- Rileva pagine di sequestro
- Utilizza proxy Tor automaticamente

### Alert System
- Logging locale in formato JSON
- Report HTML interattivi
- Screenshot automatici delle pagine sospette

## Requisiti di Sistema

- **Python**: 3.7 o superiore
- **Firefox**: Per gli screenshot automatici delle pagine sospette
- **Tor**: Opzionale, per il monitoraggio dei siti onion (porta 9050)
- **Git**: Per clonare i repository necessari
- **Sistema Operativo**: Windows, macOS, Linux

## Dipendenze

- `dnspython` - Risoluzione DNS
- `requests` - Richieste HTTP
- `selenium` - Automazione browser
- `beautifulsoup4` - Parsing HTML
- `rich` - Output colorato
- `PySocks` - Supporto proxy SOCKS

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## Contributi

I contributi sono benvenuti! Per favore:

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## Dipendenze Esterne

- **[deepdarkCTI](https://github.com/fastfire/deepdarkCTI)**: Repository di intelligence che contiene i domini da monitorare. Deve essere clonato separatamente nella cartella del progetto.

## Disclaimer

Questo strumento è destinato esclusivamente a scopi educativi e di ricerca. Gli utenti sono responsabili del rispetto delle leggi locali e delle normative applicabili.
