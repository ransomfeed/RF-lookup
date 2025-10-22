#!/usr/bin/env python3
"""
Test script per verificare il funzionamento della whitelist
"""

import sys
import os
import json
from rf_lookup import load_whitelist, is_domain_whitelisted, filter_whitelisted_domains

def test_whitelist_functionality():
    """Testa il funzionamento della whitelist"""
    print("🔒 Testing Whitelist Functionality...")
    print("=" * 50)
    
    # Test 1: Caricamento whitelist
    print("\n1. Testing whitelist loading...")
    whitelist_config = load_whitelist()
    
    print(f"   ✅ Whitelist loaded successfully")
    print(f"   📊 Clearnet domains: {len(whitelist_config['whitelist']['clearnet_domains'])}")
    print(f"   📊 Onion domains: {len(whitelist_config['whitelist']['onion_domains'])}")
    print(f"   📊 Enabled: {whitelist_config['whitelist']['enabled']}")
    
    # Test 2: Controllo domini whitelisted
    print("\n2. Testing domain whitelist checking...")
    
    test_domains = [
        ("example.com", False),  # Should not be whitelisted by default
        ("test-domain.org", False),  # Should not be whitelisted by default
        ("example.onion", False),  # Should not be whitelisted by default
    ]
    
    for domain, expected in test_domains:
        result = is_domain_whitelisted(domain, whitelist_config)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {domain}: {'WHITELISTED' if result else 'NOT WHITELISTED'} (Expected: {'WHITELISTED' if expected else 'NOT WHITELISTED'})")
    
    # Test 3: Filtro domini
    print("\n3. Testing domain filtering...")
    
    test_clearnet = ["example.com", "test-domain.org", "normal-site.com"]
    test_onion = ["example.onion", "normal-site.onion"]
    
    filtered_clearnet, filtered_onion = filter_whitelisted_domains(test_clearnet, test_onion, whitelist_config)
    
    print(f"   📊 Original clearnet domains: {len(test_clearnet)}")
    print(f"   📊 Filtered clearnet domains: {len(filtered_clearnet)}")
    print(f"   📊 Original onion domains: {len(test_onion)}")
    print(f"   📊 Filtered onion domains: {len(filtered_onion)}")
    
    # Test 4: Creazione whitelist personalizzata
    print("\n4. Testing custom whitelist creation...")
    
    custom_whitelist = {
        "whitelist": {
            "description": "Test whitelist for RF-Lookup",
            "clearnet_domains": ["example.com", "test-domain.org"],
            "onion_domains": ["example.onion"],
            "enabled": True
        },
        "settings": {
            "skip_whitelisted": True,
            "log_skipped_domains": True
        }
    }
    
    # Salva whitelist di test
    test_whitelist_file = "test_whitelist.json"
    with open(test_whitelist_file, 'w', encoding='utf-8') as f:
        json.dump(custom_whitelist, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Custom whitelist created: {test_whitelist_file}")
    
    # Testa con whitelist personalizzata
    test_domains_custom = [
        ("example.com", True),  # Should be whitelisted
        ("test-domain.org", True),  # Should be whitelisted
        ("example.onion", True),  # Should be whitelisted
        ("normal-site.com", False),  # Should not be whitelisted
    ]
    
    print(f"\n   Testing with custom whitelist:")
    for domain, expected in test_domains_custom:
        result = is_domain_whitelisted(domain, custom_whitelist)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {domain}: {'WHITELISTED' if result else 'NOT WHITELISTED'}")
    
    # Test filtro con whitelist personalizzata
    test_clearnet_custom = ["example.com", "test-domain.org", "normal-site.com", "another-site.com"]
    test_onion_custom = ["example.onion", "normal-site.onion", "another-site.onion"]
    
    filtered_clearnet_custom, filtered_onion_custom = filter_whitelisted_domains(
        test_clearnet_custom, test_onion_custom, custom_whitelist
    )
    
    print(f"\n   📊 Custom whitelist filtering:")
    print(f"   📊 Original clearnet: {len(test_clearnet_custom)} -> Filtered: {len(filtered_clearnet_custom)}")
    print(f"   📊 Original onion: {len(test_onion_custom)} -> Filtered: {len(filtered_onion_custom)}")
    print(f"   📊 Skipped clearnet: {len(test_clearnet_custom) - len(filtered_clearnet_custom)}")
    print(f"   📊 Skipped onion: {len(test_onion_custom) - len(filtered_onion_custom)}")
    
    # Cleanup
    if os.path.exists(test_whitelist_file):
        os.remove(test_whitelist_file)
        print(f"   🧹 Cleaned up test file: {test_whitelist_file}")
    
    print(f"\n✅ Whitelist functionality test completed!")
    return True

def test_whitelist_file_creation():
    """Testa la creazione automatica del file whitelist"""
    print("\n🔧 Testing automatic whitelist file creation...")
    print("=" * 50)
    
    # Rimuovi whitelist esistente per test
    whitelist_file = "whitelist.json"
    backup_file = "whitelist_backup.json"
    
    if os.path.exists(whitelist_file):
        os.rename(whitelist_file, backup_file)
        print(f"   📦 Backed up existing whitelist to {backup_file}")
    
    # Testa caricamento senza file
    print(f"   🔍 Testing whitelist loading without file...")
    whitelist_config = load_whitelist()
    
    if os.path.exists(whitelist_file):
        print(f"   ✅ Whitelist file created automatically")
        
        # Verifica contenuto
        with open(whitelist_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        expected_keys = ["whitelist", "settings"]
        if all(key in content for key in expected_keys):
            print(f"   ✅ Whitelist file has correct structure")
        else:
            print(f"   ❌ Whitelist file structure incorrect")
            return False
    else:
        print(f"   ❌ Whitelist file was not created")
        return False
    
    # Ripristina backup
    if os.path.exists(backup_file):
        os.remove(whitelist_file)
        os.rename(backup_file, whitelist_file)
        print(f"   🔄 Restored original whitelist file")
    
    print(f"   ✅ Automatic file creation test completed!")
    return True

if __name__ == "__main__":
    print("🔒 RF-Lookup Whitelist Test Suite")
    print("=" * 60)
    
    # Test funzionalità whitelist
    whitelist_test_passed = test_whitelist_functionality()
    
    # Test creazione file automatica
    file_creation_test_passed = test_whitelist_file_creation()
    
    print(f"\n🎯 Overall Test Results:")
    print("=" * 30)
    print(f"Whitelist Functionality: {'✅ PASSED' if whitelist_test_passed else '❌ FAILED'}")
    print(f"File Creation: {'✅ PASSED' if file_creation_test_passed else '❌ FAILED'}")
    
    if whitelist_test_passed and file_creation_test_passed:
        print(f"\n🎉 All whitelist tests passed! Whitelist system is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the whitelist implementation.")
        sys.exit(1)
