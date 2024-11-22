var leftbtn = document.getElementById('left');
var rightbtn = document.getElementById('right');
var upbtn = document.getElementById('up');
var downbtn = document.getElementById('down');
var recordbtn = document.getElementById('recordMode');
var delaybtn = document.getElementById('delaybtn');
var delayinput = document.getElementById('delay').value;
var speedinput = document.getElementById('speed').value;
var isMouseDownL, isMouseDownR, isMouseDownU, isMouseDownD = false;
var timeoutId;
var recordMode = false;
var Hdir, Hcapacitor, Vdir, Vcapacitor = 0

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendCommand(direction) {
    eel.send_data(direction);
    console.log("command sent")
}

delaybtn.addEventListener('click', () => {
    var delayinput = document.getElementById('delay').value;
    sendCommand({"delay":delayinput,"recordMode":recordMode});
    alert("delay added = "+delayinput);
    document.getElementById('delay').value = 0;
});

recordbtn.addEventListener('click', () => {
    recordMode = !recordMode;
    alert("record mode : "+recordMode);
});

leftbtn.addEventListener('mousedown', () => {
    timeoutId = setTimeout(() => {
        Hcapacitor--;
        Hdir = -1;
        isMouseDownL = true;
    }, 500);
});
leftbtn.addEventListener('mouseup', () => {
    clearTimeout(timeoutId);
    if (isMouseDownL == false) Hcapacitor--; Hdir = -1;
    isMouseDownL = false
    console.log("Command cancelled.");
});
rightbtn.addEventListener('mousedown', () => {
    timeoutId = setTimeout(() => {
        Hcapacitor++;
        Hdir = +1;
        isMouseDownR = true;
    }, 500);
});
rightbtn.addEventListener('mouseup', () => {
    clearTimeout(timeoutId);
    if (isMouseDownR == false) Hcapacitor++; Hdir = +1;
    isMouseDownR = false;
});
upbtn.addEventListener('mousedown', () => {
    timeoutId = setTimeout(() => {
        Vcapacitor--; 
        Vdir = -1;
        isMouseDownU = true;
    }, 500);
});
upbtn.addEventListener('mouseup', () => {
    clearTimeout(timeoutId);
    if (isMouseDownR == false) Vcapacitor--; Vdir = -1;
    isMouseDownU = false;
});
downbtn.addEventListener('mousedown', () => {
    timeoutId = setTimeout(() => {
        Vcapacitor++; 
        Vdir = +1;
        isMouseDownD = true;
    }, 500);
});
downbtn.addEventListener('mouseup', () => {
    clearTimeout(timeoutId);
    if (isMouseDownR == false) Vcapacitor++; Vdir = +1;
    isMouseDownD = false;
});


async function holdCheck() {
    while (true) {
        var speedinput = document.getElementById("speed").value;
        
        if (isMouseDownL){
            sendCommand({"H": -1,"speed":speedinput, "recordMode":recordMode}); 
            console.log("<");
        }
        if (isMouseDownR){ 
            sendCommand({"H": 1, "speed":speedinput, "recordMode":recordMode}); 
            console.log(">");
        }
        if (isMouseDownU){
            sendCommand({"V": -1,"speed":speedinput, "recordMode":recordMode}); 
            console.log("<");
        }
        if (isMouseDownD){ 
            sendCommand({"V": 1, "speed":speedinput, "recordMode":recordMode}); 
            console.log(">");
        }
        await delay(speedinput);
    }
}

holdCheck();