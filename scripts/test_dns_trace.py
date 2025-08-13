#!/usr/bin/env python3
"""
DNS By Eye - DNS Trace Test Script

This script tests the DNS delegation tracing functionality for various domains,
including both working and broken configurations.

Usage:
    python3 scripts/test_dns_trace.py [domain]
    
If no domain is provided, it will test several predefined domains including
the intentionally broken test.apathy.ca domain.

Examples:
    python3 scripts/test_dns_trace.py test.apathy.ca
    python3 scripts/test_dns_trace.py google.com
    python3 scripts/test_dns_trace.py
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import trace_delegation, is_valid_domain
import dns.resolver

def test_domain(domain, verbose=True):
    """Test DNS delegation tracing for a specific domain."""
    print(f"\n{'='*60}")
    print(f"Testing DNS delegation for: {domain}")
    print(f"{'='*60}")
    
    # Validate domain format
    if not is_valid_domain(domain):
        print(f"❌ Invalid domain format: {domain}")
        return False
    
    print(f"✅ Domain format is valid")
    
    try:
        # Perform DNS trace
        trace, chain, timing = trace_delegation(domain, verbose=verbose, debug=True)
        
        # Display results
        print(f"\n📊 Results:")
        print(f"Chain: {' → '.join(chain)}")
        print(f"Trace levels: {len(trace)}")
        
        # Show each level
        for i, node in enumerate(trace):
            zone = node['zone']
            nameservers = node['nameservers']
            response_time = node.get('response_time', 0)
            error_type = node.get('error_type')
            is_slow = node.get('is_slow', False)
            
            print(f"\nLevel {i}: {zone}")
            print(f"  Response time: {response_time}ms {'(SLOW)' if is_slow else ''}")
            
            if error_type:
                print(f"  Error type: {error_type}")
            
            print(f"  Nameservers ({len(nameservers)}):")
            for ns in nameservers[:5]:  # Show first 5
                print(f"    - {ns}")
            if len(nameservers) > 5:
                print(f"    - ... and {len(nameservers) - 5} more")
        
        # Summary
        total_time = sum(node.get('response_time', 0) for node in trace)
        error_count = sum(1 for node in trace if node.get('error_type'))
        
        print(f"\n📈 Summary:")
        print(f"  Total response time: {total_time:.2f}ms")
        print(f"  Levels with errors: {error_count}/{len(trace)}")
        print(f"  Status: {'❌ Has errors' if error_count > 0 else '✅ All levels working'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during DNS trace: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("DNS By Eye - DNS Trace Test Script")
    print("==================================")
    
    # Test domains
    if len(sys.argv) > 1:
        # Test specific domain provided as argument
        domain = sys.argv[1]
        test_domain(domain)
    else:
        # Test predefined domains
        test_domains = [
            "test.apathy.ca",      # Intentionally broken test domain
            "google.com",          # Working domain
            "cloudflare.com",      # Working domain
            "nonexistent.example", # Non-existent domain
        ]
        
        print("Testing multiple domains...")
        
        results = {}
        for domain in test_domains:
            results[domain] = test_domain(domain, verbose=False)
        
        # Final summary
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        
        for domain, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{domain:<25} {status}")

if __name__ == "__main__":
    main()
