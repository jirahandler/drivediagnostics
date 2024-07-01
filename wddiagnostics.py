#!/usr/bin/env python3
import subprocess
import sys

# Define the drive to check 
drive_path = "/dev/sda" 

def run_smartctl(command, drive_path):
    """Runs smartctl command and handles potential errors."""
    try:
        result = subprocess.run(
            ["smartctl", *command.split(), drive_path],
            capture_output=True,
            text=True
        )
        result.check_returncode()  # Raise exception for non-zero exit codes
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing smartctl: {e}")
        if "Device does not support SCSI SMART commands" in e.stderr:
            print("This drive likely does not support SMART diagnostics.")
        sys.exit(1)
    except FileNotFoundError:
        print("smartctl not found. Please install it (e.g., 'sudo apt install smartmontools').")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    # Basic SMART health check
    health_output = run_smartctl("-H", drive_path)
    print(health_output)
    if "PASSED" not in health_output:
        print("Drive health check FAILED!")
    
    # Detailed SMART information (-x flag)
    info_output = run_smartctl("-x", drive_path)
    print(info_output)

    # Get detailed SMART attributes (-A flag)
    print("\nSMART Attributes:")
    attr_output = run_smartctl("-A", drive_path)
    lines = attr_output.split("\n")
    for line in lines:
        if line.startswith("ID#"):
            print(line)
        elif line.strip():  # Ignore empty lines
            parts = line.split()
            if len(parts) >= 10:  # Check for sufficient number of parts
                attr_id = parts[0]
                attr_name = parts[1]
                attr_value = parts[9]
                print(f"{attr_id:<5} {attr_name:<25} {attr_value}")


if __name__ == "__main__":
    main()

