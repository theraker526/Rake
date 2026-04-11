from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def get_discord_token():
    profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    
    print(f"Using Chrome profile: {profile_path}")
    print("Starting browser...")
    
    o = Options()
    o.add_argument(f'--user-data-dir={profile_path}')
    o.add_argument('--profile-directory=Default')
    o.add_argument('--no-sandbox')
    o.add_argument('--disable-dev-shm-usage')
    o.add_argument('--disable-blink-features=AutomationControlled')
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
        time.sleep(6)
        
        print("Extracting token...")
        token = driver.execute_script("""
            return (webpackChunkdiscord_app.push(
                [[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m
            ).find(m=>m?.exports?.default?.getToken!==void 0)
             .exports.default.getToken()
        """)
        
        driver.quit()
        
        return token
        
    except Exception as e:
        print(f"Error: {e}")
        try:
            driver.quit()
        except:
            pass
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
        print("\nFailed to get token.")
        print("Make sure you're logged into Discord in Chrome.")
