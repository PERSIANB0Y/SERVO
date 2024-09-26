import threading
import time

gill = 0
stopLoop = False


def loop_function():
    global gill, stopLoop
    while True:
        print(f"gill : {gill}")
        time.sleep(0.1)
        if (stopLoop):
            break

def change_variable():
    global gill, stopLoop
    for i in range(5):
        gill += 1
        time.sleep(1)
    stopLoop = True

loop_thread = threading.Thread(target=loop_function)
loop_thread.daemon = True
loop_thread.start()

change_variable()

print("Main thread is finished, but loop continues running in the background.")
