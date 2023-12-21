from .record import Record
from nmflows.utils.buffer import Buffer
from nmflows.parser.headers import DatalinkHeader, NetworkHeader, TransportHeader


class PktHeaderRecord(Record):

    def __init__(self, rformat, length, hdr_proto, orig_len, stripped, hdr_length,
                 datalink=None, network=None, transport=None):
        assert rformat == Record.FORMAT_RAW_PACKET
        super().__init__(rformat, length)
        self._header_proto = hdr_proto          # protocol type of header that follows
        self._original_length = orig_len        # this is the length of the original packet before sampling
        self._stripped = stripped               # number of bytes removed from original packet
        self._header_length = hdr_length        # this is the length of the header data that follows
        self._datalink = datalink
        self._network = network
        self._transport = transport

    @property
    def original_length(self):
        return self._original_length
    
    @property
    def payload_length(self):
        return (self._datalink.length
                 + self._network.header_length
                 + self._network.payload_length)

    @property
    def datalink(self) -> DatalinkHeader:
        return self._datalink

    @property
    def network(self) -> NetworkHeader:
        return self._network

    @property
    def transport(self) -> TransportHeader:
        return self._transport

    @classmethod
    def from_bytes(cls, rformat, length, data):
        buffer = Buffer.from_bytes(data)
        hdr_proto = buffer.read_uint(0)
        orig_len = buffer.read_uint(4)
        stripped = buffer.read_uint(8)
        header_length = buffer.read_uint(12)
        if hdr_proto == 1:                      # header is Ethernet
            start_of_header = 16
            datalink_data = buffer.read_bytes(start_of_header, header_length)
            datalink = DatalinkHeader.from_bytes(datalink_data)

            start_of_header += datalink.length
            network_data = buffer.read_bytes(start_of_header, header_length - datalink.length)
            network = NetworkHeader.from_bytes(network_data, datalink.ether_type)

            start_of_header += network.length
            transport_data = buffer.read_bytes(start_of_header, header_length - network.length - datalink.length)
            transport = TransportHeader.from_bytes(transport_data, network.upper_proto)
        else:
            raise NotImplementedError('non_ethernet_header_in_sampled_record')

        return cls(rformat, length, hdr_proto, orig_len,
                   stripped, header_length, datalink, network, transport)
