import paramiko
import os
import re
import pandas as pd

os.chdir(r"C:\Users\**\Desktop\SSH")
# hostname = '172.17.23.2'
username = '**'
password = '**'

# ssh.load_system_host_keys()
with open("lldp.txt", 'w') as w:
    with open("HW_LIST.txt", encoding='utf-8') as f:
        for line in f:
            hostname = line.replace('\n', '')
            w.write(str(hostname))
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command('dis lldp nei bri | no')
            lldp = stdout.read().decode('utf-8')
            w.write(lldp)
            w.write('\n------END------\n')
            ssh.close()
            print("---Connection Closed---")

peer = re.compile(r"^(.*?)\s+(.*?)\s+(.*?)\s+(\d+)$")
hostname = re.compile(r"\<(.*)\>")

lst = []
with open("lldp.txt", encoding = 'utf-8') as f:
    for line in f:
        if hostname.search(line):
            host = hostname.search(line).group(1)

        if peer.search(line):
            localInt = peer.search(line).group(1)
            remoteH = peer.search(line).group(2)
            remoteInt = peer.search(line).group(3)
            lst.append([host, localInt, remoteH, remoteInt])

df = pd.DataFrame(lst, columns =['local-host', 'local-inter', 'remote-host','remote-inter'])
df.to_excel("lldp.xlsx")
print("---Finished---")
