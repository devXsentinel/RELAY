"""
RELAY GUI — Ultra-lightweight Offline Peer-to-Peer Mesh (< 10 KB)
Zero external dependencies (pure Python). E2EE (SHA256-CTR + HMAC-SHA256).
Multi-hop store-and-forward routing, loop prevention, reverse ACKs.
Supports: Direct Computer Wi-Fi Hotspot, Ad-Hoc mesh, Bluetooth PAN, Multi-subnet broadcast.
Usage: python relay_gui.py [CALLSIGN] [SHARED_KEY] [OPTIONAL_PEER_IP]
"""
import socket,threading,time,json,uuid,sys,hashlib,hmac,os,tkinter as tk
from tkinter import scrolledtext
if len(sys.argv)>1 and sys.argv[1].lower() in("-h","--help","help"):
    print("RELAY GUI — Offline Computer Mesh (< 10 KB)\nUsage: python relay_gui.py [CALLSIGN] [KEY] [PEER_IP]")
    sys.exit(0)
GRP,PORT,MH='239.255.37.37',37373,10
nid=sys.argv[1].upper() if len(sys.argv)>1 else "N"+uuid.uuid4().hex[:4].upper()
rk=sys.argv[2] if len(sys.argv)>2 else os.environ.get("RELAY_KEY","RELAY-SEC-V1")
SK=hashlib.sha256(rk.encode()).digest();KT=SK[:3].hex().upper()
dd,pr,om,pip=set(),{},{},set()
if len(sys.argv)>3:pip.add(sys.argv[3])
st={"tx":0,"rx":0,"fwd":0,"ack":0}
MB=hasattr(sys,'getandroidapilevel') or os.environ.get("PYDROID3")
def crypt(b,n):
    ks=b"".join(hashlib.sha256(SK+n+i.to_bytes(4,'big')).digest() for i in range((len(b)+31)//32))
    return bytes(p^k for p,k in zip(b,ks))
def enc_p(t):
    pt,n=t.encode(),os.urandom(8);ct=crypt(pt,n)
    return(n+hmac.new(SK,n+ct,"sha256").digest()[:8]+ct).hex()
def dec_p(h):
    try:
        r=bytes.fromhex(h);n,mc,ct=r[:8],r[8:16],r[16:]
        if not hmac.compare_digest(mc,hmac.new(SK,n+ct,"sha256").digest()[:8]):return None
        return crypt(ct,n).decode()
    except:return None
so=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
so.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
so.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
try:so.setsockopt(socket.SOL_SOCKET,15,1)
except:pass
so.bind(('',PORT))
mq=socket.inet_aton(GRP)+b'\x00'*4
for o,v in[(socket.IP_ADD_MEMBERSHIP,mq),(socket.IP_MULTICAST_LOOP,1)]:
    try:so.setsockopt(socket.IPPROTO_IP,o,v)
    except:pass
def bcast(pk):
    try:
        raw=json.dumps(pk).encode()
        tgs={(GRP,PORT),('255.255.255.255',PORT)}
        try:
            for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
                tgs.add((ip.rsplit('.',1)[0]+'.255',PORT))
        except:pass
        for ip in pip:tgs.add((ip,PORT))
        for tg in tgs:
            try:so.sendto(raw,tg)
            except:pass
    except:pass
root=tk.Tk();root.title(f"RELAY — [{nid}]");root.configure(bg="#0f0f11")
if MB:root.attributes("-fullscreen",True)
else:root.geometry("740x550");root.minsize(500,370)
CB,CX,CA,CD,CF,CR="#18181c","#121214","#00e676","#71717a","#f4f4f5","#27272a"
if MB:FS,FC,FH,FB,Fs,Fi="sans-serif","monospace",12,11,9,10
else:FS,FC,FH,FB,Fs,Fi="Segoe UI","Consolas",14,10,8,11
F8,C8=(FS,Fs,"bold"),(FC,Fs)
hdr=tk.Frame(root,bg=CB,padx=8,pady=6 if MB else 10);hdr.pack(side=tk.TOP,fill=tk.X)
tk.Label(hdr,text="RELAY",font=(FS,FH,"bold"),fg=CA,bg=CB).pack(side=tk.LEFT)
if not MB:tk.Label(hdr,text=" SECURE MESH",font=(FS,8),fg=CD,bg=CB).pack(side=tk.LEFT,pady=4)
tk.Label(hdr,text=f" {nid} ",font=(FC,FB,"bold"),fg=CA,bg="#102e1c",bd=1,relief=tk.SOLID).pack(side=tk.RIGHT,padx=(4,0))
sd=tk.Label(hdr,text="● 0",font=(FC,Fs,"bold"),fg=CD,bg=CB);sd.pack(side=tk.RIGHT,padx=6)
def ophs():
    if sys.platform=='win32':os.system('start ms-settings:network-mobilehotspot')
    elif sys.platform=='linux':os.system('nmcli dev wifi hotspot &')
    lr("⚡ Wi-Fi Signal: Use Computer Hotspot to mesh without router\n",("sy","L"))
tk.Button(hdr,text="⚡ HOTSPOT",font=(FS,Fs,"bold"),bg=CR,fg="#fbbf24",bd=0,padx=6,pady=2,
    activebackground="#3f3f46",cursor="hand2",command=ophs).pack(side=tk.RIGHT,padx=4)
ftr=tk.Frame(root,bg=CX,padx=8,pady=3);ftr.pack(side=tk.BOTTOM,fill=tk.X)
sl=tk.Label(ftr,text="TX:0 RX:0 FWD:0 ACK:0",font=C8,fg=CD,bg=CX);sl.pack(side=tk.LEFT)
tk.Label(ftr,text=f"🔒#{KT}",font=C8,fg=CA,bg=CX).pack(side=tk.RIGHT)
bot=tk.Frame(root,bg=CB,padx=6,pady=6 if MB else 8);bot.pack(side=tk.BOTTOM,fill=tk.X)
cr=tk.Frame(bot,bg=CB);cr.pack(fill=tk.X)
tk.Label(cr,text="TO:",font=(FS,Fs,"bold"),fg="#a1a1aa",bg=CB).pack(side=tk.LEFT)
eo={"bg":CX,"fg":CF,"insertbackground":"#fff","bd":1,"relief":tk.SOLID,"highlightbackground":CR}
de=tk.Entry(cr,font=(FC,Fi,"bold"),width=8 if MB else 12,**eo);de.pack(side=tk.LEFT,padx=(4,6))
me=tk.Entry(cr,font=(FS,Fi),**eo);me.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=(0,6))
def send():
    d,t=de.get().strip().upper(),me.get().strip()
    if not d or not t or d==nid:return
    if '.' in d:pip.add(d)
    me.delete(0,tk.END);pid=uuid.uuid4().hex[:8]
    pk={"t":"msg","i":pid,"f":nid,"o":d,"x":enc_p(t),"h":MH,"p":[nid],"e":time.time()+3600}
    dd.add(pid);om[pid]=(d,t);st["tx"]+=1;upst()
    bcast(pk);pcm(f"YOU → {d} [🔒]","so",t,f"id:{pid[:6]}",True)
me.bind("<Return>",lambda _:send())
tk.Button(cr,text="SEND",bg=CA,fg="#000",font=(FS,Fs,"bold"),bd=0,padx=10 if MB else 16,
    pady=6 if MB else 4,cursor="hand2",activebackground="#059669",command=send).pack(side=tk.RIGHT)
mid=tk.Frame(root,bg="#0f0f11",padx=6,pady=4);mid.pack(fill=tk.BOTH,expand=True)
pv=not MB
pf=tk.Frame(mid,bg=CB,width=140 if not MB else 120,padx=6,pady=6)
if pv:pf.pack(side=tk.LEFT,fill=tk.Y,padx=(0,6))
pf.pack_propagate(False)
ph=tk.Frame(pf,bg=CB);ph.pack(fill=tk.X,pady=(0,4))
tk.Label(ph,text="PEERS",font=(FS,Fs,"bold"),fg="#a1a1aa",bg=CB).pack(side=tk.LEFT)
pc=tk.Label(ph,text="(0)",font=(FC,Fs),fg=CA,bg=CB);pc.pack(side=tk.RIGHT)
pb=tk.Listbox(pf,bg=CX,fg=CF,font=(FC,FB),bd=0,highlightthickness=1,
    highlightbackground=CR,selectbackground=CA,selectforeground="#000",activestyle="none")
pb.pack(fill=tk.BOTH,expand=True,pady=(0,4))
cf=tk.Frame(mid,bg=CB,bd=0);cf.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
def togp():
    global pv;pv=not pv
    if pv:pf.pack(side=tk.LEFT,fill=tk.Y,padx=(0,6),before=cf)
    else:pf.pack_forget()
def ops(_):
    s=pb.curselection()
    if s:
        de.delete(0,tk.END);de.insert(0,pb.get(s[0]).replace("● ","").strip())
        me.focus_set()
        if MB:togp()
pb.bind("<<ListboxSelect>>",ops)
tk.Button(pf,text="SCAN",bg=CR,fg="#e4e4e7",font=(FS,Fs,"bold"),bd=0,pady=3,
    activebackground="#3f3f46",cursor="hand2",command=lambda:[sping(),upui()]).pack(fill=tk.X)
def add_ip():
    v=de.get().strip()
    if '.' in v:
        pip.add(v);sping();lr(f"Linked IP: {v}\n",("sy","L"))
    else:lr("Type IP in TO: and click +IP\n",("md","L"))
tk.Button(pf,text="+ DIRECT IP",bg=CR,fg="#38bdf8",font=(FS,Fs,"bold"),bd=0,pady=3,
    activebackground="#3f3f46",cursor="hand2",command=add_ip).pack(fill=tk.X,pady=(3,0))
if MB:tk.Button(hdr,text="☰",bg=CR,fg=CF,font=(FS,FB,"bold"),bd=0,padx=8,command=togp).pack(side=tk.LEFT,padx=(8,0))
ch=scrolledtext.ScrolledText(cf,bg=CX,fg=CF,font=(FS,FB),bd=0,wrap=tk.WORD,height=6 if MB else 10,
    state=tk.DISABLED,padx=10,pady=8,highlightthickness=1,highlightbackground=CR)
ch.pack(fill=tk.BOTH,expand=True)
ch.tag_config("R",justify="right",rmargin=10);ch.tag_config("L",justify="left",lmargin1=10,lmargin2=10)
ch.tag_config("mh",foreground="#fff",font=(FS,FH-1,"bold"))
for t,c,f in[("si",CA,F8),("so","#fbbf24",F8),("se","#ef4444",F8),("md","#52525b",C8),("ak",CA,(FC,Fs,"bold")),("sy","#38bdf8",C8)]:
    ch.tag_config(t,foreground=c,font=f)
def upst():sl.config(text=f"TX:{st['tx']} RX:{st['rx']} FWD:{st['fwd']} ACK:{st['ack']}")
def lr(t,tg):
    ch.config(state=tk.NORMAL);ch.insert(tk.END,t,tg);ch.see(tk.END);ch.config(state=tk.DISABLED)
def pcm(h,ht,m,ft="",io=False):
    ts,a=time.strftime("%H:%M:%S"),"R" if io else "L"
    lr(f"\n[{ts}] {h}\n",(ht,a));lr(f"{m}\n",("mh",a))
    if ft:lr(f"{ft}\n",("md",a))
def upui():
    global pr;now=time.time()
    pr={p:ts for p,ts in pr.items() if now-ts<=15}
    pb.delete(0,tk.END)
    for p in sorted(pr.keys()):pb.insert(tk.END,f"● {p}")
    cn=len(pr);pc.config(text=f"({cn})");sd.config(text=f"● {cn}",fg=CA if cn else CD)
def sping():bcast({"t":"ping","i":uuid.uuid4().hex[:8],"f":nid,"h":1,"p":[nid],"e":time.time()+10})
def hpkt(data):
    try:pk=json.loads(data.decode())
    except:return
    s=pk.get("f")
    if s and s!=nid:
        np=s not in pr;pr[s]=time.time();root.after(0,upui)
        if np:sping();root.after(0,lambda:lr(f"Discovered: {s}\n",("sy","L")))
    if pk.get("t")=="ping" or(pk.get("f")==nid and pk.get("t")!="ack"):return
    pid=pk.get("i")
    if not pid or nid in pk.get("p",[]) or pid in dd or pk.get("h",0)<=0 or pk.get("e",0)<time.time():return
    dd.add(pid)
    if len(dd)>300:dd.clear()
    pk["p"].append(nid);pk["h"]-=1
    pt=pk.get("t")
    if pt=="msg":
        if pk.get("o")==nid:
            st["rx"]+=1;root.after(0,upst)
            rs=f"via:{' -> '.join(pk['p'])} h:{pk['h']}"
            dc=dec_p(pk.get("x",""))
            if dc is not None:root.after(0,lambda:pcm(f"FROM: {pk['f']} [🔒]","si",dc,rs))
            else:root.after(0,lambda:pcm(f"FROM: {pk['f']} [⚠️]","se","[FAIL]",rs))
            ak={"t":"ack","i":uuid.uuid4().hex[:8],"f":nid,"o":pk["f"],"h":MH,"p":[nid],"r":pid,"e":time.time()+1800}
            dd.add(ak["i"]);bcast(ak)
        else:
            st["fwd"]+=1;upst()
            root.after(0,lambda:lr(f"  ⇄ Relay {pid[:6]}→{pk.get('o')} h:{pk['h']}\n",("md","L")))
            bcast(pk)
    elif pt=="ack":
        if pk.get("o")==nid:
            st["ack"]+=1;root.after(0,upst)
            og=om.get(pk.get("r"));ds=f': "{og[1]}"' if og else ""
            root.after(0,lambda:lr(f"✓ Done→{pk.get('f')}{ds}\n",("ak","R")))
        else:bcast(pk)
run=True
def ll():
    while run:
        try:
            d,a=so.recvfrom(4096)
            if a and a[0] not in('127.0.0.1','0.0.0.0'):pip.add(a[0])
            hpkt(d)
        except:pass
def pl():
    while run:
        try:sping();root.after(0,upui);time.sleep(4)
        except:pass
def oc():
    global run;run=False
    try:so.close()
    except:pass
    root.destroy()
root.protocol("WM_DELETE_WINDOW",oc)
threading.Thread(target=ll,daemon=True).start()
threading.Thread(target=pl,daemon=True).start()
lr(f"Node online [{nid}] Lock#{KT}\n",("sy","L"))
root.mainloop()
