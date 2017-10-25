
class NoRefMatchException(Exception):
    def __init__(self, sort):
        self.sort = sort
