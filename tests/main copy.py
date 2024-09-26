import eel
import threading
import json
import time
from pyfirmata import Arduino, util, OUTPUT

eel.init('web')
jsonFilePath = 'jsonData.json'
board = Arduino('COM11')  # Change COM3 to your Arduino port

Ap = 9
Am = 8
Bp = 7
Bm = 6
current_step = 0
steps_request = 0
acceleration = 0
hold = 0
direction = 0
recordModeState = False
jsonDataExample = "{'time':0, 'direction':1}"

step_sequence = [
    [1, 0, 0, 0],  # Step 1
    [0, 1, 0, 0],  # Step 2
    [0, 0, 1, 0],  # Step 3
    [0, 0, 0, 1]   # Step 4
]

board.digital[Ap].mode = OUTPUT
board.digital[Am].mode = OUTPUT
board.digital[Bp].mode = OUTPUT
board.digital[Bm].mode = OUTPUT




def read_json():
    try:
        with open(jsonFilePath, 'r') as file:
            print(json.load(file))
            return json.load(file)
    except FileNotFoundError:
        return {"event1": {}}
    except ValueError:
        return {"event1": {}}

def write_json(jsonFilePath, data):
    with open(jsonFilePath, 'w') as file:
        json.dump(data, file, indent=4)

def add_step(jsonData):
    print("Adding new data to the last event")
    data = read_json()
    last_event = data[f"event{len(data)}"]
    next_step = f"step{len(last_event) + 1}"
    last_event[next_step] = jsonData
    write_json(jsonFilePath, data)

def add_event(jsonData):
    print("creating new event")
    data = read_json()
    print(f"event{len(data) + 1}")
    data[f"event{len(data) + 1}"] = {}
    write_json(jsonFilePath, data)
    add_step(jsonData)



def doStep():
    global direction, current_step
    current_step = current_step + direction
    if current_step > 3:current_step = 0
    elif current_step < 0:current_step = 3
    board.digital[Ap].write(step_sequence[current_step][0])
    board.digital[Bp].write(step_sequence[current_step][1])
    board.digital[Am].write(step_sequence[current_step][2])
    board.digital[Bm].write(step_sequence[current_step][3])
    time.sleep(0.07)
    board.digital[Ap].write(0)  # || to unlock the motor after turning
    board.digital[Bp].write(0)  # ||
    board.digital[Bm].write(0)  # ||
    board.digital[Am].write(0)  # ||

def holdFL():
    global stopThread
    while (True):
        print(hold)
        doStep()
        if (stopThread): break


@eel.expose
def send_data(jsonData, recordMode):
    global stopThread, direction, steps_request, hold, acceleration, current_step

    data = json.loads(jsonData)
    steps_request = data['steps']
    if (data['hold'] == 1): 
        stopThread = False 
    else :
        stopThread = True 

    print(data)
    print(f"steps request :{steps_request}   hold:{hold}")

    steps_to_move = abs(steps_request)
    direction = 1 if steps_request > 0 else -1

    if (recordMode == True):
        if (recordMode != recordModeState):
            add_ent(data)
        add_step(data)

    for i in range(steps_to_move):
        doStep()
    
    loop_thread = threading.Thread(target=holdFL,daemon=True)
    loop_thread.start()
    

eel.start('index.html', size=(500, 300))
