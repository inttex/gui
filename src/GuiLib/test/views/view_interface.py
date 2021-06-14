# Created by hillerj at 23.09.2020
from abc import ABC, abstractmethod


class AbstractView(ABC):
    @abstractmethod
    def run_view(self):
        pass