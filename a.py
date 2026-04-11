from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import tempfile
import shutil

def get_discord_token():
    original_profile = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default')
    temp_profile = os.path.join(tempfile.gettempdir(), 'chrome_temp_profile')
    
    print("Copying Chrome profile to temp location...")
    
    if os.path.exists(temp_profile):
        shutil.rmtree(temp_profile, ignore_errors=True)
    
    os.makedirs(temp_profile, exist_ok=True)
    
    folders_to_copy = [
        'Local Storage',
        'Session Storage',
        'Cookies',
        'Login Data',
        'Web Data',
    ]
    
    for folder in folders_to_copy:
        src = os.path.join(original_profile, folder)
        dst = os.path.join(temp_profile, 'Default', folder)
        if os.path.exists(src):
            try:
                shutil.copytree(src, dst)
                print(f"  ✓ Copied {folder}")
            except Exception as e:
                print(f"  ✗ Failed to copy {folder}: {e}")
    
    local_state_src = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')
    local_state_dst = os.path.join(temp_profile, 'Local State')
    shutil.copy2(local_state_src, local_state_dst)
    print("  ✓ Copied Local State")
    
    print("\nStarting headless browser...")
    
    o = Options()
    o.add_argument(f'--user-data-dir={temp_profile}')
    o.add_argument('--profile-directory=Default')
    o.add_argument('--headless=new')
    o.add_argument('--no-sandbox')
    o.add_argument('--disable-dev-shm-usage')
    o.add_argument('--disable-blink-features=AutomationControlled')
    o.add_argument('--disable-gpu')
    o.add_argument('--window-size=1920,1080')
    o.add_argument('--remote-debugging-port=9222')
    o.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    o.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    o.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=o
        )
        
        print("Opening Discord...")
        driver.get('https://discord.com/app')
        
        print("Waiting for Discord to load...")
        time.sleep(8)
        
        print("Extracting token...")
        token = driver.execute_script("""
            return (webpackChunkdiscord_app.push(
                [[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m
            ).find(m=>m?.exports?.default?.getToken!==void 0)
             .exports.default.getToken()
        """)
        
        driver.quit()
        shutil.rmtree(temp_profile, ignore_errors=True)
        
        return token
        
    except Exception as e:
        print(f"Error: {e}")
        try:
            driver.quit()
        except:
            pass
        shutil.rmtree(temp_profile, ignore_errors=True)
        return None

if __name__ == '__main__':
    token = get_discord_token()
    
    if token:
        print("\n" + "="*60)
        print("TOKEN FOUND:")
        print("="*60)
        print(token)
        print("="*60)
    else:
        print("\nFailed.")
        print("Discord may have detected headless mode and blocked the session.")
        print("Just use F12 in Discord and run the JavaScript.")
