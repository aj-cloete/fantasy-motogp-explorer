import inspect
from dataclasses import dataclass, field


@dataclass
class RiderEventStats:
    grid_position: int
    q1_position: int
    q2_position: int
    sprint_position: int
    final_position: int
    q1_points: float
    q2_points: float
    sprint_points: float
    final_points: float
    qualifying_vs_final_position: int
    qualifying_vs_final_position_points: float
    event_num: int
    points: float
    race_time: str
    race_time_float: float
    fastest_lap: int
    finished: bool = field(init=False)
    had_fastest_lap: bool = field(init=False)

    def __post_init__(self):
        self.final_position = self.final_position if self.final_points else -99
        self.finished = self.final_position > 0
        self.had_fastest_lap = self.fastest_lap > 0
        self.race_time = str(self.race_time)


@dataclass
class RiderStats:
    wpr_history: dict
    avg_points: float
    podium: int
    last_event: float
    last_3_events: float
    last_5_events: float
    season_points: float
    starts: int
    avg_qualifying_pos: float
    is_prev_season: int
    cost_dynamic: int
    total_points: float
    avg_grid_pos: float
    avg_finishing_pos: float
    prices: list[int]
    events: list[RiderEventStats]
    _prices: list[int] = field(init=False, repr=False)
    _events: list[RiderEventStats] = field(init=False, repr=False)

    @classmethod
    def from_dict(cls, env):
        default_env = {k: None for k in inspect.signature(cls).parameters}
        default_env.update(env)
        return cls(**{k: v for k, v in default_env.items() if k in inspect.signature(cls).parameters})

    @property
    def prices(self):
        return self._prices

    @prices.setter
    def prices(self, prices: dict):
        ret = []
        i = 1
        while True:
            price = prices.get(str(i))
            if not price:
                break
            ret.append(price)
            i += 1
        self._prices = ret

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, events: dict):
        ret = []
        i = 1
        while True:
            event_stats = events.get(str(i))
            if not event_stats:
                break
            ret.append(RiderEventStats(event_num=i, **event_stats))
            i += 1
        self._events = ret


@dataclass
class _Rider:
    first_name: str
    last_name: str
    country: str
    number: int
    status: str
    id: int
    constructor_id: int
    squad_id: int
    cost: float
    stats: RiderStats
    _stats: RiderStats = field(init=False, repr=False)
    team_id: int = field(init=False)
    rider: str = field(init=False)
    _cost_millions: int = field(init=False)

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
        self._stats = RiderStats.from_dict(stats)

    @property
    def cost(self):
        return round(float(self._cost_millions) / 1000000, 2)

    @cost.setter
    def cost(self, cost: int):
        self._cost_millions = cost


class Rider(_Rider):
    @property
    def team_id(self):
        return self.squad_id

    @property
    def rider(self):
        return f"{self.first_name[0]} {self.last_name[:3]}".upper()
