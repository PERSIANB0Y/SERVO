import json, eel, time
from pyfirmata import Arduino, util, OUTPUT

eel.init('./web')
jsonFilePath = 'jsonData.json'
board = Arduino('COM11')

Cp, Dp, Cm, Dm, Ap, Am, Bp, Bm = 13, 12, 11, 10, 9, 8, 7, 6
current_step, current_step2, recordModeState, Vrecord, Hrecord = 0, 0, False, 0, 0
Hcapacitor, Vcapacitor, Vdir, Hdir = 0, 0, 0, 0
step_sequence = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

for pin in [Cp, Cm, Dp, Dm, Ap, Am, Bp, Bm]:
    board.digital[pin].mode = OUTPUT

def read_json():
    try:
        with open(jsonFilePath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: file not found!")
        return {}
    except ValueError:
        print("Error: Value error in JSON!")
        return {}

def write_json(data):
    with open(jsonFilePath, 'w') as file:
        json.dump(data, file, indent=4)

def add_step(jsonData):
    print("Adding new data to the last event")
    data = read_json()
    last_event_key = f"event{len(data)}"
    if last_event_key not in data:
        print("Error: Event not found!")
        return
    last_event = data[last_event_key]
    next_step_key = f"step{len(last_event) + 1}"
    last_event[next_step_key] = jsonData
    write_json(data)

def add_event(jsonData):
    global event_start_time
    print("Creating new event")
    data = read_json()
    next_event_key = f"event{len(data) + 1}"
    data[next_event_key] = {}
    write_json(data)
    add_step(jsonData)
    

def do_stepH(H):
    global current_step
    current_step = (current_step + H) % 4
    for pin, val in zip([Ap, Bp, Am, Bm], step_sequence[current_step]):
        board.digital[pin].write(val)

def do_stepV(V):
    global current_step2
    current_step2 = (current_step2 + V) % 4
    for pin, val in zip([Cp, Dp, Cm, Dm], step_sequence[current_step2]):
        board.digital[pin].write(val)

@eel.expose
def send_data(jsonData) :
    global recordModeState, event_start_time, Vcapacitor, Hcapacitor, Vdir, Hdir
    
    recordMode = jsonData['recordMode']
    if "V" in jsonData:
        V = jsonData["V"]
        do_stepV(V)

    if "H" in jsonData:
        H = jsonData["H"]
        do_stepH(H)
        
        # Vdir = 0
        # Vcapacitor = 0
        # if recordMode:
        #     if Hdir != H: Hcapacitor = 0
        #     Hdir = H
        #     Hcapacitor = Hcapacitor + H

    if "delay" in jsonData:
        jsonData["delay"] = int(jsonData["delay"])
        print("adding a delay...")


    print(f"Vcapacitor : {Vcapacitor}")
    print(f"Hcapacitor : {Hcapacitor}")

    
    if recordMode:
        if recordMode != recordModeState:
            
            add_event(jsonData)
        else:
            add_step(jsonData)
    
    recordModeState = recordMode

eel.start('index.html', size=(450, 600))

for pin in [Cp, Cm, Dp, Dm, Ap, Am, Bp, Bm]:
    board.digital[pin].write(0)