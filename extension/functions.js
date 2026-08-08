export function on(){
chrome.storage.local.set({"status":"Connecting..."});
chrome.runtime.sendMessage({ack:"Connecting..."});
chrome.proxy.settings.set(
    {
        value:{mode:"fixed_servers",
               rules:{
                singleProxy:{
                    scheme:"http",
                    host:"127.0.0.1",
                    port:8080
                }
               }
        },
        scope:"regular",
    },()=>{}
);
chrome.storage.local.set({"status":"Connected"});
chrome.runtime.sendMessage({ack:"<span style='color:blue;'>Connected</span>"});
}

export function off(){
chrome.storage.local.set({"status":"Disconnected"});
chrome.runtime.sendMessage({ack:"<span style='color:red;'>Disconnected</span>"});
chrome.proxy.settings.set(
    {
        value:{mode:"direct"
               
               
        },
        scope:"regular",
    },()=>{}
);
}