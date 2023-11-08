from typing import Optional, List, Dict

from .base import Diffable
from .medication import Medication


class Treatment(Diffable):
    destination: Optional[str] = None
    doctors: List[str] = []
    medications: Dict[str, Medication] = {}

