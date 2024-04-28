import inspect
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

    @classmethod
    def from_dict(cls, env):
        default_env = {k: None for k in inspect.signature(cls).parameters}
        default_env.update(env)
        return cls(**{k: v for k, v in default_env.items() if k in inspect.signature(cls).parameters})

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
