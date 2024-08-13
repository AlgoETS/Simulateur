from abc import ABC, abstractmethod


class NoiseStrategy(ABC):
    @abstractmethod
    def generate_noise(self, price, fluctuation_rate, time_index=None):
        pass
