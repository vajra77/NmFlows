

class PeeringMatrixException(Exception):

    def __init__(self, msg):
        reason = f"[matrix]: {msg}"
        super().__init__(reason)
