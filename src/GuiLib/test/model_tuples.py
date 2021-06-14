# Created by hillerj at 11.06.2021
from typing import NamedTuple, List

from GuiLib.drawables.drawable_collector import DrawableTuple


class AlgoInput(NamedTuple):
    slider1: float = 0
    slider2: float = 0
    slider3: float = 0


class AlgoResult(NamedTuple):
    txt: str = 'no_result_string'
    drawable_tuples: List[DrawableTuple] = []
    success: bool = False
