from .mac_entry import MACEntry
from urllib.request import urlopen
import json


class MACDirectory:

    def __init__(self, url):
        self._ixf_url = url
        self._entries = {}
        self._parse()

    def get(self, mac):
        return self._entries[mac]

    def __iter__(self):
        return iter(self._entries.values())

    def _parse(self):
        response = urlopen(self._ixf_url)
        data = json.loads(response.read())
        for member in data['member_list']:
            asnum = member['asnum']
            name = member['name']
            for conn in member['connection_list']:
                if 'vlan_list' in conn.keys():
                    for vlan in conn['vlan_list']:
                        address6 = "undef"
                        if 'ipv4' in vlan.keys():
                            address4 = vlan['ipv4']['address']
                            if len(vlan['ipv4']['mac_addresses']) == 1:
                                mac = vlan['ipv4']['mac_addresses'][0] or None
                                if 'ipv6' in vlan.keys():
                                    address6 = vlan['ipv6']['address']
                                if mac is not None:
                                    entry = MACEntry(mac, asnum, name, address4, address6)
                                    self._entries[mac] = entry
