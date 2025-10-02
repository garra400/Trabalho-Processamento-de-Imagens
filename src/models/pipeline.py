from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal


Category = Literal["color", "filter", "edge", "binary", "morphology"]


@dataclass
class PipelineStep:
    category: Category
    method: str
    params: Dict[str, Any] = field(default_factory=dict)

    def display_text(self) -> str:
        p = ", ".join(f"{k}={v}" for k, v in self.params.items())
        return f"{self.category}:{self.method}({p})" if p else f"{self.category}:{self.method}"


@dataclass
class Pipeline:
    steps: List[PipelineStep] = field(default_factory=list)
    saved_snapshot: List[PipelineStep] = field(default_factory=list)

    def add_step(self, step: PipelineStep) -> None:
        self.steps.append(step)

    def delete_step(self, index: int) -> None:
        if 0 <= index < len(self.steps):
            del self.steps[index]

    def move_up(self, index: int) -> None:
        if 1 <= index < len(self.steps):
            self.steps[index - 1], self.steps[index] = self.steps[index], self.steps[index - 1]

    def move_down(self, index: int) -> None:
        if 0 <= index < len(self.steps) - 1:
            self.steps[index + 1], self.steps[index] = self.steps[index], self.steps[index + 1]

    def save_snapshot(self) -> None:
        # Deep-ish copy: steps are dataclasses with primitives only
        self.saved_snapshot = [PipelineStep(s.category, s.method, dict(s.params)) for s in self.steps]

    def revert_to_snapshot(self) -> None:
        self.steps = [PipelineStep(s.category, s.method, dict(s.params)) for s in self.saved_snapshot]
