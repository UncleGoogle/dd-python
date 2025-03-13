from __future__ import annotations
from dataclasses import dataclass, field

from smartschedule.planning.parallelization.parallel_stages import ParallelStages


@dataclass
class ParallelStagesList:
    all: list[ParallelStages] = field(default_factory=list)

    def add(self, parallel_stages: ParallelStages) -> None:
        self.all = self.all + [parallel_stages]

    def __str__(self) -> str:
        return " | ".join([str(parallel_stages) for parallel_stages in self.all])
