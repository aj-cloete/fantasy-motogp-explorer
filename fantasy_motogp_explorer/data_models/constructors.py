from dataclasses import dataclass, field

from data_models.common import Stats


@dataclass(kw_only=True)
class ConstructorStats(Stats):
    pass


@dataclass
class Constructor:
    id: int
    name: str
    num_riders: int
    cost: float
    stats: ConstructorStats
    _stats: ConstructorStats = field(init=False, repr=False)
    _cost_millions: int = field(init=False, repr=False)

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, stats: dict):
        self._stats = ConstructorStats(**stats)

    @property
    def cost(self):
        return round(float(self._cost_millions) / 1000000, 2)

    @cost.setter
    def cost(self, cost: int):
        self._cost_millions = cost
