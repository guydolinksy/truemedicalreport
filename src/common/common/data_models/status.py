from enum import Enum


class Status(str, Enum):
    unassigned = 'unassigned'
    undecided = 'undecided'
    decided = 'decided'
