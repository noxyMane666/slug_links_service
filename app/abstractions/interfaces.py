from abc import ABC, abstractmethod


class SlugGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass