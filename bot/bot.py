from abc import ABC, abstractmethod

class Bot(ABC):

    @abstractmethod
    def choose_direction(self, snake, opponent, map_size, apple):
        raise NotImplementedError("Needs to be implemented")