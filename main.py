#!/usr/bin/env python3
import wexpect
import time
import sys
import json
from datetime import datetime
import requests
def upload_data(data):
    # Define the URL for the POST request.
    url = "https://192.168.2.45:1880/api/foresight/ups/upload"

    # Example payload data. Adjust this dictionary as needed.
    payload = data

    # Optional headers if you need to specify content type or authentication.
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request with the JSON payload.
        response = requests.post(url, json=payload, headers=headers, verify=False)
        
        # Print the response status code and body.
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
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
def get_json(data):
    lines = data.splitlines()

    # Find the header line that contains the desired table columns.
    header_index = None
    for i, line in enumerate(lines):
        if all(keyword in line for keyword in ["ID", "MAC", "Name", "Group", "IP", "Type", "State"]):
            header_index = i
            break

    if header_index is None:
        print("Table header not found.")
        exit(1)

    # The header line is assumed to be at header_index.
    header_line = lines[header_index].strip()
    # Split header into column names (assumes columns are separated by whitespace).
    headers = header_line.split()

    # Start reading table rows after the header and the following separator line.
    table_data = []
    for line in lines[header_index+2:]:
        stripped = line.strip()
        # Stop when encountering an empty line, a line of dashes, or the "Total" summary.
        if not stripped or stripped.startswith("-") or stripped.startswith("Total"):
            break
        # Split the row into values.
        row_values = stripped.split()
        # Zip headers and values into a dictionary.
        row_dict = dict(zip(headers, row_values))
        table_data.append(row_dict)

    # Output the extracted table data as JSON.
    #upload_data(json.dumps(table_data, indent=2))
    upload_data(table_data)
    
def main():


    print(sys.argv[1])
    # Configuration parameters
    host = sys.argv[1]#"10.3.100.111"
    username = "x" # Replace with ur username
    password = "x" # Replace with ur password
    remote_command = "screen-length 0 temporary"  # Verify this command works on the target 
    remote_command_2 = "display ap all"
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
        print("command 1 done")
        # Wait for command to complete (adjust time as needed)
        time.sleep(1)  # Ping with 2s deadline + buffer
 
        child.sendline(remote_command_2)
        
        print("command 2 done")
        # Wait for command to complete (adjust time as needed)
        #time.sleep(10)  # Ping with 2s deadline + buffer
        
        # Capture output
        child.expect(wexpect.EOF, timeout=10)  # Wait for command completion
        print(child.before)
        child.sendline("")
        output = child.before
        
        # Save to file with timestamp
     
        
    except wexpect.EOF:
        print("Connection closed unexpectedly.")
        print("Last output:", child.before)
    except wexpect.TIMEOUT:
        print("Operation timed out.")
        print("Last output:", child.before)
        get_json(child.before)
        with open(output_file, 'w') as f:
            f.write(f"Command executed at {datetime.now()}\n")
            f.write("="*50 + "\n")
            f.write(child.before)
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