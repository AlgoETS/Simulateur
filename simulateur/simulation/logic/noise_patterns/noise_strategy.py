import numpy as np
from abc import ABC, abstractmethod
import noise


class NoiseStrategy(ABC):


    @abstractmethod
    def generate_noise(self,price, fluctuation_rate,time_index=None):
        pass