import {on,off} from "./functions.js"
chrome.runtime.onInstalled.addListener((det)=>{if(det.reason!=="install" && det.reason !=="update") return;});
chrome.runtime.onMessage.addListener((m,s,sr)=>{

    

if (m.signal=="on"){
on();

}else if(m.signal=="off"){
off();
}
});


