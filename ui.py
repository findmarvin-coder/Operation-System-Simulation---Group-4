import os
import sys
import time
import re

# Constants
WIDTH = 56
INNER_WIDTH = 52
TYPE_DELAY = 0.005
MAX_TYPE_SECONDS = 1.5
RULE = "<RULE>"

# Enable ANSI on Windows
COLOR = sys.stdout.isatty()
if COLOR and os.name == "nt":
    os.system("")
if os.name == "nt" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def green(text):
    return f"\033[92m{text}\033[0m" if COLOR else str(text)

def red(text):
    return f"\033[91m{text}\033[0m" if COLOR else str(text)

def vlen(text):
    """Visible length of text, ignoring ANSI escape codes."""
    return len(re.sub(r'\033\[[0-9;]*m', '', str(text)))

def ansi_wrap(text, width=INNER_WIDTH):
    """Wraps text strictly to width, maintaining active ANSI colors."""
    lines = []
    current_line = ""
    current_len = 0
    current_color = ""
    
    parts = re.split(r'(\033\[[0-9;]*m)', str(text))
    for part in parts:
        if part.startswith('\033'):
            current_color = part
            current_line += part
        else:
            while part:
                space_left = width - current_len
                if len(part) <= space_left:
                    current_line += part
                    current_len += len(part)
                    part = ""
                else:
                    current_line += part[:space_left]
                    lines.append(current_line)
                    part = part[space_left:]
                    current_line = current_color
                    current_len = 0
    if current_len > 0 or not lines:
        lines.append(current_line)
    return lines

def clear():
    """Clear the terminal completely."""
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write('\033[2J\033[3J\033[H')
        sys.stdout.flush()

def tprint(text, delay=TYPE_DELAY, animate=True):
    """Typewriter print that fires ANSI codes instantly."""
    if not animate or os.environ.get("OSSIM_NO_TYPEWRITER") == "1":
        sys.stdout.write(text)
        return

    parts = re.split(r'(\033\[[0-9;]*m)', text)
    for part in parts:
        if part.startswith('\033'):
            sys.stdout.write(part)
        else:
            for char in part:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)

def box(title, lines, animate=True):
    """Draws a width-56 ASCII box containing the given lines."""
    clear()
    
    processed_lines = []
    for line in lines:
        if line == RULE:
            processed_lines.append(RULE)
        else:
            processed_lines.extend(ansi_wrap(line, INNER_WIDTH))

    total_chars = sum(vlen(l) for l in processed_lines if l != RULE)
    delay = TYPE_DELAY
    if animate and total_chars > 0 and total_chars * delay > MAX_TYPE_SECONDS:
        delay = MAX_TYPE_SECONDS / total_chars

    sys.stdout.write("┌" + "─" * (WIDTH - 2) + "┐\n")
    sys.stdout.write("│ " + title.center(INNER_WIDTH) + " │\n")
    sys.stdout.write("├" + "─" * (WIDTH - 2) + "┤\n")
    sys.stdout.flush()

    for line in processed_lines:
        if line == RULE:
            sys.stdout.write("├" + "─" * (WIDTH - 2) + "┤\n")
        else:
            padding = " " * (INNER_WIDTH - vlen(line))
            sys.stdout.write("│ ")
            tprint(line, delay, animate)
            sys.stdout.write(padding + " │\n")
        sys.stdout.flush()

    sys.stdout.write("└" + "─" * (WIDTH - 2) + "┘\n")
    sys.stdout.flush()

def menu_screen(title, options):
    """Displays an instant menu box and gets a valid choice."""
    lines = [f"{i+1}. {opt}" for i, opt in enumerate(options)]
    box(title, lines, animate=False)
    
    while True:
        try:
            choice = int(input("\nSelect an option: "))
            if 1 <= choice <= len(options):
                return choice
            print(red(f"Please enter a number between 1 and {len(options)}."))
        except ValueError:
            print(red("Invalid input. Please enter a number."))

def prompt_screen(title, lines, animate=False):
    box(title, lines, animate)

def result(title, lines):
    box(title, lines, animate=True)
    pause()

def pause():
    input("\nPress Enter to continue...")

def table_lines(headers, rows):
    """Generates evenly spaced columns to perfectly fit 52 characters."""
    col_widths = [max(vlen(str(item)) for item in col) for col in zip(headers, *rows)]
    
    total_content = sum(col_widths)
    num_gaps = len(headers) - 1
    
    if num_gaps > 0 and total_content < INNER_WIDTH:
        base_gap = (INNER_WIDTH - total_content) // num_gaps
        extra = (INNER_WIDTH - total_content) % num_gaps
    else:
        base_gap = 1
        extra = 0

    def format_row(row):
        line = ""
        for i, item in enumerate(row):
            s = str(item)
            if i < len(row) - 1:
                pad = base_gap + (1 if i < extra else 0)
                line += s.ljust(col_widths[i] + pad)
            else:
                line += s.ljust(col_widths[i])
        return line[:INNER_WIDTH]

    lines = [format_row(headers), RULE]
    for row in rows:
        lines.append(format_row(row))
    return lines

def read_int(prompt, min_val=0, max_val=float('inf')):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val: return val
            print(red(f"Must be between {min_val} and {max_val}."))
        except ValueError:
            print(red("Please enter a valid integer."))

def read_int_list(prompt):
    while True:
        try:
            parts = input(prompt).strip().split()
            if not parts: raise ValueError
            return [int(x) for x in parts]
        except ValueError:
            print(red("Please enter space-separated integers."))

def read_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val: return val
        print(red("Input cannot be empty."))