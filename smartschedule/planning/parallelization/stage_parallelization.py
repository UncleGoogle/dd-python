from smartschedule.planning.parallelization.parallel_stages import ParallelStages
from smartschedule.planning.parallelization.parallel_stages_list import (
    ParallelStagesList,
)
from smartschedule.planning.parallelization.stage import Stage
from collections import defaultdict, deque


class StageParallelization:

    def of(self, stages: set[Stage]) -> ParallelStagesList:
        parallel_stages = ParallelStagesList()
        trees = self._make_trees(stages)
        for level in trees:
            print(level)
            parallel_stages.add(ParallelStages(level))
        return parallel_stages

    def _make_trees(self, stages: set[Stage]) -> list[set[Stage]]:
        levels = []
        visited = set()
        visiting = set()

        def visit(stage) -> bool:
            if stage in visited:
                return True
            if stage in visiting:
                return False  # Cycle detected
            visiting.add(stage)
            for dep in stage.dependencies:
                if not visit(dep):
                    return False
            visiting.remove(stage)
            visited.add(stage)
            return True

        # root level
        root_level = set()
        for stage in stages:
            if not stage.dependencies:
                root_level.add(stage)
        levels.append(root_level)

        # other levels
        remaining_stages = stages - root_level
        while remaining_stages:
            next_level = set()
            for stage in remaining_stages:
                if all(dep in levels[-1] for dep in stage.dependencies):
                    next_level.add(stage)
            if not next_level:
                return []  # Cycle detected
            levels.append(next_level)
            remaining_stages -= next_level

        # Check for cycles
        for stage in stages:
            if not visit(stage):
                return []  # Cycle detected

        return levels


