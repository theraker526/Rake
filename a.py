import os
import json
import base64
from Crypto.Cipher import AES
import win32crypt
import sqlite3
import shutil

try:
    local_state = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')
    with open(local_state, 'r', encoding='utf-8') as f:
        encrypted_key = json.load(f)['os_crypt']['encrypted_key']
    
    key = win32crypt.CryptUnprotectData(base64.b64decode(encrypted_key)[5:], None, None, None, 0)[1]
    
    db_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    temp_db = 'ChromePasswords.db'
    shutil.copy2(db_path, temp_db)
    
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
    
    print("\n" + "="*100)
    print(f"{'URL':<50} {'USERNAME':<25} {'PASSWORD':<25}")
    print("="*100)
    
    for url, username, encrypted_pass in cursor.fetchall():
        if encrypted_pass:
            try:
                nonce = encrypted_pass[3:15]
                ciphertext = encrypted_pass[15:-16]
                cipher = AES.new(key, AES.MODE_GCM, nonce)
                password = cipher.decrypt(ciphertext).decode(errors='ignore')
                print(f"{url:<50} {username:<25} {password:<25}")
            except Exception as e:
                print(f"{url:<50} {username:<25} [DECRYPT FAILED]")
    
    conn.close()
    os.remove(temp_db)
    print("="*100 + "\n")

except FileNotFoundError:
    print("Chrome not found! Are you sure you're using Chrome?")
except Exception as e:
    print(f"Error: {e}")
