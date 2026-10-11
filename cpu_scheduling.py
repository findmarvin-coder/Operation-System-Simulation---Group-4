import ui

def get_processes():
    ui.prompt_screen("CPU SCHEDULING", ["Enter process details or load sample data.", 
                                        "1. Enter Manually", "2. Load Sample Data"])
    choice = ui.read_int("\nChoice (1-2): ", 1, 2)
    
    procs = []
    if choice == 2:
        procs = [{"pid": "P1", "at": 0, "bt": 5, "pr": 2},
                 {"pid": "P2", "at": 1, "bt": 3, "pr": 1},
                 {"pid": "P3", "at": 2, "bt": 8, "pr": 4},
                 {"pid": "P4", "at": 3, "bt": 6, "pr": 3}]
    else:
        n = ui.read_int("\nNumber of processes: ", 1, 10)
        for i in range(1, n + 1):
            ui.prompt_screen(f"PROCESS {i}", ["Enter Arrival, Burst, Priority (space-separated)", "Example: 0 5 2"])
            while True:
                vals = ui.read_int_list(f"P{i} [AT BT PR]: ")
                if len(vals) >= 3:
                    at, bt, pr = vals[:3]
                    break
                print(ui.red("Error: You must enter at least 3 numbers separated by spaces."))
                
            procs.append({"pid": f"P{i}", "at": at, "bt": bt, "pr": pr})
    return procs

def render_gantt(gantt):
    lines = []
    blocks = []
    times = []
    
    for p, start, end in gantt:
        block = f"| {p} "
        if not blocks:
            times.append(str(start))
        blocks.append(block)
        times.append(str(end))
        
    blocks.append("|")
    
    current_b = ""
    current_t = ""
    for i in range(len(blocks) - 1):
        b = blocks[i]
        t = times[i].ljust(len(b))
        if ui.vlen(current_b) + ui.vlen(b) + 1 > ui.INNER_WIDTH:
            lines.append(current_b + "|")
            lines.append(current_t + times[i])
            lines.append(ui.RULE)
            current_b = ""
            current_t = ""
        current_b += b
        current_t += t
    
    lines.append(current_b + "|")
    lines.append(current_t + times[-1])
    return lines

def display_stats(procs, gantt):
    stats = {}
    for p in procs:
        stats[p["pid"]] = {"at": p["at"], "bt": p["bt"], "pr": p["pr"], "first_start": -1, "ct": 0}
        
    for p, start, end in gantt:
        if p == "IDLE": continue
        if stats[p]["first_start"] == -1:
            stats[p]["first_start"] = start
        stats[p]["ct"] = end
        
    rows = []
    tot_wt = tot_tat = tot_rt = 0
    for p in sorted(procs, key=lambda x: int(x["pid"][1:])):
        s = stats[p["pid"]]
        tat = s["ct"] - s["at"]
        wt = tat - s["bt"]
        rt = s["first_start"] - s["at"]
        tot_wt += wt
        tot_tat += tat
        tot_rt += rt
        rows.append([p["pid"], s["at"], s["bt"], s["pr"], s["ct"], wt, tat, rt])
        
    n = len(procs)
    headers = ["PID", "AT", "BT", "PR", "CT", "WT", "TAT", "RT"]
    
    lines = render_gantt(gantt)
    lines.append(ui.RULE)
    lines.extend(ui.table_lines(headers, rows))
    lines.append(ui.RULE)
    lines.append(f"Avg WT: {tot_wt/n:.2f} | Avg TAT: {tot_tat/n:.2f} | Avg RT: {tot_rt/n:.2f}")
    
    # Split the legend so it neatly fits the box
    lines.append("Legend: CT=Completion, WT=Waiting")
    lines.append("        TAT=Turnaround, RT=Response")
    return lines

def schedule(procs, algo, quantum=None):
    rem = {p["pid"]: p["bt"] for p in procs}
    gantt = []
    time = 0
    completed = 0
    n = len(procs)
    
    ready_q = []
    in_queue = set()
    
    def get_arrived(t):
        return [p for p in procs if p["at"] <= t and rem[p["pid"]] > 0]
        
    while completed < n:
        arrived = get_arrived(time)
        if not arrived:
            if not gantt or gantt[-1][0] != "IDLE":
                gantt.append(["IDLE", time, time+1])
            else:
                gantt[-1][2] += 1
            time += 1
            continue
            
        if algo == "FCFS":
            sel = sorted(arrived, key=lambda x: (x["at"], int(x["pid"][1:])))[0]
            run_time = rem[sel["pid"]]
        elif algo == "SJF":
            sel = sorted(arrived, key=lambda x: (rem[x["pid"]], x["at"], int(x["pid"][1:])))[0]
            run_time = rem[sel["pid"]]
        elif algo == "PRIORITY":
            sel = sorted(arrived, key=lambda x: (x["pr"], x["at"], int(x["pid"][1:])))[0]
            run_time = rem[sel["pid"]]
        elif algo == "RR":
            new_arrived = sorted([p for p in arrived if p["pid"] not in in_queue], 
                                 key=lambda x: (x["at"], int(x["pid"][1:])))
            for p in new_arrived:
                ready_q.append(p)
                in_queue.add(p["pid"])
                
            if not ready_q:
                time += 1
                continue
                
            sel = ready_q.pop(0)
            in_queue.remove(sel["pid"])
            run_time = min(quantum, rem[sel["pid"]])

        pid = sel["pid"]
        
        if gantt and gantt[-1][0] == pid:
            gantt[-1][2] += run_time
        else:
            gantt.append([pid, time, time + run_time])
            
        time += run_time
        rem[pid] -= run_time
        
        if algo == "RR":
            new_arrived = sorted([p for p in get_arrived(time) if p["pid"] not in in_queue and p["pid"] != pid], 
                                 key=lambda x: (x["at"], int(x["pid"][1:])))
            for p in new_arrived:
                ready_q.append(p)
                in_queue.add(p["pid"])
                
            if rem[pid] > 0:
                ready_q.append(sel)
                in_queue.add(pid)
            else:
                completed += 1
        else:
            completed += 1

    ui.result(f"ALGORITHM: {algo}", display_stats(procs, gantt))

def run_menu():
    procs = get_processes()
    while True:
        choice = ui.menu_screen("CPU SCHEDULING", [
            "FCFS", "SJF (Non-Preemptive)", "Round Robin", 
            "Priority Scheduling", "Compare All", "Back"
        ])
        
        if choice == 1: schedule(procs, "FCFS")
        elif choice == 2: schedule(procs, "SJF")
        elif choice == 3: 
            ui.prompt_screen("ROUND ROBIN", ["Enter Time Quantum:"])
            q = ui.read_int("\nQuantum: ", 1)
            schedule(procs, "RR", q)
        elif choice == 4: schedule(procs, "PRIORITY")
        elif choice == 5:
            schedule(procs, "FCFS")
            schedule(procs, "SJF")
            ui.prompt_screen("ROUND ROBIN", ["Enter Time Quantum for comparison:"])
            q = ui.read_int("\nQuantum: ", 1)
            schedule(procs, "RR", q)
            schedule(procs, "PRIORITY")
        elif choice == 6: break