import ui
import os
import platform
import shutil

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def get_size(bytes_val):
    """Converts bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0

def show_info():
    lines = []
    
    # OS Info
    lines.append(f"OS Name : {platform.system()} {platform.release()}")
    lines.append(f"Arch    : {platform.machine()}")
    lines.append(f"Python  : {platform.python_version()}")
    lines.append(ui.RULE)
    
    # CPU Info
    if HAS_PSUTIL:
        lines.append(f"CPU Cores : {psutil.cpu_count(logical=False)} Phys / {psutil.cpu_count(logical=True)} Log")
        lines.append(f"CPU Usage : {psutil.cpu_percent()}%")
    else:
        lines.append(f"CPU Cores : {os.cpu_count()} Logical")
        lines.append("CPU Usage : N/A (Requires psutil)")
        
    lines.append(ui.RULE)
    
    # RAM Info
    if HAS_PSUTIL:
        mem = psutil.virtual_memory()
        lines.append(f"RAM Total : {get_size(mem.total)}")
        lines.append(f"RAM Used  : {get_size(mem.used)} ({mem.percent}%)")
    else:
        lines.append("RAM Info  : N/A (Requires psutil)")
        
    lines.append(ui.RULE)
    
    # Storage Info
    total, used, free = shutil.disk_usage("/")
    lines.append(f"Storage Total : {get_size(total)}")
    lines.append(f"Storage Free  : {get_size(free)}")
    
    lines.append(ui.RULE)
    
    # Processes
    if HAS_PSUTIL:
        lines.append(f"Running Procs : {len(psutil.pids())}")
    else:
        lines.append("Running Procs : N/A")

    if not HAS_PSUTIL:
        lines.append(ui.RULE)
        lines.append(ui.red("Tip: Run 'pip install psutil' for full details."))
        
    ui.result("SYSTEM INFORMATION", lines)

def run_menu():
    show_info()