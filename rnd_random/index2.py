from Exscript.util.interact import read_login
from Exscript.protocols import SSH2

account = read_login()              
conn = SSH2()                       
conn.connect('192.168.8.95')     
conn.login(account)  

conn.execute('ping -w 2 192.168.8.80')           

print(conn.response)

conn.send('exit\r')               
conn.close()  