import cpu_scheduling
import file_management
import memory_management
import process_management
import system_info
import ui


def run():
    """Run the top-level menu for the operating-system simulator."""
    while True:
        choice = ui.menu_screen("OS SIMULATOR", [
            "CPU Scheduling",
            "Process Management",
            "Memory Management",
            "File Management",
            "System Information",
            "Exit",
        ])

        if choice == 1:
            cpu_scheduling.run_menu()
        elif choice == 2:
            process_management.run_menu()
        elif choice == 3:
            memory_management.run_menu()
        elif choice == 4:
            file_management.run_menu()
        elif choice == 5:
            system_info.run_menu()
        elif choice == 6:
            ui.box("OS SIMULATOR", ["Exiting..."], animate=False)
            break


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")