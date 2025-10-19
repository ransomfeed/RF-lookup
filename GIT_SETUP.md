# RF-Lookup Git Repository Setup

## Inizializzazione Repository

Per inizializzare il repository Git per RF-Lookup:

```bash
# Inizializza il repository Git
git init

# Aggiungi tutti i file (rispetta .gitignore)
git add .

# Primo commit
git commit -m "Initial commit: RF-Lookup v2.1.0"

# Aggiungi il remote origin (sostituisci con il tuo URL)
git remote add origin https://github.com/yourusername/RF-lookup.git

# Push al repository remoto
git push -u origin main
```

## File Inclusi nel Repository

- `rf_lookup.py` - Script principale
- `test_rf_lookup.py` - Script di test
- `test_cti_extraction.py` - Test estrazione domini CTI
- `requirements.txt` - Dipendenze Python
- `README.md` - Documentazione
- `LICENSE` - Licenza MIT
- `.gitignore` - File Git ignore

## File Esclusi dal Repository

- `venv/` - Ambiente virtuale Python
- `deepdarkCTI/` - Repository CTI esterno
- `rf_lookup_logs/` - Log generati
- `*.json` - File di stato generati
- `screenshots/` - Screenshot generati
- `images/` - Immagini temporanee
- `__pycache__/` - Cache Python
- File temporanei e di sistema

## Note per gli Sviluppatori

1. Il repository `deepdarkCTI` deve essere clonato separatamente
2. I file di log e stato vengono generati automaticamente
3. L'ambiente virtuale non deve essere incluso nel repository
4. Tutti i file temporanei sono esclusi tramite `.gitignore`
