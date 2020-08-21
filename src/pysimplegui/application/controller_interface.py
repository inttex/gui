# Created by hillerj at 20.08.2020
from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def apply_algo(self, input_data):
        pass
