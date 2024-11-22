import json, eel
from pyfirmata import Arduino, util, OUTPUT

eel.init('web')
jsonFilePath = 'jsonData.json'
board = Arduino('COM11')

Cp, Dp, Cm, Dm, Ap, Am, Bp, Bm = 13, 12, 11, 10, 9, 8, 7, 6
current_step, current_step2= 0, 0
step_sequence = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

for pin in [Cp, Cm, Dp, Dm, Ap, Am, Bp, Bm]:
    board.digital[pin].mode = OUTPUT

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
def saveJson(jsonData):
    print("saveJson() called...  params:",jsonData)    
    try:
        with open('jsonData.json', 'w') as json_file:
            json.dump(jsonData, json_file, indent=4)
        print("JSON data saved successfully.")
    except Exception as e:
        print("Error saving JSON:", e)

@eel.expose
def doStep(direction):
    print("doStep() called")
    print(f"step request received to {direction}")
    if direction == "left": do_stepH(-1)
    if direction == "right": do_stepH(1)
    if direction == "down": do_stepV(-1)
    if direction == "up": do_stepV(1)

@eel.expose
def do_move():
    print("do_move() called")

eel.start('index.html', size=(1500, 900))

for pin in [Cp, Cm, Dp, Dm, Ap, Am, Bp, Bm]:
    board.digital[pin].write(0)
    print("motors turned off")