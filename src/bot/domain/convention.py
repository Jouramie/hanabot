from abc import ABC


class Convention(ABC):
    def __init__(self, name):
        self.name = name
