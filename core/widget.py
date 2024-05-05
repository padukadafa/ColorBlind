from abc import ABC,abstractmethod

class Widget(ABC):
    @abstractmethod
    def render(self):
        raise NotImplementedError