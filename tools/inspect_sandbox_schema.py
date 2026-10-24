"""Read-only hash-locked metadata inspection. No WASM execution or code modification.
IL2CPP metadata layouts checked against official Perfare/Il2CppDumper sources.
Output is a local analysis file, not a game patch.
"""
import struct,json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
import UnityPy,hashlib
assert hashlib.sha256((r/'Build/EBS.wasm').read_bytes()).hexdigest()=='4bd3a7a9e740c0a876ef25a11e4f108eacff3a2d6c49326d65610fd72b2f42e1'
env=UnityPy.load(str(r/'Build/EBS.data'));m=next(iter(env.files.values())).files['Il2CppData/Metadata/global-metadata.dat'].bytes
assert struct.unpack_from('<II',m)==(0xFAB11BAF,31)
w=(r/'Build/EBS.wasm').read_bytes()
u=lambda b,p:struct.unpack_from('<I',b,p)[0]
def leb(b,p):
 n=s=0
 while True:
  v=b[p];p+=1;n|=(v&127)<<s;s+=7
  if v<128:return n,p
mem=bytearray(32*1024*1024);p=8
while p<len(w):
 sid=w[p];n,p=leb(w,p+1);end=p+n
 if sid==11:
  count,p=leb(w,p)
  for i in range(count):
   flag,p=leb(w,p);assert flag==0
   assert w[p]==65;addr,p=leb(w,p+1);assert w[p]==11;p+=1
   size,p=leb(w,p);mem[addr:addr+size]=w[p:p+size];p+=size
  print('segments',count)
 p=end
so,ss=struct.unpack_from('<II',m,8+2*8);to,ts=struct.unpack_from('<II',m,8+19*8);fo,fs=struct.unpack_from('<II',m,8+11*8)
assert ts%88==0
num=ts//88
s=lambda n:m[so+n:m.index(0,so+n)].decode()
types=[]
for i in range(num):
 p=to+i*88
 types.append(dict(name=s(u(m,p)),index=i,byval=u(m,p+8),fieldStart=u(m,p+32),fieldCount=struct.unpack_from('<H',m,p+68)[0],methodStart=u(m,p+36),methodCount=struct.unpack_from('<H',m,p+64)[0]))
print('types',num)
candidates=[]
needle=struct.pack('<I',num);pos=mem.find(needle)
while pos>=0:
 if pos>=40 and u(mem,pos+8)==num:
  base=pos-40;words=struct.unpack_from('<16I',mem,base)
  if 0<words[6]<1000000 and 0<words[7]<len(mem):candidates.append((base,words))
 pos=mem.find(needle,pos+1)
print('registration',candidates)
assert len(candidates)==1
base,words=candidates[0];table=words[7]
primitives={2:'bool',8:'int',9:'uint',12:'float',14:'string',28:'object'}
def ty(ptr):
 data,bits=struct.unpack_from('<II',mem,ptr);kind=bits>>16&255
 name=primitives.get(kind,str(kind))
 if kind in (17,18):name=types[data]['name']
 if kind==29:name=ty(data)[0]+'[]'
 return name,bits&65535
out={}
for t in types:
 if t['name'] not in ['Level_Manager','LevelValues','ArmyInspector','StatsValues','LevelDesignValues','LevelDesign','LevelSetUp','ArmyBalance']:continue
 fields=[]
 for i in range(t['fieldStart'],t['fieldStart']+t['fieldCount']):
  nameidx,ti,token=struct.unpack_from('<III',m,fo+i*12);name,attrs=ty(u(mem,table+ti*4));fields.append(dict(name=s(nameidx),type=name,attrs=hex(attrs)))
 out[t['name']]={**t,'fields':fields}
print('schema saved')
dest=r/'output/analysis';dest.mkdir(parents=True,exist_ok=True)
(dest/'field-schema.json').write_text(json.dumps(out,indent=2))
