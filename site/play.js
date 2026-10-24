'use strict';
const canvas=document.querySelector('canvas'), loading=document.querySelector('#loading');
const status=document.querySelector('#loading-status'), progress=document.querySelector('#loading-progress');
function resize(){
 let width=innerWidth,height=innerHeight;
 if(width/height>16/9)width=height*16/9;else height=width*9/16;
 canvas.style.width=width+'px';canvas.style.height=height+'px';
}
addEventListener('resize',resize);resize();
document.querySelector('#retry').addEventListener('click',()=>location.reload());
window.adConfig=()=>{};window.unityInstance=null;
// Same local callback used by the verified build. No remote account or payment calls.
window.domainTimer=setInterval(()=>window.unityInstance?.SendMessage('H5MadKidGames','H5_OnDomainApproved'),100);
Promise.resolve().then(()=>{
 if(!window.localReady)throw Error('存档初始化失败，请确认浏览器允许本站使用本地存储。');
 return window.localReady;
}).then(()=>createUnityInstance(canvas,{
 dataUrl:sandbox?'Build/EBS.sandbox.data':'Build/EBS.standard.data',
 frameworkUrl:'Build/EBS.framework.js',codeUrl:'Build/EBS.wasm',
 streamingAssetsUrl:'StreamingAssets',companyName:'madkidgames.com',
 productName:'Epic Battle Simulator 2',productVersion:'1.11.4',
},value=>{
 progress.value=value;status.textContent='正在加载游戏… '+Math.round(value*100)+'%';
})).then(instance=>{
 window.unityInstance=instance;loading.hidden=true;canvas.focus({preventScroll:true});
}).catch(error=>{
 clearInterval(window.domainTimer);progress.hidden=true;
 status.textContent='游戏加载失败';
 document.querySelector('#loading-hint').textContent=String(error?.message||error);
 document.querySelector('#retry').hidden=false;console.error(error);
});
