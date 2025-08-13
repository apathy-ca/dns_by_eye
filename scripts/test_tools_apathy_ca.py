#!/usr/bin/env python3
"""
Simple test script to check DNS trace for tools.apathy.ca
"""

import sys
import os

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from main import trace_delegation, is_valid_domain
    
    domain = 'tools.apathy.ca'
    print(f"Testing domain: {domain}")
    print(f"Domain valid: {is_valid_domain(domain)}")
    print()
    
    try:
        trace, chain, timing = trace_delegation(domain, verbose=False, debug=True)
        print(f"Chain: {' → '.join(chain)}")
        print(f"Trace length: {len(trace)}")
        print()
        
        for i, node in enumerate(trace):
            print(f"Level {i}: {node['zone']}")
            print(f"  Nameservers ({len(node['nameservers'])}):")
            for ns in node['nameservers'][:5]:  # Show first 5
                print(f"    - {ns}")
            if len(node['nameservers']) > 5:
                print(f"    - ... and {len(node['nameservers']) - 5} more")
            print(f"  Response time: {node.get('response_time', 'N/A')}ms")
            print(f"  Error type: {node.get('error_type', 'None')}")
            print()
            
    except Exception as e:
        print(f"DNS trace error: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the dns_by_eye directory")
