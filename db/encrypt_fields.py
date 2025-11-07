"""
Database Field Encryption Module
Provides encryption/decryption for sensitive fields (GDPR/compliance)
NOTE: This is a demonstration module - do not run encrypt_emails() in production without backup
"""
import sqlite3
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def get_or_create_key():
    """Get existing key or create new one"""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print(f"[✓] Created new encryption key: {KEY_FILE}")
    
    with open(KEY_FILE, "rb") as f:
        return f.read()

def get_fernet():
    """Get Fernet cipher instance"""
    key = get_or_create_key()
    return Fernet(key)

def encrypt_field(value):
    """Encrypt a field value"""
    fernet = get_fernet()
    return fernet.encrypt(value.encode()).decode()

def decrypt_field(value):
    """Decrypt a field value"""
    fernet = get_fernet()
    return fernet.decrypt(value.encode()).decode()

def encrypt_emails(dry_run=True):
    """
    Encrypt email addresses in database
    WARNING: Only run in production after backup!
    
    Args:
        dry_run: If True, only shows what would be encrypted
    """
    conn = sqlite3.connect('levqor.db')
    cursor = conn.cursor()
    
    # Find unencrypted emails
    cursor.execute("SELECT id, email FROM users WHERE email NOT LIKE 'enc:%'")
    rows = cursor.fetchall()
    
    if not rows:
        print("[ℹ] No unencrypted emails found")
        conn.close()
        return
    
    print(f"[📋] Found {len(rows)} emails to encrypt")
    
    if dry_run:
        print("[ℹ] DRY RUN - No changes will be made")
        for user_id, email in rows:
            print(f"   Would encrypt: {email}")
        conn.close()
        return
    
    # Perform encryption
    for user_id, email in rows:
        encrypted = "enc:" + encrypt_field(email)
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (encrypted, user_id))
        print(f"[✓] Encrypted: {email}")
    
    conn.commit()
    conn.close()
    print(f"[✓] Encrypted {len(rows)} emails successfully")

if __name__ == "__main__":
    import sys
    
    if "--encrypt" in sys.argv:
        print("[⚠] WARNING: This will encrypt all emails in the database!")
        print("    Make sure you have a backup before proceeding.")
        confirm = input("    Type 'yes' to continue: ")
        if confirm.lower() == "yes":
            encrypt_emails(dry_run=False)
        else:
            print("[✗] Cancelled")
    else:
        encrypt_emails(dry_run=True)
