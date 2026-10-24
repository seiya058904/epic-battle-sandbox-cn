/* Validated UnityPrf layout observed in this hash-locked build only. */
(function(root){
 'use strict';
 function entries(input){
  const b=Uint8Array.from(input), decoder=new TextDecoder('utf-8',{fatal:true});
  const header=[85,110,105,116,121,80,114,102,0,0,1,0,0,0,16,0];
  if(!header.every((v,i)=>b[i]===v))throw Error('不支持的 PlayerPrefs 头部');
  let p=16;const out=[];
  function take(n){if(p+n>b.length)throw Error('PlayerPrefs 数据截断');const at=p;p+=n;return at}
  while(p<b.length){
   const n=b[take(1)];if(!n||n>=254)throw Error('不支持的存档键格式');
   const key=decoder.decode(b.subarray(take(n),p));const type=b[take(1)];
   const offset=take(type>=254?4:type);const view=new DataView(b.buffer);
   const value=type===254?view.getInt32(offset,true):type===255?view.getFloat32(offset,true):decoder.decode(b.subarray(offset,p));
   out.push({key,type,offset,value});
  }
  return {bytes:b,entries:out};
 }
 function topUp(input){
  const parsed=entries(input), matches=parsed.entries.filter(e=>e.key==='Consumables');
  if(matches.length!==1||matches[0].type!==254||matches[0].value<0)throw Error('未找到唯一有效的本地宝石整数，存档未修改');
  new DataView(parsed.bytes.buffer).setInt32(matches[0].offset,999999999,true);
  return parsed.bytes;
 }
 const troops='AK47 Archer AxeMan Ballista BearRider Berseker Camel CannonMan CatapultMan Chariot Crossbow Giant Gladiator Guard Hwacha Kamikaze Knight M16 Mage MageTower Man Musketeer Ninja OrganGun Pirate ShieldMan SpearMan TrebuchetMan WarElephant Spartan Sentinel SamuraiNEW FireDragonNEW Minigun Rhino Guardian Wolf'.split(' ');
 function fullSandbox(input){
  const header=Uint8Array.from([85,110,105,116,121,80,114,102,0,0,1,0,0,0,16,0]);
  const parsed=entries(input||header), seen=new Set(), replacements=new Map([['Consumables',999999999],['LevelsCompleted',105],['EpicLevelsCompleted',10]]);
  for(const key of troops)replacements.set(key,2);
  for(const key of ['Spartan','Sentinel','SamuraiNEW','FireDragonNEW','Minigun','Rhino','Guardian','Wolf'])replacements.set(key+'Boss',2);
  // Local simulation availability only: never write receipt, IAP or subscription flags.
  for(const key of ['Spartan','Sentinel','Samurai','FireDragon','Minigun','Rhino','Guardian','Wolf'])replacements.set('Locked'+key,0);
  const chunks=[header];
  function integer(key,value){const name=new TextEncoder().encode(key),b=new Uint8Array(name.length+6);b[0]=name.length;b.set(name,1);b[name.length+1]=254;new DataView(b.buffer).setInt32(name.length+2,value,true);return b}
  for(const e of parsed.entries){
   if(seen.has(e.key))throw Error('重复存档键，未修改');seen.add(e.key);
   const start=e.offset-2-new TextEncoder().encode(e.key).length,end=e.offset+(e.type>=254?4:e.type);
   chunks.push(replacements.has(e.key)?integer(e.key,replacements.get(e.key)):parsed.bytes.slice(start,end));
  }
  for(const [key,value]of replacements)if(!seen.has(key))chunks.push(integer(key,value));
  const out=new Uint8Array(chunks.reduce((n,b)=>n+b.length,0));let at=0;for(const b of chunks){out.set(b,at);at+=b.length}return out;
 }
 const api={entries,topUp,fullSandbox,troops};if(typeof module!=='undefined')module.exports=api;else root.LocalPrefs=api;
})(globalThis);
