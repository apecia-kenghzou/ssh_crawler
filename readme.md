# SSH Command Executor

A Python script to connect to remote hosts via SSH, execute commands, and log outputs. Includes a Windows batch file for multi-IP execution.

## Features

- **SSH Connectivity**: Connect to remote hosts using SSH
- **Remote Command Execution**: Run custom commands on target machines
- **Logging**: Save outputs to timestamped log files
- **Batch Execution**: Execute across multiple IPs using a batch file

## Prerequisites

- Python 3.x
- `wexpect` module (install using):
  ```bash
  pip install wexpect
  ```
  Windows environment for batch file execution (or adapt shell script)

## File Structure
Copy
project-root/
├── main.py          # Main Python script
└── run_ips.bat      # Batch file for multi-IP execution
## Setup
Clone Repository
``` bash
git clone https://your-repository-url.git
```
## Install Dependencies
``` bash
pip install wexpect
```
## Configuration
Update these variables in main.py:

- host/host_list
- username
- password
- remote_command

## Usage
Single IP Execution
``` bash
python main.py 192.168.2.1
```
## Multiple IP Execution (Batch File)
# Contents of main.bat:

``` batch
@echo off
set IP_LIST=192.168.2.1 192.168.2.2 192.168.2.3
for %%I in (%IP_LIST%) do (
    python main.py %%I
)
pause
```
Execute by:

Double-clicking run_ips.bat

## Customization
# SSH Credentials
Modify in main.py:

``` python
username = "your_username"
password = "your_password"
remote_command = "your-custom-command"
```

### IP Management
Update:

IP_LIST in main.bat

## Uses Error to capture the information
License
MIT License

Acknowledgements
Built with Python and wexpect

Inspired by automation needs for multi-device SSH management
