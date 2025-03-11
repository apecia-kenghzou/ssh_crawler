#!/usr/bin/env python3
import subprocess
import time

def run_ssh_command(host, command):
    """
    Executes an SSH command on the specified host.
    Make sure that SSH keys are set up or that you handle authentication appropriately.
    """
    # Build the SSH command
    ssh_cmd = ["ssh", host, command]
    
    try:
        # Execute the SSH command and capture the output
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing SSH command: {e}")
        return None, e.stderr

def main():
    # Set your SSH host and command here
    host = "apecia@192.168.8.95"  # Replace with your username and host
    command = "echo Hello from the remote host"  # Replace with your desired command

    print("Executing SSH command...")
    stdout, stderr = run_ssh_command(host, command)
    
    if stdout:
        print("SSH command output:")
        print(stdout)
    if stderr:
        print("SSH command error:")
        print(stderr)
    
    # Delay for the next action
    delay_seconds = 5  # Set the delay (in seconds) before the next action
    print(f"Waiting for {delay_seconds} seconds before proceeding to the next action...")
    time.sleep(delay_seconds)
    
    # Next action after the delay
    print("Proceeding with the next action!")

if __name__ == "__main__":
    main()
