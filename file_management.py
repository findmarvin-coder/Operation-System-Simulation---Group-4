import ui

fs = {
    "Documents": {
        "report.txt": "Final project report.",
        "assignment.txt": "Math homework."
    },
    "Programs": {
        "calculator.py": "print(1+1)",
        "quiz.py": "print('Hello')"
    }
}

def resolve_path(path):
    parts = [p for p in path.split("/") if p]
    if not parts: return None, None
    
    current = fs
    for part in parts[:-1]:
        if part in current and isinstance(current[part], dict):
            current = current[part]
        else:
            return None, None
    return current, parts[-1]

def create_file():
    ui.prompt_screen("CREATE FILE", ["Format: Directory/filename.txt (or just filename)"])
    path = ui.read_nonempty("\nFile Path: ")
    parent, name = resolve_path(path)
    
    if parent is None:
        ui.result("ERROR", [ui.red("Directory not found.")])
        return
    if name in parent:
        ui.result("ERROR", [ui.red("File already exists.")])
        return
        
    print("\nEnter content (End with an empty line):")
    content = []
    while True:
        line = input()
        if not line: break
        content.append(line)
        
    parent[name] = "\n".join(content)
    ui.result("SUCCESS", [ui.green(f"File '{name}' created.")])

def read_file():
    ui.prompt_screen("READ FILE", ["Enter path to file."])
    path = ui.read_nonempty("\nFile Path: ")
    parent, name = resolve_path(path)
    
    if parent is not None and name in parent and isinstance(parent[name], str):
        lines = parent[name].split("\n")
        ui.result(f"FILE: {name}", lines)
    else:
        ui.result("ERROR", [ui.red("File not found or is a directory.")])

def delete_item():
    ui.prompt_screen("DELETE", ["Enter path to file or directory."])
    path = ui.read_nonempty("\nPath: ")
    parent, name = resolve_path(path)
    
    if parent is not None and name in parent:
        if isinstance(parent[name], dict) and parent[name]:
            ans = input(f"Directory '{name}' is not empty. Delete? (y/n): ")
            if ans.lower() != 'y':
                ui.result("CANCELLED", ["Deletion cancelled."])
                return
        del parent[name]
        ui.result("SUCCESS", [ui.green(f"'{name}' deleted.")])
    else:
        ui.result("ERROR", [ui.red("Item not found.")])

def create_dir():
    ui.prompt_screen("CREATE DIRECTORY", ["Format: ParentDir/NewDir"])
    path = ui.read_nonempty("\nDirectory Path: ")
    parent, name = resolve_path(path)
    
    if parent is None:
        ui.result("ERROR", [ui.red("Parent directory not found.")])
        return
    if name in parent:
        ui.result("ERROR", [ui.red("Item already exists.")])
        return
        
    parent[name] = {}
    ui.result("SUCCESS", [ui.green(f"Directory '{name}' created.")])

def list_files():
    lines = []
    def traverse(d, indent=""):
        for k, v in d.items():
            if isinstance(v, dict):
                lines.append(f"{indent}{k}/")
                traverse(v, indent + "    ")
            else:
                lines.append(f"{indent}{k}")
                
    traverse(fs)
    if not lines:
        lines = ["File system is empty."]
    ui.result("FILE SYSTEM", lines)

def run_menu():
    while True:
        choice = ui.menu_screen("FILE MANAGEMENT", [
            "Create File", "Read File", "Delete File/Directory", 
            "Create Directory", "List Files", "Back"
        ])
        if choice == 1: create_file()
        elif choice == 2: read_file()
        elif choice == 3: delete_item()
        elif choice == 4: create_dir()
        elif choice == 5: list_files()
        elif choice == 6: break