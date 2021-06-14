# Created by hillerj at 20.08.2020
from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def init_files_input(self, input, callback):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def run_algo(self, algo_input, visual_result_callback):
        pass
