from lootnika import logging, sout, traceback
from taskstore import Document

from typing import List, Tuple, Dict
import pickle


class WorkerLogMsg:
    def __init__(self, owner:str,  level: int, text: str):
        # assert owner in ['main', 'task'], f'owner must be main or task'

        self.owner = owner
        self.level = level
        self.text = text

