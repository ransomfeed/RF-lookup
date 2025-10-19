#!/usr/bin/env python3
"""
Test script per verificare l'estrazione dei domini dai file CTI
"""

import sys
import os
from rf_lookup import extract_online_domains_from_cti

def test_cti_extraction():
    """Testa l'estrazione dei domini dai file CTI"""
    print("🔍 Testing CTI Domain Extraction...")
    print("=" * 50)
    
    try:
        # Estrai domini dai file CTI
        clearnet_domains, onion_sites = extract_online_domains_from_cti()
        
        print(f"\n📊 Results:")
        print(f"   Clearnet domains: {len(clearnet_domains)}")
        print(f"   Onion sites: {len(onion_sites)}")
        
        print(f"\n🌐 Sample Clearnet Domains:")
        for i, domain in enumerate(clearnet_domains[:10], 1):
            print(f"   {i:2d}. {domain}")
        
        print(f"\n🧅 Sample Onion Sites:")
        for i, onion in enumerate(onion_sites[:10], 1):
            print(f"   {i:2d}. {onion}")
        
        # Verifica che non ci siano duplicati
        clearnet_unique = len(set(clearnet_domains))
        onion_unique = len(set(onion_sites))
        
        print(f"\n✅ Validation:")
        print(f"   Clearnet domains unique: {clearnet_unique}/{len(clearnet_domains)}")
        print(f"   Onion sites unique: {onion_unique}/{len(onion_sites)}")
        
        if clearnet_unique == len(clearnet_domains) and onion_unique == len(onion_sites):
            print("   ✅ No duplicates found!")
        else:
            print("   ⚠️  Some duplicates detected")
        
        # Verifica che i domini siano nel formato corretto
        print(f"\n🔍 Format Validation:")
        invalid_clearnet = [d for d in clearnet_domains if '.' not in d or d.endswith('.onion')]
        invalid_onion = [o for o in onion_sites if not o.endswith('.onion')]
        
        if not invalid_clearnet and not invalid_onion:
            print("   ✅ All domains have correct format!")
        else:
            print(f"   ⚠️  Found {len(invalid_clearnet)} invalid clearnet domains")
            print(f"   ⚠️  Found {len(invalid_onion)} invalid onion sites")
        
        print(f"\n🎯 Summary:")
        print(f"   Total domains to monitor: {len(clearnet_domains) + len(onion_sites)}")
        print(f"   Ready for RF-Lookup monitoring!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return False

if __name__ == "__main__":
    success = test_cti_extraction()
    if success:
        print("\n✅ CTI extraction test completed successfully!")
    else:
        print("\n❌ CTI extraction test failed!")
        sys.exit(1)
