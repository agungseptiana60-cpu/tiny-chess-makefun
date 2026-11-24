import json,os
from urllib.request import Request,urlopen
U=os.environ["MAKEFUN_ENV_URL"]
V={'P':100,'N':320,'B':330,'R':500,'Q':1000,'K':0}
D8=[(a,b)for a in(-1,0,1)for b in(-1,0,1)if a or b]
KN=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
def post(p,b):return json.load(urlopen(Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
def parse(f):
 z=f.split();b=[]
 for c in z[0]:
  if c.isdigit():b+=['.']*int(c)
  elif c!='/':b.append(c)
 return b,z[1]=='w',z[2],-1 if z[3]=='-'else(8-int(z[3][1]))*8+ord(z[3][0])-97
def uci(m):f,t,p=m;return chr(97+f%8)+str(8-f//8)+chr(97+t%8)+str(8-t//8)+(p or"")
def atk(b,s,w):
 x,y=s%8,s//8;P,N,K,Q='PNKQ'if w else'pnkq'
 for ds,ch in((((1,1),(-1,1))if w else((1,-1),(-1,-1)),P),(KN,N),(D8,K)):
  for dx,dy in ds:
   if 0<=x+dx<8 and 0<=y+dy<8 and b[(y+dy)*8+x+dx]==ch:return 1
 for dx,dy in D8:
  nx,ny=x,y
  while 1:
   nx+=dx;ny+=dy
   if not(0<=nx<8 and 0<=ny<8):break
   c=b[ny*8+nx]
   if c!='.':
    if c==Q or c.upper()==('B'if dx and dy else'R')and c.isupper()==w:return 1
    break
 return 0
def gen(b,w,ca,ep):
 ms=[]
 for i,c in enumerate(b):
  if c=='.'or c.isupper()!=w:continue
  x,y=i%8,i//8;u=c.upper()
  if u=='P':
   d=-8 if w else 8;one=i+d;last=0 if w else 7
   pr='q'if one//8==last else''
   if b[one]=='.':
    ms.append((i,one,pr))
    if y==(6 if w else 1)and b[i+2*d]=='.':ms.append((i,i+2*d,''))
   for dx in(-1,1):
    if 0<=x+dx<8:
     t=one+dx
     if(b[t]!='.'and b[t].isupper()!=w)or t==ep:ms.append((i,t,pr))
   continue
  ds=KN if u=='N'else D8 if u in'KQ'else[(1,0),(-1,0),(0,1),(0,-1)]if u=='R'else[(1,1),(1,-1),(-1,1),(-1,-1)]
  for dx,dy in ds:
   nx,ny=x,y
   while 1:
    nx+=dx;ny+=dy
    if not(0<=nx<8 and 0<=ny<8):break
    t=ny*8+nx;v=b[t]
    if v=='.'or v.isupper()!=w:ms.append((i,t,''))
    if v!='.'or u in'NK':break
 k=60 if w else 4;R='R'if w else'r'
 if b[k]==('K'if w else'k'):
  for dr,ch,em,rk in((1,'K',(1,2),3),(-1,'Q',(-1,-2,-3),-4)):
   if(ch if w else ch.lower())in ca and all(b[k+j]=='.'for j in em)and b[k+rk]==R and not any(atk(b,k+j,not w)for j in(0,dr,2*dr)):ms.append((k,k+2*dr,''))
 return ms
def do(st,m):
 b,w,ca,ep=st;f,t,p=m;nb=b[:];c=nb[f];nb[f]='.'
 if c.upper()=='P'and t==ep:nb[t+(8 if w else-8)]='.'
 nb[t]=(p.upper()if w else p)if p else c
 if c.upper()=='K'and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);nb[rt]=nb[rf];nb[rf]='.'
 nc=ca
 if c.upper()=='K':
  for ch in('KQ'if w else'kq'):nc=nc.replace(ch,'')
 for s,ch in((63,'K'),(56,'Q'),(7,'k'),(0,'q')):
  if f==s or t==s:nc=nc.replace(ch,'')
 return nb,not w,nc,t if c.upper()=='P'and abs(t-f)==16 else-1
def leg(st):
 b,w,ca,ep=st
 if('K'if w else'k')not in b:return[]
 return[m for m in gen(b,w,ca,ep)if not atk((n:=do(st,m))[0],n[0].index('K'if w else'k'),not w)]
def ev(b):
 s=0
 for i,c in enumerate(b):
  if c=='.':continue
  x=i%8;y=7-i//8;w=c.isupper();u=c.upper();cx=min(x,7-x);cy=min(y,7-y);a=y if w else 7-y
  bn=a*7+cx*4+12 if u=='P'else(cx+cy)*9-8 if u=='N'else(cx+cy)*5 if u=='B'else(14 if a==6 else 0)+cx*2 if u=='R'else(cx+cy)*2 if u=='Q'else(cx+cy)*10-20
  s+=V[u]+bn if w else-(V[u]+bn)
 return s
N=[0]
class A(Exception):pass
def sr(st,d,a,be):
 b,w,ca,ep=st;N[0]+=1
 if N[0]>6000:raise A
 if d<-2:return ev(b)if w else-ev(b)
 ms=leg(st)
 if not ms:return-99999 if atk(b,b.index('K'if w else'k'),not w)else 0
 if d<=0:
  s=ev(b)if w else-ev(b)
  if s>=be:return be
  a=max(a,s);ms=[m for m in ms if b[m[1]]!='.'or m[2]]
 ms.sort(key=lambda m:-(V.get(b[m[1]].upper(),0)*10-V[b[m[0]].upper()]//10+(900 if m[2]else 0)))
 for m in ms:
  a=max(a,-sr(do(st,m),d-1,-be,-a))
  if a>=be:break
 return a
def ch(fen,lg):
 st=parse(fen);b,w,ca,ep=st;want={uci(m):m for m in leg(st)};cand=[want[u]for u in lg if u in want]
 best=cand[0]
 for d in(1,2,3):
  N[0]=0;bs=-10**9
  try:
   for m in cand:
    sc=-sr(do(st,m),d-1,-10**9,10**9)
    if sc>bs:bs,best=sc,m
  except A:break
 return uci(best)
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":ch(g["fen"],g["legal_moves"])})
