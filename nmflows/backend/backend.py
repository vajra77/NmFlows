from nmflows.peermatrix.peer_flow import PeerFlow
from abc import ABCMeta, abstractmethod

class Backend(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def store_flows(self, src: PeerFlow):
        raise NotImplementedError

    @abstractmethod
    def store_peer(self, src: PeerFlow):
        raise NotImplementedError

    def __repr__(self):
        return "ABS/null"
