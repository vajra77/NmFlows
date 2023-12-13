from nmflows.peermatrix.peering_flow import PeeringFlow
from abc import ABCMeta, abstractmethod

class Backend(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def store_flows(self, src: PeeringFlow):
        raise NotImplementedError

    @abstractmethod
    def store_peer(self, src: PeeringFlow):
        raise NotImplementedError

    def __repr__(self):
        return "ABS/null"
