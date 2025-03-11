import paramiko

def ssh_exec_command(host, port, username, password, command):
    # Create an SSH client instance
    ssh = paramiko.SSHClient()
    # Automatically add the remote server's SSH key (only use this for testing or trusted hosts)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the remote host
        ssh.connect(host, port=port, username=username, password=password)
        print(f"Connected to {host}")
        
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Read output and error streams
        output = stdout.read().decode()
        error = stderr.read().decode()
        file_name = f"{host}_result.txt"
    
        # Save the output locally
        with open(file_name, "w") as file:
            file.write(output)

        return output, error
        
    except Exception as e:
        return "", f"Error: {str(e)}"
        
    finally:
        # Ensure the connection is closed
        ssh.close()

if __name__ == "__main__":
    # Define your SSH parameters and command to execute
    host = "10.3.100.210"       # Replace with the target host's IP or hostname
    port = 22                    # Default SSH port
    username = "python"   # Replace with your username
    password = "Python123"   # Replace with your password or use key authentication
    command = "display station all |  include PHNIX|SFBF4_WAR|AP13_KLIA_SFB_GNDPABX|AP22_KLIA_SFB_F4|SFBF4_EAST"  # Replace with the command/script you want to execute

    output, error = ssh_exec_command(host, port, username, password, command)

    if output:
        print("Command Output:")
        print(output)
    if error:
        print("Command Error:")
        print(error)
