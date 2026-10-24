/* Only this loopback page's sandbox IDB copy is edited. No IAP/account flags. */
'use strict';
if(location.origin!=='http://127.0.0.1:8765')throw Error('请使用固定地址 http://127.0.0.1:8765/local.html');
const sandbox=new URLSearchParams(location.search).get('sandbox')!=='0';
const nativeOpen=indexedDB.open.bind(indexedDB), NORMAL='/idbfs', SANDBOX='/idbfs-ebs-local-sandbox-v2';
const nativeWindowOpen=window.open.bind(window);
window.open=(url,...args)=>{if(new URL(url,location.href).origin!==location.origin){console.warn('本地模式阻止外部导航');return null}return nativeWindowOpen(url,...args)};
function request(req){return new Promise((resolve,reject)=>{req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error)})}
function done(tx){return new Promise((resolve,reject)=>{tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error||Error('存档事务中止'))})}
async function openDB(name){const req=nativeOpen(name,21);req.onupgradeneeded=()=>{const db=req.result;if(!db.objectStoreNames.contains('FILE_DATA'))db.createObjectStore('FILE_DATA').createIndex('timestamp','timestamp',{unique:false})};return request(req)}
async function readFiles(name){const db=await openDB(name);try{const s=db.transaction('FILE_DATA').objectStore('FILE_DATA');return await Promise.all([request(s.getAllKeys()),request(s.getAll())])}finally{db.close()}}
window.localReady=(async()=>{
 if(sandbox){
  const db=await openDB(SANDBOX);let tx=db.transaction('FILE_DATA');let count=await request(tx.objectStore('FILE_DATA').count());
  if(!count){
   const names=(await indexedDB.databases()).map(d=>d.name);
   let [keys,values]=names.includes('/idbfs-ebs-local-sandbox-v1')?await readFiles('/idbfs-ebs-local-sandbox-v1'):[[],[]];
   if(!keys.some(k=>String(k).endsWith('/PlayerPrefs')))[keys,values]=await readFiles(NORMAL);
   if(!keys.some(k=>String(k).endsWith('/PlayerPrefs'))){
    const dir='/idbfs/573c4e13a250a56ce7a0928edd2dcd62';
    keys.push(dir,dir+'/PlayerPrefs');values.push({timestamp:new Date(),mode:16895},{timestamp:new Date(),mode:33206,contents:LocalPrefs.fullSandbox()});
   }
   tx=db.transaction('FILE_DATA','readwrite');const finished=done(tx);keys.forEach((key,i)=>tx.objectStore('FILE_DATA').put(values[i],key));await finished;
  }
  tx=db.transaction('FILE_DATA');const s=tx.objectStore('FILE_DATA');const [keys,values]=await Promise.all([request(s.getAllKeys()),request(s.getAll())]);
  const i=keys.findIndex(k=>String(k).endsWith('/PlayerPrefs'));if(i<0)throw Error('沙盒存档缺少 PlayerPrefs');
  const v=values[i];v.contents=LocalPrefs.fullSandbox(v.contents);v.timestamp=new Date();tx=db.transaction('FILE_DATA','readwrite');const finished=done(tx);tx.objectStore('FILE_DATA').put(v,keys[i]);await finished;db.close();
 }
 indexedDB.open=function(name,...rest){return nativeOpen(name===NORMAL&&sandbox?SANDBOX:name,...rest)};
})();
