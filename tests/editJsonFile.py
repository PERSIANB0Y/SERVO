import json

jsonFilePath = 'jsonData.json'

# Function to read the existing JSON data
def read_json():
    try:
        with open(jsonFilePath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"event1": {}}


# Function to write the updated JSON data
def write_json(jsonFilePath, data):
    with open(jsonFilePath, 'w') as file:
        json.dump(data, file, indent=4)

# Function to append new step to event
def add_step(jsonData):
    print("Adding new data to the last event")
    data = read_json()
    last_event = data[f"event{len(data)}"]
    next_step = f"step{len(last_event) + 1}"
    last_event[next_step] = jsonData
    write_json(jsonFilePath, data)

# Function to create new event
def add_event(jsonData):
    print("creating new event")
    data = read_json()
    print(f"event{len(data) + 1}")
    data[f"event{len(data) + 1}"] = {}
    # data[next_event] = jsonData
    # write_json(jsonFilePath, data)
    write_json(jsonFilePath, data)
    add_step(jsonData)

new_event = input("New event? (y/n): ").strip().lower()
new_step = input("Enter new data (e.g., {'time':0, 'direction':1}): ").strip()
new_step = eval(new_step)

if new_event == "y":
    add_event(new_step) 
else:
    add_step(new_step)

# Read and print the updated data
updated_data = read_json()
print(json.dumps(updated_data, indent=4))