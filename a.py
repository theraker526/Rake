from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
import tempfile
import shutil

def get_discord_token():
    original_profile = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default')
    temp_profile = os.path.join(tempfile.gettempdir(), 'chrome_temp_profile')

    if os.path.exists(temp_profile):
        shutil.rmtree(temp_profile, ignore_errors=True)
    os.makedirs(os.path.join(temp_profile, 'Default'), exist_ok=True)

    for folder in ['Local Storage', 'Session Storage', 'Cookies']:
        src = os.path.join(original_profile, folder)
        dst = os.path.join(temp_profile, 'Default', folder)
        if os.path.exists(src):
            try:
                shutil.copytree(src, dst)
            except:
                pass

    shutil.copy2(
        os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State'),
        os.path.join(temp_profile, 'Local State')
    )

    o = Options()
    o.add_argument(f'--user-data-dir={temp_profile}')
    o.add_argument('--profile-directory=Default')
    o.add_argument('--no-sandbox')
    o.add_argument('--headless=new')
    o.add_argument('--disable-dev-shm-usage')
    o.add_argument('--disable-blink-features=AutomationControlled')
    o.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    o.add_experimental_option('useAutomationExtension', False)
    
    # Manually point to your existing Chrome binary
    o.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    try:
        # Use ChromeDriver from PATH instead of webdriver-manager
        # since 146 may not be in webdriver-manager yet
        service = Service()  # Uses chromedriver from PATH if available
        
        driver = webdriver.Chrome(service=service, options=o)
        print("Browser started!")
        
        driver.get('https://discord.com/app')
        print("Waiting for Discord...")
        time.sleep(8)
        
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
        print("TOKEN:")
        print("="*60)
        print(token)
        print("="*60)
    else:
        print("Failed.")             .exports.default.getToken()
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
