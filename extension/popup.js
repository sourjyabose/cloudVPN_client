chrome.storage.local.get("status").then((stat)=>{if (stat.status!==undefined) document.getElementById("status").innerHTML=stat.status;if(stat.status=="Connected" || stat.status=="Connecting..."){document.getElementsByTagName("input")[0].checked=true;}});
document.getElementsByTagName("input")[0].addEventListener("change",(ev)=>{if(ev.currentTarget.checked){on();}else{off();}});

chrome.runtime.onMessage.addListener((m,s,sr)=>{document.getElementById("status").innerHTML=m.ack;});

function on(){
        chrome.runtime.sendMessage({signal:"on"});
}
function off(){
        chrome.runtime.sendMessage({signal:"off"});
}
