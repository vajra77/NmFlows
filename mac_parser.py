from nmflows.utils.mac_directory import MACDirectory
from config import CONFIG

dir = MACDirectory(CONFIG['ixf_url'])

entry = dir.get('c4:d4:38:81:a3:2b')

print(entry)

#for entry in dir:
#    print(entry)