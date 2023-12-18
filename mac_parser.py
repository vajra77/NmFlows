from nmflows.utils.mac_directory import MACDirectory
from config import CONFIG

macdir = MACDirectory(CONFIG['ixf_url'])

for entry in macdir:
    print(entry)