#!/usr/bin/env python3
import wexpect
import time
import sys
from datetime import datetime
def clean_output(output, command):
    """Extract output appearing after the specified command"""
    lines = output.split('\n')
    
    # Find the command line (may include shell prompts)
    command_line = None
    for idx, line in enumerate(lines):
        if command in line:  # Look for command anywhere in line
            command_line = idx
            break
    
    if command_line is not None:
        # Return everything after command line, stripping empty lines
        return '\n'.join(lines[command_line+1:]).strip()
    
    # Fallback: return original output if command not found
    return output.strip()
def main():


    print(sys.argv[1])
    # Configuration parameters
    host = sys.argv[1]#"10.3.100.210"
    username = "x" # Replace with ur username
    password = "x" # Replace with ur password
    remote_command = "ping 127.0.0.1"  # Verify this command works on the target OS
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    clean_ip = host.replace('.', '_')  # Replace dots with underscores
    output_file = f"ssh_result_{timestamp}_{clean_ip}.log"
    # Create SSH command
    ssh_command = f"ssh {username}@{host}"

    try:
        # Start SSH process
        child = wexpect.spawn(ssh_command, encoding='utf-8', timeout=10)
        
        # Uncomment for debugging
        #child.logfile = sys.stdout

        # Wait for password prompt (case-insensitive)
        child.expect([r"[Pp]assword:", "password:", "Password:"])
        
        # Send password immediately
        child.sendline(password)
        
        # Wait for shell prompt (adjust pattern for your system)
        #child.expect(r"[\$#>\]] $")  # Common shell prompt patterns
        time.sleep(1)  # Ping with 2s deadline + buffer
        # Execute remote command
        child.sendline(remote_command)
        
        # Wait for command to complete (adjust time as needed)
        time.sleep(1)  # Ping with 2s deadline + buffer
        
        # Capture output
        child.expect(wexpect.EOF, timeout=1)  # Wait for command completion
        output = child.before
        
        # Save to file with timestamp
     
        
    except wexpect.EOF:
        print("Connection closed unexpectedly.")
        print("Last output:", child.before)
    except wexpect.TIMEOUT:
        print("Operation timed out.")
        print("Last output:", child.before)
        with open(output_file, 'w') as f:
            f.write(f"Command executed at {datetime.now()}\n")
            f.write("="*50 + "\n")
            f.write(clean_output(child.before,remote_command))
            f.write("\n" + "="*50 + "\n")
            f.write("End of output\n")
        
        print(f"Successfully saved output to {output_file}")
        print("Command output:\n", child.before)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'child' in locals():
            child.close()

if __name__ == "__main__":
    main()