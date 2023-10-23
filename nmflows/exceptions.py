

class ParserException(Exception):

    def __init__(self, msg):
        super().__init__(f"#parser {msg}")


class EthParserException(ParserException):

    def __init__(self, msg):
        super().__init__(f"#eth {msg}")

class IPParserException(ParserException):

    def __init__(self, msg):
        super().__init__(f"#ip {msg}")
