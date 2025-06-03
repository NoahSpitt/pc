"""Entry point for PC simulator."""

from builder import PCBuilder
from shell_sim import Shell


def main():
    builder = PCBuilder()
    while True:
        print("=== PC Simulator ===")
        print("1. Create configuration")
        print("2. List configurations")
        print("3. Load configuration and start shell")
        print("4. Quit")
        choice = input("Choice: ")
        if choice == '1':
            builder.create_config()
        elif choice == '2':
            for name in builder.list_configs():
                print(name)
        elif choice == '3':
            name = input("Configuration name: ")
            try:
                cfg = builder.load_config(name)
            except FileNotFoundError:
                print("Configuration not found")
                continue
            print(f"Launching shell for {cfg.name}...")
            shell = Shell(cfg.name)
            shell.loop()
        elif choice == '4':
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

