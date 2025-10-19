#!/usr/bin/env python3
"""
Test script per verificare le funzionalità di logging locale del RF-Lookup
"""

import sys
import os
import json
from datetime import datetime, timezone

# Aggiungi il percorso dello script principale
sys.path.append('/Users/nuke/Documents/recon/RF-lookup')

# Importa le funzioni di logging
from rf_lookup import log_alert, generate_html_report

def test_logging_system():
    """Testa il sistema di logging locale"""
    print("🧪 Testando il sistema di logging locale...")
    
    # Test 1: Log di un cambio DNS
    print("\n1. Testando log cambio DNS...")
    log_alert(
        alert_type="DNS Change",
        domain="test-domain.com",
        record_type="A",
        records=["192.168.1.1", "192.168.1.2"],
        previous_records=["192.168.1.100"],
        seizure_capture=None
    )
    
    # Test 2: Log di un sequestro
    print("\n2. Testando log sequestro...")
    log_alert(
        alert_type="Seizure - FBI",
        domain="seized-site.com",
        record_type="N/A",
        records=["Seized"],
        previous_records=["Active"],
        seizure_capture="screenshots/test_screenshot.png"
    )
    
    # Test 3: Log di un sito onion
    print("\n3. Testando log sito onion...")
    log_alert(
        alert_type="Onion Seized",
        domain="test.onion",
        record_type="N/A",
        records=["Seized"],
        previous_records=["Online"],
        seizure_capture=None
    )
    
    # Test 4: Generazione report HTML
    print("\n4. Testando generazione report HTML...")
    report_path = generate_html_report()
    if report_path:
        print(f"✅ Report HTML generato: {report_path}")
    else:
        print("❌ Errore nella generazione del report HTML")
    
    # Test 5: Verifica file creati
    print("\n5. Verificando file creati...")
    log_dir = "rf_lookup_logs"
    if os.path.exists(log_dir):
        files = os.listdir(log_dir)
        print(f"📁 File nella cartella {log_dir}:")
        for file in files:
            file_path = os.path.join(log_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"   - {file} ({size} bytes)")
    else:
        print("❌ Cartella di log non trovata")
    
    print("\n✅ Test completato!")

if __name__ == "__main__":
    test_logging_system()
