from dataclasses import dataclass, field

from data_models.common import Stats


@dataclass(kw_only=True)
class TeamStats(Stats):
    pass


@dataclass
class Team:
    id: int
    name: str
    num_riders: int
    is_wildcard: int
    cost: float
    stats: TeamStats
    _is_wildcard: bool = field(init=False, repr=False)
    _stats: TeamStats = field(init=False, repr=False)
    _cost_millions: int = field(init=False, repr=False)

    @property
    def is_wildcard(self):
        return self._is_wildcard

    @is_wildcard.setter
    def is_wildcard(self, is_wildcard: int):
        self._is_wildcard = bool(is_wildcard)

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, stats: dict):
        self._stats = TeamStats(**stats)

    @property
    def cost(self):
        return round(float(self._cost_millions) / 1000000, 2)

    @cost.setter
    def cost(self, cost: int):
        self._cost_millions = cost
