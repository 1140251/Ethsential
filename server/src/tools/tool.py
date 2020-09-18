from abc import ABC, abstractmethod


class Tool(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, str):
        pass

    @property
    def image(self):
        raise NotImplementedError

    @property
    def command(self):
        raise NotImplementedError

    @property
    def lang_supported(self):
        raise NotImplementedError
