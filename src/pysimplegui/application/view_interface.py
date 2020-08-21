# Created by hillerj at 20.08.2020
from abc import ABC, abstractmethod


class ViewInterface(ABC):

    @abstractmethod
    def update_view(self):
        pass
