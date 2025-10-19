#!/usr/bin/env python3
"""
Test script per verificare il rilevamento dei sequestri onion
"""

import sys
import os
from rf_lookup import check_onion_status, is_tor_running

def test_onion_seizure_detection():
    """Testa il rilevamento dei sequestri onion"""
    print("🧅 Testing Onion Seizure Detection...")
    print("=" * 50)
    
    # Test con alcuni domini onion di esempio
    test_onions = [
        "alphabay522szl32u4ci5e3iokdsyth56ei7rwngr2wm7i5jo54j2eid.onion",
        "4pt4axjgzmm4ibmxplfiuvopxzf775e5bqseyllafcecryfthdupjwyd.onion",
        "sn2sfdqay6cxztroslaxa36covrhoowe6a5xug6wlm6ek7nmeiujgvad.onion"
    ]
    
    print(f"\n🔍 Testing {len(test_onions)} onion sites...")
    
    # Verifica se Tor è in esecuzione
    if not is_tor_running():
        print("❌ Tor is not running! Please start Tor first.")
        print("   On macOS: brew install tor && tor")
        return False
    
    print("✅ Tor is running, proceeding with tests...")
    
    results = []
    
    for onion in test_onions:
        print(f"\n🔍 Testing: {onion}")
        print("-" * 40)
        
        try:
            result = check_onion_status(onion)
            results.append({
                "onion": onion,
                "result": result,
                "status": "success"
            })
            print(f"✅ Test completed for {onion}")
            
        except Exception as e:
            print(f"❌ Error testing {onion}: {e}")
            results.append({
                "onion": onion,
                "result": False,
                "status": "error",
                "error": str(e)
            })
    
    # Riepilogo risultati
    print(f"\n📊 Test Results Summary:")
    print("=" * 50)
    
    successful_tests = [r for r in results if r["status"] == "success"]
    failed_tests = [r for r in results if r["status"] == "error"]
    
    print(f"✅ Successful tests: {len(successful_tests)}")
    print(f"❌ Failed tests: {len(failed_tests)}")
    
    if successful_tests:
        print(f"\n🔍 Detailed Results:")
        for result in successful_tests:
            status_text = "SEIZED" if result["result"] else "ACTIVE"
            print(f"   {result['onion'][:30]}... -> {status_text}")
    
    if failed_tests:
        print(f"\n❌ Errors:")
        for result in failed_tests:
            print(f"   {result['onion'][:30]}... -> {result['error']}")
    
    return len(failed_tests) == 0

def test_seizure_keywords():
    """Testa le keyword di rilevamento sequestri"""
    print("\n🔍 Testing Seizure Keywords...")
    print("=" * 50)
    
    # Simula contenuto HTML di pagine sequestrate
    test_cases = [
        {
            "name": "FBI Seizure Page",
            "content": "This hidden site has been seized by the FBI. Federal Bureau of Investigation.",
            "should_detect": True
        },
        {
            "name": "Europol Seizure Page", 
            "content": "This domain has been seized by Europol in cooperation with law enforcement.",
            "should_detect": True
        },
        {
            "name": "Normal Site",
            "content": "Welcome to our marketplace. We sell various products and services.",
            "should_detect": False
        },
        {
            "name": "Site mentioning FBI (not seized)",
            "content": "We discuss FBI investigations and law enforcement topics on this forum.",
            "should_detect": False
        },
        {
            "name": "Operation Seizure",
            "content": "This site was seized pursuant to Operation Onymous court order.",
            "should_detect": True
        }
    ]
    
    seizure_keywords = [
        "this hidden site has been seized",
        "this domain has been seized", 
        "seized by law enforcement",
        "seized by the fbi",
        "seized by europol",
        "operation onymous",
        "operation bayonet",
        "law enforcement seizure",
        "federal bureau of investigation",
        "department of justice seizure"
    ]
    
    correct_detections = 0
    
    for test_case in test_cases:
        content_lower = test_case["content"].lower()
        found_keywords = [keyword for keyword in seizure_keywords if keyword in content_lower]
        
        # Additional pattern checks
        seizure_indicators = [
            "seized" in content_lower and ("fbi" in content_lower or "law enforcement" in content_lower),
            "operation" in content_lower and ("seized" in content_lower or "takedown" in content_lower),
            "warrant" in content_lower and "seized" in content_lower,
            "court order" in content_lower and "seized" in content_lower
        ]
        
        is_seized = len(found_keywords) > 0 or any(seizure_indicators)
        
        status = "✅" if is_seized == test_case["should_detect"] else "❌"
        if is_seized == test_case["should_detect"]:
            correct_detections += 1
            
        print(f"{status} {test_case['name']}: {'DETECTED' if is_seized else 'NOT DETECTED'} (Expected: {'DETECTED' if test_case['should_detect'] else 'NOT DETECTED'})")
        if found_keywords:
            print(f"    Keywords found: {found_keywords}")
    
    print(f"\n📊 Keyword Detection Accuracy: {correct_detections}/{len(test_cases)} ({correct_detections/len(test_cases)*100:.1f}%)")
    
    return correct_detections == len(test_cases)

if __name__ == "__main__":
    print("🧅 RF-Lookup Onion Seizure Detection Test")
    print("=" * 60)
    
    # Test keyword detection
    keyword_test_passed = test_seizure_keywords()
    
    # Test actual onion sites (only if Tor is running)
    onion_test_passed = test_onion_seizure_detection()
    
    print(f"\n🎯 Overall Test Results:")
    print("=" * 30)
    print(f"Keyword Detection: {'✅ PASSED' if keyword_test_passed else '❌ FAILED'}")
    print(f"Onion Site Testing: {'✅ PASSED' if onion_test_passed else '❌ FAILED'}")
    
    if keyword_test_passed and onion_test_passed:
        print(f"\n🎉 All tests passed! Onion seizure detection is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the configuration.")
        sys.exit(1)
