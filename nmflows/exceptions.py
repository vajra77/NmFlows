

class ParserException(Exception):

    def __init__(self, msg):
        super().__init__(f"#parser {msg}")
