from netmiko import ConnectHandler
import json
import os
from textfsm import TextFSM
import time

os.chdir('/Users/**/desktop')
# os.chdir('/Users/**/Documents/03_Python/02_ntc-template/ntc-templates/ntc_templates/templates')
# os.environ["NTC_TEMPLATES_DIR"] = '/Users/**/Documents/03_Python/02_ntc-template/ntc-templates/ntc_templates/templates'


seconds = time.time()
result = time.localtime(seconds)
logname = str(result.tm_hour)+'-'+str(result.tm_min)+'-'+str(result.tm_sec)+"-"+"agghw21-log.txt"

agghw21 = {
    'device_type': 'huawei_vrpv8',
    'host':   '172.17.23.2',
    'username': 'HW_admin',
    'password': '**',
    'port' : 22,          # optional, defaults to 22
    'secret': 'secret',     # optional, defaults to ''
    "session_log": logname,
}


net_connect = ConnectHandler(**agghw21)

commands = ['return',
            'terminal command timestamp ',
            "dis ip rou 10.51.0.101",
            "tracert 10.51.0.101",
            "dis ip rou vpn FM_IPVPN5 10.0.0.109",
            "tracert -vpn FM_IPVPN5 10.0.0.109"]

output = net_connect.send_config_set(commands*3)
output = net_connect.send_command("dis users | in ipcorengt")
output = net_connect.send_command('display inter 100GE7/0/0',use_textfsm=True,textfsm_template='huawei_vrp_display_interface.textfsm')

net_connect.disconnect()
print(output)
