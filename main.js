const {app,BrowserWindow}=require('electron')
app.whenReady().then(()=>{
    windows=new BrowserWindow({width:800,height:600});
    windows.loadFile('main.html')

})