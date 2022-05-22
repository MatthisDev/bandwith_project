import subprocess
import json

connection_data = subprocess.run('speedtest-cli --json', shell=True, capture_output= True)
print(connection_data)
x = json.load(connection_data)
print(x)