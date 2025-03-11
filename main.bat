@echo off
rem Batch file to run main.py with a list of IP addresses

rem Define the list of IP addresses
rem example  set IP_LIST=192.168.3.1 192.168.3.2 192.168.3.3
set IP_LIST=192.168.3.1 192.168.3.2 192.168.3.3
for %%I in (%IP_LIST%) do (
    echo Executing for IP: %%I
    python main.py %%I
    rem Optionally, check for errors:
    if errorlevel 1 (
        echo An error occurred with IP: %%I
    )
)

echo All commands executed.
pause
