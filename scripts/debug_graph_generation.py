#!/usr/bin/env python3
"""
Debug script to test graph generation for tools.apathy.ca
This script helps identify why domain graphs might not be appearing.
"""

import os
import sys
import tempfile
import time
import random
from graphviz import Digraph

def test_graphviz_availability():
    """Test if Graphviz is properly installed and working."""
    print("=== Testing Graphviz Availability ===")
    try:
        # Test basic Graphviz functionality
        with tempfile.NamedTemporaryFile(suffix='.gv', delete=False) as tmp_file:
            tmp_name = tmp_file.name
            
        test_dot = Digraph()
        test_dot.node('test', 'test')
        test_dot.render(tmp_name, format='png', cleanup=True)
        
        # Check if PNG was created
        png_file = tmp_name + '.png'
        if os.path.exists(png_file):
            print("✅ Graphviz is working - PNG file created")
            # Clean up test files
            try:
                os.remove(png_file)
            except:
                pass
            try:
                os.remove(tmp_name)
            except:
                pass
            return True
        else:
            print("❌ Graphviz failed - PNG file not created")
            return False
                
    except Exception as e:
        print(f"❌ Graphviz error: {e}")
        return False

def test_directory_permissions():
    """Test if the generated directory is writable."""
    print("\n=== Testing Directory Permissions ===")
    
    generated_dir = "app/static/generated"
    
    # Check if directory exists
    if not os.path.exists(generated_dir):
        print(f"❌ Directory {generated_dir} does not exist")
        return False
    
    # Test write permissions
    try:
        test_file = os.path.join(generated_dir, "test_write.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"✅ Directory {generated_dir} is writable")
        return True
    except Exception as e:
        print(f"❌ Directory {generated_dir} write error: {e}")
        return False

def test_graph_generation_for_domain(domain="tools.apathy.ca"):
    """Test graph generation for a specific domain."""
    print(f"\n=== Testing Graph Generation for {domain} ===")
    
    try:
        # Simulate the graph generation logic from main.py
        dot = Digraph(comment=f'DNS Delegation Graph for {domain}')
        dot.attr(rankdir='TB')
        dot.attr('graph', dpi='96')
        dot.attr('node', fontsize='10')
        
        # Add some test nodes (simulating a DNS trace)
        dot.node(domain, domain, shape='box', style='filled', fillcolor='lightblue')
        dot.node('ns1.example.com', 'ns1.example.com')
        dot.node('ns2.example.com', 'ns2.example.com')
        dot.edge(domain, 'ns1.example.com')
        dot.edge(domain, 'ns2.example.com')
        
        # Generate filename like in main.py
        timestamp = str(int(time.time()))
        random_id = str(random.randint(1000, 9999))
        filename = domain.replace('.', '_') + '_test_' + timestamp + '_' + random_id
        
        # Try to render
        graph_path = "app/static/generated/" + filename
        dot.render(graph_path, format='png', cleanup=True)
        
        # Check if file was created
        png_file = graph_path + '.png'
        if os.path.exists(png_file):
            file_size = os.path.getsize(png_file)
            print(f"✅ Graph generated successfully: {filename}.png ({file_size} bytes)")
            
            # Clean up test file
            os.remove(png_file)
            return True
        else:
            print(f"❌ Graph file not created: {filename}.png")
            return False
            
    except Exception as e:
        print(f"❌ Graph generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_url_generation():
    """Test URL generation for static files."""
    print("\n=== Testing URL Generation ===")
    
    try:
        # This would normally use Flask's url_for, but we'll simulate it
        static_url_path = os.environ.get('STATIC_URL_PATH', '/static')
        test_filename = 'generated/test_file.png'
        
        if static_url_path == '/static':
            expected_url = f"/static/{test_filename}"
        else:
            expected_url = f"{static_url_path}/{test_filename}"
            
        print(f"✅ Static URL path: {static_url_path}")
        print(f"✅ Expected URL format: {expected_url}")
        return True
        
    except Exception as e:
        print(f"❌ URL generation error: {e}")
        return False

def main():
    """Run all diagnostic tests."""
    print("DNS By Eye - Graph Generation Diagnostic")
    print("=" * 50)
    
    tests = [
        test_graphviz_availability,
        test_directory_permissions,
        test_graph_generation_for_domain,
        test_url_generation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    if all(results):
        print("✅ All tests passed - Graph generation should work")
    else:
        print("❌ Some tests failed - Graph generation may not work")
        print("\nFailed tests indicate potential issues with:")
        if not results[0]:
            print("- Graphviz installation or configuration")
        if not results[1]:
            print("- File system permissions in generated directory")
        if not results[2]:
            print("- Graph rendering process")
        if not results[3]:
            print("- URL generation for static files")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
