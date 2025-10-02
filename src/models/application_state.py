from dataclasses import dataclass, field
from typing import List


@dataclass
class ApplicationState:
    imported_files: List[str] = field(default_factory=list)
    intensity: float = 1.0
    iterations: int = 1
