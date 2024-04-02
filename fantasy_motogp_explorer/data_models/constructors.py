from dataclasses import dataclass, field

from data_models.common import Stats


@dataclass(kw_only=True)
class ConstructorStats(Stats):
    pass


@dataclass
class Constructor:
    id: int
    name: str
    cost: int
    num_riders: int
    stats: ConstructorStats
    _stats: ConstructorStats = field(init=False, repr=False)

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, stats: dict):
        self._stats = ConstructorStats(**stats)
