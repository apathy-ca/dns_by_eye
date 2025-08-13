# DNS By Eye - Scripts Directory

This directory contains diagnostic, testing, and utility scripts for DNS By Eye.

## Scripts Overview

### 🔧 Diagnostic Scripts

#### `debug_graph_generation.py`
**Purpose**: Comprehensive diagnostic tool for graph generation issues.

**What it tests**:
- Graphviz installation and functionality
- File system permissions in the generated directory
- Graph rendering process
- URL generation for static files

**Usage**:
```bash
# Run from DNS By Eye root directory
python3 scripts/debug_graph_generation.py

# Or from within container
docker exec -it dns-by-eye python3 /app/scripts/debug_graph_generation.py
```

**When to use**: When domain graphs are not appearing in the web interface.

---

#### `test_dns_trace.py`
**Purpose**: Test DNS delegation tracing functionality for various domains.

**Features**:
- Tests both working and broken domains
- Validates domain format
- Shows complete delegation chain
- Displays timing and error information
- Supports single domain or batch testing

**Usage**:
```bash
# Test a specific domain
python3 scripts/test_dns_trace.py test.apathy.ca

# Test multiple predefined domains
python3 scripts/test_dns_trace.py

# From container
docker exec -it dns-by-eye python3 /app/scripts/test_dns_trace.py test.apathy.ca
```

**Test domains included**:
- `test.apathy.ca` - Intentionally broken test domain
- `google.com` - Working domain
- `cloudflare.com` - Working domain  
- `nonexistent.example` - Non-existent domain

---

### 🛠️ Utility Scripts

#### `cleanup-generated.sh`
**Purpose**: Clean up generated graph files and temporary data.

**Usage**:
```bash
./scripts/cleanup-generated.sh
```

**What it cleans**:
- Generated PNG graph files
- Temporary Graphviz files
- Old cached data

---

#### `setup-ssl.sh`
**Purpose**: Set up SSL certificates for HTTPS deployment.

**Usage**:
```bash
./scripts/setup-ssl.sh
```

**Requirements**: Certbot and proper domain configuration.

---

#### `troubleshoot.sh`
**Purpose**: General troubleshooting script for common issues.

**Usage**:
```bash
./scripts/troubleshoot.sh
```

**Checks**:
- Container status
- Log files
- Configuration issues
- Network connectivity

---

## Common Use Cases

### 🔍 Debugging Graph Generation Issues

If domain graphs are not appearing:

1. **Run the graph diagnostic**:
   ```bash
   python3 scripts/debug_graph_generation.py
   ```

2. **Check specific domain**:
   ```bash
   python3 scripts/test_dns_trace.py test.apathy.ca
   ```

3. **Clean up old files**:
   ```bash
   ./scripts/cleanup-generated.sh
   ```

### 🧪 Testing DNS Analysis

To verify DNS analysis is working correctly:

1. **Test the broken domain**:
   ```bash
   python3 scripts/test_dns_trace.py test.apathy.ca
   ```
   Expected: Shows 4 delegation levels with broken nameservers

2. **Test a working domain**:
   ```bash
   python3 scripts/test_dns_trace.py google.com
   ```
   Expected: Shows complete delegation chain without errors

3. **Batch test multiple domains**:
   ```bash
   python3 scripts/test_dns_trace.py
   ```

### 🐛 General Troubleshooting

For general issues:

1. **Run troubleshooting script**:
   ```bash
   ./scripts/troubleshoot.sh
   ```

2. **Check container logs**:
   ```bash
   docker logs dns-by-eye
   ```

3. **Verify configuration**:
   ```bash
   docker exec -it dns-by-eye python3 -c "from config import Config; print(vars(Config))"
   ```

## Script Development Guidelines

### Adding New Scripts

1. **Place in appropriate category**:
   - Diagnostic scripts: Test functionality and identify issues
   - Utility scripts: Perform maintenance tasks
   - Test scripts: Validate specific features

2. **Include proper documentation**:
   - Docstring explaining purpose
   - Usage examples
   - Expected output

3. **Make scripts executable**:
   ```bash
   chmod +x scripts/your_script.sh
   ```

4. **Use proper shebang**:
   - Python scripts: `#!/usr/bin/env python3`
   - Shell scripts: `#!/bin/bash`

### Best Practices

- **Error handling**: Include try/catch blocks and meaningful error messages
- **Verbose output**: Show progress and results clearly
- **Cleanup**: Remove temporary files after use
- **Documentation**: Update this README when adding new scripts

## Environment Variables

Scripts may use these environment variables:

- `STATIC_URL_PATH`: URL path for static files (default: `/static`)
- `DNS_TIMEOUT`: DNS query timeout in seconds
- `LOG_LEVEL`: Logging level for debug output

## Dependencies

Scripts require these Python packages:
- `dnspython` - DNS operations
- `graphviz` - Graph generation
- `flask` - Web framework (for URL generation)

System dependencies:
- `graphviz` - Graph rendering engine
- `bash` - Shell script execution

## Troubleshooting Scripts

If scripts fail to run:

1. **Check Python path**:
   ```bash
   python3 -c "import sys; print(sys.path)"
   ```

2. **Verify dependencies**:
   ```bash
   python3 -c "import dns.resolver, graphviz; print('Dependencies OK')"
   ```

3. **Check permissions**:
   ```bash
   ls -la scripts/
   ```

4. **Run from correct directory**:
   Scripts should be run from the DNS By Eye root directory.

---

For more information, see the main DNS By Eye documentation.
