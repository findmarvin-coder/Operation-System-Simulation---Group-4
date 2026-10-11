import ui

def get_data():
    ui.prompt_screen("MEMORY MANAGEMENT", ["1. Enter Manually", "2. Load Sample Data"])
    choice = ui.read_int("\nChoice (1-2): ", 1, 2)
    
    if choice == 2:
        return [100, 500, 200, 300, 600], [212, 417, 112, 426]
    else:
        ui.prompt_screen("MANUAL ENTRY", ["Enter sizes separated by space."])
        blocks = ui.read_int_list("\nMemory Blocks: ")
        procs = ui.read_int_list("Process Sizes: ")
        return blocks, procs

def simulate_memory(algo, blocks_orig, procs):
    blocks = list(blocks_orig) 
    allocations = []
    waiting = []
    total_frag = 0
    
    for i, p_size in enumerate(procs):
        pid = f"P{i+1}"
        assigned_block = -1
        
        if algo == "First Fit":
            for j, b_size in enumerate(blocks):
                if b_size >= p_size:
                    assigned_block = j
                    break
        elif algo == "Best Fit":
            min_frag = float('inf')
            for j, b_size in enumerate(blocks):
                if b_size >= p_size and b_size - p_size < min_frag:
                    min_frag = b_size - p_size
                    assigned_block = j
        elif algo == "Worst Fit":
            max_frag = -1
            for j, b_size in enumerate(blocks):
                if b_size >= p_size and b_size - p_size > max_frag:
                    max_frag = b_size - p_size
                    assigned_block = j
                    
        if assigned_block != -1:
            frag = blocks[assigned_block] - p_size
            total_frag += frag
            allocations.append([pid, p_size, assigned_block+1, blocks[assigned_block], frag, ui.green("Allocated")])
            blocks[assigned_block] = 0 
        else:
            waiting.append(pid)
            allocations.append([pid, p_size, "-", "-", "-", ui.red("WAITING")])
            
    lines = []
    headers = ["Proc", "Size", "Block", "B-Size", "Frag", "Status"]
    lines.extend(ui.table_lines(headers, allocations))
    lines.append(ui.RULE)
    
    if waiting:
        lines.append("Waiting Processes: " + ui.red(", ".join(waiting)))
    else:
        lines.append("Waiting Processes: " + ui.green("None"))
        
    lines.append(f"Total Internal Fragmentation: {total_frag} KB")
    ui.result(f"MEMORY: {algo.upper()}", lines)

def run_menu():
    blocks, procs = get_data()
    while True:
        choice = ui.menu_screen("MEMORY MANAGEMENT", [
            "First Fit", "Best Fit", "Worst Fit", "Compare All", "Back"
        ])
        if choice == 1: simulate_memory("First Fit", blocks, procs)
        elif choice == 2: simulate_memory("Best Fit", blocks, procs)
        elif choice == 3: simulate_memory("Worst Fit", blocks, procs)
        elif choice == 4:
            simulate_memory("First Fit", blocks, procs)
            simulate_memory("Best Fit", blocks, procs)
            simulate_memory("Worst Fit", blocks, procs)
        elif choice == 5: break