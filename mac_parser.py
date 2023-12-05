from nmflows.utils.mac_directory import MACDirectory
from config import CONFIG

dir = MACDirectory(CONFIG['ixf_url'])

for entry in dir:
    print(entry)