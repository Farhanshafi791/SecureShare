#!/usr/bin/env python3
"""
DEPRECATED: Migration script to convert existing files from Fernet to AES encryption
This script is no longer needed as SecureShare now uses AES-256 encryption by default.
Kept for historical reference only.
"""

import sys

def main():
    """Main function that shows deprecation message"""
    print("⚠️  This migration script is DEPRECATED.")
    print("📝 SecureShare now uses AES-256 encryption by default.")
    print("💡 If you need to run migration, please install 'cryptography' package:")
    print("   pip install cryptography")
    print("🔧 Contact support if you need to migrate from legacy Fernet encryption.")
    return False

if __name__ == '__main__':
    main()
    sys.exit(0)
