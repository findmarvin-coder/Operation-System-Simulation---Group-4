import ui

processes = {}
next_pid = 101
current_running = None

VALID_TRANSITIONS = {
    "New": ["Ready"],
    "Ready": ["Running"],
    "Running": ["Waiting", "Ready", "Terminated"],
    "Waiting": ["Ready"]
}

def get_state_color(state):
    if state == "Running": return ui.green(state)
    if state == "Terminated": return ui.red(state)
    if state == "Waiting": return ui.red(state)
    return state

def create_process():
    global next_pid
    ui.prompt_screen("CREATE PROCESS", ["Enter the name of the new process."])
    name = ui.read_nonempty("\nProcess Name: ")
    processes[next_pid] = {"name": name, "state": "New"}
    ui.result("SUCCESS", [ui.green(f"Process '{name}' created with PID {next_pid}.")])
    next_pid += 1

def terminate_process():
    global current_running
    ui.prompt_screen("TERMINATE PROCESS", ["Enter the PID of the process to terminate."])
    pid = ui.read_int("\nPID: ")
    
    if pid not in processes:
        ui.result("ERROR", [ui.red("Process not found.")])
        return
        
    processes[pid]["state"] = "Terminated"
    if current_running == pid:
        current_running = None
    ui.result("SUCCESS", [ui.green(f"Process {pid} terminated.")])

def display_processes():
    if not processes:
        ui.result("PROCESS LIST", ["No active processes."])
        return
        
    headers = ["PID", "Process Name", "State"]
    rows = [[str(p), processes[p]["name"], get_state_color(processes[p]["state"])] for p in processes]
    ui.result("PROCESS LIST", ui.table_lines(headers, rows))

def change_state():
    global current_running
    ui.prompt_screen("CHANGE PROCESS STATE", ["Enter PID and select new state."])
    pid = ui.read_int("\nPID: ")
    
    if pid not in processes:
        ui.result("ERROR", [ui.red("Process not found.")])
        return
        
    p = processes[pid]
    current = p["state"]
    if current == "Terminated":
        ui.result("ERROR", [ui.red("Cannot change state of a Terminated process.")])
        return
        
    valid_next = VALID_TRANSITIONS.get(current, []) + ["Terminated"]
    
    ui.prompt_screen(f"CHANGE STATE (PID {pid})", 
                     [f"Current state: {current}", "Valid next states:"] + 
                     [f"- {state}" for state in valid_next])
    
    new_state = ui.read_nonempty("\nNew State: ").capitalize()
    
    if new_state not in valid_next:
        ui.result("ERROR", [ui.red(f"Invalid transition from {current} to {new_state}.")])
        return
        
    if new_state == "Running":
        if current_running is not None and current_running != pid:
            ui.result("ERROR", [ui.red(f"PID {current_running} is already running. Only 1 CPU.")])
            return
        current_running = pid
    elif current == "Running" and new_state != "Running":
        current_running = None
        
    p["state"] = new_state
    ui.result("SUCCESS", [ui.green(f"Process {pid} moved to {new_state}.")])

def lifecycle_demo():
    steps = [
        ("New", "Process is created and resides in memory."),
        ("Ready", "Admitted to the ready queue, waiting for CPU."),
        ("Running", "Scheduler assigns CPU. Process executes."),
        ("Waiting", "Process requests I/O and yields CPU."),
        ("Ready", "I/O completes, returns to ready queue."),
        ("Running", "CPU assigned again. Process finishes work."),
        ("Terminated", "Process completes and releases resources.")
    ]
    
    for state, desc in steps:
        lines = [f"Demo Process State: {get_state_color(state)}", ui.RULE, desc]
        ui.result("STATE TRANSITION DEMO", lines)

def run_menu():
    while True:
        choice = ui.menu_screen("PROCESS MANAGEMENT", [
            "Create Process", "Terminate Process", "Display Processes", 
            "Change Process State", "State Transition Demo", "Back to Main Menu"
        ])
        if choice == 1: create_process()
        elif choice == 2: terminate_process()
        elif choice == 3: display_processes()
        elif choice == 4: change_state()
        elif choice == 5: lifecycle_demo()
        elif choice == 6: break